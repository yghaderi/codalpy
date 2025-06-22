from io import BytesIO

import polars as pl
import requests

from codalpy.utils.fund import clean_raw_portfolio_df, find_download_endpoint
from codalpy.utils.http import HEADERS
from codalpy.utils.models import Letter
from codalpy.utils.query import Consts, QueryParam


class Fund:
    def __init__(self, symbol: str, jdate_from: str):
        self._symbol = symbol
        self._jdate_from = jdate_from
        self._query = QueryParam(
            symbol=self.symbol,
            length=-1,
            from_date=self._jdate_from,
            category=3,
            letter_type=8,
            company_state=2,
            company_type=3,
        )
        self._consts = Consts()

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self, value: str):
        self._query = QueryParam.model_validate({**self._query.dict(), "symbol": value})
        self._symbol = value

    @property
    def jdate(self):
        return self._jdate_from

    @jdate.setter
    def jdate(self, value: str):
        self._query.from_date = value
        self._jdate_from = value

    def letter(self) -> list[Letter]:
        r = requests.get(
            url=self._consts.search_url,
            params=self._query.model_dump(by_alias=True),
            headers=HEADERS,
        )
        data: dict = r.json()
        pages = str(data.get("Page"))
        Letter.base_url = self._consts.base_url
        letters = [Letter.model_validate(i) for i in data["Letters"]]
        if pages.isdigit():
            pages = int(pages)
            if pages > 1:
                for p in range(2, pages + 1):
                    self._query.page_number = p
                    r = requests.get(
                        url=self._consts.search_url,
                        params=self._query.model_dump(by_alias=True),
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
        >>> from codalpy import Fund
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
                    f"{self._consts.base_url}/Reports/{xlsx_endpoint}",
                    stream=True,
                    headers=HEADERS,
                )

                raw_df = pl.read_excel(
                    BytesIO(xlsx.content),
                    sheet_id=1,
                    raise_if_empty=False,
                    infer_schema_length=0,
                )
                if raw_df.is_empty() or raw_df.shape[1] < 9:
                    raw_df = pl.read_excel(
                        BytesIO(xlsx.content),
                        has_header=False,
                        sheet_id=2,
                        raise_if_empty=False,
                        infer_schema_length=0,
                    )
                print(raw_df)
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
