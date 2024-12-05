import requests
from bs4 import BeautifulSoup
import pandas as pd
base_url = "https://coinmarketcap.com"

historical_url = f"{base_url}/historical/"

#hago un request con el metodo get a la historical_url
respuesta = requests.get(historical_url)

headers = [
    "Rank", "Name", "Symbol", "Market Cap", "Price",
    "Circulating Supply", "Volume (24h)", "% 1h", "% 24h", "% 7d","Date"
]

btc_data = []


if respuesta.status_code == 200:
    #Crea conexión a /historical/
    soup = BeautifulSoup(respuesta.text, 'html.parser')
    #Busca todos los <a> con dicha clase
    historical_links = soup.find_all('a', class_="historical-link cmc-link")
    
    filtered_links = []

    for link in historical_links:
        try:
            href = link['href']
            date_part = href.split('/historical/')[1][:-2]
            year = int(date_part[:4])
            if year > 2020:
                filtered_links.append((link.text.strip(), href))
        except KeyError:
            print("No existe el atributo href")

    for fecha, href in filtered_links:
        historical_url = f"{base_url}{href}"
        print(f"Extrayendo del dia {fecha}")
        # Solicitar la página histórica
        response_hist = requests.get(historical_url)
        if response_hist.status_code != 200:
            print(f"No hay respuesta para /historical/{fecha}")
            continue
        # Procesar  coinmarket/historical/...
        soup_hist = BeautifulSoup(response_hist.text, 'html.parser')
        mes_soup = soup_hist.find("h1", class_="sc-9a24a11e-0")
        if mes_soup:
            mes = " ".join(mes_soup.text.split()[3:])
        else:
            mes = "Fecha desconocida"
        tr=soup_hist.find("tr",class_="cmc-table-row")
        tds=tr.find_all("td")
        # Verifica si 
        if tds[2].text=="BTC":
            btc_dicc={
                headers[i]: tds[i].text.strip() for i in range(len(headers))
            }
            btc_dicc["Date"]=mes
            btc_data.append(btc_dicc)
        
#Convierte a CSV
data=pd.DataFrame(btc_data)
#Guarda el CSV
data.to_csv("bitcoins.csv") 