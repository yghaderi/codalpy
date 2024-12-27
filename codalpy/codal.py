from typing import Literal
from io import BytesIO
from urllib.parse import urlparse, parse_qs
import re
import requests

import polars as pl
from pydantic import BaseModel, ConfigDict, alias_generators, field_validator

from codalpy.utils.models import Letter, FinancialStatement, GetFinancialStatement
from codalpy.utils.http import get, HEADERS
from codalpy.utils.gen_df import clean_df
from codalpy.utils import etf


class QueryParam(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_pascal, populate_by_name=True
    )

    symbol: str
    category: Literal[1, 3] = 1  # گروه اطلاعیه --> اطلاعات و صورت مالی سالانه
    publisher_type: Literal[1] = 1  # نوع شرکت --> ناشران
    letter_type: Literal[6, 8] = 6  # نوع اطلاعیه --> اطلاعات و صورتهای مالی میاندوره ای ok
    length: Literal[-1, 3, 6, 9, 12]  # طول دوره
    audited: bool = True  # حسابرسی شده
    not_audited: bool = True  # حسابرسی نشده
    mains: bool = True  # فقط شرکت اصلی ok
    childs: bool = False  # فقط زیر-مجموعه‌ها ok
    consolidatable: bool = True  # اصلی ok
    not_consolidatable: bool = True  # تلفیقی ok
    auditor_ref: Literal[-1] = -1
    company_state: Literal[1, 2] = 1
    company_type: Literal[1, 3] = 1
    page_number: int = 1
    tracing_no: Literal[-1] = -1  # ok
    publisher: bool = False  # ok
    is_not_audited: bool = False
    from_date: str = "1396/01/01"


