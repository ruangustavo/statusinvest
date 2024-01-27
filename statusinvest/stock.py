from typing import Self

from utils import str_to_float


class Stock:
    def __init__(
        self: Self,
        code: str,
        price: float,
        dividend_yield_in_percent: float,
        net_price: float,
        price_over_asset_value: float,
        return_on_equity_in_percent: float,
    ) -> None:
        self.code = code
        self.price = str_to_float(price)
        self.dividend_yield_in_percent = str_to_float(dividend_yield_in_percent)
        self.net_price = str_to_float(net_price)
        self.price_over_asset_value = str_to_float(price_over_asset_value)

        self.return_on_equity_in_percent = return_on_equity_in_percent.replace("%", "")
        self.return_on_equity_in_percent = str_to_float(
            self.return_on_equity_in_percent
        )

    def __repr__(self: Self) -> str:
        attrs = ", ".join(f"{attr}={value}" for attr, value in self.__dict__.items())
        return f"Stock({attrs})"
