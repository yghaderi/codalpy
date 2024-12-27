# metafid
## Codal

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/codalpy)
![PyPI - Version](https://img.shields.io/pypi/v/codalpy)
![PyPI - Downloads](https://img.shields.io/pypi/dm/codalpy?logoColor=blue&color=blue)
![GitHub](https://img.shields.io/github/license/yghaderi/codalpy)

<div dir="rtl">
کدال برای گرفتن و پالایشِ داده از codal.ir در حالِ توسعه است.
<br/>
<a href="https://yghaderi.github.io/codalpy/_build/index.html"> راهنمایِ بهره-گیران</a>
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
from codalpy import Codal, QueryParam
query = QueryParam(symbol="زاگرس",length=12, from_date="1400/01/01")
codal = Codal(query=query, category="production")
codal.income_statement()
# Output
"""
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
```

### صورت وضعیتِ مالی

```python
from codalpy import Codal, QueryParam
query = QueryParam(symbol="زاگرس",length=12, from_date="1400/01/01")
codal = Codal(query=query, category="production")
codal.balance_sheet()

# Output
"""
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
```

### صورت وضعیت پورتفوی صندوق سرمایه گذاری
```python
from codalpy import Codal, QueryParam
query = QueryParam(symbol="پتروآگاه",length=-1, from_date="1403/01/01", category=3, letter_type=8, company_state=2, company_type=3)
codal = Codal(query=query, category="etf")
codal.etf_portfolio()
# Output
"""
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
```