class Codal:
    def __init__(self, query: QueryParam, category: Literal["production", "etf"]) -> None:
        self.base_url = "https://codal.ir"
        self.search_url = "https://search.codal.ir/api/search/v2/q?"
        self.api = "api/search/v2/q"
        self._query = query
        self._category = category

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value: QueryParam):
        self._query = value

    def letter(self):
        r = get(
            url=self.search_url,
            params=self._query.model_dump(by_alias=True),
            rtype="josn",
        )
        if isinstance(r, dict):
            pages = str(r.get("Page"))
            Letter.base_url = self.base_url
            letters = [Letter.model_validate(i) for i in r["Letters"]]
            if pages.isdigit:
                pages = int(pages)
                if pages > 1:

                    for p in range(2, pages + 1):
                        self._query.page_number = p
                        r = get(
                            url=self.search_url,
                            params=self._query.model_dump(by_alias=True),
                            rtype="josn",
                        )
                        if isinstance(r, dict):
                            letters.extend(
                                [Letter.model_validate(i) for i in r["Letters"]]
                            )
            return letters

    def _get_financial_statement(
            self, sheet_id: Literal["0", "1"]
    ) -> GetFinancialStatement | None:
        letters = self.letter()
        if letters is not None:
            records = []
            get_error = []
            match_error = []
            validation_error = []
            for i in letters:
                urlp = urlparse(i.url)
                params = parse_qs(urlp.query)
                params["SheetId"] = [sheet_id]
                r = get(url=f"{self.base_url}{urlp.path}", params=params, rtype="text")
                if r is not None:
                    pattern = r"var datasource = (.*?);"
                    match = re.search(pattern, r)
                    if match:
                        text = match.group(1)
                        try:
                            records.append(
                                (i, FinancialStatement.model_validate_json(text))
                            )
                        except Exception as e:
                            validation_error.append((i, str(e)))
                    else:
                        match_error.append((i, str(r)))
                else:
                    get_error.append(i)
            return GetFinancialStatement(
                records=records,
                get_error=get_error,
                match_error=match_error,
                validation_error=validation_error,
            )

    def income_statement(self) -> pl.DataFrame | None:
        """
        .. raw:: html

            <div dir="rtl">
                صورت-عملکردِ مالی رو بهت میده
            </div>

        Returns
        -------
        polars.DataFrame

        example
        -------
        >>> from codalpy import Codal, QueryParam
        >>> query = QueryParam(symbol="زاگرس",length=12, from_date="1400/01/01")
        >>> codal = Codal(query=query, category="production")
        >>> codal.income_statement()
        shape: (8, 29)
        ┌───────────┬───────────────┬──────────────┬────────────────────┬───┬─────────────────────────────────┬─────────────────────────────────┬─────────────────────────────────┬─────────────────────────────────┐
        │ sales     ┆ cost_of_sales ┆ gross_profit ┆ operating_expenses ┆ … ┆ url                             ┆ attachment_url                  ┆ pdf_url                         ┆ excel_url                       │
        │ ---       ┆ ---           ┆ ---          ┆ ---                ┆   ┆ ---                             ┆ ---                             ┆ ---                             ┆ ---                             │
        │ i64       ┆ i64           ┆ i64          ┆ i64                ┆   ┆ str                             ┆ str                             ┆ str                             ┆ str                             │
        ╞═══════════╪═══════════════╪══════════════╪════════════════════╪═══╪═════════════════════════════════╪═════════════════════════════════╪═════════════════════════════════╪═════════════════════════════════╡
        │ 258734831 ┆ -192020455    ┆ 66714376     ┆ -57185171          ┆ … ┆ https://codal.ir/Reports/Decis… ┆ https://codal.ir/Reports/Attac… ┆ https://codal.ir/DownloadFile.… ┆ https://excel.codal.ir/service… │
        │ 258734831 ┆ -192020455    ┆ 66714376     ┆ -57363718          ┆ … ┆ https://codal.ir/Reports/Decis… ┆ https://codal.ir/Reports/Attac… ┆ https://codal.ir/DownloadFile.… ┆ https://excel.codal.ir/service… │
        │ 214213606 ┆ -145108587    ┆ 69105019     ┆ -44188435          ┆ … ┆ https://codal.ir/Reports/Decis… ┆ https://codal.ir/Reports/Attac… ┆ https://codal.ir/DownloadFile.… ┆ https://excel.codal.ir/service… │
        │ 214213606 ┆ -147350610    ┆ 66862996     ┆ -46301021          ┆ … ┆ https://codal.ir/Reports/Decis… ┆ https://codal.ir/Reports/Attac… ┆ https://codal.ir/DownloadFile.… ┆ https://excel.codal.ir/service… │
        │ 192628444 ┆ -132224423    ┆ 60404021     ┆ -32817902          ┆ … ┆ https://codal.ir/Reports/Decis… ┆ https://codal.ir/Reports/Attac… ┆ https://codal.ir/DownloadFile.… ┆ https://excel.codal.ir/service… │
        │ 192628444 ┆ -132224423    ┆ 60404021     ┆ -32834603          ┆ … ┆ https://codal.ir/Reports/Decis… ┆ https://codal.ir/Reports/Attac… ┆ https://codal.ir/DownloadFile.… ┆ https://excel.codal.ir/service… │
        │ 143234768 ┆ -61344224     ┆ 81890544     ┆ -34001119          ┆ … ┆ https://codal.ir/Reports/Decis… ┆ https://codal.ir/Reports/Attac… ┆ https://codal.ir/DownloadFile.… ┆ https://excel.codal.ir/service… │
        │ 143234768 ┆ -61251730     ┆ 81983038     ┆ -31375649          ┆ … ┆ https://codal.ir/Reports/Decis… ┆ https://codal.ir/Reports/Attac… ┆ https://codal.ir/DownloadFile.… ┆ https://excel.codal.ir/service… │
        └───────────┴───────────────┴──────────────┴────────────────────┴───┴─────────────────────────────────┴─────────────────────────────────┴─────────────────────────────────┴─────────────────────────────────┘
        """
        data = self._get_financial_statement("1")
        if data:
            if data.records:
                df = clean_df(data.records, self._category, "IncomeStatement")
                return df

    def balance_sheet(self) -> pl.DataFrame | None:
        """
        .. raw:: html

            <div dir="rtl">
                صورت-وضعیتِ مالی رو بهت میده
            </div>

        Returns
        -------
        polars.DataFrame

        example
        -------
        >>> from codalpy import Codal, QueryParam
        >>> query = QueryParam(symbol="زاگرس",length=12, from_date="1400/01/01")
        >>> codal = Codal(query=query, category="production")
        >>> codal.balance_sheet()
        shape: (8, 54)
        ┌──────────────────────────────┬─────────────────────┬──────────┬───────────────────────┬───┬─────────────────────────────────┬─────────────────────────────────┬─────────────────────────────────┬─────────────────────────────────┐
        │ property_plant_and_equipment ┆ investment_property ┆ goodwill ┆ long_term_investments ┆ … ┆ url                             ┆ attachment_url                  ┆ pdf_url                         ┆ excel_url                       │
        │ ---                          ┆ ---                 ┆ ---      ┆ ---                   ┆   ┆ ---                             ┆ ---                             ┆ ---                             ┆ ---                             │
        │ i64                          ┆ i64                 ┆ i64      ┆ i64                   ┆   ┆ str                             ┆ str                             ┆ str                             ┆ str                             │
        ╞══════════════════════════════╪═════════════════════╪══════════╪═══════════════════════╪═══╪═════════════════════════════════╪═════════════════════════════════╪═════════════════════════════════╪═════════════════════════════════╡
        │ 57889093                     ┆ 0                   ┆ 2138291  ┆ 251279                ┆ … ┆ https://codal.ir/Reports/Decis… ┆ https://codal.ir/Reports/Attac… ┆ https://codal.ir/DownloadFile.… ┆ https://excel.codal.ir/service… │
        │ 62330228                     ┆ 0                   ┆ 2138291  ┆ 251279                ┆ … ┆ https://codal.ir/Reports/Decis… ┆ https://codal.ir/Reports/Attac… ┆ https://codal.ir/DownloadFile.… ┆ https://excel.codal.ir/service… │
        │ 42330444                     ┆ 0                   ┆ 117755   ┆ 11279                 ┆ … ┆ https://codal.ir/Reports/Decis… ┆ https://codal.ir/Reports/Attac… ┆ https://codal.ir/DownloadFile.… ┆ https://excel.codal.ir/service… │
        │ 42330444                     ┆ 0                   ┆ 117755   ┆ 11279                 ┆ … ┆ https://codal.ir/Reports/Decis… ┆ https://codal.ir/Reports/Attac… ┆ https://codal.ir/DownloadFile.… ┆ https://excel.codal.ir/service… │
        │ 15940028                     ┆ 0                   ┆ 163858   ┆ 4039308               ┆ … ┆ https://codal.ir/Reports/Decis… ┆ https://codal.ir/Reports/Attac… ┆ https://codal.ir/DownloadFile.… ┆ https://excel.codal.ir/service… │
        │ 15940028                     ┆ 0                   ┆ 147157   ┆ 4039308               ┆ … ┆ https://codal.ir/Reports/Decis… ┆ https://codal.ir/Reports/Attac… ┆ https://codal.ir/DownloadFile.… ┆ https://excel.codal.ir/service… │
        │ 12746494                     ┆ 0                   ┆ 138823   ┆ 4039308               ┆ … ┆ https://codal.ir/Reports/Decis… ┆ https://codal.ir/Reports/Attac… ┆ https://codal.ir/DownloadFile.… ┆ https://excel.codal.ir/service… │
        │ 10613508                     ┆ 0                   ┆ 138823   ┆ 11279                 ┆ … ┆ https://codal.ir/Reports/Decis… ┆ https://codal.ir/Reports/Attac… ┆ https://codal.ir/DownloadFile.… ┆ https://excel.codal.ir/service… │
        └──────────────────────────────┴─────────────────────┴──────────┴───────────────────────┴───┴─────────────────────────────────┴─────────────────────────────────┴─────────────────────────────────┴─────────────────────────────────┘
        """
        data = self._get_financial_statement("0")
        if data:
            if data.records:
                df = clean_df(data.records, self._category, "BalanceSheet")
                return df

    def etf_portfolio(self):
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
        shape: (368, 19)
        ┌───────────┬───────────┬───────────┬───────────┬───┬──────────┬───────────┬───────────┬───────────┐
        │ name      ┆ volume_be ┆ total_cos ┆ net_proce ┆ … ┆ symbol   ┆ title     ┆ url       ┆ attachmen │
        │ ---       ┆ g         ┆ t_beg     ┆ eds_beg   ┆   ┆ ---      ┆ ---       ┆ ---       ┆ t_url     │
        │ str       ┆ ---       ┆ ---       ┆ ---       ┆   ┆ str      ┆ str       ┆ str       ┆ ---       │
        │           ┆ i64       ┆ i64       ┆ i64       ┆   ┆          ┆           ┆           ┆ str       │
        ╞═══════════╪═══════════╪═══════════╪═══════════╪═══╪══════════╪═══════════╪═══════════╪═══════════╡
        │ ‫آريان     ┆ 6334379   ┆ 723873677 ┆ 907982617 ┆ … ┆ پتروآگاه ┆ صورت      ┆ https://c ┆ https://c │
        │ كيميا تك  ┆           ┆ 10        ┆ 96        ┆   ┆          ┆ وضعیت     ┆ odal.ir/R ┆ odal.ir/R │
        │           ┆           ┆           ┆           ┆   ┆          ┆ پورتفوی   ┆ eports/At ┆ eports/At │
        │           ┆           ┆           ┆           ┆   ┆          ┆ صندوق     ┆ tac…      ┆ tac…      │
        │           ┆           ┆           ┆           ┆   ┆          ┆ سرمای…    ┆           ┆           │
        │ ‫املاح      ┆ 5561313   ┆ 832807586 ┆ 110840874 ┆ … ┆ پتروآگاه ┆ صورت      ┆ https://c ┆ https://c │
        │ ايران     ┆           ┆ 24        ┆ 912       ┆   ┆          ┆ وضعیت     ┆ odal.ir/R ┆ odal.ir/R │
        │           ┆           ┆           ┆           ┆   ┆          ┆ پورتفوی   ┆ eports/At ┆ eports/At │
        │           ┆           ┆           ┆           ┆   ┆          ┆ صندوق     ┆ tac…      ┆ tac…      │
        │           ┆           ┆           ┆           ┆   ┆          ┆ سرمای…    ┆           ┆           │
        │ ‫املاح      ┆ 0         ┆ 0         ┆ 0         ┆ … ┆ پتروآگاه ┆ صورت      ┆ https://c ┆ https://c │
        │ ايران     ┆           ┆           ┆           ┆   ┆          ┆ وضعیت     ┆ odal.ir/R ┆ odal.ir/R │
        │ (تقدم)    ┆           ┆           ┆           ┆   ┆          ┆ پورتفوی   ┆ eports/At ┆ eports/At │
        │           ┆           ┆           ┆           ┆   ┆          ┆ صندوق     ┆ tac…      ┆ tac…      │
        │           ┆           ┆           ┆           ┆   ┆          ┆ سرمای…    ┆           ┆           │
        │ ‫ایرکا     ┆ 26608118  ┆ 614331682 ┆ 727104993 ┆ … ┆ پتروآگاه ┆ صورت      ┆ https://c ┆ https://c │
        │ پارت صنعت ┆           ┆ 04        ┆ 70        ┆   ┆          ┆ وضعیت     ┆ odal.ir/R ┆ odal.ir/R │
        │           ┆           ┆           ┆           ┆   ┆          ┆ پورتفوی   ┆ eports/At ┆ eports/At │
        │           ┆           ┆           ┆           ┆   ┆          ┆ صندوق     ┆ tac…      ┆ tac…      │
        │           ┆           ┆           ┆           ┆   ┆          ┆ سرمای…    ┆           ┆           │
        │ ‫تراكتور   ┆ 5000000   ┆ 477442656 ┆ 521876250 ┆ … ┆ پتروآگاه ┆ صورت      ┆ https://c ┆ https://c │
        │ سازي      ┆           ┆ 00        ┆ 00        ┆   ┆          ┆ وضعیت     ┆ odal.ir/R ┆ odal.ir/R │
        │           ┆           ┆           ┆           ┆   ┆          ┆ پورتفوی   ┆ eports/At ┆ eports/At │
        │           ┆           ┆           ┆           ┆   ┆          ┆ صندوق     ┆ tac…      ┆ tac…      │
        │           ┆           ┆           ┆           ┆   ┆          ┆ سرمای…    ┆           ┆           │
        │ …         ┆ …         ┆ …         ┆ …         ┆ … ┆ …        ┆ …         ┆ …         ┆ …         │
        │ ‫پديده     ┆ 15094056  ┆ 134574637 ┆ 156194204 ┆ … ┆ پتروآگاه ┆ صورت      ┆ https://c ┆ https://c │
        │ شيمي قرن  ┆           ┆ 694       ┆ 678       ┆   ┆          ┆ وضعیت     ┆ odal.ir/R ┆ odal.ir/R │
        │           ┆           ┆           ┆           ┆   ┆          ┆ پورتفوی   ┆ eports/At ┆ eports/At │
        │           ┆           ┆           ┆           ┆   ┆          ┆ صندوق     ┆ tac…      ┆ tac…      │
        │           ┆           ┆           ┆           ┆   ┆          ┆ سرمای…    ┆           ┆           │
        │ ‫پست بانك  ┆ 5570715   ┆ 516123082 ┆ 458510733 ┆ … ┆ پتروآگاه ┆ صورت      ┆ https://c ┆ https://c │
        │ ايران     ┆           ┆ 64        ┆ 55        ┆   ┆          ┆ وضعیت     ┆ odal.ir/R ┆ odal.ir/R │
        │           ┆           ┆           ┆           ┆   ┆          ┆ پورتفوی   ┆ eports/At ┆ eports/At │
        │           ┆           ┆           ┆           ┆   ┆          ┆ صندوق     ┆ tac…      ┆ tac…      │
        │           ┆           ┆           ┆           ┆   ┆          ┆ سرمای…    ┆           ┆           │
        │ ‫کشتیرانی  ┆ 633333    ┆ 105679909 ┆ 125346325 ┆ … ┆ پتروآگاه ┆ صورت      ┆ https://c ┆ https://c │
        │ دریای خزر ┆           ┆ 66        ┆ 53        ┆   ┆          ┆ وضعیت     ┆ odal.ir/R ┆ odal.ir/R │
        │           ┆           ┆           ┆           ┆   ┆          ┆ پورتفوی   ┆ eports/At ┆ eports/At │
        │           ┆           ┆           ┆           ┆   ┆          ┆ صندوق     ┆ tac…      ┆ tac…      │
        │           ┆           ┆           ┆           ┆   ┆          ┆ سرمای…    ┆           ┆           │
        │ ‫گ.س.وت.ص. ┆ 53000000  ┆ 100928530 ┆ 974139178 ┆ … ┆ پتروآگاه ┆ صورت      ┆ https://c ┆ https://c │
        │ پتروشيمي  ┆           ┆ 916       ┆ 50        ┆   ┆          ┆ وضعیت     ┆ odal.ir/R ┆ odal.ir/R │
        │ خليج فارس ┆           ┆           ┆           ┆   ┆          ┆ پورتفوی   ┆ eports/At ┆ eports/At │
        │           ┆           ┆           ┆           ┆   ┆          ┆ صندوق     ┆ tac…      ┆ tac…      │
        │           ┆           ┆           ┆           ┆   ┆          ┆ سرمای…    ┆           ┆           │
        │ ‫گسترش     ┆ 40983555  ┆ 620900858 ┆ 657946200 ┆ … ┆ پتروآگاه ┆ صورت      ┆ https://c ┆ https://c │
        │ سوخت سبزز ┆           ┆ 25        ┆ 99        ┆   ┆          ┆ وضعیت     ┆ odal.ir/R ┆ odal.ir/R │
        │ اگرس(سهام ┆           ┆           ┆           ┆   ┆          ┆ پورتفوی   ┆ eports/At ┆ eports/At │
        │ ي عام…    ┆           ┆           ┆           ┆   ┆          ┆ صندوق     ┆ tac…      ┆ tac…      │
        │           ┆           ┆           ┆           ┆   ┆          ┆ سرمای…    ┆           ┆           │
        └───────────┴───────────┴───────────┴───────────┴───┴──────────┴───────────┴───────────┴───────────┘
        """
        letters = self.letter()
        df = pl.DataFrame()
        for letter in letters:
            if letter.has_attachment:
                attachment = requests.get(letter.attachment_url, headers=HEADERS)
                xlsx_endpoint = etf.find_download_endpoint(attachment.text)
                xlsx = requests.get(f"{self.base_url}/Reports/{xlsx_endpoint}", stream=True, headers=HEADERS)
                raw_df = pl.read_excel(BytesIO(xlsx.content), sheet_id=2)
                clean_df = etf.clean_raw_df(raw_df)
                clean_df = clean_df.with_columns(
                    [
                        pl.lit(letter.publish_date_time).alias("publish_date_time"),
                        pl.lit(letter.symbol).alias("symbol"),
                        pl.lit(letter.title).alias("title"),
                        pl.lit(letter.url).alias("url"),
                        pl.lit(letter.attachment_url).alias("attachment_url"),
                    ]
                )
                df = pl.concat([df, clean_df])
        return df
