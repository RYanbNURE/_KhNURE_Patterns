import pytest

student_implementation = pytest.importorskip("student_implementation")


def test_student_reservation_detects_overlap_and_adjacent_interval() -> None:
    from datetime import datetime

    reservation = student_implementation.Reservation(
        1,
        "student-1",
        "equipment-1",
        datetime(2026, 11, 2, 10, 0),
        datetime(2026, 11, 2, 11, 0),
    )

    assert reservation.overlaps(
        datetime(2026, 11, 2, 10, 30), datetime(2026, 11, 2, 11, 30)
    )
    assert not reservation.overlaps(
        datetime(2026, 11, 2, 11, 0), datetime(2026, 11, 2, 12, 0)
    )