from datetime import date, datetime, timedelta
from typing import Any, Dict

from sqlalchemy.orm import selectinload

from app.extensions import db
from app.exceptions import ForbiddenError, NotFoundError
from app.models.maintenance import MaintenanceStatus
from app.models.manual import Manual
from app.models.motorcycle import Motorcycle
from app.models.user import User


class StatisticService:
    """Сервис для работы со статистикой"""

    @staticmethod
    def get_garage_stats(user_id: int) -> Dict[str, Any]:
        """Получить данные для гаража"""
        user = db.session.get(
            User,
            user_id,
            options=[
                selectinload(User.motorcycles).selectinload(Motorcycle.maintenances),
            ],
        )

        if not user:
            raise NotFoundError("Пользователь не найден")

        motorcycles = Motorcycle.query.filter_by(owner_id=user.id).all()
        if not motorcycles:
            return {
                "motorcycles": [],
                "cost": 0,
                "plan_maintenances_count": 0,
                "maintenances_count": 0,
            }

        moto_data = []
        cost = 0
        plan_count = 0
        completed_count = 0

        for m in motorcycles:
            moto_data.append({"id": m.id, "name": m.name})
            
            for maintenance in m.maintenances:
                if maintenance.status == MaintenanceStatus.PLANNED.value:
                    plan_count += 1
                elif maintenance.status == MaintenanceStatus.COMPLETED.value:
                    completed_count += 1
                    if maintenance.cost:
                        cost += maintenance.cost

        return {
            "motorcycles": moto_data,
            "cost": cost,
            "plan_maintenances_count": plan_count,
            "maintenances_count": completed_count,
        }

    @staticmethod
    def get_moto_garage_stats(moto_id: int, user_id: int) -> Dict[str, Any]:
        """Получить детальную статистику по мотоциклу для гаража"""
        moto = db.session.get(
            Motorcycle,
            moto_id,
            options=[selectinload(Motorcycle.maintenances)]
        )
        user = db.session.get(User, user_id)

        if not moto:
            raise NotFoundError("Мотоцикл не найден")
        if not user:
            raise NotFoundError("Пользователь не найден")
        if int(moto.owner_id) != int(user.id):
            raise ForbiddenError("Вы не являетесь владельцем этого мотоцикла")

        planned = [m for m in moto.maintenances if m.status == MaintenanceStatus.PLANNED.value]
        completed = [m for m in moto.maintenances if m.status == MaintenanceStatus.COMPLETED.value]

        planned_maintenances = sorted(
            planned,
            key=lambda x: x.planned_mileage or 0,
            reverse=False,
        )[:5]

        recent_maintenances = sorted(
            completed,
            key=lambda x: x.completed_date or date.min,
            reverse=True,
        )[:5]

        nodes = []  # TODO: реализовать узлы здоровья

        completed_with_cost = [m for m in completed if m.cost]
        total_cost = sum(m.cost for m in completed_with_cost)
        avg_cost = round(total_cost / len(completed_with_cost)) if completed_with_cost else 0
        max_cost = max((m.cost for m in completed_with_cost), default=0)

        today = date.today()
        month_start_date = today.replace(day=1)

        month_cost = sum(
            m.cost for m in completed_with_cost
            if m.completed_date and m.completed_date >= month_start_date
        )

        money_chart_data = []
        for i in range(5, -1, -1):
            month_date = month_start_date - timedelta(days=i * 30)
            month_start_dt = month_date.replace(day=1)

            if month_date.month == 12:
                month_end = date(month_date.year + 1, 1, 1)
            else:
                month_end = date(month_date.year, month_date.month + 1, 1)

            month_cost_total = sum(
                m.cost for m in completed_with_cost
                if m.completed_date and month_start_dt <= m.completed_date < month_end
            )

            money_chart_data.append({
                "month": f"{month_date.strftime('%b')} {month_date.year}",
                "value": month_cost_total
            })

        return {
            "motorcycle": moto.to_dict(),
            "planned_maintenances": [m.to_dict() for m in planned_maintenances],
            "recent_maintenances": [m.to_dict() for m in recent_maintenances],
            "nodes": nodes,
            "total_cost": total_cost,
            "max_cost": max_cost,
            "average_cost": avg_cost,
            "month_cost": month_cost,
            "money_chart_data": money_chart_data,
            "total_maintenances": len(completed),
            "month_maintenances": len([
                m for m in completed
                if m.completed_date and m.completed_date >= month_start_date
            ]),
            "freq_chart_data": [],
        }

    @staticmethod
    def get_repair_stats(user_id: int) -> Dict[str, Any]:
        """Получить статистику для страницы ремонта"""
        user = db.session.get(
            User,
            user_id,
            options=[
                selectinload(User.motorcycles).selectinload(Motorcycle.maintenances),
            ],
        )

        if not user:
            raise NotFoundError("Пользователь не найден")

        overdue = 0
        planned = 0
        motorcycles = []
        maintenances = []

        for moto in user.motorcycles:
            for maint in moto.maintenances:
                if maint.status == MaintenanceStatus.OVERDUE.value:
                    overdue += 1
                elif maint.status == MaintenanceStatus.PLANNED.value:
                    planned += 1
                
                maint_dict = maint.to_dict()
                maint_dict["moto_name"] = moto.name
                maintenances.append(maint_dict)

            motorcycles.append(moto.to_dict())

        return {
            "overdue": overdue,
            "soon": 0,
            "planned": planned,
            "motorcycles": motorcycles,
            "maintenances": maintenances,
        }

    @staticmethod
    def get_maintenance_stats(user_id: int) -> Dict[str, Any]:
        """Получить статистику для страницы обслуживания"""
        motorcycles = (
            Motorcycle.query.filter_by(owner_id=user_id)
            .options(selectinload(Motorcycle.maintenances))
            .all()
        )

        all_maintenances = []
        planned_count = 0
        overdue_count = 0
        completed_count = 0

        for motorcycle in motorcycles:
            for maintenance in motorcycle.maintenances:
                maint_dict = maintenance.to_dict()
                maint_dict["moto_name"] = motorcycle.name
                
                if maintenance.status == MaintenanceStatus.PLANNED.value:
                    planned_count += 1
                elif maintenance.status == MaintenanceStatus.OVERDUE.value:
                    overdue_count += 1
                elif maintenance.status == MaintenanceStatus.COMPLETED.value:
                    completed_count += 1
                
                all_maintenances.append(maint_dict)

        return {
            "motorcycles": [m.to_dict() for m in motorcycles],
            "history_maintenances": [m for m in all_maintenances if m["status"] == MaintenanceStatus.COMPLETED.value],
            "planned_maintenances": [m for m in all_maintenances if m["status"] in (MaintenanceStatus.PLANNED.value, MaintenanceStatus.OVERDUE.value)],
            "all_maintenances_count": len(all_maintenances),
            "planned_maintenances_count": planned_count,
            "overdue_maintenances_count": overdue_count,
        }

    @staticmethod
    def get_registrations_chart(user_id: int) -> Dict[str, Any]:
        """Получить данные для графика регистраций (только для админа)"""
        user = db.session.get(User, user_id)
        if not user or user.role != "admin":
            raise ForbiddenError("Доступ запрещен. Требуются права администратора")

        now = datetime.now()
        registrations_data = []
        month_names = ["Янв", "Фев", "Мар", "Апр", "Май", "Июн", "Июл", "Авг", "Сен", "Окт", "Ноя", "Дек"]

        for i in range(11, -1, -1):
            month_date = now.replace(day=1) - timedelta(days=i * 30)
            month_start_dt = datetime(month_date.year, month_date.month, 1)
            
            if month_date.month == 12:
                month_end = datetime(month_date.year + 1, 1, 1)
            else:
                month_end = datetime(month_date.year, month_date.month + 1, 1)

            count = User.query.filter(
                User.created_at >= month_start_dt, User.created_at < month_end
            ).count()

            month_label = f"{month_names[month_date.month - 1]} {month_date.year}"
            registrations_data.append({"month": month_label, "value": count})

        users_count = User.query.count()
        motos_count = Motorcycle.query.count()
        manuals_count = Manual.query.count()

        last_reg = User.query.order_by(User.created_at.desc()).limit(5).all()
        last_reg_data = [u.to_dict() for u in last_reg]

        return {
            "registrations": registrations_data,
            "users_count": users_count,
            "motos_count": motos_count,
            "manuals_count": manuals_count,
            "last_reg": last_reg_data,
        }