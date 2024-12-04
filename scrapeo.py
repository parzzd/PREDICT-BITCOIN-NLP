import requests
from bs4 import BeautifulSoup

base_url = "https://coinmarketcap.com"
historical_url = f"{base_url}/historical/"

#hago un request con el metodo get a la historical_url
respuesta = requests.get(historical_url)


if respuesta.status_code == 200:
    soup = BeautifulSoup(respuesta.text, 'html.parser')

    historical_links = soup.find_all('a', class_="historical-link cmc-link")
    
    filtered_links = []
    for link in historical_links:
        href = link['href']
        if '/historical/' in href:
            date_part = href.split('/historical/')[1][:8]  # Extrae "YYYYMMDD"
            year = int(date_part[:4])
            if year > 2020:
                filtered_links.append((link.text.strip(), href))  # Guardar fecha y href



    for fecha, href in filtered_links:
        # Construir la URL completa
        historical_url = f"{base_url}{href}"
        print(f"Extrayendo datos de: {historical_url} para la fecha {fecha}")

        # Solicitar la página histórica
        response_hist = requests.get(historical_url)
        if response_hist.status_code != 200:
            print(f"No se pudo acceder a la página histórica para la fecha {fecha}")
            continue

        # Procesar la página histórica
        soup_hist = BeautifulSoup(response_hist.text, 'html.parser')
        mes_soup = soup_hist.find("h1", class_="sc-9a24a11e-0")
        if mes_soup:
            mes = " ".join(mes_soup.text.split()[3:])
        else:
            mes = "Fecha desconocida"

        # Obtener filas de la tabla
        rows = soup_hist.find_all('tr', class_="cmc-table-row")
        for row in rows:
            if 'BTC' in row.text:  # Filtrar datos de Bitcoin
                columns = row.find_all('td')
                if len(columns) >= 10:  # Validar que haya suficientes columnas
                    rank = columns[0].text.strip()
                    name = columns[1].text.strip()
                    market_cap = columns[3].text.strip()
                    price = columns[4].text.strip()
                    print(f"Fecha: {mes}, Rank: {rank}, Nombre: {name}, Precio: {price}, Market Cap: {market_cap} \n")
