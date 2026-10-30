from datetime import datetime, timedelta

import pytest

from solution import (
    Equipment,
    MaximumDurationPolicy,
    Reservation,
    ReservationController,
    ReservationService,
    Student,
    UnlimitedReservationPolicy,
)


def test_reservation_expert_detects_overlap_and_allows_adjacent_intervals(
    starts_at: datetime, ends_at: datetime
) -> None:
    reservation = Reservation(
        1, "student-1", "equipment-1", starts_at, ends_at
    )

    assert reservation.overlaps(datetime(2026, 11, 2, 10, 30), ends_at)
    assert not reservation.overlaps(ends_at, datetime(2026, 11, 2, 12, 0))


def test_service_creates_and_stores_reservation(
    reservation_service, starts_at: datetime, ends_at: datetime
) -> None:
    reservation = reservation_service.reserve(
        "student-1", "equipment-1", starts_at, ends_at
    )

    assert reservation.reservation_id == 1
    assert reservation_service.list_reservations() == (reservation,)


def test_service_rejects_unknown_student(
    reservation_service, starts_at: datetime, ends_at: datetime
) -> None:
    with pytest.raises(ValueError, match="студент"):
        reservation_service.reserve(
            "unknown-student", "equipment-1", starts_at, ends_at
        )

    assert reservation_service.list_reservations() == ()


def test_service_rejects_unknown_equipment(
    reservation_service, starts_at: datetime, ends_at: datetime
) -> None:
    with pytest.raises(ValueError, match="обладнання"):
        reservation_service.reserve(
            "student-1", "unknown-equipment", starts_at, ends_at
        )


@pytest.mark.parametrize(
    ("invalid_start", "invalid_end"),
    [
        (datetime(2026, 11, 2, 10, 0), datetime(2026, 11, 2, 10, 0)),
        (datetime(2026, 11, 2, 11, 0), datetime(2026, 11, 2, 10, 0)),
    ],
)
def test_service_rejects_empty_or_reversed_intervals(
    reservation_service, invalid_start: datetime, invalid_end: datetime
) -> None:
    with pytest.raises(ValueError, match="Час завершення"):
        reservation_service.reserve(
            "student-1", "equipment-1", invalid_start, invalid_end
        )


def test_service_rejects_overlapping_reservation_for_same_equipment(
    reservation_service, starts_at: datetime, ends_at: datetime
) -> None:
    reservation_service.reserve("student-1", "equipment-1", starts_at, ends_at)

    with pytest.raises(ValueError, match="вже заброньоване"):
        reservation_service.reserve(
            "student-2",
            "equipment-1",
            datetime(2026, 11, 2, 10, 30),
            datetime(2026, 11, 2, 11, 30),
        )

    assert len(reservation_service.list_reservations()) == 1


def test_service_allows_adjacent_reservations_for_same_equipment(
    reservation_service, starts_at: datetime, ends_at: datetime
) -> None:
    reservation_service.reserve("student-1", "equipment-1", starts_at, ends_at)

    next_reservation = reservation_service.reserve(
        "student-2", "equipment-1", ends_at, datetime(2026, 11, 2, 12, 0)
    )

    assert next_reservation.reservation_id == 2


def test_service_allows_same_time_for_different_equipment(
    reservation_service, starts_at: datetime, ends_at: datetime
) -> None:
    reservation_service.reserve("student-1", "equipment-1", starts_at, ends_at)

    second_reservation = reservation_service.reserve(
        "student-2", "equipment-2", starts_at, ends_at
    )

    assert second_reservation.equipment_id == "equipment-2"
    assert len(reservation_service.list_reservations()) == 2


def test_controller_delegates_reservation_request(
    reservation_controller, starts_at: datetime, ends_at: datetime
) -> None:
    reservation = reservation_controller.create_reservation(
        "student-1", "equipment-1", starts_at, ends_at
    )

    assert reservation.reservation_id == 1


def test_controller_accepts_a_service_with_only_the_reserve_operation(
    starts_at: datetime, ends_at: datetime
) -> None:
    expected = Reservation(7, "student-1", "equipment-1", starts_at, ends_at)
    calls = []

    class ReserveOnlyService:
        def reserve(
            self,
            student_id: str,
            equipment_id: str,
            requested_start: datetime,
            requested_end: datetime,
        ) -> Reservation:
            calls.append(
                (student_id, equipment_id, requested_start, requested_end)
            )
            return expected

    controller = ReservationController(ReserveOnlyService())
    result = controller.create_reservation(
        "student-1", "equipment-1", starts_at, ends_at
    )

    assert result is expected
    assert calls == [("student-1", "equipment-1", starts_at, ends_at)]


def test_unlimited_policy_accepts_a_valid_reservation(
    starts_at: datetime, ends_at: datetime
) -> None:
    policy = UnlimitedReservationPolicy()

    policy.validate(Equipment("equipment-1", "Проєктор", "projector"), starts_at, ends_at)


def test_maximum_duration_policy_accepts_limit_and_rejects_longer_interval(
    starts_at: datetime,
) -> None:
    policy = MaximumDurationPolicy({"projector": timedelta(hours=2)})
    equipment = Equipment("equipment-1", "Проєктор", "projector")

    policy.validate(equipment, starts_at, starts_at + timedelta(hours=2))
    with pytest.raises(ValueError, match="Тривалість бронювання"):
        policy.validate(equipment, starts_at, starts_at + timedelta(hours=3))


def test_service_uses_injected_policy_without_changing_service_code(
    starts_at: datetime,
) -> None:
    service = ReservationService(
        [Student("student-1", "Олена Коваль")],
        [Equipment("equipment-1", "Проєктор", "projector")],
        MaximumDurationPolicy({"projector": timedelta(hours=1)}),
    )

    with pytest.raises(ValueError, match="Тривалість бронювання"):
        service.reserve(
            "student-1",
            "equipment-1",
            starts_at,
            starts_at + timedelta(hours=2),
        )