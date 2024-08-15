from dataclasses import dataclass

__all__ = ["income_statement"]


@dataclass
class IncomeStatementDict:
    production: dict[str, str]


@dataclass
class BalanceSheetDict:
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

balance_sheet = BalanceSheetDict(
    production={
        # 1402
        "دارايي‌هاي ثابت مشهود": "tangible_fixed_assets",
        "سرمايه‌گذاري در املاک": "investment_property",
        "دارايي‌هاي نامشهود": "intangible_assets",
        "سرمايه‌گذاري‌هاي بلندمدت": "long_term_investments",
        "دريافتني‌هاي بلندمدت": "long_term_receivable",
        "دارايي ماليات انتقالي": "",
        "ساير دارايي‌ها": "other_assets",
        "جمع دارايي‌هاي غيرجاري": "total_non_current_assets",

        "سفارشات و پيش‌پرداخت‌ها": "prepayments",
        "موجودي مواد و کالا": "inventories",
        "دريافتني‌هاي تجاري و ساير دريافتني‌ها": "receivables",
        "سرمايه‌گذاري‌هاي کوتاه‌مدت": "short_term_investments",
        "موجودي نقد": "cash",
        "دارايي‌هاي نگهداري شده براي فروش": "assets_for_Sale",
        "جمع دارايي‌هاي جاري": "total_current_assets",
        "جمع دارايي‌ها": "total_assets",

        "سرمايه": "common_stock",
        "افزايش سرمايه در جريان": "receives_for_capital_advance",
        "صرف سهام": "capital_surplus",
        "صرف سهام خزانه": "treasury_shares_surplus",
        "اندوخته قانوني": "legal_reserve",
        "ساير اندوخته‌ها": "other_reserves",
        "مازاد تجديدارزيابي دارايي‌ها": "revaluation_surplus",
        "تفاوت تسعير ارز عمليات خارجي": "exchange_reserve",
        "سود(زيان) انباشته": "retained_earnings",
        "سهام خزانه": "treasury_shares",
        "جمع حقوق مالکانه": "total_equity",

        "پرداختني‌هاي بلندمدت": "long_term_payable",
        "تسهيلات مالي بلندمدت": "long_term_debt",
        "بدهي ماليات انتقالي": "",
        "ذخيره مزاياي پايان خدمت کارکنان": "allowance_for_post_retirement",
        "جمع بدهي‌هاي غيرجاري": "total_non_current_liabilities",

        "پرداختني‌هاي تجاري و ساير پرداختني‌ها": "payables",
        "ماليات پرداختني": "",
        "سود سهام پرداختني": "dividends_payable",
        "تسهيلات مالي": "short_term_debt",
        "ذخاير": "provisions",
        "پيش‌دريافت‌ها": "deferred_revenue",
        "بدهي‌هاي ‌مرتبط ‌با دارايي‌هاي نگهداري‌‌شده براي ‌فروش": "liabilities_related_to_assets_for_sale",
        "جمع بدهي‌هاي جاري": "total_current_liabilities",
        "جمع بدهي‌ها": "total_liabilities",
        "جمع حقوق مالکانه و بدهي‌ها": "total_liabilities_equity",
    }
)
