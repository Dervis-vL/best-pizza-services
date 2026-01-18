"""Main logic for the pizza data scraper.

This script is a web scraper. It fetches information from 50toppizza.it,
concerning the best pizza's in the world. The web scraper collects:
Rank, name, country, region, place, address. 

The information is linked to an object.
"""

import urllib.request as url_request

from bs4 import BeautifulSoup as bs

from pizza_data_scraper import enums, constants, utils


def get_scraped_data(location: enums.Categories, year: enums.Year) -> bs:
    """Function for scraping data from the best pizza's website.

    :param location: The location to scrape.
    :type location: enums.Location
    :param year: The year to scrape.
    :type year: enums.Year

    :return: The parsed HTML content.
    :rtype: BeautifulSoup§
    """
    # get endpoint
    endpoint = utils.create_endpoint(location, year)
    # url for best pizza's in Italy
    data_url = constants.URL_HOME / endpoint

    # Load page
    page = url_request.urlopen(str(data_url))
    # Create HTML soup
    soup =  bs(page, features="html.parser")
    # Get url from pizzeria cards
    cards = soup.select("a#scheda")
    pizzeria_url = utils.get_pizzeria_url_from_card(cards[0], "href")




# def pizza50(location: enums.Location, year: enums.Year) -> tuple[list[str], list[str], list[str], list[str], list[str]]:
#     """Function for scraping data from the best pizza's website.

#     :param location: The location to scrape.
#     :type location: enums.Location
#     :param year: The year to scrape.
#     :type year: enums.Year

#     :return: A tuple containing lists of ranks, names, regions, places, and addresses.
#     :rtype: tuple[list[str], list[str], list[str], list[str], list[str]]
#     """
#     # url for best pizza's in Italy
#     data_url = settings.source_page.url_home / f"{settings.source_page.selection_type}-{location.value}-{year.value}/"

#     # Load page
#     page = url_request.urlopen(data_url)
#     # Parse HTML
#     soup = bs(page, features="html.parser")

#     # fetch lines with relevant data from Italy
#     id_rank_names_it = "h2"
#     id_place_region_it = "h5"
#     id_url_address_it = "a"

#     html_rank_names_it = soup_italy.body.findAll(id_rank_names_it)
#     html_place_region_it = soup_italy.body.findAll(id_place_region_it)
#     html_url_address_it = soup_italy.body.findAll(id_url_address_it)

#     # find all rank, name, region, place and address' via regex in Italy
#     regex_rank_it = re.findall('h2 class="oro margin-bottom-30" style="margin-top:0px;">(.*?)°<\/h2>', str(html_rank_names_it))
#     regex_name_it = re.findall('h2 class="rosso caps scotchmodern" style="margin-top: 0px;margin-bottom: 0px;line-height:27px;font-size:27px;">(.*?)<\/h2>', str(html_rank_names_it))
#     regex_region_place_it = re.findall('<h5 class="h4-2019 nero" style="margin-top: 0px;margin-bottom: 0px;">   (.*?)<\/h5>', str(html_place_region_it))
#     regex_url_address_it = re.findall('href="https://www.50toppizza.it/en/recensione/(.*?)">', str(html_url_address_it))

#     regex_address_it = []
#     id_address_it = "span"
#     for url in regex_url_address_it:
#         link = url + "en/recensione/" + url
#         page = urllib.request.urlopen(link)
#         soup = bs(page, features="html.parser")
#         html = soup.body.findAll(id_address_it)
#         regex = re.findall('<p>(.*?)</p>', str(html))
#         for address in regex:
#             if len(address) > 0:
#                 regex_address_it.append(address)

#     loop = 1
#     regex_region_it = []
#     regex_place_it = []
#     for itm in regex_region_place_it:
#         if loop % 2 == 0:
#             regex_place_it.append(itm)
#             loop += 1
#         else:
#             regex_region_it.append(itm)
#             loop += 1

#     return regex_rank_it, regex_name_it, regex_region_it, regex_place_it, regex_address_it

# def pizza50_eu(url_blank):
#     # START code to the ranking of the top 50 pizzarias of Europe
#     # url for best pizza's in Europe
#     url_eu = r'https://www.50toppizza.it/en/50-top-europe-2020/'

#     # load html code from url links EU
#     page_eu = url_request.urlopen(url_eu)
#     soup_eu = bs(page_eu, features="html.parser")

#     # fetch lines with relevant data from Europe
#     id_rank_names_eu = "h2"
#     id_place_region_eu = "h5"

#     html_rank_names_eu = soup_eu.body.findAll(id_rank_names_eu)
#     html_place_region_eu = soup_eu.body.findAll(id_place_region_eu)

#     # find all rank, name, region, place and address via regex in Europe
#     regex_rank_eu = re.findall('h2 class="oro margin-bottom-30" style="margin-top:0px;">(.*?)°<\/h2>', str(html_rank_names_eu))
#     regex_name_eu = re.findall('h2 class="rosso caps scotchmodern" style="margin-top: 0px;margin-bottom: 0px;line-height:27px;font-size:27px;">(.*?)<\/h2>', str(html_rank_names_eu))
#     regex_country_city_eu = re.findall('<h5 class="h4-2019 nero" style="margin-top: 0px;margin-bottom: 0px;">   (.*?)<\/h5>', str(html_place_region_eu))

#     loop = 1
#     regex_country_eu = []
#     regex_city_eu = []
#     for itm in regex_country_city_eu:
#         if loop % 2 == 0:
#             regex_city_eu.append(itm)
#             loop += 1
#         else:
#             regex_country_eu.append(itm)
#             loop += 1

#     return regex_rank_eu, regex_name_eu, regex_country_eu, regex_city_eu
