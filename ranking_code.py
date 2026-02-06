import urllib.request # modulo que usa python para cosas de internet
import json
import csv
from datetime import datetime
import os
import streamlit as st
import pandas as pd

# --- CONFIGURACIÓN --- (variables)
# Intenta leer de GitHub (env) y si no, de Streamlit (secrets)
API_KEY = os.getenv("API_KEY") or st.secrets.get("API_KEY")
LIMITE = 400  # Número de monedas a rastrear
ARCHIVO_DATOS = 'historico_top400_ranking.csv'

def obtener_top_rankings():
    # Usamos 'listings/latest' para traer la lista completa por ranking
    url = f'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit={LIMITE}'
    headers = { # diccionario de python (clave: valor)
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': API_KEY,
    }

    try:
        req = urllib.request.Request(url, headers=headers) # guarda en req un objeto de la clase Request. Analogía: creas una carta y le pones la dirección a donde tiene que ir (url) y el contenido (diccionario headers  )
        with urllib.request.urlopen(req) as response: # abre la conexión para usarla bajo el nombre response, lo que en response vienen datos ilegibles en bytes
            data = json.loads(response.read().decode()) # response.read() convierte los 0s y 1s en bloques
            # decode() traduce a UTF-8
            #json.loads() convierte la string UTF-8 en listas y diccionarios: la base de datos en crudo e información del paquete (data y status)
            monedas = data['data'] # nos quedamos con data, que es la base de datos en especifico.
            fecha = datetime.now().strftime('%Y-%m-%d') #fecha del momento de ejecución
            
            datos_a_guardar = []
            for moneda in monedas:
                datos_a_guardar.append([
                    fecha,
                    moneda['name'],
                    moneda['symbol'],
                    moneda['cmc_rank']
                ]) #lista de listas. Cada lista es una moneda
            
            guardar_en_csv(datos_a_guardar)
            print(f"[{fecha}] Guardadas {len(monedas)} monedas exitosamente.")

    except Exception as e:
        print(f"Error al obtener datos: {e}")

def guardar_en_csv(filas):
    columnas = ['Fecha', 'Nombre', 'Ticker', 'Ranking']
    df_nuevo = pd.DataFrame(filas, columns=columnas)

    if os.path.isfile(ARCHIVO_DATOS):
        # 1. Leemos lo que ya tenemos
        df_antiguo = pd.read_csv(ARCHIVO_DATOS)
        # 2. Juntamos lo viejo con lo nuevo
        df_final = pd.concat([df_antiguo, df_nuevo], ignore_index=True)
    else:
        df_final = df_nuevo

    # 3. EL TRUCO: Eliminamos duplicados
    # Si coinciden Fecha y Ticker, se queda con el último (keep='last')
    df_final = df_final.drop_duplicates(subset=['Fecha', 'Ticker'], keep='last')

    # 4. Guardamos el archivo limpio (sobrescribiendo el anterior)
    df_final.to_csv(ARCHIVO_DATOS, index=False, encoding='utf-8')
    print(f"Base de datos actualizada y limpia de duplicados.")

if __name__ == "__main__":
    obtener_top_rankings()