from typing import ClassVar
from pydantic import BaseModel, ConfigDict, alias_generators, field_validator

from codalpy.utils.utils import norm_char


class Letter(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_pascal, populate_by_name=True
    )

    base_url: ClassVar[str]

    tracing_no: int
    symbol: str
    company_name: str
    title: str
    letter_code: str
    sent_date_time: str
    publish_date_time: str
    has_html: bool
    is_estimate: bool
    has_excel: bool
    has_pdf: bool
    has_xbrl: bool
    has_attachment: bool
    url: str
    attachment_url: str
    pdf_url: str
    excel_url: str

    @field_validator(
        "symbol",
        "company_name",
        "letter_code",
        "title",
        "sent_date_time",
        "publish_date_time",
        mode="after",
    )
    def serialize_norm_char(cls, v: str):
        return norm_char(v)

    @field_validator("url", "attachment_url", "pdf_url", mode="after")
    def serialize_url(cls, v: str):
        if v:
            if v[0] != "/":
                v = f"/{v}"
            return f"{cls.base_url}{v}"


class Cell(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel, populate_by_name=True
    )

    address: str
    category: int
    cell_group_name: str
    col_span: int
    column_code: int
    column_sequence: int
    decimal_place: int
    period_end_to_date: str
    row_code: int
    row_sequence: int
    row_span: int
    row_type_name: str
    value: str
    value_type_name: str
    year_end_to_date: str


class Table(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel, populate_by_name=True
    )

    sequence: int
    sheet_code: int
    version_no: str
    alias_name: str | None
    cells: list[Cell]


class Sheet(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel, populate_by_name=True
    )

    version_no: int
    alias_name: str
    code: int
    sequence: int
    tables: list[Table]


class FinancialStatement(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel, populate_by_name=True
    )

    is_audited: bool
    period: int
    period_end_to_date: str
    period_extra_day: int
    register_date_time: str
    sent_date_time: str | None
    sheets: list[Sheet]
    type: int
    year_end_to_date: str


class GetFinancialStatement(BaseModel):
    records: list[tuple[Letter, FinancialStatement]]
    get_error: list[Letter]
    match_error: list[tuple[Letter, str]]
    validation_error: list[tuple[Letter, str]]
