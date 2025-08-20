from io import BytesIO

import polars as pl
import requests

from codalpy.utils.data import symbols
from codalpy.utils.fund import clean_raw_portfolio_df, find_download_endpoint
from codalpy.utils.http import HEADERS
from codalpy.utils.models import Letter
from codalpy.utils.query import Consts, QueryParam
from codalpy.utils.utils import normalize_fs_item

__all__ = ["Fund"]


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
        self._query = QueryParam.model_validate(
            {**self._query.model_dump(), "symbol": value}
        )
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

    @staticmethod
    def supported_funds() -> list[dict[str, str]]:
        """
        .. raw:: html

            <div dir="rtl">
                اسم و نمادِ صندوق‌هایی که پشتیبانی میشه رو بهت میده.
            </div>

        Returns
        -------
        list[dict[str, str]]

        example
        -------
        >>> from codalpy import Fund
        >>> Fund.supported_funds()
        """
        return symbols.get("funds", [])

    def monthly_portfolio(self) -> pl.DataFrame:
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
        >>> fund = Fund(symbol="شتاب", jdate_from="1404/01/01")
        >>> fund.monthly_portfolio()
        shape: (760, 18)
        ┌─────────────────────────────┬────────────┬────────────────┬──────────────────┬───┬────────┬─────────────────────────────────┬─────────────────────────────────┬─────────────────────────────────┐
        │ name                        ┆ volume_beg ┆ total_cost_beg ┆ net_proceeds_beg ┆ … ┆ symbol ┆ title                           ┆ url                             ┆ attachment_url                  │
        │ ---                         ┆ ---        ┆ ---            ┆ ---              ┆   ┆ ---    ┆ ---                             ┆ ---                             ┆ ---                             │
        │ str                         ┆ i64        ┆ i64            ┆ i64              ┆   ┆ str    ┆ str                             ┆ str                             ┆ str                             │
        ╞═════════════════════════════╪════════════╪════════════════╪══════════════════╪═══╪════════╪═════════════════════════════════╪═════════════════════════════════╪═════════════════════════════════╡
        │ آهن و فولاد غدیر ایرانیان    ┆ 4556339    ┆ 31093465496    ┆ 24367250852      ┆ … ┆ شتاب   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
        │ البرزدارو                   ┆ 26671574   ┆ 80704956520    ┆ 99052112711      ┆ … ┆ شتاب   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
        │ انتقال داده های آسیاتک      ┆ 138080161  ┆ 557028375688   ┆ 521719877943     ┆ … ┆ شتاب   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
        │ ایران خودرو دیزل            ┆ 207374030  ┆ 349859951641   ┆ 321990921362     ┆ … ┆ شتاب   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
        │ ایران‌ خودرو                 ┆ 730831581  ┆ 291639316957   ┆ 422086700327     ┆ … ┆ شتاب   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
        │ …                           ┆ …          ┆ …              ┆ …                ┆ … ┆ …      ┆ …                               ┆ …                               ┆ …                               │
        │ مهرمام میهن                 ┆ 0          ┆ 0              ┆ 0                ┆ … ┆ شتاب   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
        │ سرمایه گذاری گروه توسعه ملی ┆ 0          ┆ 0              ┆ 0                ┆ … ┆ شتاب   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
        │ اختیارخ فزر-38000-14031212  ┆ 0          ┆ 0              ┆ 0                ┆ … ┆ شتاب   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
        │ اختیارخ فزر-36000-14031212  ┆ 0          ┆ 0              ┆ 0                ┆ … ┆ شتاب   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
        │ گروه دارویی سبحان           ┆ 0          ┆ 0              ┆ 0                ┆ … ┆ شتاب   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
        └─────────────────────────────┴────────────┴────────────────┴──────────────────┴───┴────────┴─────────────────────────────────┴─────────────────────────────────┴─────────────────────────────────┘
        """
        letters = self.letter()
        df = pl.DataFrame()
        for letter in letters:
            if letter.has_attachment:
                attachment = requests.get(letter.attachment_url, headers=HEADERS)
                xlsx_endpoint = find_download_endpoint(attachment.text)
                endpoint = ""
                if len(xlsx_endpoint) > 1:
                    for i in xlsx_endpoint:
                        if normalize_fs_item(self._symbol) in normalize_fs_item(
                            i["description"]
                        ):
                            endpoint = i["link"]
                            break
                elif len(xlsx_endpoint) == 1:
                    endpoint = xlsx_endpoint[0]["link"]
                if endpoint:
                    xlsx = requests.get(
                        f"{self._consts.base_url}/Reports/{endpoint}",
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
                    clean_df = clean_raw_portfolio_df(raw_df)
                    clean_df = clean_df.with_columns(
                        publish_date_time=pl.lit(letter.publish_date_time),
                        symbol=pl.lit(self._symbol),
                        title=pl.lit(letter.title),
                        url=pl.lit(letter.url),
                        attachment_url=pl.lit(letter.attachment_url),
                    )
                    df = pl.concat([df, clean_df])
        return df
