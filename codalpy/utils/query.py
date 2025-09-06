import re
from dataclasses import dataclass
from enum import Enum
from typing import Annotated, Literal

import jdatetime as jdt
from pydantic import BaseModel, BeforeValidator, ConfigDict, alias_generators


@dataclass
class Consts:
    base_url: str = "https://www.codal.ir"
    base_search_url: str = "https://search.codal.ir"
    api_endpoint: str = "/api/search/v2/q"

    @property
    def search_url(self):
        return f"{self.base_search_url}{self.api_endpoint}"


def validate_jdate(jdate: str):
    """Validate Jalali date format.
    returns: str yyyy/mm/dd
    """
    pattern = r"^(\d{4})[-/](\d{2})[-/](\d{2})$"
    match = re.match(pattern, jdate)
    if not match:
        raise ValueError("Invalid date format. Use YYYY-MM-DD or YYYY/MM/DD")
    year, month, day = map(int, match.groups())
    try:
        return jdt.date(year, month, day).strftime("%Y/%m/%d")
    except ValueError:
        raise ValueError("Invalid Jalali date")


JDate = Annotated[str, BeforeValidator(validate_jdate)]


class QueryCategory(Enum):
    ALL = -1
    ANNUAL_FINANCIAL_STATEMETNS = 1  # اطلاعات و صورت مالی سالانه
    MONTHLY_ACTIVITY = 3  # گزارش عملکرد ماهانه


class QueryLetterType(Enum):
    ALL = -1
    INTERIM_FINANCIAL_STATEMENTS = 6  # صورت‌های مالی میان‌دوره‌ای
    PORTFOLIO_POSITION = 8  # صورت وضعیت پورتفوی
    MONTHLY_ACTIVITY = 58  # گزارش عملکرد ماهانه


class QueryParam(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_pascal, populate_by_name=True
    )

    symbol: str
    category: QueryCategory = QueryCategory.ALL  # گروه اطلاعیه
    publisher_type: Literal[1] = 1  # نوع شرکت --> ناشران
    letter_type: QueryLetterType = QueryLetterType.ALL
    length: Literal[-1, 3, 6, 9, 12] = -1  # طول دوره
    audited: bool = True  # حسابرسی شده
    not_audited: bool = True  # حسابرسی نشده
    mains: bool = True  # فقط شرکت اصلی ok
    childs: bool = False  # فقط زیر-مجموعه‌ها ok
    consolidatable: bool = True  # اصلی ok
    not_consolidatable: bool = True  # تلفیقی ok
    auditor_ref: Literal[-1] = -1
    company_state: Literal[0, 1, 2] = 0
    company_type: Literal[-1, 1, 3] = -1
    page_number: int = 1
    tracing_no: Literal[-1] = -1  # ok
    publisher: bool = False  # ok
    is_not_audited: bool = False
    from_date: JDate = "1396/01/01"
    to_date: JDate = "1405/01/01"
