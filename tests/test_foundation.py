from nexasupply_intelligence.evidence import assess_evidence
from nexasupply_intelligence.state_machine import InvalidTransition, ScanState, ScanStateMachine


def test_evidence_is_bounded_and_explainable():
    assessment = assess_evidence(
        authoritative_sources=2,
        corroborating_sources=2,
        source_count=3,
        has_primary_document=True,
        claim_is_direct=True,
    )
    assert 0 <= assessment.score <= 1
    assert assessment.confidence == "HIGH"
    assert assessment.reasons


def test_negative_counts_are_rejected():
    try:
        assess_evidence(source_count=-1)
    except ValueError as exc:
        assert "negative" in str(exc)
    else:
        raise AssertionError("expected ValueError")


def test_scan_follows_controlled_path():
    scan = ScanStateMachine()
    for state in (
        ScanState.COLLECTING,
        ScanState.VALIDATING,
        ScanState.CLASSIFIED,
        ScanState.PROPOSED,
        ScanState.REVIEW_REQUIRED,
        ScanState.APPROVED,
        ScanState.APPLIED,
    ):
        assert scan.transition(state) == state


def test_terminal_state_rejects_transition():
    scan = ScanStateMachine(ScanState.REJECTED)
    try:
        scan.transition(ScanState.APPROVED)
    except InvalidTransition:
        pass
    else:
        raise AssertionError("expected InvalidTransition")
