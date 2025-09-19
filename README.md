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
from codalpy import Codal
codal = Codal(issuer = "اهرم", from_jdate= "1404-04-04", to_jdate="1404-06-06")
codal.fund_monthly_portfolio()
"""
shape: (603, 18)
┌──────────────────────────────┬────────────┬────────────────┬──────────────────┬───┬────────┬─────────────────────────────────┬─────────────────────────────────┬─────────────────────────────────┐
│ name                         ┆ volume_beg ┆ total_cost_beg ┆ net_proceeds_beg ┆ … ┆ symbol ┆ title                           ┆ url                             ┆ attachment_url                  │
│ ---                          ┆ ---        ┆ ---            ┆ ---              ┆   ┆ ---    ┆ ---                             ┆ ---                             ┆ ---                             │
│ str                          ┆ i64        ┆ i64            ┆ i64              ┆   ┆ str    ┆ str                             ┆ str                             ┆ str                             │
╞══════════════════════════════╪════════════╪════════════════╪══════════════════╪═══╪════════╪═════════════════════════════════╪═════════════════════════════════╪═════════════════════════════════╡
│ آهن و فولاد غدیر ایرانیان     ┆ 24500000   ┆ 140495106806   ┆ 123719463000     ┆ … ┆ اهرم   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
│ اقتصادی و خودکفایی آزادگان   ┆ 58949663   ┆ 428681824109   ┆ 363313257531     ┆ … ┆ اهرم   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
│ البرزدارو                    ┆ 266248175  ┆ 853755414625   ┆ 982697425906     ┆ … ┆ اهرم   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
│ الحاوی                       ┆ 79400000   ┆ 175805992152   ┆ 102290130720     ┆ … ┆ اهرم   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
│ الکتریک‌ خودرو شرق‌            ┆ 117032944  ┆ 427355209792   ┆ 310735053213     ┆ … ┆ اهرم   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
│ …                            ┆ …          ┆ …              ┆ …                ┆ … ┆ …      ┆ …                               ┆ …                               ┆ …                               │
│ کشت و دامداری فکا            ┆ 38000000   ┆ 42921313500    ┆ 137950282800     ┆ … ┆ اهرم   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
│ کویر تایر                    ┆ 84043466   ┆ 168768973101   ┆ 619056648665     ┆ … ┆ اهرم   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
│ ح . سرمایه گذاری‌البرز(هلدینگ‌ ┆ 0          ┆ 0              ┆ 0                ┆ … ┆ اهرم   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
│ سنگ آهن گهرزمین              ┆ 0          ┆ 0              ┆ 0                ┆ … ┆ اهرم   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
│ ح . سنگ آهن گهرزمین          ┆ 0          ┆ 0              ┆ 0                ┆ … ┆ اهرم   ┆ صورت وضعیت پورتفوی صندوق سرمای… ┆ https://www.codal.ir/Reports/A… ┆ https://www.codal.ir/Reports/A… │
└──────────────────────────────┴────────────┴────────────────┴──────────────────┴───┴────────┴─────────────────────────────────┴─────────────────────────────────┴─────────────────────────────────┘
"""
```
