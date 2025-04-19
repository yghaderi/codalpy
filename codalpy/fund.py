import json
from io import BytesIO
from pathlib import Path

import polars as pl
import requests

from codalpy.utils.fund import clean_raw_portfolio_df, find_download_endpoint
from codalpy.utils.http import HEADERS
from codalpy.utils.models import Letter
from codalpy.utils.query import Consts, Issuer, QueryParam, Symbol


class Fund:
    def __init__(self, query: QueryParam):
        self._query = query
        self.consts = Consts()
        self.funds: list[Issuer] = []

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value: QueryParam):
        self._query = value

    def load_funds(self):
        pkg_dir = Path(__file__).parent
        json_path = pkg_dir / "data/symbols.json"
        with open(json_path) as f:
            d = json.load(f).get("funds")
            assert d is not None, "Funds data not found"
            self.funds = [Issuer.model_validate(i) for i in d]

    def handle_symbol(self) -> Issuer:
        if not self.funds:
            self.load_funds()

        symbol = Symbol(symbol=self.query.symbol, issuers=self.funds)
        fund = symbol.match_symbol()
        self.query.symbol = fund.symbol
        return fund

    def letter(self) -> list[Letter]:
        r = requests.get(
            url=self.consts.search_url,
            params=self.query.model_dump(by_alias=True),
            headers=HEADERS,
        )
        data: dict = r.json()
        pages = str(data.get("Page"))
        Letter.base_url = self.consts.base_url
        letters = [Letter.model_validate(i) for i in data["Letters"]]
        if pages.isdigit():
            pages = int(pages)
            if pages > 1:
                for p in range(2, pages + 1):
                    self.query.page_number = p
                    r = requests.get(
                        url=self.consts.search_url,
                        params=self.query.model_dump(by_alias=True),
                        headers=HEADERS,
                    )
                    data: dict = r.json()
                    letters.extend([Letter.model_validate(i) for i in data["Letters"]])
        return letters

    def monthly_portfolio(self):
        """
        .. raw:: html

            <div dir="rtl">
                پورتفوی سهامِ صندوق‌هایِ ETF رو به صورتِ‌ ماهانه بهت میده.
            </div>

        Returns
        -------
        polars.DataFrame

        example
        -------
        >>> from codalpy import Codal, QueryParam
        >>> query = QueryParam(symbol="پتروآگاه",length=-1, from_date="1403/01/01", category=3, letter_type=8, company_state=2, company_type=3)
        >>> codal = Codal(query=query, category="etf")
        >>> codal.etf_portfolio()
        """
        letters = self.letter()
        df = pl.DataFrame()
        for letter in letters:
            if letter.has_attachment:
                attachment = requests.get(letter.attachment_url, headers=HEADERS)
                xlsx_endpoint = find_download_endpoint(attachment.text)
                xlsx = requests.get(
                    f"{self.consts.base_url}/Reports/{xlsx_endpoint}",
                    stream=True,
                    headers=HEADERS,
                )
                raw_df = pl.read_excel(
                    BytesIO(xlsx.content), sheet_id=1, raise_if_empty=False
                )
                if raw_df.is_empty() or raw_df.shape[1] < 9:
                    raw_df = pl.read_excel(BytesIO(xlsx.content), sheet_id=2)
                clean_df = clean_raw_portfolio_df(raw_df)
                clean_df = clean_df.with_columns(
                    publish_date_time=pl.lit(letter.publish_date_time),
                    symbol=pl.lit(letter.symbol),
                    title=pl.lit(letter.title),
                    url=pl.lit(letter.url),
                    attachment_url=pl.lit(letter.attachment_url),
                )
                df = pl.concat([df, clean_df])
        return df
