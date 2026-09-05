"""Registry of tools, in display order."""
import importlib

ORDER = [
    # date
    "age", "days_between", "add_days", "timer",
    # text
    "word_counter", "case_converter", "password", "lines",
    # numbers
    "percentage", "discount", "roman", "units", "random",
    # health
    "bmi", "calories",
    # money
    "loan", "vat", "split_bill",
    # images
    "resize", "convert_image", "qr",
]


def load():
    out = []
    for name in ORDER:
        mod = importlib.import_module("tools." + name)
        out.append(mod.TOOL)
    return out
