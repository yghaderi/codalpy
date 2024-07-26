from typing import Literal
import polars as pl
from codal.models import IncomeStatements, Cell
from codal.utils import translate
from codal import dicts
from codal import cols


def _cells(item: IncomeStatements)-> list[Cell]|None:
    if item.sheets[0].tables[0].alias_name == "IncomeStatement":
        return item.sheets[0].tables[0].cells
    elif item.sheets[0].tables[1].alias_name == "IncomeStatement":
        return item.sheets[0].tables[1].cells

def income_statement(records: list[IncomeStatements], category:str):
    df_concat = pl.DataFrame()
    for item in records:
        cells = _cells(item)

        if cells is not None:
            cells = [(i.column_sequence, i.row_sequence, i.value) for i in cells]
            df = pl.from_records(cells, schema=["col", "row", "value"], orient="row")
            df = (
                df.pivot(values="value", on="col", index="row")
                .rename({"1": "item", "2": "value"})
                .select(["item", "value"])
            )
            match category:
                case "production":
                    df = df.with_columns(
                        pl.struct(["item"]).map_elements(
                            lambda x: translate(x["item"],dicts.income_statement.production), return_dtype=pl.String
                        )
                    )
                    df = df.filter(pl.col("item").is_in(cols.income_statement), pl.col("value")!="")
                    df = df.with_columns(pl.col("value").cast(pl.Int64), pl.lit(0).alias("index"))
                    df = df.pivot(
                            values="value", on="item", index = "index",aggregate_function="sum"
                        )
                    if "special_items" not in df.columns:
                                    df_ = df.with_columns(pl.lit(0).cast(pl.Int64).alias("special_items"))
                    df = df.select(cols.income_statement)
                    df = df.with_columns(
                        [
                            pl.lit(item.is_audited).alias("is_audited"),
                            pl.lit(item.period_end_to_date).alias(
                                "period_end_to_date"
                            ),
                            pl.lit(item.year_end_to_date).alias(
                                "year_end_to_date"
                            ),
                            pl.lit(item.register_date_time).alias(
                                "register_date_time"
                            ),
                            pl.lit(item.sent_date_time).alias(
                                "sent_date_time"
                            ),
                        ]
                    )
                    df_concat  =pl.concat([df_concat, df])
    return df_concat
