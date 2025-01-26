# Assignment-002-PAB-
Calculadora de Densidade de Variantes

Descrição do Programa

A Calculadora de Densidade de Variantes é uma ferramenta de linha de comando projetada para integrar dados de ficheiros GFF (General Feature Format) e VCF (Variant Call Format). Filtra variantes genéticas com base nas suas posições em relação a elementos genómicos especificados e calcula a densidade de variantes para cada elemento. A ferramenta gera um ficheiro VCF filtrado contendo as variantes relevantes e um relatório YAML que resume as densidades de variantes por elemento.

Esta ferramenta é particularmente útil em análises genómicas onde é importante compreender a distribuição de variantes em elementos genómicos específicos (por exemplo, genes ou regiões codificantes).

Estrutura do Programa

O programa está implementado como um único script Python (João_Fontinha_2024160902-Cláudio_Barroso_2024147362-variant_density_calculator.py) que inclui os seguintes componentes:

1. Classe Feature

Representa elementos genómicos extraídos do ficheiro GFF.

Atributos: feature_type, start, end, feature_id e length.

2. Classe Variant

Representa variantes genéticas extraídas do ficheiro VCF.

Atributos: chrom, pos, variant_id, ref, alt, qual, filter e info.

3. Funções

parse_gff(file_path, feature_types): Analisa o ficheiro GFF para extrair elementos de tipos especificados.

parse_vcf(file_path): Analisa o ficheiro VCF para extrair variantes.

filter_variants(features, variants): Filtra variantes com base nas suas posições em relação aos elementos especificados e calcula as densidades.

4. Programa Principal

Utiliza a biblioteca argparse para lidar com argumentos da linha de comando.

Lê os ficheiros de entrada (GFF e VCF), processa os dados e gera ficheiros de saída (VCF filtrado e relatório YAML).

Utilização do Programa

Requisitos

Python 3.6 ou superior.

Biblioteca Python necessária:

PyYAML (Instale com pip install pyyaml)

Instalação

Clone o repositório e navegue para o diretório do projeto:

$ git clone https://github.com/Rufuszl/João_Fontinha_2024160902-Cláudio_Barroso_2024147362-variant_density_calculator.git
$ cd João_Fontinha_2024160902-Cláudio_Barroso_2024147362-variant_density_calculator

Execução do Programa

Execute o script com os seguintes argumentos:

$ João_Fontinha_2024160902-Cláudio_Barroso_2024147362-variant_density_calculator.py -gff Homo_sapiens.GRCh38.113.chromosome.21.gff3 -vcf homo_sapiens-chr21.vcf -var filtered_variants_output.vcf -rep density_report_output.yml -ftr gene,CDS

Argumentos:

-gff: Caminho para o ficheiro GFF de entrada.

-vcf: Caminho para o ficheiro VCF de entrada.

-var: Caminho para o ficheiro VCF filtrado de saída.

-rep: Caminho para o ficheiro YAML de relatório de saída.

-ftr: Lista de tipos de elementos separada por vírgulas (por exemplo, gene,CDS).

Exemplo de Utilização:

$ João_Fontinha_2024160902-Cláudio_Barroso_2024147362-variant_density_calculator.py \
    -gff data/example.gff \
    -vcf data/example.vcf \
    -var output/filtered_variants.vcf \
    -rep output/report.yaml \
    -ftr gene,CDS

Saída

Ficheiro VCF Filtrado:

Contém apenas as variantes que estão dentro dos elementos especificados.

Relatório YAML:

Resume as densidades de variantes por elemento. Exemplo:

FilteringReport:
  Feature_Type: gene
  TotalFeatures: 10
  TotalVariants: 50
  VariantsPerFeature:
    - FeatureID: gene1
      Length: 1500
      VariantCount: 5
      Density: 3.33
    - FeatureID: gene2
      Length: 2000
      VariantCount: 10
      Density: 5.00

Melhores Práticas

Utilize um sistema de controlo de versões (como Git) para gerir alterações no código.

Teste o programa com conjuntos de dados pequenos antes de processar ficheiros grandes.

Certifique-se de que os ficheiros de entrada estão devidamente formatados para evitar erros.
