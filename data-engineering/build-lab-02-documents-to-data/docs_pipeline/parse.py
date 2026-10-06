import re

FIELDS = {
    "invoice_no": r"Invoice No:\s*(INV-\d+)",
    "date": r"Date:\s*(\d{4}-\d{2}-\d{2})",
    "total": r"TOTAL\s*\$([\d,]+\.\d{2})",
}


def parse(text):
    lines = [ln.strip() for ln in text.splitlines()]
    lines = [ln for ln in lines if ln]
    rec = {"vendor": lines[0]}
    for name, pattern in FIELDS.items():
        m = re.search(pattern, text, re.I)
        rec[name] = m.group(1) if m else None
    if rec["total"]:
        amount = rec["total"].replace(",", "")
        rec["total"] = float(amount)
    rec["text"] = " ".join(lines)
    return rec
