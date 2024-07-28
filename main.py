import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

base_url = "https://data.bmkg.go.id/"

data_location = []

def get_locations():
  url = base_url + "prakiraan-cuaca/"
  response = requests.get(url)
  soup = BeautifulSoup(response.content, "html.parser")
  table = soup.find('table', class_='table table-striped')
  headers = [header.text for header in table.find_all('th')]
  rows = table.find_all('tr')[1:]


  for row in rows:
    cells = row.find_all('td')
    link = cells[2].find('a')['href'].strip().replace('../', '')
    data_location.append({
      'id': cells[0].text.strip(),
      headers[1]: cells[1].text.strip(),
      headers[2]: cells[2].text.strip(),
      'link': link,
      headers[3]: cells[3].text.strip(),
      headers[4]: cells[4].text.strip(),
    })

def main():
  print("Weather App")
  print("1. Cari Lokasi")
  print("2. Pilih Lokasi")

  choice = input("Masukkan pilihan (1 atau 2): ")

  if(choice == '1'):
    get_locations()
  elif(choice == '2'):
    print("AMBIL DATA")

if __name__ == '__main__':
  main()