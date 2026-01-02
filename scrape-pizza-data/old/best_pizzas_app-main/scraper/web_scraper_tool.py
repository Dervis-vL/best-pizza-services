import urllib.request
from bs4 import BeautifulSoup as bs
import re, openpyxl

'''
Step 1
This script is a web scraper. It fetches information from 50toppizza.it,
concerning the best pizza's in the world. The web scraper collects:
Rank, name, country, region, place, address. 

The information is linked to an object.
'''

# url to main page of best pizza ever site
url_blank = r'https://www.50toppizza.it/'

def pizza50_it(url_blank):
    # START code to the ranking of the top 100 pizzarias of Italy
    # url for best pizza's in Italy
    url_italy = r'https://www.50toppizza.it/en/50-top-classifica-italia-2020/'

    # load html code from url links Italy
    page_italy = urllib.request.urlopen(url_italy)
    soup_italy = bs(page_italy, features="html.parser")

    # fetch lines with relevant data from Italy
    id_rank_names_it = "h2"
    id_place_region_it = "h5"
    id_url_address_it = "a"

    html_rank_names_it = soup_italy.body.findAll(id_rank_names_it)
    html_place_region_it = soup_italy.body.findAll(id_place_region_it)
    html_url_address_it = soup_italy.body.findAll(id_url_address_it)

    # find all rank, name, region, place and address' via regex in Italy
    regex_rank_it = re.findall('h2 class="oro margin-bottom-30" style="margin-top:0px;">(.*?)°<\/h2>', str(html_rank_names_it))
    regex_name_it = re.findall('h2 class="rosso caps scotchmodern" style="margin-top: 0px;margin-bottom: 0px;line-height:27px;font-size:27px;">(.*?)<\/h2>', str(html_rank_names_it))
    regex_region_place_it = re.findall('<h5 class="h4-2019 nero" style="margin-top: 0px;margin-bottom: 0px;">   (.*?)<\/h5>', str(html_place_region_it))
    regex_url_address_it = re.findall('href="https://www.50toppizza.it/en/recensione/(.*?)">', str(html_url_address_it))

    regex_address_it = []
    id_address_it = "span"
    for url in regex_url_address_it:
        link = url_blank + "en/recensione/" + url
        page = urllib.request.urlopen(link)
        soup = bs(page, features="html.parser")
        html = soup.body.findAll(id_address_it)
        regex = re.findall('<p>(.*?)</p>', str(html))
        for address in regex:
            if len(address) > 0:
                regex_address_it.append(address)

    loop = 1
    regex_region_it = []
    regex_place_it = []
    for itm in regex_region_place_it:
        if loop % 2 == 0:
            regex_place_it.append(itm)
            loop += 1
        else:
            regex_region_it.append(itm)
            loop += 1

    return regex_rank_it, regex_name_it, regex_region_it, regex_place_it, regex_address_it

def pizza50_eu(url_blank):
    # START code to the ranking of the top 50 pizzarias of Europe
    # url for best pizza's in Europe
    url_eu = r'https://www.50toppizza.it/en/50-top-europe-2020/'

    # load html code from url links EU
    page_eu = urllib.request.urlopen(url_eu)
    soup_eu = bs(page_eu, features="html.parser")

    # fetch lines with relevant data from Europe
    id_rank_names_eu = "h2"
    id_place_region_eu = "h5"

    html_rank_names_eu = soup_eu.body.findAll(id_rank_names_eu)
    html_place_region_eu = soup_eu.body.findAll(id_place_region_eu)

    # find all rank, name, region, place and address via regex in Europe
    regex_rank_eu = re.findall('h2 class="oro margin-bottom-30" style="margin-top:0px;">(.*?)°<\/h2>', str(html_rank_names_eu))
    regex_name_eu = re.findall('h2 class="rosso caps scotchmodern" style="margin-top: 0px;margin-bottom: 0px;line-height:27px;font-size:27px;">(.*?)<\/h2>', str(html_rank_names_eu))
    regex_country_city_eu = re.findall('<h5 class="h4-2019 nero" style="margin-top: 0px;margin-bottom: 0px;">   (.*?)<\/h5>', str(html_place_region_eu))

    loop = 1
    regex_country_eu = []
    regex_city_eu = []
    for itm in regex_country_city_eu:
        if loop % 2 == 0:
            regex_city_eu.append(itm)
            loop += 1
        else:
            regex_country_eu.append(itm)
            loop += 1

    return regex_rank_eu, regex_name_eu, regex_country_eu, regex_city_eu

def toppizza_data(info_it, info_eu):

    file_name = "50_top_pizza.xlsx"
    dir = r"C:\Users\ddvanleersum\Documents\01_Dervis\06_Programming\Python\Scripts\Web tools"
    path = dir + "\\" + file_name

    ws_title_it = "Italy"
    ws_title_eu = "Europe"

    wb = openpyxl.Workbook()
    ws = wb['Sheet']
    ws.title = ws_title_it
    ws2 = wb.create_sheet(title=ws_title_eu)

    for itm in range(int(len(info_it[0]))):
        ws.cell(itm+1, 1).value = info_it[0][itm]
        ws.cell(itm+1, 2).value = info_it[1][itm]
        ws.cell(itm+1, 3).value = info_it[2][itm]
        ws.cell(itm+1, 4).value = info_it[3][itm]
        ws.cell(itm+1, 5).value = info_it[4][itm]

    for itm in range(len(info_eu[0])):
        ws2.cell(itm+1, 1).value = info_eu[0][itm]
        ws2.cell(itm+1, 2).value = info_eu[1][itm]
        ws2.cell(itm+1, 3).value = info_eu[2][itm]
        ws2.cell(itm+1, 4).value = info_eu[3][itm]

    wb.save(path)
    wb.close()

if __name__ == "__main__":
    pizza_it = pizza50_it(url_blank)
    pizza_eu = pizza50_eu(url_blank)

    toppizza_data(pizza_it, pizza_eu)
    
    # print(pizza50_eu[0])
  