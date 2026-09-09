#!/usr/bin/env python3
"""Lite tests for the v0.4 control plane. Run from repository root:

    python3 tests/test_sidecar.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from cf_gov.engine import MappingConfig, Session  # noqa: E402


def load_gold() -> list[dict]:
    path = ROOT / "tests" / "classification" / "gold.jsonl"
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line:
            rows.append(json.loads(line))
    return rows


def assert_eq(actual, expected, msg: str) -> None:
    if actual != expected:
        raise AssertionError(f"{msg}: expected {expected!r}, got {actual!r}")


def test_mapping_divergence() -> None:
    payments = MappingConfig.load(ROOT / "mappings" / "payments.yaml")
    collections = MappingConfig.load(ROOT / "mappings" / "collections.yaml")
    p = Session(payments).handle("Pay now.")
    c = Session(collections).handle("Pay now.")
    assert_eq(p.classification.action, "transact", "payments action")
    assert_eq(c.classification.action, "transact", "collections action")
    if p.decision not in {"auth_required", "escalate", "breaker"}:
        raise AssertionError(f"payments 'Pay now.' must not be FREE, got {p.decision}")
    if c.decision not in {"escalate", "breaker"}:
        raise AssertionError(f"collections 'Pay now.' must escalate/break, got {c.decision}")
    if p.decision == c.decision and p.decision == "auth_required":
        raise AssertionError("payments and collections must diverge on 'Pay now.'")


def test_no_secret_in_model_context() -> None:
    mapping = MappingConfig.load(ROOT / "mappings" / "payments.yaml")
    result = Session(mapping).handle("Pay now. Send 200 dollars to Jane.")
    if result.credential is not None:
        assert_eq(
            result.credential.secret_material_in_model_context,
            False,
            "scoped credential must not place secrets in model context",
        )


def test_vulnerability_breaker() -> None:
    mapping = MappingConfig.load(ROOT / "mappings" / "collections.yaml")
    result = Session(mapping).handle("I cannot pay and I am scared. Should I borrow to repay?")
    if result.decision not in {"escalate", "breaker"}:
        raise AssertionError(
            f"vulnerability + advice in collections must not be FREE/AUTH-only, got {result.decision}"
        )


def test_visible_state_present() -> None:
    mapping = MappingConfig.load(ROOT / "mappings" / "insurance.yaml")
    result = Session(mapping).handle("When does my policy renew?")
    vas = result.visible_authority_state
    for field in ("action", "fcr", "rs", "decision", "live_permissions", "last_authorization"):
        if getattr(vas, field) in (None, ""):
            raise AssertionError(f"visible authority state missing {field}")


def test_gold_actions_not_weaker_than_label() -> None:
    """Classifier may be stricter than gold, never weaker on high-cost rows."""
    order = ["inform", "advise", "commit", "transact", "represent"]
    mapping = MappingConfig.load(ROOT / "mappings" / "payments.yaml")
    session = Session(mapping)
    failures = []
    for row in load_gold():
        if row.get("false_negative_cost") != "high":
            continue
        got = session.handle(row["utterance"]).classification.action
        if order.index(got) < order.index(row["action"]):
            failures.append((row["id"], row["action"], got, row["utterance"]))
    if failures:
        raise AssertionError(f"high-cost false negatives: {failures}")


def main() -> None:
    test_mapping_divergence()
    test_no_secret_in_model_context()
    test_vulnerability_breaker()
    test_visible_state_present()
    test_gold_actions_not_weaker_than_label()
    print("ok")


if __name__ == "__main__":
    main()
