import requests
from bs4 import BeautifulSoup
import json
import time 
import os

# Definindo o header para evitar bloqueios
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9"
}

# caminho para a pasta output
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True) # cria a pasta output, se esta ainda não existir


# função para levantar os links da página principal
def get_links_recetas(limit = 5): # limite de links a serem levantados
    url = "https://www.recetasgratis.net/"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()  
        soup = BeautifulSoup(response.text, 'html.parser')

        links = []
        count = 0
        for a in soup.find_all('a', class_='titulo titulo--bloque'):
            href = a.get('href')
            if href:
                links.append(href)
                count += 1
                if count >= limit:
                    break
                time.sleep(1)   
            
        
        return links
    except Exception as e:
        print(f"Erro ao buscar links em {url}: {e}")
        return []

# função para coletar os dados de cada receita
def scrape_receta(url):
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')

        # extrair título da receita
        titulo = soup.find('h1', class_='titulo').text.strip()

        # extrair imagem da receita 
        imagem = soup.find('img', class_='imagen')
        imagem_url = imagem['src'] if imagem else None

        # extrair ingredientes
        ingredientes = []
        ingredientes_section = soup.find('div', class_='ingredientes')
        if ingredientes_section:
            for li in ingredientes_section.find_all('li', class_='ingrediente'):
                ingrediente = li.find('label').text.strip() if li.find('label') else None
                if ingrediente:
                    ingredientes.append(ingrediente)

        # extrair passos
        passos = []
        passos_section = soup.find_all('div', class_='apartado')
        for sec in passos_section:
            if sec.find('div', class_='orden'):
                p = sec.find('p')
                if p:
                    passos.append(p.get_text(strip=True))

        # extrair valores nutricionais
        nutricion = {}
        nutricion_section = soup.find('div', id='nutritional-info')
        if nutricion_section:
            for li in nutricion_section.find_all('li'):
                texto = li.get_text(strip=True)
                if ':' in texto:
                    chave, valor = texto.split(':', 1)
                    nutricion[chave.strip()] = valor.strip()

        return {
            "titulo"      : titulo,
            "imagem"      : imagem_url,
            "ingredientes": ingredientes,
            "nutricion"   : nutricion,
            "passos"      : passos
        }
    except Exception as e:
        print(f"Erro ao coletar dados de {url}: {e}")
        return None

# função principal para buscar as receitas
def main():
   
    links = get_links_recetas(limit=5)
    if links:
        todas_receitas = []
        for link in links:
            print(f"📥 Coletando dados de: {link}")
            dados = scrape_receta(link)
            if dados:
                todas_receitas.append(dados)

        output_file = os.path.join(OUTPUT_DIR, 'receitas.json')
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(todas_receitas, f, ensure_ascii=False, indent=2)

        print(f"✅ Dados das receitas salvos com sucesso em: {output_file}")
    else:
        print("❌ Nenhum link encontrado para as receitas.")

if __name__ == "__main__":
    main()