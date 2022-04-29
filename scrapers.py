import requests
from bs4 import BeautifulSoup
import json
import re

def fetch_nepse_table_data() -> list[dict]:
    """
    Returns a `list` of `dict` having following data:
    * `Company Name`
    * `No. of Tx`
    * `Max Price`
    * `Min Price`
    * `Closing Price`
    * `Traded Shares`
    * `Amount`
    * `Prev. Closing`
    * `Difference Rs.`
    """
    html_table = requests.get('http://www.nepalstock.com/todaysprice/export').text
    soup = BeautifulSoup(html_table, features='lxml')
    rows = soup.findAll('tr')

    stocks = []

    for i in rows[1:]:
        stock = {
            'Company Name': i.findAll('td')[0].text,
            'No. of Tx': i.findAll('td')[1].text,
            'Max Price': i.findAll('td')[2].text,
            'Min Price': i.findAll('td')[3].text,
            'Closing Price': i.findAll('td')[4].text,
            'Traded Shares': i.findAll('td')[5].text,
            'Amount': i.findAll('td')[6].text,
            'Prev. Closing': i.findAll('td')[7].text,
            'Difference Rs.': i.findAll('td')[8].text,
        }
        stocks.append(stock)
    return stocks


def fetch_symbols_from_merolagani() -> list[tuple]:
    """
    Returns a list of tuple i.e. (`Nepse Code`, `Stock Name`)
    """
    with requests.get('http://merolagani.com/handlers/AutoSuggestHandler.ashx?type=Company') as resp:
        suggestions = json.loads(resp.text)
        companies = [
            (
                re.findall('(.*)\s*\(.*\)', _['l'])[0].strip(),
                re.findall('\((.*)\)', _['l'])[0].strip()
            )
            for _ in suggestions
        ]

        return companies


def get_stock_info(nepse_code: str) -> dict:
    """
    Fetch stock info from `MeroLagani` which contains:
    * `Sector`
    * `Shares Outstanding`
    * `Market Price`
    * `% Change`
    * `Last Traded On`
    * `52 Weeks High - Low`
    * `180 Day Average`
    * `120 Day Average`
    * `1 Year Yield`
    * `P/E Ratio`
    * `Book Value`
    * `PBV`
    * `30-Day Avg Volume`
    * `Market Capitalization`
    """
    page_source = requests.get(f'https://merolagani.com/CompanyDetail.aspx?symbol={nepse_code}').text
    soup = BeautifulSoup(page_source, features='lxml')
    table = soup.find('table')
    info = dict()

    for tbody in table.children:
        data = tuple([_.strip() for _ in tbody.get_text().split('\n') if _.strip()])
        if data and len(data) == 2:
            info[data[0]] = data[1]

    return info