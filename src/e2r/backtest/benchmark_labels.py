"""Evaluation-only benchmark labels for blind discovery replay."""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import date
from enum import Enum
from pathlib import Path
from typing import Mapping, Sequence

from e2r.models import Market


DEFAULT_BENCHMARK_LABEL_PATH = Path("data/benchmark_labels/e2r_known_winners.json")


class BenchmarkGroup(str, Enum):
    STRUCTURAL = "structural"
    ONE_OFF = "one_off"
    BOOM_BUST = "boom_bust"
    VALUATION_OVERHEAT = "valuation_overheat"
    CYCLICAL = "cyclical"


class ExpectedMinLayer(str, Enum):
    EVENT_SEARCH = "event_search"
    DEEP_RESEARCH = "deep_research"
    STAGE2 = "stage2"
    STAGE3 = "stage3"


@dataclass(frozen=True)
class BenchmarkLabel:
    """A hidden label used only after candidate generation is complete."""

    label_id: str
    symbol: str
    company_name: str
    market: Market
    expected_window_start: date
    expected_window_end: date
    expected_group: BenchmarkGroup
    expected_min_layer: ExpectedMinLayer
    expected_safe_stage: str
    notes: str
    evaluation_only: bool = True

    def __post_init__(self) -> None:
        if not self.evaluation_only:
            raise ValueError("benchmark labels must be evaluation_only")
        if not isinstance(self.market, Market):
            object.__setattr__(self, "market", Market(self.market))
        if not isinstance(self.expected_group, BenchmarkGroup):
            object.__setattr__(self, "expected_group", BenchmarkGroup(self.expected_group))
        if not isinstance(self.expected_min_layer, ExpectedMinLayer):
            object.__setattr__(self, "expected_min_layer", ExpectedMinLayer(self.expected_min_layer))
        if self.expected_window_end < self.expected_window_start:
            raise ValueError("expected_window_end cannot be before expected_window_start")


def load_benchmark_labels(path: str | Path = DEFAULT_BENCHMARK_LABEL_PATH) -> tuple[BenchmarkLabel, ...]:
    """Load labels for evaluation only."""

    rows = json.loads(Path(path).read_text(encoding="utf-8"))
    return tuple(benchmark_label_from_mapping(item) for item in rows)


def benchmark_label_from_mapping(row: Mapping[str, object]) -> BenchmarkLabel:
    return BenchmarkLabel(
        label_id=str(row["label_id"]),
        symbol=str(row["symbol"]),
        company_name=str(row["company_name"]),
        market=Market(str(row["market"])),
        expected_window_start=date.fromisoformat(str(row["expected_window_start"])),
        expected_window_end=date.fromisoformat(str(row["expected_window_end"])),
        expected_group=BenchmarkGroup(str(row["expected_group"])),
        expected_min_layer=ExpectedMinLayer(str(row["expected_min_layer"])),
        expected_safe_stage=str(row["expected_safe_stage"]),
        notes=str(row.get("notes") or ""),
        evaluation_only=bool(row.get("evaluation_only", True)),
    )


def labels_for_market(labels: Sequence[BenchmarkLabel], market: Market) -> tuple[BenchmarkLabel, ...]:
    return tuple(item for item in labels if item.market == market)


__all__ = [
    "BenchmarkGroup",
    "BenchmarkLabel",
    "DEFAULT_BENCHMARK_LABEL_PATH",
    "ExpectedMinLayer",
    "benchmark_label_from_mapping",
    "labels_for_market",
    "load_benchmark_labels",
]
