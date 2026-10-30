"""Демонструє сценарій резервування обладнання."""

from datetime import datetime

from solution import build_demo_controller


def main() -> None:
    controller = build_demo_controller()
    reservation = controller.create_reservation(
        "student-1",
        "equipment-1",
        datetime(2026, 11, 2, 10, 0),
        datetime(2026, 11, 2, 11, 0),
    )
    print(
        f"Бронювання №{reservation.reservation_id} створено: "
        f"{reservation.student_id} — {reservation.equipment_id}, "
        f"{reservation.starts_at:%Y-%m-%d %H:%M}–{reservation.ends_at:%H:%M}."
    )


if __name__ == "__main__":
    main()