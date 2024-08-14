import jdatetime as jdt


def norm_char(w: str):
    dict_ = {
        "ي": "ی",
        "ك": "ک",
        "\u200c": " ",
        "۰": "0",
        "۱": "1",
        "۲": "2",
        "۳": "3",
        "۴": "4",
        "۵": "5",
        "۶": "6",
        "۷": "7",
        "۸": "8",
        "۹": "9",
        "/": "-",
    }
    return w.translate(str.maketrans(dict_))


def normalize_fs_item(w: str):
    dict_ = {
        " ": "",
        "–": "",
        "(": "",
        ")": "",
        "،": "",
        "ي": "ی",
        "ى": "ی",
        "آ": "ا",
        "\u200f": "",
        "\u200c": "",
    }
    return w.translate(str.maketrans(dict_))


def translate(item: str, dict_: dict):
    for k, v in dict_.items():
        if item and normalize_fs_item(k) == normalize_fs_item(item):
            return v
    return item


def fiscal_month(fiscal_year_ending_date: str, period_ending_date: str):
    fm = [3, 6, 9, 12]
    days = (
        jdt.date.fromisoformat(fiscal_year_ending_date.replace("/", "-"))
        - jdt.date.fromisoformat(period_ending_date.replace("/", "-"))
    ).days
    return min(fm, key=lambda x: abs(x - (365 - days) / 30))
