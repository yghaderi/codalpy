import polars as pl
from codalpy.utils.models import IncomeStatement, Cell, Letter
from codalpy.utils import translate, cols, dicts
from codalpy.utils import fiscal_month


def _cells(item: IncomeStatement) -> list[Cell] | None:
    if item.sheets[0].tables[0].alias_name == "IncomeStatement":
        return item.sheets[0].tables[0].cells
    elif item.sheets[0].tables[1].alias_name == "IncomeStatement":
        return item.sheets[0].tables[1].cells


def income_statement(
    records: list[tuple[Letter, IncomeStatement]], category: str
) -> pl.DataFrame | None:
    df_concat = pl.DataFrame()
    for letter, incs in records:
        cells = _cells(incs)

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
                            lambda x: translate(
                                x["item"], dicts.income_statement.production
                            ),
                            return_dtype=pl.String,
                        )
                    )
                    df = df.filter(
                        pl.col("item").is_in(cols.income_statement),
                        pl.col("value") != "",
                    )
                    df = df.with_columns(
                        pl.col("value").cast(pl.Int64), pl.lit(0).alias("index")
                    )
                    df = df.pivot(
                        values="value",
                        on="item",
                        index="index",
                        aggregate_function="sum",
                    )
                    if "exceptional_cost" not in df.columns:
                        df = df.with_columns(
                            pl.lit(0).cast(pl.Int64).alias("exceptional_cost")
                        )
                    df = df.select(cols.income_statement)
                    df = df.with_columns(
                        [
                            pl.lit(incs.is_audited).alias("is_audited"),
                            pl.lit(incs.period_end_to_date).alias("period_ending_date"),
                            pl.lit(incs.year_end_to_date).alias(
                                "fiscal_year_ending_date"
                            ),
                            pl.lit(
                                fiscal_month(
                                    incs.year_end_to_date, incs.period_end_to_date
                                )
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
