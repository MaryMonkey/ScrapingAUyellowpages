import pandas as pd
import numpy as np
import requests
from lxml import html
import unicodecsv as csv
import argparse


def au_yellowpage_scrape(totalpage):

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Cache-Control': 'max-age=286',
        'Connection': 'keep-alive',
        'Host': 'www.yellowpages.com.au',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36'}

    scrapped_results = []

    for pagenumber in range(1, totalpage + 1):
        url = 'https://www.yellowpages.com.au/search/listings?clue=Accountants+%26+Auditors&locationClue=QLD&pageNumber={}&referredBy=www.yellowpages.com.au&eventType=pagination'.format(
            pagenumber)
        print('... please wait...')
        print("retrieving ", url, " page ", str(pagenumber))

        response = requests.get(url, verify=False, headers=headers)
        print('parsing page ', str(pagenumber))

        if response.status_code == 200:
            parser = html.fromstring(response.text)
            base_url = "https://www.yellowpages.com.au"
            parser.make_links_absolute(base_url)
            XPATH_LISTINGS = "//div[@class='search-results search-results-data listing-group']//div[@class='search-contact-card call-to-actions-5 feedback-feature-on']"
            listings = parser.xpath(XPATH_LISTINGS)

            for results in listings:

                try:
                    XPATH_BUSINESS_NAME = ".//div[@class='body left']//a[@class='listing-name']//text()"
                    raw_business_name = results.xpath(XPATH_BUSINESS_NAME)[0]
                    XPATH_INDUSTRY_CATEGORY = ".//div[@class='body left']//p[@class='listing-heading']//text()"
                    raw_industry_category = results.xpath(XPATH_INDUSTRY_CATEGORY)[
                        0].split(' - ')[0]
                    XPATH_BUSINESS_PAGE = ".//div[@class='body left']//a[@class='listing-name']//@href"
                    raw_business_page = results.xpath(XPATH_BUSINESS_PAGE)[0]
                    XPATH_SUBURB = ".//div[@class='body left']//p[@class='listing-heading']//text()"
                    raw_suburb = results.xpath(XPATH_SUBURB)[
                        0].split(' - ')[1].split(', ')[0]
                    XPATH_STATE = ".//div[@class='body left']//p[@class='listing-heading']//text()"
                    raw_state = results.xpath(XPATH_STATE)[0].split(', ')[
                        1].split(' ')[0]
                    XPATH_POSTCODE = ".//div[@class='body left']//p[@class='listing-heading']//text()"
                    raw_postcode = results.xpath(XPATH_POSTCODE)[
                        0].split(' ')[-1]
                except BaseException:
                    XPATH_BUSINESS_NAME = ".//div[@class='body left right']//a[@class='listing-name']//text()"
                    raw_business_name = results.xpath(XPATH_BUSINESS_NAME)[0]
                    XPATH_INDUSTRY_CATEGORY = ".//div[@class='body left right']//p[@class='listing-heading']//text()"
                    raw_industry_category = results.xpath(XPATH_INDUSTRY_CATEGORY)[
                        0].split(' - ')[0]
                    XPATH_BUSINESS_PAGE = ".//div[@class='body left right']//a[@class='listing-name']//@href"
                    raw_business_page = results.xpath(XPATH_BUSINESS_PAGE)[0]
                    XPATH_SUBURB = ".//div[@class='body left right']//p[@class='listing-heading']//text()"
                    raw_suburb = results.xpath(XPATH_SUBURB)[
                        0].split(' - ')[1].split(', ')[0]
                    XPATH_STATE = ".//div[@class='body left right']//p[@class='listing-heading']//text()"
                    raw_state = results.xpath(XPATH_STATE)[0].split(', ')[
                        1].split(' ')[0]
                    XPATH_POSTCODE = ".//div[@class='body left right']//p[@class='listing-heading']//text()"
                    raw_postcode = results.xpath(XPATH_POSTCODE)[
                        0].split(' ')[-1]

                XPATH_TELEPHONE = ".//span[@class='contact-text']//text()"
                XPATH_STREET = ".//div[@class='body left listing-address-container']//div[@class='body']//p[@class='listing-address mappable-address mappable-address-with-poi']//text()"
                XPATH_COMPANY_WEBSITE = ".//div[@class='real-actions cag-groups-3 cag-items-5']//div[3]//div[1]//a/@href"

                raw_telephone = results.xpath(XPATH_TELEPHONE)[0]
                raw_street = results.xpath(XPATH_STREET)[0].split(
                    ', ')[0] if results.xpath(XPATH_STREET) else None
                raw_company_website = results.xpath(XPATH_COMPANY_WEBSITE)

                business_name = ''.join(
                    raw_business_name).strip() if raw_business_name else None
                telephone = ''.join(
                    raw_telephone).strip() if raw_telephone else None
                industry_category = ''.join(
                    raw_industry_category).strip() if raw_industry_category else None
                business_page = ''.join(
                    raw_business_page).strip() if raw_business_page else None
                street = ''.join(raw_street).strip() if raw_street else None
                suburb = ''.join(raw_suburb).strip() if raw_suburb else None
                state = ''.join(raw_state).strip() if raw_state else None
                postcode = ''.join(
                    raw_postcode).strip() if raw_postcode else None
                mobile_service = 'Yes' if not street else 'No'
                company_website = ''.join(
                    raw_company_website).strip() if raw_company_website else None

                business_details = {
                    'Business Name': business_name,
                    'Industry Category': industry_category,
                    'Telephone': telephone,
                    'Business Page': business_page,
                    'Street': street,
                    'Suburb': suburb,
                    'State': state,
                    'Postcode': postcode,
                    'Mobile Business Service': mobile_service,
                    'Company Website': company_website
                }
                scrapped_results.append(business_details)

    return scrapped_results


if __name__ == "__main__":
    sr = au_yellowpage_scrape(29)
    if sr:
        # writing the result to scraped-data.csv
        with open('scraped-data.csv', 'wb') as csvfile:
            fieldnames = [
                'Business Name',
                'Industry Category',
                'Telephone',
                'Business Page',
                'Street',
                'Suburb',
                'State',
                'Postcode',
                'Mobile Business Service',
                'Company Website']
            writer = csv.DictWriter(
                csvfile,
                fieldnames=fieldnames,
                quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for data in sr:
                writer.writerow(data)
    print('Done writing!')
