import json
import re
from pathlib import Path


RAW_PATH = "raw.txt"


def parse_money(s: str) -> float:
    # "1 200,00" -> 1200.00
    s = s.strip().replace("\u00a0", " ").replace(" ", "")
    s = s.replace(",", ".")
    return float(s)


def extract_all_prices(text: str) -> list[float]:
    # Matches numbers like: 154,00 or 1 200,00 or 7 330,00
    money_re = re.compile(r"(?<!\d)(?:\d{1,3}(?:[ \u00a0]\d{3})*|\d+),\d{2}(?!\d)")
    return [parse_money(m) for m in money_re.findall(text)]


def extract_datetime(text: str) -> dict | None:
    m = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})", text)
    if not m:
        return None
    return {"date": m.group(1), "time": m.group(2), "datetime": f"{m.group(1)} {m.group(2)}"}


def extract_payment(text: str) -> dict | None:
    # Example:
    # Банковская карта:
    # 18 009,00
    m = re.search(r"Банковская\s+карта:\s*\n\s*([\d\s\u00a0]+,\d{2})", text)
    if not m:
        return None
    return {"method": "Банковская карта", "amount": parse_money(m.group(1))}


def extract_total(text: str) -> float | None:
    # Example:
    # ИТОГО:
    # 18 009,00
    m = re.search(r"ИТОГО:\s*\n\s*([\d\s\u00a0]+,\d{2})", text)
    return parse_money(m.group(1)) if m else None


def extract_items(lines: list[str]) -> list[dict]:
    """
    Expected item block shape:
      N.
      <name possibly spans multiple lines>
      <qty> x <unit_price>
      <line_total>
      Стоимость
      <line_total>
    """
    items = []
    i = 0

    item_start_re = re.compile(r"^\s*(\d+)\.\s*$")
    qty_price_re = re.compile(r"^\s*([\d,]+)\s*x\s*([\d\s\u00a0]+,\d{2})\s*$")
    money_line_re = re.compile(r"^\s*[\d\s\u00a0]+,\d{2}\s*$")

    while i < len(lines):
        m = item_start_re.match(lines[i])
        if not m:
            i += 1
            continue

        line_no = int(m.group(1))
        i += 1

        # Collect name lines until the "qty x unit_price" line
        name_parts = []
        while i < len(lines) and lines[i].strip() and not qty_price_re.match(lines[i]) and not item_start_re.match(lines[i]):
            name_parts.append(lines[i].strip())
            i += 1
        name = " ".join(name_parts).strip()

        qty = unit_price = line_total = None

        if i < len(lines):
            m2 = qty_price_re.match(lines[i])
            if m2:
                qty = float(m2.group(1).replace(",", "."))
                unit_price = parse_money(m2.group(2))
                i += 1

                # Next line often contains line total
                if i < len(lines) and money_line_re.match(lines[i]):
                    line_total = parse_money(lines[i])
                    i += 1

                # Skip "Стоимость" and its repeated amount if present
                if i < len(lines) and lines[i].strip().lower().startswith("стоим"):
                    i += 1
                    if i < len(lines) and money_line_re.match(lines[i]):
                        i += 1

        items.append(
            {
                "line_no": line_no,
                "name": name,
                "quantity": qty,
                "unit_price": unit_price,
                "line_total": line_total,
            }
        )

    return items


def main() -> None:
    text = Path(RAW_PATH).read_text(encoding="utf-8", errors="replace")
    lines = [l.rstrip("\n") for l in text.splitlines()]

    items = extract_items(lines)
    prices = extract_all_prices(text)
    total = extract_total(text)
    payment = extract_payment(text)
    dt = extract_datetime(text)

    # Compute total from parsed items (if possible)
    computed_total = None
    if items and all(isinstance(it.get("line_total"), (int, float)) for it in items):
        computed_total = round(sum(it["line_total"] for it in items), 2)

    out = {
        "datetime": dt,
        "payment": payment,
        "total_reported": total,
        "total_computed_from_items": computed_total,
        "currency": "KZT",
        "items": items,
        "product_names": [it["name"] for it in items if it.get("name")],
        "all_prices_found": prices,
        "counts": {"items": len(items), "prices_found": len(prices)},
    }

    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()