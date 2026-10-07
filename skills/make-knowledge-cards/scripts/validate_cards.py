#!/usr/bin/env python3
"""
validate_cards.py - deterministic structure checker for make-knowledge-cards decks.

Usage:
    python validate_cards.py <deck.md>
    python3   validate_cards.py <deck.md>
    uv run python validate_cards.py <deck.md>

The checker verifies the format contract defined in SKILL.md:
  - one level-1 deck title
  - cards as level-3 headings "### N. Title", numbered from 1
  - exactly three non-empty bold-labelled field bullets per card
  - no duplicate card titles
  - no more than 8 cards
  - no answer leakage in the third field (example or self-test)

Fewer than 5 cards produce a warning (allowed only for genuinely thin
sources); structural problems produce errors.

Exit code: 0 = no errors (warnings allowed), 1 = at least one error.
"""

import re
import sys
from pathlib import Path

MAX_CARDS = 8
TARGET_MIN = 5
THIN_MIN = 3

CARD_RE = re.compile(r"^###\s+(\d+)(?:[.、)][ \t]*|[ \t]+)(.+?)\s*$")
# Accept both "**Label:** value" (colon inside bold) and "**Label**: value".
FIELD_RE = re.compile(r"^-\s+\*\*(.+?)(?:[：:]\*\*|\*\*[：:])[ \t]*(.*)$")
ANSWER_RE = re.compile(
    r"(答案|解答|参考回答|正确答案)\s*[:：]"
    r"|\banswer\s*[:：]"
    r"|\bans\.?\s*[:：]",
    re.IGNORECASE,
)


def normalize_title(title):
    return re.sub(r"[^\w一-鿿]", "", title.lower())


def parse_deck(text):
    h1 = None
    cards = []
    current = None
    for line in text.splitlines():
        if line.startswith("# ") and not line.startswith("## ") and h1 is None:
            h1 = line[2:].strip()
            continue
        card_match = CARD_RE.match(line)
        if card_match:
            current = {
                "number": int(card_match.group(1)),
                "title": card_match.group(2).strip(),
                "fields": [],
                "stray": [],
            }
            cards.append(current)
            continue
        if current is None:
            continue
        field_match = FIELD_RE.match(line)
        if field_match:
            current["fields"].append(
                [field_match.group(1).strip(), field_match.group(2).strip()]
            )
        elif line.startswith("#") or line.lstrip().startswith("- "):
            current["stray"].append(line.strip())
        elif line.strip() and current["fields"]:
            # Treat non-empty continuation lines as part of the last field.
            current["fields"][-1][1] = (
                current["fields"][-1][1] + " " + line.strip()
            ).strip()
    return h1, cards


def validate(text):
    errors, warnings = [], []
    h1, cards = parse_deck(text)

    if not h1:
        warnings.append("No level-1 deck title found (start the deck with '# <title>').")

    if not cards:
        errors.append(
            "No cards found. Each card must start with a level-3 heading like '### 1. Title'."
        )
        return errors, warnings

    if len(cards) > MAX_CARDS:
        errors.append(
            f"Found {len(cards)} cards; the maximum is {MAX_CARDS}. Merge or drop the weakest points."
        )

    expected_numbers = list(range(1, len(cards) + 1))
    actual_numbers = [card["number"] for card in cards]
    if actual_numbers != expected_numbers:
        warnings.append(
            f"Card numbers are {actual_numbers}; they should be sequential 1..{len(cards)}."
        )

    seen_titles = set()
    for index, card in enumerate(cards, start=1):
        label = f"Card {card['number']}"
        if not card["title"]:
            errors.append(f"{label}: title is empty.")
        normalized = normalize_title(card["title"])
        if normalized and normalized in seen_titles:
            errors.append(f"{label}: duplicate title '{card['title']}'.")
        seen_titles.add(normalized)

        if card["stray"]:
            errors.append(
                f"{label}: contains bullets or headings outside the three field lines "
                f"({len(card['stray'])} extra item(s))."
            )

        fields = card["fields"]
        if len(fields) != 3:
            errors.append(
                f"{label}: expected exactly 3 field bullets, found {len(fields)} "
                "(title field, explanation field, example/self-test field)."
            )
            continue
        for field_index, (field_label, value) in enumerate(fields, start=1):
            if not field_label:
                errors.append(f"{label}: field {field_index} has an empty label.")
            if not value:
                errors.append(f"{label}: field '{field_label or field_index}' is empty.")

        third_value = fields[2][1]
        if ANSWER_RE.search(third_value):
            errors.append(
                f"{label}: the example/self-test field appears to contain an answer. "
                "Self-test items must be questions without answers."
            )

    if len(cards) < TARGET_MIN:
        if len(cards) < THIN_MIN:
            warnings.append(
                f"Only {len(cards)} cards. This is acceptable only if the source is very thin; "
                "tell the user and never invent points to reach 5."
            )
        else:
            warnings.append(
                f"{len(cards)} cards (< {TARGET_MIN}); add the thin-source note under the deck title."
            )

    return errors, warnings


def main():
    if len(sys.argv) != 2:
        print("Usage: python validate_cards.py <deck.md>")
        return 1

    deck_path = Path(sys.argv[1])
    if not deck_path.is_file():
        print(f"[ERROR] File not found: {deck_path}")
        return 1

    text = deck_path.read_text(encoding="utf-8")
    errors, warnings = validate(text)

    print(f"Validating: {deck_path}")
    for message in warnings:
        print(f"[WARN] {message}")
    for message in errors:
        print(f"[ERROR] {message}")
    if not errors:
        card_count = len(parse_deck(text)[1])
        print(f"[OK] Deck passed structural validation ({card_count} card(s)).")
    print(f"Result: {len(errors)} error(s), {len(warnings)} warning(s).")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
