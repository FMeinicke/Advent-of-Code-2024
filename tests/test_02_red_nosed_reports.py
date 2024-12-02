from __future__ import annotations

import pytest

from solutions._02_red_nosed_reports import is_report_safe


@pytest.mark.parametrize(
    "report, is_safe",
    (
        pytest.param([7, 6, 4, 2, 1], True, id="safe_decreasing"),
        pytest.param([1, 2, 7, 8, 9], False, id="unsafe_increase"),
        pytest.param([9, 7, 6, 2, 1], False, id="unsafe_increase"),
        pytest.param([1, 3, 2, 4, 5], False, id="unsafe_increasing_decreasing"),
        pytest.param([8, 6, 4, 4, 1], False, id="unsafe_no_increase_decrease"),
        pytest.param([1, 3, 6, 7, 9], True, id="safe_increasing"),
    ),
)
def test_is_report_safe(report, is_safe):
    assert is_report_safe(report) == is_safe
