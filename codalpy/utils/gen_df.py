from typing import Literal
import polars as pl
from codalpy.utils.models import FinancialStatement, Cell, Letter
from codalpy.utils.utils import (
    translate,
    fiscal_month,
    pascal_to_snake_case,
    normalize_fs_item,
)
from codalpy.utils import cols, dicts


def _cells(
    item: FinancialStatement, fs: Literal["BalanceSheet", "IncomeStatement"]
) -> list[Cell] | None:
    if item.sheets[0].tables[0].alias_name == fs:
        r = item.sheets[0].tables[0].cells
        if r:
            return r
    if item.sheets[0].tables[1].alias_name == fs:
        r = item.sheets[0].tables[1].cells
        if r:
            return r


def cells_to_df(cells: list[Cell]) -> pl.DataFrame:
    cells_ = [(i.column_sequence, i.row_sequence, i.value) for i in cells]
    df = pl.from_records(cells_, schema=["col", "row", "value"], orient="row")
    df = df.pivot(values="value", on="col", index="row")
    df_filter = df.filter(pl.col("1") == "شرح")
    index = []
    df_ = pl.DataFrame()
    for i, v in enumerate(df_filter.row(0)):
        if normalize_fs_item(str(v)) == "شرح":
            index.append(i)
    for i in index:
        selected = df.select([str(i), str(i + 1)])
        selected.columns = ["item", "value"]
        df_ = pl.concat([df_, selected])
    return df_


def clean_df(
    records: list[tuple[Letter, FinancialStatement]],
    category: Literal["production"],
    fs: Literal["BalanceSheet", "IncomeStatement"],
) -> pl.DataFrame | None:
    snake_fs = pascal_to_snake_case(fs)
    df_concat = pl.DataFrame()
    for letter, data in records:
        cells = _cells(data, fs)
        if cells is not None:
            df = cells_to_df(cells)
            df = df.filter(pl.col("value") != "")
            df = df.with_columns(
                pl.struct(["item"]).map_elements(
                    lambda x: translate(x["item"], dicts.dicts[snake_fs][category]),
                    return_dtype=pl.String,
                )
            )
            df = df.filter(
                pl.col("item").is_in(dicts.dicts[snake_fs][category].values())
            ).with_columns([pl.col("value").cast(pl.Int64), pl.lit(0).alias("index")])
            df = df.pivot(
                values="value",
                on="item",
                index="index",
                aggregate_function="sum",
            )
            miss_cols = set(cols.select[snake_fs][category]) - set(df.columns)
            if miss_cols:
                df = df.with_columns(
                    [pl.lit(0).cast(pl.Int64).alias(i) for i in miss_cols]
                )
            df = df.select(cols.select[snake_fs][category])
            df = df.with_columns(
                [
                    pl.lit(data.is_audited).alias("is_audited"),
                    pl.lit(data.period_end_to_date).alias("period_ending_date"),
                    pl.lit(data.year_end_to_date).alias("fiscal_year_ending_date"),
                    pl.lit(
                        fiscal_month(data.year_end_to_date, data.period_end_to_date)
                    ).alias("fiscal_month"),
                    pl.lit(letter.publish_date_time).alias("publish_date_time"),
                    pl.lit(False).alias("consolidated"),
                    pl.lit(letter.symbol).alias("symbol"),
                    pl.lit(letter.title).alias("title"),
                    pl.lit(letter.url).alias("url"),
                    pl.lit(letter.attachment_url).alias("attachment_url"),
                    pl.lit(letter.pdf_url).alias("pdf_url"),
                    pl.lit(letter.excel_url).alias("excel_url"),
                ]
            )
            df_concat = pl.concat([df_concat, df])

    return df_concat
