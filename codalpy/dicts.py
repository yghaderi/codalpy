from pydantic import BaseModel

__all__ = ["income_statement"]


class IncomeStatementDict(BaseModel):
    production: dict[str, str]


income_statement = IncomeStatementDict(
    production={
        "درآمدهاي عملياتي": "sales",
        "بهاى تمام شده درآمدهاي عملياتي": "cost_of_sales",
        "سود(زيان) ناخالص": "gross_profit",
        "هزينه‏ هاى فروش، ادارى و عمومى": "operating_expenses",
        "هزينه کاهش ارزش دريافتني‏ ها (هزينه استثنايي)": "exceptional_cost",
        "ساير درآمدها": "other_operating_income",
        "سایر درآمدهای عملیاتی": "other_operating_income",
        "سایر هزینه ها": "other_operating_expense",
        "سایر هزینه‌های عملیاتی": "other_operating_expense",
        "سود(زيان) عملياتى": "operating_income",
        "هزينه‏ هاى مالى": "interest_expense",
        "ساير درآمدها و هزينه ‏هاى غيرعملياتى": "other_income",
        "سایر درآمدها و هزینه‌های غیرعملیاتی- درآمد سرمایه‌گذاری‌ها": "other_income",
        "سایر درآمدها و هزینه‌های غیرعملیاتی- اقلام متفرقه": "other_income",
        "سود(زيان) عمليات در حال تداوم قبل از ماليات": "pretax_income",
        "مالیات بر درآمد": "taxes",
        "سال جاري": "taxes",
        "سال‌هاي قبل": "taxes",
        "سود(زيان) خالص عمليات در حال تداوم": "net_income_from_continuing_operations",
        "سود (زيان) خالص عمليات متوقف شده": "discontinued_operations",
        "سود (زیان) عملیات متوقف ‌شده پس از اثر مالیاتی": "discontinued_operations",
        "سود(زيان) خالص": "net_income",
        "سود (زيان) خالص هر سهم – ريال": "earnings_per_share",
        "سرمایه": "shares_outstanding",
    }
)
