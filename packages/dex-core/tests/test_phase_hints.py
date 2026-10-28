"""The hint each phase checkpoint writes, on a confirmed and an unconfirmed command.

An unconfirmed command reaches a phase checkpoint only when its earlier phases
spent nothing (every profile fresh in the cache), so its hint must not talk
about a confirmed budget it never had or a re-profile the re-run will not do.
A confirmed command's hint is unchanged.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from exmergo_dex_core import command_args
from exmergo_dex_core.envelope import Cost, Paradigm
from exmergo_dex_core.guards.cost_guard import ConfirmationRequiredError

ESTIMATE = 178257920.0


class _AskingGate:
    """A billed gate whose phase preflight always asks: the case every phase
    hint is written for. No session budget, so no session note is added."""

    paradigm = Paradigm.BYTES_SCANNED
    session_ceiling = None
    session_spent = None

    def __init__(self, confirmed: bool):
        self.confirmed = confirmed

    def preflight_phase(self, estimate: float) -> None:
        raise ConfirmationRequiredError(Cost(estimate=estimate, paradigm=self.paradigm))


def _hint(phase: str, confirmed: bool) -> str:
    adapter = SimpleNamespace(cost_gate=_AskingGate(confirmed))
    counts = {"candidate_count": 27, "object_count": 13}
    if phase == "verify":
        request = command_args.verify_handshake(
            "explore relationships", adapter, ESTIMATE, **counts
        )
    elif phase == "overlap":
        request = command_args.overlap_handshake(
            "explore relationships", adapter, ESTIMATE, cap=200, elided=0, **counts
        )
    elif phase == "check-cumulative":
        request = command_args.cumulative_handshake(
            "explore profile", adapter, ESTIMATE, **counts
        )
    else:
        request = command_args.sample_handshake("explore cluster", adapter, ESTIMATE)
    assert request is not None
    assert request.data["phase"] == phase
    return request.data["hint"]


PHASES = ["verify", "overlap", "check-cumulative", "sample"]


@pytest.mark.parametrize("phase", PHASES)
def test_an_unconfirmed_hint_asks_for_confirmation_without_a_confirmed_budget(phase):
    hint = _hint(phase, confirmed=False)
    assert "beyond what remains of the confirmed budget" not in hint
    assert "a re-run re-profiles first" not in hint
    assert "178257920 bytes_scanned, and this command was not confirmed" in hint
    assert "--confirm --budget 178257920" in hint


@pytest.mark.parametrize("phase", PHASES)
def test_a_confirmed_hint_still_names_the_confirmed_budget(phase):
    hint = _hint(phase, confirmed=True)
    assert "178257920 bytes_scanned beyond what remains of the confirmed budget" in hint
    assert "--confirm --budget 178257920" in hint


def test_the_confirmed_verify_hint_is_unchanged():
    assert _hint("verify", confirmed=True) == (
        "found 27 candidate relationship(s) across 13 object(s); verifying them all "
        "is estimated at 178257920 bytes_scanned beyond what remains of the confirmed "
        "budget. Profiles and unverified relationships are already saved to the "
        "exploration cache; re-run the same command with --confirm --budget 178257920 "
        "to profile and verify in one pass (a re-run re-profiles first)"
    )


@pytest.mark.parametrize("phase", ["verify", "overlap", "check-cumulative"])
def test_an_unconfirmed_hint_says_the_cached_profiles_are_reused(phase):
    assert "(the cached profiles are reused)" in _hint(phase, confirmed=False)
