from pydantic import BaseModel

__all__ = ["income_statement"]
class IncomeStatementDict(BaseModel):
    production: dict[str, str]


income_statement = IncomeStatementDict(
    production={
        "درآمدهاي عملياتي": "sales",
        "بهاى تمام شده درآمدهاي عملياتي": "cost_of_goods_sold",
        "سود(زيان) ناخالص": "gross_profit",
        "هزينه‏ هاى فروش، ادارى و عمومى": "marketing_general_and_administrative_expenses",
        "هزينه کاهش ارزش دريافتني‏ ها (هزينه استثنايي)": "special_items",
        "ساير درآمدها": "other_operating_income",
        "سایر درآمدهای عملیاتی": "other_operating_income",
        "سایر هزینه ها": "other_operating_expense",
        "سایر هزینه‌های عملیاتی": "other_operating_expense",
        "سود(زيان) عملياتى": "operating_income",
        "هزينه‏ هاى مالى": "interest_expense",
        "ساير درآمدها و هزينه ‏هاى غيرعملياتى": "other_income",
        "سایر درآمدها و هزینه‌های غیرعملیاتی- درآمد سرمایه‌گذاری‌ها": "other_income",
        "سایر درآمدها و هزینه‌های غیرعملیاتی- اقلام متفرقه": "other_income",
        "سود(زيان) عمليات در حال تداوم قبل از ماليات": "income_from_continuing_operations_before_taxes",
        "مالیات بر درآمد": "income_tax",
        "سال جاري": "income_tax",
        "سال‌هاي قبل": "income_tax",
        "سود(زيان) خالص عمليات در حال تداوم": "net_income_from_continuing_operations",
        "سود (زيان) خالص عمليات متوقف شده": "income_from_discontinued_operations_net_of_tax",
        "سود (زیان) عملیات متوقف ‌شده پس از اثر مالیاتی": "income_from_discontinued_operations_net_of_tax",
        "سود(زيان) خالص": "net_income",
        "سود (زيان) خالص هر سهم – ريال": "eps",
        "سرمایه": "listed_capital",
    }
)
