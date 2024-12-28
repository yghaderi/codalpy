import polars as pl
import re


def handle_cols(df: pl.DataFrame) -> dict:
    df = df.head(10).fill_null(strategy="forward").unique(subset=df.columns[0], keep="last").transpose()
    level0 = 0
    jdate = ""
    counter = {}
    result = []

    mapping = {
        "تعداد": "volume",
        "بهای تمام شده": "total_cost",
        "خالص ارزش فروش": "net_proceeds",
        "نام شرکت": "name",
        "شرکت": "name",
        "مبلغ فروش": "sale_amount",
        "خرید طی دوره": "pop",
        "فروش طی دوره": "sop",
        "تغییرات طی دوره": "cop",
        "قیمت بازار هر سهم": "price",
        "درصد به کل دارایی ها": "pct_of_total_assets"
    }
    df = df.with_columns(pl.all().str.replace_many(mapping).str.replace_all("\u202b", ""))
    for i, name in enumerate(df.columns):
        l = df[name].to_list()
        for item in l:
            if isinstance(item, str):
                if i < 5:
                    match = re.search(r"\b\d{4}/\d{2}/\d{2}\b", item)
                    if match:
                        jdate = match.group(0)
                if "name" in item:
                    level0 = i
    df = df.select([df.columns[level0]])
    df.columns = ["level0"]
    df = df.with_columns(level0=pl.col("level0").fill_null("del"))

    for item in df["level0"].to_list():
        if item not in counter:
            counter[item] = 1
        else:
            counter[item] += 1

        match item:
            case "name":
                result.append(item)
            case "volume":
                match counter[item]:
                    case 1:
                        result.append(f"{item}_beg")
                    case 2:
                        result.append(f"{item}_pop")
                    case 3:
                        result.append(f"{item}_sop")
                    case 4:
                        result.append(f"{item}_end")
            case "total_cost":
                match counter[item]:
                    case 1:
                        result.append(f"{item}_beg")
                    case 2:
                        result.append(f"{item}_pop")
                    case 3:
                        result.append(f"{item}_end")
            case "net_proceeds":
                match counter[item]:
                    case 1:
                        result.append(f"{item}_beg")
                    case 2:
                        result.append(f"{item}_end")
            case "sale_amount":
                result.append(f"{item}_sop")
            case "price":
                result.append(f"{item}_end")
            case "pct_of_total_assets":
                result.append(f"{item}_end")
            case _:
                result.append(f"{item}_{counter[item]}")
    return {"cols": result, "jdate": jdate, "head_idx": level0}


def clean_raw_df(df: pl.DataFrame) -> pl.DataFrame:
    cols, jdate, head_idx = handle_cols(df).values()
    df = df[head_idx + 1:]
    df.columns = cols

    df = df.select([i for i in cols if not i[-1].isnumeric()])
    df = df.drop_nulls().filter(pl.col("volume_beg").map_elements(lambda x: x.isnumeric(), return_dtype=pl.Boolean))
    df = df.with_columns([
        pl.col(i).cast(pl.Float64).cast(pl.Int64) for i in df.columns[1:-1]
    ]).with_columns(
        pct_of_total_assets_end=pl.col("pct_of_total_assets_end").cast(pl.Float64),
        jdate=pl.lit(jdate)
    )
    return df


def find_download_endpoint(text: str) -> str:
    pattern = r"window\.open\(&#39;([^&#]+)&#39;"
    match = re.search(pattern, text)
    return match.group(1)
