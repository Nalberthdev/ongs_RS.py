import overpy
import requests
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from datetime import datetime
import time

nltk.download('vader_lexicon')

# Configuração da Overpass API
api = overpy.Overpass()

# Data de início das enchentes no RS (maio de 2024)
DATA_INICIO_ENCHENTES = datetime(2024, 5, 1)

# Busca ONGs no Rio Grande do Sul via OpenStreetMap
def buscar_ongs_osm():
    query = """
    [out:json];
    area["name"="Rio Grande do Sul"]->.rs;
    (
      node["amenity"="ngo"](area.rs);
      way["amenity"="ngo"](area.rs);
      node["office"="ngo"](area.rs);
      way["office"="ngo"](area.rs);
      node["amenity"="community_centre"](area.rs);
      way["amenity"="community_centre"](area.rs);
    );
    out body;
    """
    resultado = api.query(query)
    ongs = []
    for node in resultado.nodes + resultado.ways:
        nome = node.tags.get('name', 'ONG Sem Nome')
        print(f"Encontrada: {nome}")
        ongs.append({
            'nome': nome,
            'lat': node.lat if hasattr(node, 'lat') else node.center_lat,
            'lon': node.lon if hasattr(node, 'lon') else node.center_lon
        })
    return ongs

# Busca informações adicionais na web
def buscar_info_web(nome_ong):
    url = f"https://www.google.com/search?q={nome_ong}+Rio+Grande+do+Sul+ONG"
    headers = {'User-Agent': 'Mozilla/5.0'}
    try:
        resposta = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(resposta.text, 'html.parser')
        website = soup.find('cite')
        website = website.text if website else "Não disponível"
        texto = soup.get_text().lower()[:1000]  # Limite para evitar excesso
        print(f"Busca para {nome_ong}: {len(texto)} caracteres encontrados")
        return {'website': website, 'texto': texto}
    except Exception as e:
        print(f"Erro na busca para {nome_ong}: {e}")
        return {'website': 'Não disponível', 'texto': ''}

# Análise de sentimento
def analisar_sentimento(texto):
    sid = SentimentIntensityAnalyzer()
    score = sid.polarity_scores(texto)
    sentimento = 'positivo' if score['compound'] > 0.05 else 'negativo' if score['compound'] < -0.05 else 'neutro'
    print(f"Sentimento para texto: {sentimento} (score: {score['compound']})")
    return sentimento

# Função principal
def main():
    print("Buscando ONGs no Rio Grande do Sul via OpenStreetMap...")
    ongs_osm = buscar_ongs_osm()
    print(f"Total de ONGs encontradas: {len(ongs_osm)}")
    
    if not ongs_osm:
        print("Nenhuma ONG encontrada no OpenStreetMap. Tente ajustar a query.")
        return
    
    ongs_com_detalhes = []
    for ong in ongs_osm[:10]:  # Limite para teste
        print(f"\nProcessando: {ong['nome']}")
        info = buscar_info_web(ong['nome'])
        sentimento = analisar_sentimento(info['texto'])
        ongs_com_detalhes.append({
            'nome': ong['nome'],
            'website': info['website'],
            'sentimento': sentimento,
            'texto': info['texto']
        })
        time.sleep(1)  # Evitar bloqueio

    # Filtrar ONGs com menções positivas ou neutras
    ongs_filtradas = [ong for ong in ongs_com_detalhes if ong['sentimento'] in ['positivo', 'neutro']]
    print(f"ONGs com sentimento positivo ou neutro: {len(ongs_filtradas)}")
    
    # Ranking das 5 ONGs
    ranking = sorted(ongs_filtradas, key=lambda x: len(x['texto']), reverse=True)[:5]
    print("\n=== Ranking das 5 ONGs com menções positivas ou neutras (estimado) ===")
    for i, ong in enumerate(ranking, 1):
        print(f"{i}. {ong['nome']} - Sentimento: {ong['sentimento']}")
        print(f"   Website: {ong['website']}")
        print()

    # ONGs menos visíveis
    menos_visiveis = [ong for ong in ongs_filtradas if len(ong['texto']) < 200]
    print("\n=== ONGs menos visíveis com menções positivas ou neutras ===")
    for ong in menos_visiveis:
        print(f"{ong['nome']} - Sentimento: {ong['sentimento']}")
        print(f"   Website: {ong['website']}")
        print()

if __name__ == "__main__":
    main()