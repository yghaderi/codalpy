import polars as pl
import re


def clean_raw_df(df: pl.DataFrame) -> pl.DataFrame:
    values_idx = 0
    for row in df.rows():
        isnumeric_ = sum([str(i).isnumeric() for i in row])
        values_idx += 1
        if isnumeric_ > 4:
            break
    cols = ['name',
            'volume_beg',
            'total_cost_beg',
            'net_proceeds_beg',
            'volume_pop',
            'total_cost_pop',
            'volume_sop',
            'sale_amount_sop',
            'volume_end',
            'price_end',
            'total_cost_end',
            'net_proceeds_end',
            'pct_of_total_assets_end']
    cols.reverse()
    data = {}
    idx = 0

    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            return False

    for row in df[values_idx:].transpose().rows():
        if cols:
            if idx == 0:
                data[cols.pop()] = row
                idx += 1
            else:
                is_numeric = sum([is_number(str(i)) for i in row])
                if is_numeric > len(row) / 2:
                    data[cols.pop()] = row
                idx += 1

    df = pl.DataFrame(data)
    df = df.drop_nulls().with_columns([
        pl.col(i).cast(pl.Float64).cast(pl.Int64) for i in df.columns[1:-1]
    ]).with_columns(
        pct_of_total_assets_end=pl.col("pct_of_total_assets_end").cast(pl.Float64),
    )
    return df


def find_download_endpoint(text: str) -> str:
    pattern = r"window\.open\(&#39;([^&#]+)&#39;"
    match = re.search(pattern, text)
    return match.group(1)
