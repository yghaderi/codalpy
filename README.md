# metafid
## Codal

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/codalpy)
![PyPI - Version](https://img.shields.io/pypi/v/codalpy)
![PyPI - Downloads](https://img.shields.io/pypi/dm/codalpy?logoColor=blue&color=blue)
![GitHub](https://img.shields.io/github/license/yghaderi/codalpy)

<div dir="rtl">
کدال برای گرفتن و پالایشِ داده از codal.ir در حالِ توسعه است
</div>



| حمایت از من | لینک                                             |
|-------------|--------------------------------------------------|
| دارمت       | [یه ☕🧸🍪 مهمونم کن](https://daramet.com/yghaderi) |
|


## install
```bash
python -m pip install codalpy
```




## صورت‌هایِ مالی
### صورت عملکردِ مالی

```python
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

```
