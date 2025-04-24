import requests
import json
import time 
import os
from datetime import datetime
import hashlib
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from deep_translator import GoogleTranslator

# configurar retries para lidar com falhas de conexão
session = requests.Session()
retries = Retry(total=3, backoff_factor=1, status_forcelist=[429, 500, 502, 503, 504])
session.mount('https://', HTTPAdapter(max_retries=retries))

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'alimentos_openfoodfacts.json')
LOG_FILE = os.path.join(OUTPUT_DIR, 'alimentos_log.json')

# tradutor ranhoso
translator = GoogleTranslator(source='auto', target='es')

def calculate_hash(content):
    return hashlib.sha256(json.dumps(content, sort_keys=True).encode('utf-8')).hexdigest()

def log_change():
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = {
        "timestamp": timestamp,
        "file": OUTPUT_FILE,
        "action": "modified"
    }
    
    log_data = []
    if os.path.exists(LOG_FILE):
        try:
            with open(LOG_FILE, 'r', encoding='utf-8') as f:
                log_data = json.load(f)
        except:
            pass
    
    log_data.append(log_entry)
    
    with open(LOG_FILE, 'w', encoding='utf-8') as f:
        json.dump(log_data, f, ensure_ascii=False, indent=2)

def save_if_changed(new_data):
    current_hash = calculate_hash(new_data)
    
    if os.path.exists(OUTPUT_FILE):
        try:
            with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
                existing_data = json.load(f)
            existing_hash = calculate_hash(existing_data)
            
            if current_hash == existing_hash:
                print("ℹ️ Nenhuma alteração detectada no conteúdo.")
                return False
        except:
            pass
    
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
    
    log_change()
    return True

def translate_text(text):
    if not text:
        return text
    try:
        return translator.translate(text)
    except Exception as e:
        print(f"Erro ao traduzir texto '{text}': {e}")
        return text

def translate_list(lst):
    return [translate_text(item) for item in lst if item]

