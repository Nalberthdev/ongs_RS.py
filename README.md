## Descrição Geral
O script ongs.py busca organizações não governamentais (ONGs) e iniciativas comunitárias no Rio Grande do Sul (RS) utilizando a Overpass API do OpenStreetMap (OSM), uma alternativa gratuita ao Google Places API. Ele coleta informações adicionais via busca na web, aplica análise de sentimento aos textos encontrados e gera:

Um ranking das 5 ONGs com mais menções positivas ou neutras.
Uma lista de ONGs menos visíveis (com menos texto associado) que possuem menções positivas ou neutras.
O objetivo é identificar ONGs confiáveis atuando no contexto das enchentes no RS a partir de maio de 2024, sem depender de APIs pagas.

Dependências
Python: Versão 3.x
Bibliotecas:
overpy: Interface para a Overpass API (busca no OSM).
requests: Requisições HTTP para busca na web.
beautifulsoup4: Parsing de HTML das páginas retornadas.
nltk: Análise de sentimento com o modelo VADER.

## instalação:
pip install overpy requests beautifulsoup4 nltk


# Recursos do NLTK:
O script baixa o vader_lexicon na primeira execução

nltk.download('vader_lexicon')

## Estrutura do Código
Imports e Configuração Inicial

import overpy
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime
import time

nltk.download('vader_lexicon')
api = overpy.Overpass()
DATA_INICIO_ENCHENTES = datetime(2024, 5, 1)

# Propósito: Importa bibliotecas, inicializa a Overpass API e define a data de referência das enchentes (1º de maio de 2024).


Funções
buscar_ongs_osm()
Descrição: Busca ONGs e centros comunitários no RS via Overpass API.
Parâmetros: Nenhum.
Retorno: Lista de dicionários com:
nome (str): Nome da ONG (padrão: "ONG Sem Nome").
lat (float): Latitude.
lon (float): Longitude.
Query OSM: Busca pelas tags:
"amenity"="ngo"
"office"="ngo"
"amenity"="community_centre"
Exemplo de Saída: 

[{'nome': 'ONG Exemplo', 'lat': -30.0, 'lon': -51.0}]


buscar_info_web(nome_ong)
Descrição: Faz uma busca no Google para coletar website e texto relacionado à ONG.
Parâmetros:
nome_ong (str): Nome da ONG.
Retorno: Dicionário com:
website (str): URL ou "Não disponível".
texto (str): Até 1000 caracteres de texto da busca.
Notas:
Usa User-Agent falso para evitar bloqueios.
Timeout de 5 segundos.
Exibe logs para depuração.

{'website': 'https://exemplo.org', 'texto': 'ong ajuda nas enchentes...'}


analisar_sentimento(texto)
Descrição: Analisa o sentimento do texto com o VADER.
Parâmetros:
texto (str): Texto a ser analisado.
Retorno: 'positivo' (> 0.05), 'negativo' (< -0.05) ou 'neutro'.
Notas: Exibe score compound para depuração.


Exemplo de Saída: 

'positivo'


main()
Descrição: Coordena a execução do script.
Passos:
Busca ONGs no OSM.
Processa até 10 ONGs com busca web e análise de sentimento.
Filtra ONGs com sentimento positivo ou neutro.
Gera ranking das 5 ONGs com mais texto.
Lista ONGs menos visíveis (texto < 200 caracteres).
Saída: Imprime ranking e lista no console.
Notas: Inclui time.sleep(1) para evitar bloqueios.



## Como Usar

Preparação
Salve o script como ongs.py.
Instale as dependências

pip install overpy requests beautifulsoup4 nltk

python ongs.py


Com ambiente virtual (exemplo):

& c:/Users/nal/ongs_RS.py/.venv/Scripts/python.exe c:/Users/nal/ongs_RS.py/ongs.py


Buscando ONGs no Rio Grande do Sul via OpenStreetMap...
Encontrada: ONG Exemplo
Total de ONGs encontradas: 1
Processando: ONG Exemplo
Busca para ONG Exemplo: 500 caracteres encontrados
Sentimento para texto: positivo (score: 0.7)

=== Ranking das 5 ONGs com menções positivas ou neutras (estimado) ===
1. ONG Exemplo - Sentimento: positivo
   Website: https://exemplo.org

=== ONGs menos visíveis com menções positivas ou neutras ===


## Limitações

Dados do OSM: Depende da qualidade e quantidade de ONGs no OpenStreetMap, que pode ser limitada no RS.
Busca Web: Extração aproximada, sujeita a falhas por bloqueios ou parsing impreciso.
Sentimento: O VADER pode interpretar incorretamente textos ambíguos.
Escalabilidade: Limita a 10 ONGs por execução; ajustes podem causar bloqueios.


## Personalização

Aumentar o Limite de ONGs:
Edite ongs_osm[:10] para ongs_osm[:50] ou remova o slice.
Modificar a Query OSM:
Adicione tags como "amenity"="charity"


# Refinar a Busca Web:
Altere a URL em buscar_info_web


url = f"https://www.google.com/search?q={nome_ong}+Rio+Grande+do+Sul+enchentes+2024+ONG"


## Solução de Problemas


Nenhuma ONG Encontrada:
Teste a query no Overpass Turbo.
Erro na Busca Web:
Reduza o limite (ex.: ongs_osm[:5]) ou aumente o delay (time.sleep(2)).
Sentimento Negativo:
Inspecione info['texto'] com print(info['texto']) para verificar relevância.


Autor

Desenvolvido com assistência de Grok, criado por Nalberth e Progamador Python Yotube, adaptado para uso gratuito com OpenStreetMap.

