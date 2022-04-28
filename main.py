import requests
from bs4 import BeautifulSoup
import json
import re


class Stock:
    def __init__(self) -> None:
        self.nepse_code = ''
        self.company_name = ''
        self.num_of_tx = 0
        self.max_price = 0
        self.min_price = 0
        self.closing_price = 0
        self.traded_shares = 0
        self.amount = 0
        self.prev_closing = 0
        self.difference_rs = 0


def scrape_nepse_table_data() -> list[Stock]:
    """
    Returns a list of `Stock` objects parsing the table from Nepal Stock Exchange.
    """
    html_table = requests.get('http://www.nepalstock.com/todaysprice/export').text
    soup = BeautifulSoup(html_table)
    rows = soup.findAll('tr')

    stocks = []

    for i in rows[1:]:
        stock = Stock()
        stock.company_name = i.findAll('td')[0].text
        stock.num_of_tx = i.findAll('td')[1].text
        stock.max_price = i.findAll('td')[2].text
        stock.min_price = i.findAll('td')[3].text
        stock.closing_price = i.findAll('td')[4].text
        stock.traded_shares = i.findAll('td')[5].text
        stock.amount = i.findAll('td')[6].text
        stock.prev_closing = i.findAll('td')[7].text
        stock.difference_rs = i.findAll('td')[8].text

        stocks.append(stock)

    return stocks


def fetch_symbols_from_merolagani():
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
    Fetch stock info from MeroLagani
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


if __name__ == '__main__':
    print(get_stock_info('NICA'))
