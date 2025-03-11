from pathlib import Path
from codalpy.utils.query import QueryParam, Consts, Symbol, Issuer
import json

class Fund:
    def __init__(self, query: QueryParam):
        self._query = query
        self.consts = Consts()
        self.funds:list[Issuer] = []

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value: QueryParam):
        self._query = value

    def load_funds(self):
        pkg_dir = Path(__file__).parent
        json_path = pkg_dir / "data/symbols.json"
        with open(json_path) as f:
            d = json.load(f).get("funds")
            assert d is not None, "Funds data not found"
            self.funds = [Issuer.model_validate(i)for i in d]

    def handle_symbol(self)-> Issuer:
        if not self.funds:
            self.load_funds()

        symbol = Symbol(symbol = self.query.symbol, issuers = self.funds)
        fund = symbol.match_symbol()
        self.query.symbol = fund.symbol
        return fund

    def get_data(self):
        pass
