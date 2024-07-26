from typing import Literal
from annotated_types import IsDigits
from urllib.parse import urlparse, parse_qs
import re
from codal.models import QueryParam, Letter, IncomeStatements
from codal.http import get
from codal import gen_df

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
    def income_statement(self):
        letters = self.letter()
        rs = []
        if letters is not None:
            for i in letters:
                urlp = urlparse(i.url)
                params = parse_qs(urlp.query)
                params["SheetId"] = ["1"]
                r = get(url=f"{self.base_url}{urlp.path}",params=params, rtype="text")
                if r is not None:
                    pattern = r'var datasource = (.*?);'
                    match = re.search(pattern, r)
                    if match:
                        rs.append(match.group(1))
        validated = []
        if rs:
            for j in rs:
                try:
                    data = IncomeStatements.model_validate_json(j)
                    validated.append(data)
                except Exception as e:
                    print(e)
        if validated:
            df = gen_df.income_statement(validated, self._category)
            return df
