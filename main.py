import requests
from bs4 import BeautifulSoup
import json
import xml.etree.ElementTree as ET
import os

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
    json.dump(data_location, f, ensure_ascii=False, indent=2)

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
      filename = input("Masukkan nama file untuk menyimpan hasil (tanpa ekstensi .json): ")
      if not filename:
        filename = data_location[choice - 1]['Data'].lower().replace(' ', '_')
      get_weather(data_location[choice - 1]['link'], filename)
    elif choice == '0':
      print("Keluar dari pilihan lokasi")
    else:
      print("Pilihan tidak valid")
  else:
    print("Input tidak valid")

def get_weather(link, filename):
  url = base_url + link
  response = requests.get(url)
  data_xml = response.content

  root = ET.fromstring(data_xml)

  parse_forecast(root, filename)

def parse_forecast(root, filename):
  forecast = root.find('forecast')
  issue = forecast.find('issue')

  timestamp = issue.find('timestamp').text
  year = issue.find('year').text
  month = issue.find('month').text
  day = issue.find('day').text
  hour = issue.find('hour').text
  minute = issue.find('minute').text
  second = issue.find('second').text

  weather_data = {
    'timestamp': timestamp,
    'date': f"{year}-{month}-{day}",
    'time': f"{hour}:{minute}:{second}",
    'areas': []
  }

  namespaces = {'xml': 'http://www.w3.org/XML/1998/namespace'}

  for area in root.iter('area'):
    area_id = area.attrib.get('id', 'N/A')
    latitude = area.attrib.get('latitude', 'N/A')
    longitude = area.attrib.get('longitude', 'N/A')
    coordinate = area.attrib.get('coordinate', 'N/A')
    type = area.attrib.get('type', 'N/A')
    region = area.attrib.get('region', 'N/A')
    level = area.attrib.get('level', 'N/A')
    description = area.attrib.get('description', 'N/A')
    domain = area.attrib.get('domain', 'N/A')

    name_en_element = area.find('name[@xml:lang="en_US"]', namespaces)
    name_id_element = area.find('name[@xml:lang="id_ID"]', namespaces)
    name_en = name_en_element.text
    name_id = name_id_element.text

    area_data = {
      'area_id': area_id,
      'latitude': latitude,
      'longitude': longitude,
      'coordinate': coordinate,
      'type': type,
      'region': region,
      'level': level,
      'description': description,
      'domain': domain,
      'name_en': name_en,
      'name_id': name_id,
      'parameters': []
    }

    for parameter in area.iter('parameter'):
      param_id = parameter.attrib.get('id','N/A')
      param_description = parameter.attrib.get('description', 'N/A')
      param_type = parameter.attrib.get('type', 'N/A')

      param_data = {
        'parameter_id': param_id,
        'description': param_description,
        'type': param_type,
        'timeranges': []
      }

      for timerange in parameter.iter('timerange'):
        time_type = timerange.attrib.get('type', 'N/A')
        hours = timerange.attrib.get('h', 'N/A')
        datetime = timerange.attrib.get('datetime', 'N/A')
        date = f"{datetime[:4]}-{datetime[4:6]}-{datetime[6:8]}"
        time = f"{datetime[8:10]}:{datetime[10:12]}"

        value_element = timerange.find('value')
        value = value_element.text
        unit = value_element.attrib.get('unit', 'N/A')

        timerange_data = {
          'type': time_type,
          'hours': hours,
          'date': date,
          'time': time,
          'value': value,
          'unit': unit
        }

        param_data['timeranges'].append(timerange_data)

      area_data['parameters'].append(param_data)
    weather_data['areas'].append(area_data)

  if not os.path.exists('result'):
    os.makedirs('result')
  
  filepath = os.path.join('result', f"{filename}.json")
  with open(filepath, 'w', encoding='utf-8') as f:
    json.dump(weather_data, f, ensure_ascii=False, indent=2)

  print(f"Hasil cuaca telah disimpan ke {filepath}")

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