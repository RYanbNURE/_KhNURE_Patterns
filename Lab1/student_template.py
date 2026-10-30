"""Стартовий шаблон: реалізуйте позначені TODO за принципами GRASP."""

from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Protocol


@dataclass(frozen=True)
class Student:
    student_id: str
    name: str


@dataclass(frozen=True)
class Equipment:
    equipment_id: str
    name: str
    kind: str = "general"


@dataclass(frozen=True)
class Reservation:
    reservation_id: int
    student_id: str
    equipment_id: str
    starts_at: datetime
    ends_at: datetime

    def overlaps(self, starts_at: datetime, ends_at: datetime) -> bool:
        # TODO 1: реалізуйте перевірку перетину як відповідальність Reservation.
        raise NotImplementedError("TODO 1: Information Expert")


class ReservationServicePort(Protocol):
    """Мінімальний контракт для Controller: лише операція бронювання."""

    def reserve(
        self,
        student_id: str,
        equipment_id: str,
        starts_at: datetime,
        ends_at: datetime,
    ) -> Reservation: ...


class ReservationPolicy(Protocol):
    def validate(
        self,
        equipment: Equipment,
        starts_at: datetime,
        ends_at: datetime,
    ) -> None: ...


class UnlimitedReservationPolicy:
    def validate(
        self,
        equipment: Equipment,
        starts_at: datetime,
        ends_at: datetime,
    ) -> None:
        return None


class MaximumDurationPolicy:
    def __init__(self, maximum_by_kind: dict[str, timedelta]) -> None:
        self._maximum_by_kind = dict(maximum_by_kind)

    def validate(
        self,
        equipment: Equipment,
        starts_at: datetime,
        ends_at: datetime,
    ) -> None:
        # TODO 6: перевірте тривалість за kind без змін у ReservationService.
        raise NotImplementedError("TODO 6: OCP і LSP")


class ReservationService:
    def __init__(
        self,
        students: list[Student],
        equipment: list[Equipment],
        policy: ReservationPolicy,
    ) -> None:
        self._students = {student.student_id: student for student in students}
        self._equipment = {item.equipment_id: item for item in equipment}
        self._policy = policy
        self._reservations: list[Reservation] = []

    def reserve(
        self,
        student_id: str,
        equipment_id: str,
        starts_at: datetime,
        ends_at: datetime,
    ) -> Reservation:
        # TODO 2: перевірте студента, обладнання та коректність інтервалу.
        # TODO 6: передайте перевірку тривалості політиці для цього обладнання.
        # TODO 3: знайдіть конфлікт для того самого обладнання через overlaps.
        # TODO 4: створіть бронювання, додайте його до колекції та поверніть.
        raise NotImplementedError("TODO 2-4: Information Expert і Creator")

    def list_reservations(self) -> tuple[Reservation, ...]:
        return tuple(self._reservations)


class ReservationController:
    def __init__(self, reservation_service: ReservationServicePort) -> None:
        self._reservation_service = reservation_service

    def create_reservation(
        self,
        student_id: str,
        equipment_id: str,
        starts_at: datetime,
        ends_at: datetime,
    ) -> Reservation:
        # TODO 5: делегуйте системну подію сервісу, не дублюючи його правила.
        raise NotImplementedError("TODO 5: Controller")