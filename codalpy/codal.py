from typing import Literal
from annotated_types import IsDigits
from urllib.parse import urlparse, parse_qs
import re
import polars as pl
from codalpy.models import QueryParam, Letter, IncomeStatement, GetIncomeStatement
from codalpy.http import get
from codalpy import gen_df


class Codal:
    def __init__(self, query: QueryParam, category: Literal["production"]) -> None:
        self.base_url = "https://codal.ir"
        self.search_url = "https://search.codal.ir/api/search/v2/q?"
        self.api = "api/search/v2/q"
        self._query = query
        self._category = category

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value: QueryParam):
        self._query = value

    def letter(self):
        r = get(
            url=self.search_url,
            params=self._query.model_dump(by_alias=True),
            rtype="josn",
        )
        if isinstance(r, dict):
            pages = str(r.get("Page"))
            Letter.base_url = self.base_url
            letters = [Letter.model_validate(i) for i in r["Letters"]]
            if pages.isdigit:
                pages = int(pages)
                if pages > 1:

                    for p in range(2, pages + 1):
                        self._query.page_number = p
                        r = get(
                            url=self.search_url,
                            params=self._query.model_dump(by_alias=True),
                            rtype="josn",
                        )
                        if isinstance(r, dict):
                            letters.extend(
                                [Letter.model_validate(i) for i in r["Letters"]]
                            )
            return letters

    def _get_incom_statemnt(self) -> GetIncomeStatement | None:
        letters = self.letter()
        if letters is not None:
            records = []
            get_error = []
            match_error = []
            validation_error = []
            res = []
            for i in letters:
                urlp = urlparse(i.url)
                params = parse_qs(urlp.query)
                params["SheetId"] = ["1"]
                r = get(url=f"{self.base_url}{urlp.path}", params=params, rtype="text")
                if r is not None:
                    pattern = r"var datasource = (.*?);"
                    match = re.search(pattern, r)
                    if match:
                        text = match.group(1)
                        try:
                            records.append(
                                (i, IncomeStatement.model_validate_json(text))
                            )
                        except Exception as e:
                            validation_error.append((i, str(e)))
                    else:
                        match_error.append((i, str(r)))
                else:
                    get_error.append(i)
            return GetIncomeStatement(
                records=records,
                get_error=get_error,
                match_error=match_error,
                validation_error=validation_error,
            )

    def income_statement(self) -> pl.DataFrame | None:
        data = self._get_incom_statemnt()
        if data:
            if data.records:
                df = gen_df.income_statement(data.records, self._category)
                return df
