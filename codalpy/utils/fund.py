import polars as pl
from bs4 import BeautifulSoup


def clean_raw_portfolio_df(df: pl.DataFrame) -> pl.DataFrame:
    values_idx = 0
    for row in df.rows():
        isnumeric_ = sum([str(i).isnumeric() for i in row])
        values_idx += 1
        if isnumeric_ > 4:
            break
    cols = [
        "name",
        "volume_beg",
        "total_cost_beg",
        "net_proceeds_beg",
        "volume_pop",
        "total_cost_pop",
        "volume_sop",
        "sale_amount_sop",
        "volume_end",
        "price_end",
        "total_cost_end",
        "net_proceeds_end",
        "pct_of_total_assets_end",
    ]
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
                is_numeric = sum([is_number(str(i)) for i in row])
                if is_numeric < 3:
                    data[cols.pop()] = row
                    idx += 1
            else:
                is_numeric = sum([is_number(str(i)) for i in row])
                if is_numeric > len(row) / 2:
                    data[cols.pop()] = row
                idx += 1
    df = pl.DataFrame(data)
    df = (
        df.drop_nulls()
        .filter(pl.col("name").str.len_chars() > 0)
        .with_columns(
            [pl.col(i).cast(pl.Float64).cast(pl.Int64) for i in df.columns[1:-1]]
        )
        .with_columns(
            pct_of_total_assets_end=pl.col("pct_of_total_assets_end").cast(pl.Float64),
        )
    )
    return df


def find_download_endpoint(html: str) -> list[dict[str, str]]:
    soup = BeautifulSoup(html, "html.parser")
    table = soup.find("table", {"id": "dgAttachmentList"})
    rows = table.find_all("tr")[1:]
    data = []
    for row in rows:
        onclick = row.get("onclick", "")
        link = None
        if "window.open" in onclick:
            link = onclick.split("'")[1]  # متن داخل window.open('...')

        tds = row.find_all("td")
        description = tds[1].get_text(strip=True) if len(tds) > 1 else ""
        date_added = tds[2].get_text(strip=True) if len(tds) > 2 else ""

        data.append(
            {"link": link, "description": description, "date_added": date_added}
        )
    return data
