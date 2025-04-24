import requests
import json
import time
import os

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'output')
OUTPUT_FILE = os.path.join(OUTPUT_DIR, 'exercicios.json')

# função para ir buscar os dados
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

# função para processar cada exercício e formatar os dados
def processar_exercicio(exercicio):
    try:

        detalhes = {
            "Categoria": exercicio.get("category", "Não especificado"),
            "Força": exercicio.get("force", "Não especificado"),
            "Nível": exercicio.get("level", "Não especificado"),
            "Equipamento": exercicio.get("equipment", "Não especificado"),
            "Músculos Primários": ", ".join(exercicio.get("primaryMuscles", [])),
            "Músculos Secundários": ", ".join(exercicio.get("secondaryMuscles", []))
        }

        imagens = exercicio.get("images", [])
        imagens_urls = [
            f"https://raw.githubusercontent.com/yuhonas/free-exercise-db/main/images/{exercicio['name'].replace(' ', '_')}/{img}"
            for img in imagens
        ]

        return {
            "titulo": exercicio.get("name", "Título não encontrado"),
            "detalhes": detalhes,
            "passos": exercicio.get("instructions", []),
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
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(todos_exercicios, f, ensure_ascii=False, indent=2)
        print(f"✅ Dados dos exercícios salvos com sucesso em: {OUTPUT_FILE}")
    else:
        print("❌ Nenhum dado de exercício processado.")

if __name__ == "__main__":
    main()