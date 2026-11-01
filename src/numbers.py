import re

def parse_amount(value):
    # Turn text like "60.000", "1,346,000" or "2,450.50" into a real number.
    if isinstance(value, (int, float)):
        return float(value)
    s = re.sub(r"[^\d.,]", "", str(value or ""))
    if not s:
        return None
    m = re.search(r"[.,](\d+)$", s)
    if m and len(m.group(1)) <= 2:          # decimal part, like 2,450.50
        whole = re.sub(r"[.,]", "", s[:m.start()])
        return float(f"{whole or 0}.{m.group(1)}")
    return float(re.sub(r"[.,]", "", s))     # only thousands separators