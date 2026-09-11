"""Registry of tools, in display order."""
import importlib

ORDER = [
    # date
    "age", "days_between", "working_days", "add_days", "countdown", "timer",
    # text
    "word_counter", "case_converter", "password", "lines",
    # numbers
    "percentage", "proportion", "discount", "number_words", "roman", "units", "random",
    # school & work
    "hours_calc", "weighted_average", "colf_tredicesima", "colf_ferie", "colf_tfr",
    # health
    "bmi", "calories", "running_pace",
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
