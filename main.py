import requests
from bs4 import BeautifulSoup
import json
import xml.etree.ElementTree as ET

base_url = "https://data.bmkg.go.id/"

def get_locations():
  url = base_url + "prakiraan-cuaca/"
  response = requests.get(url)
  soup = BeautifulSoup(response.content, "html.parser")
  table = soup.find('table', class_='table table-striped')
  headers = [header.text for header in table.find_all('th')]
  rows = table.find_all('tr')[1:]
  data_location = []

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

  with open('data_location.json', 'w', encoding='utf-8') as f:
    json.dump(data_location, f, ensure_ascii=False, indent=4)

def display_location(data_location):
  print("\nDaftar Lokasi:")
  for idx, location in enumerate(data_location):
    print(f"{idx + 1}. {location ['Data']}")
  choice = input("\nPilih Lokasi dengan nomor (atau ketik '0' untuk keluar): ")
  if choice.isdigit():
    choice = int(choice)
    if 1 <= choice <= len(data_location):
      print(f"Anda memilih: {data_location[choice -1]['Data']}")
      print(f"URL: {data_location[choice -1]['link']}")
    elif choice == '0':
      print("Keluar dari pilihan lokasi")
    else:
      print("Pilihan tidak valid")
  else:
    print("Input tidak valid")


def main():
  while True:
    print("Weather App")
    print("1. Cari Lokasi")
    print("2. Pilih Lokasi")
    print("3. Keluar")

    choice = input("Masukkan pilihan (1, 2 atau 3): ")

    if(choice == '1'):
      get_locations()
      print("Lokasi telah diperbarui.")
    elif(choice == '2'):
      try:
        with open('data_location.json', 'r', encoding='utf-8') as file:
          data_location = json.load(file)
          if data_location:
            display_location(data_location)
          else:
            print("Tidak ada data lokasi. Harap jalankan pilihan 1 terlebih dahulu")
      except FileNotFoundError:
        print('File JSON data lokasi tidak ditemukan. Ambil data lokasi terlebih dahulu.')
      except json.JSONDecodeError:
        print('Gagal membaca file JSON.')
      
    elif choice == '3':
      print("Terima kasih telah menggunakan Weather App")
      break
    else:
      print("Pilihan tidak valid. Harap masukkan 1 atau 2")
if __name__ == '__main__':
  main()