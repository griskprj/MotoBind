from datetime import datetime, timedelta
from typing import Any, Dict, List

from sqlalchemy.orm import selectinload

from app.exceptions import ForbiddenError, NotFoundError
from app.models.manual import Manual
from app.models.motorcycle import Motorcycle
from app.models.user import User
from app.utils.calculate_freq_maintenance import calculate_maintenance_freq
from app.utils.calculate_maintenance_money import calculate_maintenance_money
from app.utils.check_maintenance_status import check_status
from app.utils.maintenance_nodes import gen_maintenance_nodes


class StatisticService:
    """Сервис для работы со статистикой"""

    @staticmethod
    def get_dashboard_data(user_id: int) -> Dict[str, Any]:
        """
        Получить данные для дашборда пользователя
        """
        user = User.query.options(
            selectinload(User.motorcycles).selectinload(
                Motorcycle.planned_maintenances
            ),
            selectinload(User.motorcycles).selectinload(Motorcycle.maintenances),
        ).get(user_id)

        if not user:
            raise NotFoundError("Пользователь не найден")

        now = datetime.now()
        month_start = datetime(now.year, now.month, 1)
        prev_month_start = (month_start - timedelta(days=1)).replace(day=1)

        stats = {
            "motorcycles_count": 0,
            "plan_maintenances_count": 0,
            "maintenances_count": 0,
            "total_spends": 0,
            "new_motorcycles_count": 0,
            "month_maintenances_count": 0,
            "spends_change_percent": 0.0,
        }

        motorcycle_data = []
        all_planned_maintenances = []
        current_month_spends = 0
        previous_month_spends = 0

        for motorcycle in user.motorcycles[:3]:
            if motorcycle.created_at and motorcycle.created_at >= month_start:
                stats["new_motorcycles_count"] += 1

            planned_records = []
            for plan in motorcycle.planned_maintenances[:3]:
                status = check_status(plan, motorcycle)
                plan_data = plan.to_dict()
                plan_data["status"] = status
                planned_records.append(plan_data)
                stats["plan_maintenances_count"] += 1

            recent_maintenances = sorted(
                motorcycle.maintenances,
                key=lambda x: x.date if x.date else datetime.min,
                reverse=True,
            )[:3]

            for maintenance in recent_maintenances:
                if maintenance.cost:
                    stats["total_spends"] += maintenance.cost
                    stats["maintenances_count"] += 1

                    if maintenance.date:
                        if maintenance.date >= month_start:
                            current_month_spends += maintenance.cost
                            stats["month_maintenances_count"] += 1
                        elif prev_month_start <= maintenance.date < month_start:
                            previous_month_spends += maintenance.cost

            moto_dict = motorcycle.to_dict()
            moto_dict["planned_maintenances"] = planned_records
            moto_dict["recent_maintenances"] = [
                m.to_dict() for m in recent_maintenances
            ]
            motorcycle_data.append(moto_dict)
            all_planned_maintenances.extend(planned_records)

        stats["spends_change_percent"] = StatisticService._calculate_change_percent(
            current_month_spends, previous_month_spends
        )
        stats["motorcycles_count"] = len(user.motorcycles)

        all_planned_maintenances.sort(
            key=lambda x: {"overdue": 0, "soon": 1, "ok": 2}.get(
                x.get("status", "ok"), 3
            )
        )
        all_planned_maintenances = all_planned_maintenances[:3]

        return {
            "user": user.to_dict(),
            "motorcycles": motorcycle_data,
            "maintenance": all_planned_maintenances,
            **stats,
        }

    @staticmethod
    def get_dashboard_charts(user_id: int) -> Dict[str, List[Dict]]:
        """
        Получить данные для графиков дашборда
        """
        user = User.query.options(
            selectinload(User.motorcycles).selectinload(Motorcycle.maintenances)
        ).get(user_id)

        if not user:
            raise NotFoundError("Пользователь не найден")

        now = datetime.now()
        cost_data = []
        count_data = []
        month_names = [
            "Янв",
            "Фев",
            "Мар",
            "Апр",
            "Май",
            "Июн",
            "Июл",
            "Авг",
            "Сен",
            "Окт",
            "Ноя",
            "Дек",
        ]

        for i in range(11, -1, -1):
            month_date = now.replace(day=1) - timedelta(days=i * 30)
            month_start = datetime(month_date.year, month_date.month, 1)

            if month_date.month == 12:
                month_end = datetime(month_date.year + 1, 1, 1)
            else:
                month_end = datetime(month_date.year, month_date.month + 1, 1)

            month_cost = 0
            month_count = 0

            for motorcycle in user.motorcycles:
                for maintenance in motorcycle.maintenances:
                    if maintenance.date and month_start <= maintenance.date < month_end:
                        if maintenance.cost:
                            month_cost += maintenance.cost
                        month_count += 1

            month_label = f"{month_names[month_date.month - 1]} {month_date.year}"

            cost_data.append({"month": month_label, "value": month_cost})

            count_data.append({"month": month_label, "value": month_count})

        return {"cost_chart": cost_data, "count_chart": count_data}

    @staticmethod
    def get_garage_stats(user_id: int) -> Dict[str, Any]:
        """
        Получить данные для гаража
        """
        user = User.query.options(
            selectinload(User.motorcycles).selectinload(
                Motorcycle.planned_maintenances
            ),
            selectinload(User.motorcycles).selectinload(Motorcycle.maintenances),
        ).get(user_id)

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

        planned_maintenances = []
        maintenances = []
        moto_data = []
        cost = 0

        for m in motorcycles:
            moto_data.append({"id": m.id, "name": m.name})
            planned_maintenances.extend(m.planned_maintenances)
            maintenances.extend(m.maintenances)
            for maintenance in m.maintenances:
                if maintenance.cost:
                    cost += maintenance.cost

        return {
            "motorcycles": moto_data,
            "cost": cost,
            "plan_maintenances_count": len(planned_maintenances),
            "maintenances_count": len(maintenances),
        }

    @staticmethod
    def get_moto_garage_stats(moto_id: int, user_id: int) -> Dict[str, Any]:
        """
        Получить детальную статистику по мотоциклу для гаража
        """
        moto = Motorcycle.query.options(
            selectinload(Motorcycle.planned_maintenances),
            selectinload(Motorcycle.maintenances),
        ).get(moto_id)

        user = User.query.get(user_id)

        if not moto:
            raise NotFoundError("Мотоцикл не найден")
        if not user:
            raise NotFoundError("Пользователь не найден")
        if int(moto.owner_id) != int(user.id):
            raise ForbiddenError("Вы не являетесь владельцем этого мотоцикла")

        planned_maintenances = sorted(
            moto.planned_maintenances,
            key=lambda x: x.planned_mileage if x.planned_mileage else 0,
            reverse=False,
        )[:5]

        recent_maintenances = sorted(
            moto.maintenances,
            key=lambda x: x.date if x.date else datetime.min,
            reverse=True,
        )[:5]

        nodes = gen_maintenance_nodes(moto_id, user.id)
        nodes = nodes[:5] if nodes else []

        cost_data = calculate_maintenance_money(moto_id, user.id)
        cost_data["chart_data"] = cost_data.get("chart_data", [])[:5]

        freq_data = calculate_maintenance_freq(moto_id, user.id)
        freq_data["chart_data"] = freq_data.get("chart_data", [])[:5]

        return {
            "motorcycle": moto.to_dict(),
            "planned_maintenances": [m.to_dict() for m in planned_maintenances],
            "recent_maintenances": [m.to_dict() for m in recent_maintenances],
            "nodes": nodes,
            "total_cost": cost_data.get("total_cost", 0),
            "max_cost": cost_data.get("max_cost", 0),
            "average_cost": cost_data.get("average_cost", 0),
            "month_cost": cost_data.get("month_cost", 0),
            "money_chart_data": cost_data.get("chart_data", []),
            "total_maintenances": freq_data.get("total_maintenances", 0),
            "month_maintenances": freq_data.get("month_maintenances", 0),
            "freq_chart_data": freq_data.get("chart_data", []),
        }

    @staticmethod
    def get_repair_stats(user_id: int) -> Dict[str, Any]:
        """
        Получить статистику для страницы ремонта
        """
        user = User.query.options(
            selectinload(User.motorcycles).selectinload(Motorcycle.planned_maintenances)
        ).get(user_id)

        if not user:
            raise NotFoundError("Пользователь не найден")

        overdue = 0
        soon = 0
        planned = 0
        motorcycles = []
        maintenances = []

        for moto in user.motorcycles:
            for plan in moto.planned_maintenances:
                status = check_status(plan, moto)

                if status == "ok":
                    planned += 1
                elif status == "overdue":
                    overdue += 1
                elif status == "soon":
                    soon += 1

                maintenances.append(plan.to_dict())

            motorcycles.append(moto.to_dict())

        return {
            "overdue": overdue,
            "soon": soon,
            "planned": planned,
            "motorcycles": motorcycles,
            "maintenances": maintenances,
        }

    @staticmethod
    def get_maintenance_stats(user_id: int) -> Dict[str, Any]:
        """
        Получить статистику для страницы обслуживания
        """
        motorcycles = (
            Motorcycle.query.filter_by(owner_id=user_id)
            .options(
                selectinload(Motorcycle.maintenances),
                selectinload(Motorcycle.planned_maintenances),
            )
            .all()
        )

        history_maintenances = []
        planned_maintenances = []
        planned_maintenance_count = 0
        overdue_maintenance_count = 0

        for motorcycle in motorcycles:
            for maintenance in motorcycle.maintenances:
                maintenance = maintenance.to_dict()
                maintenance["moto_name"] = motorcycle.name
                history_maintenances.append(maintenance)

            for maintenance in motorcycle.planned_maintenances:
                status = check_status(maintenance, motorcycle)
                maintenance_dict = maintenance.to_dict()
                maintenance_dict["moto_name"] = motorcycle.name
                maintenance_dict["status"] = status
                planned_maintenances.append(maintenance_dict)

                if status == "overdue":
                    overdue_maintenance_count += 1
                elif status == "ok" or status == "soon":
                    planned_maintenance_count += 1

        all_maintenances_count = len(history_maintenances) + len(planned_maintenances)

        return {
            "motorcycles": [m.to_dict() for m in motorcycles],
            "history_maintenances": history_maintenances,
            "planned_maintenances": planned_maintenances,
            "all_maintenances_count": all_maintenances_count,
            "planned_maintenances_count": planned_maintenance_count,
            "overdue_maintenances_count": overdue_maintenance_count,
        }

    @staticmethod
    def get_registrations_chart(user_id: int) -> Dict[str, Any]:
        """
        Получить данные для графика регистраций (только для админа)
        """
        user = User.query.get(user_id)
        if not user or user.role != "admin":
            raise ForbiddenError("Доступ запрещен. Требуются права администратора")

        now = datetime.now()
        registrations_data = []
        month_names = [
            "Янв",
            "Фев",
            "Мар",
            "Апр",
            "Май",
            "Июн",
            "Июл",
            "Авг",
            "Сен",
            "Окт",
            "Ноя",
            "Дек",
        ]

        for i in range(11, -1, -1):
            month_date = now.replace(day=1) - timedelta(days=i * 30)
            month_start = datetime(month_date.year, month_date.month, 1)

            if month_date.month == 12:
                month_end = datetime(month_date.year + 1, 1, 1)
            else:
                month_end = datetime(month_date.year, month_date.month + 1, 1)

            count = User.query.filter(
                User.created_at >= month_start, User.created_at < month_end
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

    @staticmethod
    def _calculate_change_percent(current: float, previous: float) -> float:
        """Вычисляет процент изменения расходов"""
        if previous > 0:
            return round(((current - previous) / previous) * 100, 1)
        elif current > 0:
            return 100.0
        return 0.0
