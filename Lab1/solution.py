"""Еталонна реалізація лабораторної роботи з GRASP."""

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
        return self.starts_at < ends_at and starts_at < self.ends_at


class ReservationServicePort(Protocol):
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
        maximum = self._maximum_by_kind.get(equipment.kind)
        if maximum is not None and ends_at - starts_at > maximum:
            raise ValueError("Тривалість бронювання перевищує дозволену.")


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
        if student_id not in self._students:
            raise ValueError(f"Невідомий студент: {student_id}")
        if equipment_id not in self._equipment:
            raise ValueError(f"Невідоме обладнання: {equipment_id}")
        if starts_at >= ends_at:
            raise ValueError("Час завершення має бути пізніше за час початку.")
        self._policy.validate(self._equipment[equipment_id], starts_at, ends_at)

        for existing in self._reservations:
            if existing.equipment_id == equipment_id and existing.overlaps(
                starts_at, ends_at
            ):
                raise ValueError("Обладнання вже заброньоване на цей інтервал.")

        reservation = Reservation(
            reservation_id=len(self._reservations) + 1,
            student_id=student_id,
            equipment_id=equipment_id,
            starts_at=starts_at,
            ends_at=ends_at,
        )
        self._reservations.append(reservation)
        return reservation

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
        return self._reservation_service.reserve(
            student_id, equipment_id, starts_at, ends_at
        )


def build_demo_controller() -> ReservationController:
    students = [
        Student("student-1", "Олена Коваль"),
        Student("student-2", "Андрій Мельник"),
    ]
    equipment = [
        Equipment("equipment-1", "Мультимедійний проєктор"),
        Equipment("equipment-2", "Ноутбук"),
    ]
    service = ReservationService(students, equipment, UnlimitedReservationPolicy())
    return ReservationController(service)