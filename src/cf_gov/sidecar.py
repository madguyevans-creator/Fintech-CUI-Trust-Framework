#!/usr/bin/env python3
"""Lite sidecar CLI. No LLM. Prints Visible Authority State as JSON."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from cf_gov.engine import AuditLog, MappingConfig, Session


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Conversational Finance Governance Framework v0.4 Lite sidecar"
    )
    parser.add_argument("--mapping", required=True, help="Path to a product-line YAML mapping")
    parser.add_argument("--utterance", required=True, help="User utterance to classify")
    parser.add_argument(
        "--audit",
        default="",
        help="Optional JSONL audit path (append-only, hash-chained)",
    )
    args = parser.parse_args()

    mapping = MappingConfig.load(args.mapping)
    audit = AuditLog(Path(args.audit) if args.audit else None)
    session = Session(mapping, audit)
    result = session.handle(args.utterance)

    out = {
        "product_line": mapping.product_line,
        "decision": result.decision,
        "classification": asdict(result.classification),
        "visible_authority_state": asdict(result.visible_authority_state),
        "credential": asdict(result.credential) if result.credential else None,
        "audit_event_id": result.event.get("event_id"),
        "audit_hash": result.event.get("hash"),
    }
    print(json.dumps(out, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