def scrape_open_food_facts(limit):
    url = "https://world.openfoodfacts.org/cgi/search.pl"
    params = {
        "action": "process",
        "json": 1,
        "page_size": limit,
        "page": 1,
        "sort_by": "unique_scans_n",
        "tagtype_0": "countries",
        "tag_contains_0": "contains",
        "tag_0": "es"
    }
    
    try:
        # aumentar o timeout para 30 segundos
        response = session.get(url, params=params, headers=HEADERS, timeout=30)
        response.raise_for_status()
        data = response.json()

        alimentos = []
        for product in data.get('products', []):
            nome = product.get('product_name', 'Desconhecido')
            if not nome or nome == '':
                continue

            # traduzir o nome do produto
            # nome_traduzido = translate_text(nome)

            # nutrientes por 100g
            nutrients = product.get('nutriments', {})
            nutricion = {
                "proteina_100g": nutrients.get('proteins_100g', None),
                "carboidratos_100g": nutrients.get('carbohydrates_100g', None),
                "gorduras_100g": nutrients.get('fat_100g', None),
                "calorias_100g": nutrients.get('energy-kcal_100g', None),
                "acucares_100g": nutrients.get('sugars_100g', None),
                "fibra_100g": nutrients.get('fiber_100g', None),
                "amido_100g": nutrients.get('starch_100g', None),
                "frutose_100g": nutrients.get('fructose_100g', None),
                "glicose_100g": nutrients.get('glucose_100g', None),
                "lactose_100g": nutrients.get('lactose_100g', None),
                "maltose_100g": nutrients.get('maltose_100g', None),
                "gorduras_monoinsaturadas_100g": nutrients.get('monounsaturated-fat_100g', None),
                "gorduras_poliinsaturadas_100g": nutrients.get('polyunsaturated-fat_100g', None),
                "omega_3_100g": nutrients.get('omega-3-fat_100g', None),
                "omega_6_100g": nutrients.get('omega-6-fat_100g', None),
                "gorduras_saturadas_100g": nutrients.get('saturated-fat_100g', None),
                "gorduras_trans_100g": nutrients.get('trans-fat_100g', None),
                "colesterol_100g": nutrients.get('cholesterol_100g', None),
                "vitamina_b1_100g": nutrients.get('vitamin-b1_100g', None),
                "vitamina_b2_100g": nutrients.get('vitamin-b2_100g', None),
                "vitamina_b3_100g": nutrients.get('vitamin-b3_100g', None),
                "vitamina_b5_100g": nutrients.get('vitamin-b5_100g', None),
                "vitamina_b6_100g": nutrients.get('vitamin-b6_100g', None),
                "vitamina_b12_100g": nutrients.get('vitamin-b12_100g', None),
                "acido_folico_100g": nutrients.get('folates_100g', None),
                "vitamina_a_100g": nutrients.get('vitamin-a_100g', None),
                "vitamina_c_100g": nutrients.get('vitamin-c_100g', None),
                "vitamina_d_100g": nutrients.get('vitamin-d_100g', None),
                "vitamina_e_100g": nutrients.get('vitamin-e_100g', None),
                "vitamina_k_100g": nutrients.get('vitamin-k_100g', None),
                "calcio_100g": nutrients.get('calcium_100g', None),
                "cloro_100g": nutrients.get('chloride_100g', None),
                "cromo_100g": nutrients.get('chromium_100g', None),
                "fosforo_100g": nutrients.get('phosphorus_100g', None),
                "ferro_100g": nutrients.get('iron_100g', None),
                "magnesio_100g": nutrients.get('magnesium_100g', None),
                "manganes_100g": nutrients.get('manganese_100g', None),
                "sodio_100g": nutrients.get('sodium_100g', None),
                "zinco_100g": nutrients.get('zinc_100g', None)
                # aminoácidos não estão disponíveis diretamente no Open Food Facts
            }

            # limpar valores None
            nutricion = {k: v for k, v in nutricion.items() if v is not None}

            # alérgenos
            alergenos = product.get('allergens_tags', [])
            alergenos_traduzidos = translate_list(alergenos)

            # ingredientes
            ingredientes = product.get('ingredients_text', '').split(', ') if product.get('ingredients_text') else []
            ingredientes_traduzidos = translate_list(ingredientes)

            alimentos.append({
                "nome": nome,
                "imagem": product.get('image_url', None),
                "ingredientes": ingredientes_traduzidos,
                "nutricion": nutricion,
                "alergenos": alergenos_traduzidos,
                "fonte": "openfoodfacts.org"
            })
            time.sleep(1) # respeitar limites de taxa

        return alimentos
    except Exception as e:
        print(f"Erro ao coletar dados do Open Food Facts: {e}")
        return []

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("\n\t==={ SCRAPPER OPEN FOOD FACTS }===\n")
    
    while True:
        try:
            limit = int(input("Digite o número de alimentos a coletar (exemplo: 5): "))
            if limit < 0:
                print("Por favor, insira um número maior ou igual a 0.")
                continue
            break
        except ValueError:
            print("Por favor, insira um número válido.")
    
    print("\n\t==={ Scrapping in process, please be patient. It may take some time, big numbers are equivalent to bigger delays. }===\n")
    
    alimentos = []
    if limit > 0:
        print("📥 Coletando dados do Open Food Facts...")
        produtos = scrape_open_food_facts(limit)
        if produtos:
            alimentos.extend(produtos)
        else:
            print("❌ Nenhum alimento encontrado no Open Food Facts.")
    
    if alimentos:
        if save_if_changed(alimentos):
            print(f"✅ Dados salvos com sucesso em: {OUTPUT_FILE}")
        else:
            print(f"ℹ️ Dados não salvos, pois não houve alterações.")
    else:
        print("❌ Nenhum dado coletado para salvar.")

if __name__ == "__main__":
    main()