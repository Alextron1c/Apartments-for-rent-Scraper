import requests
from bs4 import BeautifulSoup
import io
import time
import csv
from urllib.parse import urljoin
# Total number of pages to scrape 
pages=50

def extract_size(soup):
    room_size = []
    for size in soup.find_all('span', class_="text-semi-strong"):
        if "Relevancy" in size.text: # Skip the filter box w marked with the same class
            continue
        cleansize = size.text.strip()
        room_size.append(cleansize)
    return (room_size)


def extract_address(soup):
    location=[]
    for address in doc.find_all('span', itemprop="address"):
        clean_address=address.text.strip().replace("in","") # take out the in that's included. 
        location.append(clean_address)
    return(location)



def extract_rent(soup): 
    rents=[]
    for rent in doc.find_all(lambda t: t.name == 'span' and t.text == 'Monthly Costs'):
        parent_text=rent.parent.text
        price = ''.join(filter(str.isdigit, parent_text)) # Remove all non-numeric characters from the parent text
        rents.append(price)
    return (rents)


def extract_links(soup):
    links = []
    for link in soup.find_all('span', class_="text-semi-strong"):
        if "Relevancy" in link.text:
            continue
        href = link.parent.get('href')
        url = urljoin('https://realestate.co.jp', href)
        links.append(url)
    return (links)

with open('output.csv', 'w', encoding="utf-8", newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Size', 'Address', 'Rent', 'Link'])

    for i in range(1, pages):
        r = requests.get(f'https://apartments.gaijinpot.com/en/rent/listing?prefecture=JP-13&city=&district=&min_price=&max_price=&min_meter=&rooms=&distance_station=&agent_id=&building_type=&building_age=&updated_within=&transaction_type=&order=&search=Search&page={i}')

        content = r.text
        doc= BeautifulSoup(content, 'html.parser')

        sizes = extract_size(doc)
        addresses = extract_address(doc)
        rents = extract_rent(doc)
        links = extract_links(doc)

        for j in range(len(links)):
            writer.writerow([sizes[j], addresses[j], rents[j], links[j]])