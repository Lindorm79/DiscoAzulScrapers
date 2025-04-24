import requests
import json
import time
import os
from deep_translator import GoogleTranslator
from datetime import datetime
import hashlib

translator = GoogleTranslator(source='auto', target='es')

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'exercicios.json')
LOG_FILE = os.path.join(OUTPUT_DIR, 'exercicios_log.json')

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
    
    # verificar se o arquivo já existe e comparar o hash
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
    
    # salvar novo conteúdo e registrar a alteração
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(new_data, f, ensure_ascii=False, indent=2)
    
    log_change()
    return True

def get_exercicios(limit=5):  
    url = "https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/dist/exercises.json"
    try:
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        dados = response.json()

        # limite
        dados = dados[:limit]

        return dados
    except Exception as e:
        print(f"Erro ao buscar dados do free-exercise-db: {e}")
        return []

def processar_exercicio(exercicio):
    try:
        # traduzir os detalhes (exceto o título)
        detalhes = {
            "Categoria": translator.translate(exercicio.get("category", "Não especificado")),
            "Força": translator.translate(exercicio.get("force", "Não especificado")),
            "Nível": translator.translate(exercicio.get("level", "Não especificado")),
            "Equipamento": translator.translate(exercicio.get("equipment", "Não especificado")),
            "Músculos Primários": translator.translate(", ".join(exercicio.get("primaryMuscles", []))) if exercicio.get("primaryMuscles") else "Nenhum",
            "Músculos Secundários": translator.translate(", ".join(exercicio.get("secondaryMuscles", []))) if exercicio.get("secondaryMuscles") else "Nenhum"
        }

        # traduzir os passos
        passos = [translator.translate(passo) for passo in exercicio.get("instructions", [])]

        # gerar URLs das imagens (sem tradução)
        imagens = exercicio.get("images", [])
        imagens_urls = [
            f"https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/images/{exercicio['name'].replace(' ', '_')}/{img}"
            for img in imagens
        ]

        return {
            "titulo": exercicio.get("name", "Título não encontrado"),
            "detalhes": detalhes,
            "passos": passos,
            "imagens": imagens_urls if imagens_urls else None
        }
    except Exception as e:
        print(f"Erro ao processar exercício {exercicio.get('name', 'desconhecido')}: {e}")
        return None

def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    exercicios_raw = get_exercicios(limit=5) 
    if not exercicios_raw:
        print("❌ Nenhum exercício encontrado no free-exercise-db.")
        return

    todos_exercicios = []
    for exercicio in exercicios_raw:
        print(f"📥 Processando exercício: {exercicio['name']}")
        dados = processar_exercicio(exercicio)
        if dados:
            todos_exercicios.append(dados)
        time.sleep(0.5) 

    if todos_exercicios:
        if save_if_changed(todos_exercicios):
            print(f"✅ Dados dos exercícios salvos com sucesso em: {OUTPUT_FILE}")
        else:
            print(f"ℹ️ Dados não salvos, pois não houve alterações.")
    else:
        print("❌ Nenhum dado de exercício processado.")

if __name__ == "__main__":
    main()