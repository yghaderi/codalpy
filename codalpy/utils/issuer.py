from enum import Enum

from pydantic import BaseModel


class IssuerCategory(Enum):
    FUND = "Fund"
    BANKING = "Banking"
    INSURANCE = "Insurance"
    MANUFACTURING = "Manufacturing"


class IssuerDType(BaseModel):
    name: str
    symbol: str
    alias: str
    category: IssuerCategory


class Issuer:
    def __init__(self):
        self.issuers = issuers

    def get_issuers_by_category(
        self, category: list[IssuerCategory]
    ) -> list[IssuerDType]:
        return [issuer for issuer in self.issuers if issuer.category in category]

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

    def validate(self, symbol: str) -> IssuerDType:
        item = next(
            filter(
                lambda x: self.normalize_symbol(x.symbol)
                == self.normalize_symbol(symbol),
                self.issuers,
            ),
            None,
        )
        if item == None:
            raise ValueError("Symbol not found or invalid or not supported yet.")
        return item


issuers = [
    # funds
    IssuerDType(
        symbol="اهرم",
        name="سهامی اهرمی کاریزما",
        alias="اهرم",
        category=IssuerCategory.FUND,
    ),
    IssuerDType(
        symbol="توان",
        name="سهامی اهرمی مفید",
        alias="توان",
        category=IssuerCategory.FUND,
    ),
    IssuerDType(
        symbol="نارنج اهرم",
        name="سهامی اهرمی نارنج",
        alias="نارنج اهرم",
        category=IssuerCategory.FUND,
    ),
    IssuerDType(
        symbol="بیدار",
        name="سهامی اهرمی بیدار",
        alias="بیدار",
        category=IssuerCategory.FUND,
    ),
    IssuerDType(
        symbol="جهش",
        name="سهامی اهرمی جهش فارابی",
        alias="جهش",
        category=IssuerCategory.FUND,
    ),
    IssuerDType(
        symbol="شتاب",
        name="سهامی اهرمی شتاب آگاه",
        alias="شتاب",
        category=IssuerCategory.FUND,
    ),
    IssuerDType(
        symbol="موج",
        name="سهامی اهرمی موج فیروزه",
        alias="موج",
        category=IssuerCategory.FUND,
    ),
    IssuerDType(
        symbol="استیل",
        name="بخشی صنایع مفید",
        alias="استیل",
        category=IssuerCategory.FUND,
    ),
    IssuerDType(
        symbol="اکتان",
        name="بخشی صنایع مفید",
        alias="استیل",
        category=IssuerCategory.FUND,
    ),
    IssuerDType(
        symbol="خودران",
        name="بخشی صنایع مفید",
        alias="استیل",
        category=IssuerCategory.FUND,
    ),
    IssuerDType(
        symbol="دارونو",
        name="بخشی صنایع مفید",
        alias="استیل",
        category=IssuerCategory.FUND,
    ),
    IssuerDType(
        symbol="سيمانو",
        name="بخشی صنایع مفید",
        alias="استیل",
        category=IssuerCategory.FUND,
    ),
    IssuerDType(
        symbol="معدن",
        name="بخشی صنایع مفید",
        alias="استیل",
        category=IssuerCategory.FUND,
    ),
    IssuerDType(
        symbol="شتاب",
        name="سهامی اهرمی شتاب آگاه",
        alias="شتاب",
        category=IssuerCategory.FUND,
    ),
    IssuerDType(
        symbol="موج",
        name="سهامی اهرمی موج فیروزه",
        alias="موج",
        category=IssuerCategory.FUND,
    ),
    IssuerDType(
        symbol="استیل",
        name="بخشی صنایع مفید",
        alias="استیل",
        category=IssuerCategory.FUND,
    ),
    # Manufacturing
    IssuerDType(
        symbol="شپديس",
        name="پترو شيمي پرديس",
        alias="شپديس",
        category=IssuerCategory.MANUFACTURING,
    ),
    IssuerDType(
        symbol="شيراز",
        name="پتروشيمي شيراز",
        alias="شيراز",
        category=IssuerCategory.MANUFACTURING,
    ),
    IssuerDType(
        symbol="کرماشا",
        name="صنايع پتروشيمي کرمانشاه",
        alias="کرماشا",
        category=IssuerCategory.MANUFACTURING,
    ),
    IssuerDType(
        symbol="فولاد",
        name="فولاد مبارکه اصفهان",
        alias="فولاد",
        category=IssuerCategory.MANUFACTURING,
    ),
    IssuerDType(
        symbol="فملی",
        name="ملی صنایع مس ایران",
        alias="فملی",
        category=IssuerCategory.MANUFACTURING,
    ),
    # BANKING
    IssuerDType(
        symbol="وبملت",
        name="بانک ملت",
        alias="وبملت",
        category=IssuerCategory.BANKING,
    ),
]
