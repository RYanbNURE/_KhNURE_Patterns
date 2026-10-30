from datetime import datetime

import pytest

from solution import (
    Equipment,
    UnlimitedReservationPolicy,
    ReservationController,
    ReservationService,
    Student,
)


@pytest.fixture
def students() -> list[Student]:
    return [
        Student("student-1", "Олена Коваль"),
        Student("student-2", "Андрій Мельник"),
    ]


@pytest.fixture
def equipment() -> list[Equipment]:
    return [
        Equipment("equipment-1", "Проєктор", "projector"),
        Equipment("equipment-2", "Ноутбук", "laptop"),
    ]


@pytest.fixture
def reservation_service(
    students: list[Student], equipment: list[Equipment]
) -> ReservationService:
    return ReservationService(students, equipment, UnlimitedReservationPolicy())


@pytest.fixture
def reservation_controller(
    reservation_service: ReservationService,
) -> ReservationController:
    return ReservationController(reservation_service)


@pytest.fixture
def starts_at() -> datetime:
    return datetime(2026, 11, 2, 10, 0)


@pytest.fixture
def ends_at() -> datetime:
    return datetime(2026, 11, 2, 11, 0)