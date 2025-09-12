import re
from io import BytesIO
from typing import Literal
from urllib.parse import parse_qs, urlparse

import polars as pl
import requests

from codalpy.utils.fund import clean_raw_portfolio_df, find_download_endpoint
from codalpy.utils.gen_df import clean_df
from codalpy.utils.http import HEADERS, get
from codalpy.utils.issuer import Issuer, IssuerCategory, IssuerDType
from codalpy.utils.models import (
    FinancialStatement,
    GetFinancialStatement,
    Letter,
    DataSource,
    GetDataSourceResult,
    GetDataSourceError,
)
from codalpy.utils.query import Consts, QueryCategory, QueryLetterType, QueryParam
from codalpy.utils.utils import normalize_fs_item


class Codal:
    def __init__(self, issuer: str, from_jdate: str, to_jdate: str) -> None:
        self._issuer = Issuer().validate(issuer)
        self._query = QueryParam(
            symbol=self._issuer.alias,
            from_date=from_jdate,
            to_date=to_jdate,
        )
        self._from_jdate = self._query.from_date
        self._to_jdate = self._query.to_date
        self._consts = Consts()

    @property
    def issuer(self):
        return self._issuer

    @issuer.setter
    def issuer(self, value: str):
        issuer_ = Issuer().validate(value)
        self._query = QueryParam.model_validate(
            {**self._query.model_dump(), "symbol": issuer_.alias}
        )
        self._issuer = issuer_

    @property
    def from_jdate(self):
        return self._from_jdate

    @from_jdate.setter
    def from_jdate(self, value: str):
        self._query = QueryParam.model_validate(
            {**self._query.model_dump(), "from_date": value}
        )
        self._from_jdate = self._query.from_date

    @property
    def to_jdate(self):
        return self.to_jdate

    @to_jdate.setter
    def to_jdate(self, value: str):
        self._query = QueryParam.model_validate(
            {**self._query.model_dump(), "to_date": value}
        )
        self._to_jdate = self._query.to_date

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value: QueryParam):
        self._query = value

    @staticmethod
    def supported_issuers(cagegory: list[IssuerCategory]) -> list[IssuerDType]:
        """
                .. raw:: html

                    <div dir="rtl">
        ناشرهایی که پشتیبانی میشه رو بهت میده.
                    </div>

                Parameters
                ----------
                cagegory : list[IssuerCategory]
                    The category of the issuer.

                Returns
                -------
                list[IssuerDType]

                example
                -------
                >>> from codalpy import Codal, IssuerCategory
                >>> Codal.supported_issuers([IssuerCategory.FUND])[:2]
                [IssuerDType(name='سهامی اهرمی کاریزما', symbol='اهرم', alias='اهرم', category=<IssuerCategory.FUND: 'Fund'>), IssuerDType(name='سهامی اهرمی مفید', symbol='توان', alias='توان', category=<IssuerCategory.FUND: 'Fund'>)]
        """
        return Issuer().get_issuers_by_category(cagegory)

    def letter(self) -> list[Letter]:
        r = requests.get(
            url=self._consts.search_url,
            params=self._query.model_dump(by_alias=True, mode="json"),
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
                r = get(
                    url=f"{self._consts.base_url}{urlp.path}",
                    params=params,
                    rtype="text",
                )
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

    def _get_data_source(self) -> list[GetDataSourceResult]:
        letters = self.letter()
        records: list[GetDataSourceResult] = []
        if letters is not None:
            for i in letters:
                urlp = urlparse(i.url)
                params = parse_qs(urlp.query)
                # params["SheetId"] = [sheet_id]
                r = get(
                    url=f"{self._consts.base_url}{urlp.path}",
                    params=params,
                    rtype="text",
                )
                data: DataSource | None = None
                error: GetDataSourceError | None = None
                status = "error"
                if r is not None:
                    pattern = r"var datasource = (.*?);"
                    match = re.search(pattern, r)
                    if match:
                        text = match.group(1)
                        try:
                            data = DataSource.model_validate_json(text)
                            status = "success"
                        except Exception as e:

                            error = GetDataSourceError(
                                source="validation", message=str(e)
                            )
                    else:
                        error = GetDataSourceError(
                            source="match", message="Cannot find data."
                        )
                else:
                    error = GetDataSourceError(
                        source="match", message="Cannot find data."
                    )
                records.append(
                    GetDataSourceResult(
                        status=status, letter=i, data=data, error=error
                    )
                )
        return records

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
                df = clean_df(data.records, self._issuer.category, "IncomeStatement")
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
                df = clean_df(data.records, self._issuer.category, "BalanceSheet")
                return df

    def monthly_activity(self):
        self._query.category = QueryCategory.MONTHLY_ACTIVITY
        self._query.letter_type = QueryLetterType.MONTHLY_ACTIVITY
        data = self._get_data_source()
        return data

    def fund_monthly_portfolio(self) -> pl.DataFrame:
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
        >>> from codalpy import Codal
        >>> codal = Codal(issuer = "اهرم", from_jdate= "1404-04-04", to_jdate="1405-01-01")
        >>> codal.fund_monthly_portfolio()
        shape: (603, 18)
        ┌──────────────────────────────┬────────────┬────────────────┬──────────────────┬───┬────────┬─────────────────────────────────┬─────────────────────────────────┬─────────────────────────────────┐
        │ name                         ┆ volume_beg ┆ total_cost_beg ┆ net_proceeds_beg ┆ … ┆ symbol ┆ title                           ┆ url                             ┆ attachment_url                  │
        │ ---                          ┆ ---        ┆ ---            ┆ ---              ┆   ┆ ---    ┆ ---                             ┆ ---                             ┆ ---                             │
        │ str                          ┆ i64        ┆ i64            ┆ i64              ┆   ┆ str    ┆ str                             ┆ str                             ┆ str                             │
        ╞══════════════════════════════╪════════════╪════════════════╪══════════════════╪═══╪════════╪═════════════════════════════════╪═════════════════════════════════╪═════════════════════════════════╡
        │ آهن و فولاد غدیر ایرانیان     ┆ 24500000   ┆ 140495106806   ┆ 123719463000     ┆ … ┆ اهرم   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
        │ اقتصادی و خودکفایی آزادگان   ┆ 58949663   ┆ 428681824109   ┆ 363313257531     ┆ … ┆ اهرم   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
        │ البرزدارو                    ┆ 266248175  ┆ 853755414625   ┆ 982697425906     ┆ … ┆ اهرم   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
        │ الحاوی                       ┆ 79400000   ┆ 175805992152   ┆ 102290130720     ┆ … ┆ اهرم   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
        │ الکتریک‌ خودرو شرق‌            ┆ 117032944  ┆ 427355209792   ┆ 310735053213     ┆ … ┆ اهرم   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
        │ …                            ┆ …          ┆ …              ┆ …                ┆ … ┆ …      ┆ …                               ┆ …                               ┆ …                               │
        │ کشت و دامداری فکا            ┆ 38000000   ┆ 42921313500    ┆ 137950282800     ┆ … ┆ اهرم   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
        │ کویر تایر                    ┆ 84043466   ┆ 168768973101   ┆ 619056648665     ┆ … ┆ اهرم   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
        │ ح . سرمایه گذاری‌البرز(هلدینگ‌ ┆ 0          ┆ 0              ┆ 0                ┆ … ┆ اهرم   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
        │ سنگ آهن گهرزمین              ┆ 0          ┆ 0              ┆ 0                ┆ … ┆ اهرم   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
        │ ح . سنگ آهن گهرزمین          ┆ 0          ┆ 0              ┆ 0                ┆ … ┆ اهرم   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
        └──────────────────────────────┴────────────┴────────────────┴──────────────────┴───┴────────┴─────────────────────────────────┴─────────────────────────────────┴─────────────────────────────────┘
        """
        self._query.category = QueryCategory.MONTHLY_ACTIVITY
        self._query.letter_type = QueryLetterType.PORTFOLIO_POSITION
        letters = self.letter()
        df = pl.DataFrame()
        for letter in letters:
            if letter.has_attachment:
                attachment = requests.get(letter.attachment_url, headers=HEADERS)
                xlsx_endpoint = find_download_endpoint(attachment.text)
                endpoint = ""
                if len(xlsx_endpoint) > 1:
                    for i in xlsx_endpoint:
                        if normalize_fs_item(self._issuer.symbol) in normalize_fs_item(
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
                        issuer=pl.lit(self._issuer.symbol),
                        title=pl.lit(letter.title),
                        url=pl.lit(letter.url),
                        attachment_url=pl.lit(letter.attachment_url),
                    )
                    df = pl.concat([df, clean_df])
        return df
