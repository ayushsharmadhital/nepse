import requests
from bs4 import BeautifulSoup


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


def scrape_nepse_table_data(html_table:str) -> list[Stock]:
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


stocks = []

with requests.get('http://www.nepalstock.com/todaysprice/export') as resp:
    stocks = scrape_nepse_table_data(resp.text)



if __name__ == '__main__':
    print(len(stocks))



