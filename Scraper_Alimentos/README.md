Scrapper Open Food Facts

🇵🇹 README em Português

O que é isto?

Este script Python extrai dados nutricionais de alimentos da API do Open Food Facts, como nome, ingredientes, nutrientes e alergénios, e tenta traduzir ingredientes para espanhol. Os dados são salvos em `output/alimentos_openfoodfacts.json`.

Requisitos

- Python 3.7+
- Instalar bibliotecas:

- `pip install requests deep-translator urllib3`

Como Usar

1.  Salve o script como scrapperAlimentos.py.
2.  Execute:
    `python scrapper_openfoodfacts.py`
3.  Digite quantos alimentos quer coletar (ex.: 5).
4.  Veja os resultados em output/alimentos_openfoodfacts.json.

Exemplo de Saída

`[
    {
        "nome": "Acuáfina",
        "ingredientes": ["ABIERTO Y ANTES DE: Ver botella..."],
        "nutricion": {"proteina_100g": 0, ...},
        "alergenos": [],
        "fonte": "openfoodfacts.org"
    }
]`

Notas

- Tradução: A tradução para espanhol pode falhar com textos em francês ou não ser a mais correta.
- Limitação: Não inclui aminoácidos.
- Ética: Respeite os limites da API (pausa de 1s por requisição).

---

🇪🇸 README en Español

¿Qué es esto?

Este script Python extrae datos nutricionales de alimentos de la API de Open Food Facts, como nombre, ingredientes, nutrientes y alérgenos, e intenta traducir los ingredientes al español. Los datos se guardan en output/alimentos_openfoodfacts.json.

Requisitos

- Python 3.7+
- Instalar bibliotecas:
  `pip install requests deep-translator urllib3`

Cómo Usar

1. Guarda el script como scrapperAlimentos.py.
2. Ejecuta:
   `python scrapperAlimentos.py`
3. Ingresa cuántos alimentos quieres recolectar (ej.: 5).
4. Revisa los resultados en output/alimentos_openfoodfacts.json.

Ejemplo de Salida

`[
    {
        "nome": "Acuáfina",
        "ingredientes": ["ABIERTO Y ANTES DE: Ver botella..."],
        "nutricion": {"proteina_100g": 0, ...},
        "alergenos": [],
        "fonte": "openfoodfacts.org"
    }
]`

Notas

- Traducción: La traducción al español puede fallar con textos en francés.
- Limitación: No incluye aminoácidos.
- Ética: Respeta los límites de la API (pausa de 1s por solicitud).