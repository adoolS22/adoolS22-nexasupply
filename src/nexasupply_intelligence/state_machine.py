"""Persistent-scan-friendly state machine with explicit transitions."""

from enum import StrEnum


class ScanState(StrEnum):
    CREATED = "CREATED"
    COLLECTING = "COLLECTING"
    VALIDATING = "VALIDATING"
    CLASSIFIED = "CLASSIFIED"
    PROPOSED = "PROPOSED"
    REVIEW_REQUIRED = "REVIEW_REQUIRED"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    APPLIED = "APPLIED"
    FAILED = "FAILED"


class InvalidTransition(ValueError):
    """Raised when a scan attempts an unsupported state transition."""


_TRANSITIONS: dict[ScanState, frozenset[ScanState]] = {
    ScanState.CREATED: frozenset({ScanState.COLLECTING, ScanState.FAILED}),
    ScanState.COLLECTING: frozenset({ScanState.VALIDATING, ScanState.FAILED}),
    ScanState.VALIDATING: frozenset({ScanState.CLASSIFIED, ScanState.FAILED}),
    ScanState.CLASSIFIED: frozenset({ScanState.PROPOSED, ScanState.FAILED}),
    ScanState.PROPOSED: frozenset({ScanState.REVIEW_REQUIRED, ScanState.APPROVED, ScanState.REJECTED}),
    ScanState.REVIEW_REQUIRED: frozenset({ScanState.APPROVED, ScanState.REJECTED}),
    ScanState.APPROVED: frozenset({ScanState.APPLIED, ScanState.FAILED}),
    ScanState.REJECTED: frozenset(),
    ScanState.APPLIED: frozenset(),
    ScanState.FAILED: frozenset(),
}


class ScanStateMachine:
    def __init__(self, state: ScanState = ScanState.CREATED) -> None:
        self.state = state

    def transition(self, target: ScanState) -> ScanState:
        if target not in _TRANSITIONS[self.state]:
            raise InvalidTransition(f"cannot transition {self.state} -> {target}")
        self.state = target
        return self.state
