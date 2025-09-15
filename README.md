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
from codalpy import Codal
codal = Codal(
    issuer = "شپدیس",
    from_jdate = "1401/01/01",
    to_jdate = "1404/12/29"
)
data = codal.income_statement()
```

### صورت وضعیتِ مالی

```python
from codalpy import Codal
codal = Codal(
    issuer = "شپدیس",
    from_jdate = "1401/01/01",
    to_jdate = "1404/12/29"
)
data = codal.balance_sheet()
```


### فعالیتِ ماهانه

```python
from codalpy import Codal
codal = Codal(
    issuer = "شپدیس",
    from_jdate = "1404/01/01",
    to_jdate = "1404/12/29"
)
data = codal.monthly_activity()
```

### صورت وضعیت پورتفوی صندوق سرمایه گذاری
```python
from codalpy import Fund
fund = Fund(symbol="شتاب", jdate_from="1404/01/01")
fund.monthly_portfolio()
"""
shape: (760, 18)
┌─────────────────────────────┬────────────┬────────────────┬──────────────────┬───┬────────┬─────────────────────────────────┬─────────────────────────────────┬─────────────────────────────────┐
│ name                        ┆ volume_beg ┆ total_cost_beg ┆ net_proceeds_beg ┆ … ┆ symbol ┆ title                           ┆ url                             ┆ attachment_url                  │
│ ---                         ┆ ---        ┆ ---            ┆ ---              ┆   ┆ ---    ┆ ---                             ┆ ---                             ┆ ---                             │
│ str                         ┆ i64        ┆ i64            ┆ i64              ┆   ┆ str    ┆ str                             ┆ str                             ┆ str                             │
╞═════════════════════════════╪════════════╪════════════════╪══════════════════╪═══╪════════╪═════════════════════════════════╪═════════════════════════════════╪═════════════════════════════════╡
│ آهن و فولاد غدیر ایرانیان    ┆ 4556339    ┆ 31093465496    ┆ 24367250852      ┆ … ┆ شتاب   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
│ البرزدارو                   ┆ 26671574   ┆ 80704956520    ┆ 99052112711      ┆ … ┆ شتاب   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
│ انتقال داده های آسیاتک      ┆ 138080161  ┆ 557028375688   ┆ 521719877943     ┆ … ┆ شتاب   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
│ ایران خودرو دیزل            ┆ 207374030  ┆ 349859951641   ┆ 321990921362     ┆ … ┆ شتاب   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
│ ایران‌ خودرو                 ┆ 730831581  ┆ 291639316957   ┆ 422086700327     ┆ … ┆ شتاب   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
│ …                           ┆ …          ┆ …              ┆ …                ┆ … ┆ …      ┆ …                               ┆ …                               ┆ …                               │
│ مهرمام میهن                 ┆ 0          ┆ 0              ┆ 0                ┆ … ┆ شتاب   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
│ سرمایه گذاری گروه توسعه ملی ┆ 0          ┆ 0              ┆ 0                ┆ … ┆ شتاب   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
│ اختیارخ فزر-38000-14031212  ┆ 0          ┆ 0              ┆ 0                ┆ … ┆ شتاب   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
│ اختیارخ فزر-36000-14031212  ┆ 0          ┆ 0              ┆ 0                ┆ … ┆ شتاب   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
│ گروه دارویی سبحان           ┆ 0          ┆ 0              ┆ 0                ┆ … ┆ شتاب   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
└─────────────────────────────┴────────────┴────────────────┴──────────────────┴───┴────────┴─────────────────────────────────┴─────────────────────────────────┴─────────────────────────────────┘
"""
```
