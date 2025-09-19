from typing import ClassVar, Optional

from pydantic import BaseModel, ConfigDict, Field, alias_generators, field_validator
from typing_extensions import Literal

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

    meta_table_id: int
    meta_table_code: int
    address: str
    formula: str
    validations: str
    financial_concept: Optional[str]
    cell_group_name: str
    category: int
    col_span: int
    column_code: int
    column_sequence: int
    decimal_place: int
    row_code: int
    row_sequence: int
    row_span: int
    row_type_name: str
    value: str
    value_type_name: str
    data_type_name: Optional[str]
    period_end_to_date: str
    year_end_to_date: str
    is_audited: bool


class Table(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel, populate_by_name=True
    )
    meta_table_id: int
    title_fa: Optional[str] = Field(alias="title_Fa")
    title_en: Optional[str] = Field(alias="title_En")
    sequence: int
    sheet_code: int
    code: int
    description: Optional[str]
    alias_name: Optional[str]
    version_no: str
    cells: list[Cell]


class Sheet(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel, populate_by_name=True
    )
    code: int
    title_fa: str = Field(alias="title_Fa")
    title_en: str = Field(alias="title_En")
    sequence: int
    is_dynamic: bool
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


class DataSource(BaseModel):
    model_config = ConfigDict(
        alias_generator=alias_generators.to_camel, populate_by_name=True
    )
    title_fa: str = Field(alias="title_Fa")
    title_en: str = Field(alias="title_En")
    subject: Optional[str]
    dsc: Optional[str]
    type: int
    period: int
    period_end_to_date: str
    year_end_to_date: str
    period_extra_day: int
    isConsolidated: bool
    tracing_no: int
    kind: int
    is_audited: bool
    audit_state: int
    register_date_time: str
    sent_date_time: str
    publish_date_time: str
    state: int
    is_for_auditing: bool
    sheets: list[Sheet]


class GetDataSourceError(BaseModel):
    source: Literal["match", "validation"]
    message: str


class DataSourceResult(BaseModel):
    status: Literal["success", "error"]
    letter: Letter
    data: Optional[DataSource]
    error: Optional[GetDataSourceError]
