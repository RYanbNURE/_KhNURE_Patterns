from datetime import timedelta

import pytest

student_implementation = pytest.importorskip("student_implementation")


@pytest.fixture
def student_service():
    students = [
        student_implementation.Student("student-1", "Олена Коваль"),
        student_implementation.Student("student-2", "Андрій Мельник"),
    ]
    equipment = [
        student_implementation.Equipment("equipment-1", "Проєктор", "projector"),
        student_implementation.Equipment("equipment-2", "Ноутбук", "laptop"),
    ]
    return student_implementation.ReservationService(
        students, equipment, student_implementation.UnlimitedReservationPolicy()
    )


def test_student_service_creates_and_stores_reservation(
    student_service, starts_at, ends_at
) -> None:
    pytest.fail("TODO: викличте reserve та перевірте створений і збережений об'єкт.")


def test_student_service_rejects_invalid_requests(
    student_service, starts_at, ends_at
) -> None:
    pytest.fail("TODO: перевірте невідомі ID та некоректний часовий інтервал.")


def test_student_service_prevents_conflicts_but_allows_adjacent_intervals(
    student_service, starts_at, ends_at
) -> None:
    pytest.fail("TODO: перевірте перетин і суміжні бронювання.")


def test_student_controller_delegates_to_service(
    student_service, starts_at, ends_at
) -> None:
    pytest.fail("TODO: перевірте, що Controller делегує запит сервісу.")


def test_student_controller_accepts_a_reserve_only_dependency(
    starts_at, ends_at
) -> None:
    expected = student_implementation.Reservation(
        7, "student-1", "equipment-1", starts_at, ends_at
    )

    class ReserveOnlyService:
        def reserve(
            self,
            student_id,
            equipment_id,
            requested_start,
            requested_end,
        ):
            return expected

    controller = student_implementation.ReservationController(
        ReserveOnlyService()
    )
    result = controller.create_reservation(
        "student-1", "equipment-1", starts_at, ends_at
    )

    assert result is expected


def test_refactoring_preserves_behavior_for_all_design_violations(
    student_service, starts_at, ends_at
) -> None:
    pytest.fail(
        "TODO: додайте regression/contract assertions для всіх 18 виправлень принципів."
    )


def test_student_duration_policy_obeys_the_shared_contract(starts_at) -> None:
    policy = student_implementation.MaximumDurationPolicy(
        {"projector": timedelta(hours=2)}
    )
    equipment = student_implementation.Equipment(
        "equipment-1", "Проєктор", "projector"
    )

    policy.validate(equipment, starts_at, starts_at + timedelta(hours=2))
    with pytest.raises(ValueError):
        policy.validate(equipment, starts_at, starts_at + timedelta(hours=3))


def test_student_service_uses_the_injected_duration_policy(starts_at) -> None:
    equipment = student_implementation.Equipment(
        "equipment-1", "Проєктор", "projector"
    )
    service = student_implementation.ReservationService(
        [student_implementation.Student("student-1", "Олена Коваль")],
        [equipment],
        student_implementation.MaximumDurationPolicy(
            {"projector": timedelta(hours=1)}
        ),
    )

    with pytest.raises(ValueError, match="Тривалість бронювання"):
        service.reserve(
            "student-1",
            "equipment-1",
            starts_at,
            starts_at + timedelta(hours=2),
        )

    assert service.list_reservations() == ()