from typing import Dict, Optional, Self
from urllib.parse import urljoin

import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from stock import Stock

DEFAULT_DRIVER_OPTIONS = {
    "headless": False,  # For some reason, it doesn't work with headless mode
    "use_subprocess": True,
}

TIME_TO_WAIT_PAGE_LOAD_IN_SECONDS = 10

STATUSINVEST_URL = "https://statusinvest.com.br"


class StatusInvest:
    def __init__(self: Self, driver_options: Optional[Dict[str, str]] = None) -> None:
        if driver_options is None:
            driver_options = {}

        driver_options.update(DEFAULT_DRIVER_OPTIONS)
        self.driver = uc.Chrome(**driver_options)

    def _parse_stock(self: Self) -> Stock:
        price = self.driver.find_element(
            By.CSS_SELECTOR, '[title="Valor atual do ativo"] strong.value'
        ).text
        dividend_yield_in_percent = self.driver.find_element(
            By.CSS_SELECTOR,
            '[title="Dividend Yield com base nos últimos 12 meses"] strong.value',
        ).text
        net_price = self.driver.find_element(
            By.CSS_SELECTOR,
            '[title="Dá uma ideia do quanto o mercado está disposto a pagar pelos lucros da empresa."] strong',
        ).text
        price_over_asset_value = self.driver.find_element(
            By.CSS_SELECTOR,
            '[title="Facilita a análise e comparação da relação do preço de negociação de um ativo com seu VPA."] strong',
        ).text
        return_on_equity_in_percent = self.driver.find_element(
            By.CSS_SELECTOR,
            '[title="Mede a capacidade de agregar valor de uma empresa a partir de seus próprios recursos e do dinheiro de investidores."] strong',
        ).text

        return {
            "price": price,
            "dividend_yield_in_percent": dividend_yield_in_percent,
            "net_price": net_price,
            "price_over_asset_value": price_over_asset_value,
            "return_on_equity_in_percent": return_on_equity_in_percent,
        }

    def get_stock(self: Self, code: str) -> Stock:
        stock_url = urljoin(STATUSINVEST_URL, f"/acoes/{code}")
        self.driver.get(stock_url)
        self.driver.implicitly_wait(TIME_TO_WAIT_PAGE_LOAD_IN_SECONDS)
        return Stock(code=code, **self._parse_stock())


if __name__ == "__main__":
    status_invest = StatusInvest()
    stock = status_invest.get_stock("ITSA4")
    print(stock)
