import argparse  # Importa o módulo argparse para lidar com argumentos de linha de comando
import yaml  # Importa o módulo yaml para escrever e ler ficheiros YAML


# Classe Feature
class Feature:
    # Construtor para inicializar um objeto Feature
    def __init__(self, feature_type, start, end, feature_id, length):
        self.feature_type = feature_type  # Tipo da característica (ex.: gene, CDS)
        self.start = start  # Posição inicial da característica
        self.end = end  # Posição final da característica
        self.feature_id = feature_id  # Identificador único da característica
        self.length = length  # Comprimento da característica


# Classe Variant
class Variant:
    # Construtor para inicializar um objeto Variant
    def __init__(self, chrom, pos, variant_id, ref, alt, qual, filter_, info):
        self.chrom = chrom  # Cromossoma da variante
        self.pos = pos  # Posição da variante
        self.variant_id = variant_id  # Identificador único da variante
        self.ref = ref  # Base(s) de referência
        self.alt = alt  # Base(s) alternativa(s)
        self.qual = qual  # Pontuação de qualidade da variante
        self.filter = filter_  # Estado do filtro
        self.info = info  # Informações adicionais sobre a variante

    def __str__(self):
        # Converte o objeto Variant para uma string no formato VCF
        return f"{self.chrom}\t{self.pos}\t{self.variant_id}\t{self.ref}\t{self.alt}\t{self.qual}\t{self.filter}\t{self.info}"


# Função para analisar o ficheiro GFF
def parse_gff(file_path, feature_types):
    # Inicializa uma lista vazia para armazenar objetos Feature
    features = []
    with open(file_path, "r") as file:  # Abre o ficheiro GFF
        for line in file:
            if line.startswith("#"):  # Ignora as linhas de cabeçalho
                continue
            parts = line.strip().split("\t")  # Divide a linha em colunas
            if parts[2] in feature_types:  # Verifica se o tipo de característica corresponde ao desejado
                # Analisa a coluna de atributos e converte-a em um dicionário
                attributes = {key: value for key, value in
                              [attr.split("=") for attr in parts[8].split(";") if "=" in attr]}
                # Cria um objeto Feature e adiciona-o à lista
                feature = Feature(
                    feature_type=parts[2],
                    start=int(parts[3]),
                    end=int(parts[4]),
                    feature_id=attributes.get("ID", "Unknown"),  # Default para "Unknown" caso não exista ID
                    length=int(parts[4]) - int(parts[3]) + 1  # Calcula o comprimento da característica
                )
                features.append(feature)  # Adiciona a característica à lista
    return features  # Retorna a lista de características


# Função para analisar o ficheiro VCF
def parse_vcf(file_path):
    # Inicializa uma lista vazia para armazenar objetos Variant e cabeçalhos
    variants = []
    with open(file_path, "r") as file:  # Abre o ficheiro VCF
        for line in file:
            if line.startswith("#"):  # Lida com as linhas de cabeçalho
                variants.append(line.strip())  # Adiciona a linha de cabeçalho como string
                continue
            parts = line.strip().split("\t")  # Divide a linha em colunas
            # Cria um objeto Variant e adiciona-o à lista
            variant = Variant(
                chrom=parts[0],
                pos=int(parts[1]),
                variant_id=parts[2],
                ref=parts[3],
                alt=parts[4],
                qual=parts[5],
                filter_=parts[6],
                info=parts[7]
            )
            variants.append(variant)  # Adiciona a variante à lista
    return variants  # Retorna a lista de variantes


# Função para filtrar variantes e calcular densidades
def filter_variants(features, variants):
    # Inicializa uma lista vazia para as variantes filtradas
    filtered_variants = []
    # Inicializa um dicionário para armazenar os dados do relatório
    report_data = {
        "FilteringReport": {
            "Feature_Type": features[0].feature_type if features else "Unknown",  # Tipo de característica ou "Unknown" se não houver características
            "TotalFeatures": len(features),  # Número total de características
            "TotalVariants": 0,  # Valor inicial para o número total de variantes
            "VariantsPerFeature": []  # Lista para armazenar dados das variantes para cada característica
        }
    }

    total_variants = 0  # Contador para o número total de variantes

    for feature in features:
        # Filtra as variantes que estão dentro do intervalo da característica
        feature_variants = [
            var for var in variants[1:]  # Ignora a primeira variante (cabeçalho)
            if feature.start <= var.pos <= feature.end
        ]

        # Calcula a densidade de variantes por quilobase
        variant_count = len(feature_variants)  # Número de variantes na característica
        density = (variant_count / (feature.length / 1000)) if feature.length else 0  # Cálculo da densidade

        # Atualiza o número total de variantes
        total_variants += variant_count

        # Adiciona os dados da característica atual ao relatório
        report_data["FilteringReport"]["VariantsPerFeature"].append({
            "FeatureID": feature.feature_id,
            "Length": feature.length,
            "VariantCount": variant_count,
            "Density": density
        })

        # Adiciona as variantes para a característica atual à lista de variantes filtradas
        filtered_variants.extend(feature_variants)

    # Atualiza o número total de variantes no relatório
    report_data["FilteringReport"]["TotalVariants"] = total_variants

    return filtered_variants, report_data  # Retorna as variantes filtradas e os dados do relatório


# Função principal
def main():
    # Configura a análise de argumentos de linha de comando
    parser = argparse.ArgumentParser(description="Calculadora de Densidade de Variantes")
    parser.add_argument("-gff", required=True, help="Ficheiro GFF de entrada")  # Argumento para o ficheiro GFF de entrada
    parser.add_argument("-vcf", required=True, help="Ficheiro VCF de entrada")  # Argumento para o ficheiro VCF de entrada
    parser.add_argument("-var", required=True, help="Ficheiro VCF filtrado de saída")  # Argumento para o ficheiro VCF filtrado de saída
    parser.add_argument("-rep", required=True, help="Relatório YAML de saída")  # Argumento para o ficheiro de relatório YAML
    parser.add_argument("-ftr", required=True, help="Tipo(s) de característica(s) (ex.: gene, CDS)")  # Argumento para os tipos de características
    args = parser.parse_args()  # Analisa os argumentos

    # Analisa o ficheiro GFF de entrada
    features = parse_gff(args.gff, args.ftr.split(","))
    print("features:", len(features))  # Debug: Imprime o número de características analisadas

    # Analisa o ficheiro VCF de entrada
    variants = parse_vcf(args.vcf)
    print("variants:", len(variants))  # Debug: Imprime o número de variantes analisadas

    # Filtra as variantes e gera os dados do relatório
    filtered_variants, report_data = filter_variants(features, variants)
    print("filtered_variants:", len(filtered_variants))  # Debug: Imprime o número de variantes filtradas

    # Escreve as variantes filtradas no ficheiro VCF de saída
    with open(args.var, "w") as vcf_out:
        for variant in variants:
            if isinstance(variant, str):  # Lida com as linhas de cabeçalho
                vcf_out.write(variant + "\n")
            else:  # Escreve os objetos de variantes
                vcf_out.write(str(variant) + "\n")
    print("VCF escrito")  # Debug: Confirma que o ficheiro VCF foi escrito

    # Escreve o relatório YAML no ficheiro de saída
    with open(args.rep, "w") as yaml_out:
        yaml.dump(report_data, yaml_out, default_flow_style=False, sort_keys=False)
    print("Relatório YAML escrito")  # Debug: Confirma que o relatório YAML foi escrito


# Ponto de entrada para o script
if __name__ == "__main__":
    main()
