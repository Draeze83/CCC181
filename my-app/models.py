from datetime import datetime
from typing import Optional

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Index, String, Text, false, func, text, true
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()


class Counter(db.Model):
    __tablename__ = "counters"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(60), unique=True)

    staff: Mapped[list["User"]] = relationship(back_populates="counter")
    tickets: Mapped[list["Ticket"]] = relationship(back_populates="counter")


class User(db.Model):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    student_id: Mapped[str | None] = mapped_column(String(9), unique=True)
    role: Mapped[str] = mapped_column(String(10), default="student", server_default="student")
    password_hash: Mapped[str | None] = mapped_column(String(255))
    counter_id: Mapped[int | None] = mapped_column(ForeignKey("counters.id", ondelete="SET NULL"))

    counter: Mapped[Optional["Counter"]] = relationship(back_populates="staff")
    tickets: Mapped[list["Ticket"]] = relationship(back_populates="user")

    __table_args__ = (
        CheckConstraint("email = lower(email)", name="ck_users_email_lowercase"),
        CheckConstraint(
            r"email ~ '^[^@[:space:]]+@[^@[:space:]]+\.[^@[:space:]]+$'",
            name="ck_users_email_format",
        ),
        CheckConstraint("student_id ~ '^[0-9]{4}-[0-9]{4}$'", name="ck_users_student_id_format"),
        CheckConstraint("role IN ('student', 'staff')", name="ck_users_role"),
        CheckConstraint("role = 'staff' OR student_id IS NOT NULL", name="ck_users_student_has_id"),
        CheckConstraint("role = 'student' OR password_hash IS NOT NULL", name="ck_users_staff_has_password"),
    )


class Service(db.Model):
    __tablename__ = "services"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(80), unique=True)
    prefix: Mapped[str] = mapped_column(String(3), unique=True)
    instructions: Mapped[str] = mapped_column(Text, default="", server_default="")
    avg_minutes: Mapped[int] = mapped_column(default=5, server_default="5")
    allows_remote: Mapped[bool] = mapped_column(default=True, server_default=true())
    is_active: Mapped[bool] = mapped_column(default=True, server_default=true())

    tickets: Mapped[list["Ticket"]] = relationship(back_populates="service")
    # passive_deletes lets the database's ON DELETE CASCADE remove the links
    documents: Mapped[list["ServiceDocument"]] = relationship(
        back_populates="service", cascade="all, delete-orphan", passive_deletes=True
    )

    __table_args__ = (
        CheckConstraint("prefix ~ '^[A-Z]{1,3}$'", name="ck_services_prefix"),
        CheckConstraint("avg_minutes > 0", name="ck_services_avg_minutes"),
    )


class Document(db.Model):
    __tablename__ = "documents"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)

    services: Mapped[list["ServiceDocument"]] = relationship(back_populates="document")


class ServiceDocument(db.Model):
    __tablename__ = "service_documents"

    service_id: Mapped[int] = mapped_column(ForeignKey("services.id", ondelete="CASCADE"), primary_key=True)
    document_id: Mapped[int] = mapped_column(ForeignKey("documents.id", ondelete="RESTRICT"), primary_key=True)
    copies: Mapped[int] = mapped_column(default=1, server_default="1")

    service: Mapped["Service"] = relationship(back_populates="documents")
    document: Mapped["Document"] = relationship(back_populates="services")

    __table_args__ = (
        CheckConstraint("copies > 0", name="ck_service_documents_copies"),
    )


class Ticket(db.Model):
    __tablename__ = "tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="RESTRICT"))
    service_id: Mapped[int] = mapped_column(ForeignKey("services.id", ondelete="RESTRICT"))
    counter_id: Mapped[int | None] = mapped_column(ForeignKey("counters.id", ondelete="RESTRICT"))
    status: Mapped[str] = mapped_column(String(20), default="waiting", server_default="waiting")
    is_priority: Mapped[bool] = mapped_column(default=False, server_default=false())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    called_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))
    finished_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True))

    user: Mapped["User"] = relationship(back_populates="tickets")
    service: Mapped["Service"] = relationship(back_populates="tickets")
    counter: Mapped[Optional["Counter"]] = relationship(back_populates="tickets")

    __table_args__ = (
        CheckConstraint(
            "status IN ('waiting', 'called', 'served', 'no-show', 'left')",
            name="ck_tickets_status",
        ),
        CheckConstraint("called_at >= created_at", name="ck_tickets_called_after_created"),
        CheckConstraint("finished_at >= created_at", name="ck_tickets_finished_after_created"),
        CheckConstraint("finished_at >= called_at", name="ck_tickets_finished_after_called"),
        CheckConstraint(
            "status IN ('waiting', 'left') OR called_at IS NOT NULL",
            name="ck_tickets_called_first",
        ),
        CheckConstraint(
            "(status IN ('served', 'no-show', 'left')) = (finished_at IS NOT NULL)",
            name="ck_tickets_finished_matches_status",
        ),
        # One active ticket per student per service (FR-14)
        Index(
            "uq_tickets_one_active",
            "user_id",
            "service_id",
            unique=True,
            postgresql_where=text("status IN ('waiting', 'called')"),
        ),
    )