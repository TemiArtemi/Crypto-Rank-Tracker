import urllib.request # modulo que usa python para cosas de internet
import json
import csv
from datetime import datetime
import os
import streamlit as st

# --- CONFIGURACIÓN --- (variables)
API_KEY = st.secrets["API_KEY"]
LIMITE = 400  # Número de monedas a rastrear
ARCHIVO_DATOS = 'historico_top300_ranking.csv'

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
    file_exists = os.path.isfile(ARCHIVO_DATOS) # Devuelve un booleano si archivo está en el directorio actual o no
    with open(ARCHIVO_DATOS, mode='a', newline='', encoding='utf-8') as file: # el mode='a' es añadir. El mode='w' seria borrar todo y escribir desde cero
    #newline='' para que ni haya lineas en blanco
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['Fecha', 'Nombre', 'Ticker', 'Ranking'])
        writer.writerows(filas)  # Guardamos todas las filas de golpe

if __name__ == "__main__":
    obtener_top_rankings()