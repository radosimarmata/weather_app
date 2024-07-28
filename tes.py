import requests
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET

base_url = "https://data.bmkg.go.id/"
url = "https://data.bmkg.go.id/DataMKG/MEWS/DigitalForecast/DigitalForecast-Bengkulu.xml"

response = requests.get(url)
data_xml = response.content

root = ET.fromstring(data_xml)
data_location = []

def parse_forecast(root):
  forecast = root.find('forecast')
  issue = forecast.find('issue')

  timestamp = issue.find('timestamp').text
  year = issue.find('year').text
  month = issue.find('month').text
  day = issue.find('day').text
  hour = issue.find('hour').text
  minute = issue.find('minute').text
  second = issue.find('second').text

  print(f"timestamp: {timestamp}")
  print(f"date: {year}-{month}-{day}")
  print(f"time: {hour}:{minute}:{second}")
  print('-' * 20)

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

    print(f"")
    print(f"area_id: {area_id}")
    print(f"latitude: {latitude}")
    print(f"longitude: {longitude}")
    print(f"coordinate: {coordinate}")
    print(f"type: {type}")
    print(f"region: {region}")
    print(f"level: {level}")
    print(f"description: {description}")
    print(f"domain: {domain}")

    name_en_element = area.find('name[@xml:lang="en_US"]', namespaces)
    name_id_element = area.find('name[@xml:lang="id_ID"]', namespaces)
    name_en = name_en_element.text
    name_id = name_id_element.text

    print(f"name_en: {name_en}")
    print(f"name_id: {name_id}")

    for parameter in area.iter('parameter'):
      param_id = parameter.attrib.get('id','N/A')
      param_description = parameter.attrib.get('description', 'N/A')
      param_type = parameter.attrib.get('type', 'N/A')

      print(f"  parameter_id: {param_id}")
      print(f"  description: {param_description}")
      print(f"  type: {param_type}")

      for timerange in parameter.iter('timerange'):
        time_type = timerange.attrib.get('type', 'N/A')
        hours = timerange.attrib.get('h', 'N/A')
        datetime = timerange.attrib.get('datetime', 'N/A')
        date = f"{datetime[:4]}-{datetime[4:6]}-{datetime[6:8]}"
        time = f"{datetime[8:10]}:{datetime[10:12]}"

        value_element = timerange.find('value')
        value = value_element.text
        unit = value_element.attrib.get('unit', 'N/A')

        print(f"  Timerange type: {time_type}")
        print(f"  Hours: {hours}")
        print(f"  Date: {date}")
        print(f"  Time: {time}")
        print(f"  Value: {value} {unit}")
        print('-' * 10)

      print('-' * 20)    

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

# parse_forecast(root)
if __name__ == '__main__':
  main()