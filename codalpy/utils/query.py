from typing import Literal
from dataclasses import dataclass
from pydantic import BaseModel, ConfigDict, alias_generators


@dataclass
class Consts:
    base_url: str = "https://www.codal.ir"
    base_search_url: str = "https://search.codal.ir"
    api_endpoint: str = "/api/search/v2/q"

    @property
    def search_url(self):
        return f"{self.base_search_url}{self.api_endpoint}"

class Issuer(BaseModel):
    name: str
    symbol: str

class Symbol:
    def __init__(self, symbol: str, issuers:list[Issuer]):
        self.symbol = symbol
        self.issuers= issuers

    @staticmethod
    def normalize_symbol(w: str) -> str:
        dict_ = {
            "\u200f": "",
            "\u200c": "",
            "ي": "ی",
            "ك": "ک",
            "آ": "ا",
            " ": "",
            "‌": "",
        }
        return w.translate(str.maketrans(dict_))

    def match_symbol(self) -> Issuer:
        item = next(
            filter(
                lambda x: self.normalize_symbol(x.symbol)
                == self.normalize_symbol(self.symbol),
                self.issuers,
            ),
            None,
        )
        if item == None:
            raise ValueError("Symbol not found or invalid or not supported yet.")
        return item


class QueryParam(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_pascal, populate_by_name=True
    )

    symbol: str
    category: Literal[1, 3] = 1  # گروه اطلاعیه --> اطلاعات و صورت مالی سالانه
    publisher_type: Literal[1] = 1  # نوع شرکت --> ناشران
    letter_type: Literal[6, 8] = (
        6  # نوع اطلاعیه --> اطلاعات و صورتهای مالی میاندوره ای ok
    )
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
