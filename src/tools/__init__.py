"""Registry of tools, in display order."""
import importlib

ORDER = [
    # date
    "age", "days_between", "add_days", "countdown", "timer",
    # text
    "word_counter", "case_converter", "password", "lines",
    # numbers
    "percentage", "discount", "number_words", "roman", "units", "random",
    # school & work
    "weighted_average", "colf_tredicesima", "colf_ferie", "colf_tfr",
    # health
    "bmi", "calories",
    # money
    "loan", "vat", "split_bill",
    # images
    "resize", "convert_image", "qr",
]


def load():
    """A module exposes either TOOL (one tool) or TOOLS (a list, e.g. a tool plus its preset pages)."""
    out = []
    for name in ORDER:
        mod = importlib.import_module("tools." + name)
        if hasattr(mod, "TOOLS"):
            out.extend(mod.TOOLS)
        else:
            out.append(mod.TOOL)
    return out
