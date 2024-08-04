# %%
from codal.codal import Codal, QueryParam
import polars as pl
# %%
qp = QueryParam(symbol="زاگرس", length=12)
codal = Codal(query=qp, category="production")
# %%
incom_statement = codal.income_statement()
# %%
incom_statement.head(3)
