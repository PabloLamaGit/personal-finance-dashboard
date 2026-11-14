"""Synthetic financial transaction generator."""

import random
from datetime import date, timedelta

from faker import Faker

from src.data.database import DatabaseManager


class DataSeeder:
    """Generates and persists synthetic financial transaction history."""

    _EXPENSE_CATEGORIES: list = [
        {
            "label": "Supermercado",
            "amount_range": (-120.0, -15.0),
            "weight": 25,
            "descriptions": ["Compra semanal", "Mercadona", "Lidl", "Carrefour", "Compra mensual"],
        },
        {
            "label": "Restaurantes",
            "amount_range": (-60.0, -8.0),
            "weight": 15,
            "descriptions": ["Cena con amigos", "Almuerzo trabajo", "Kebab", "Menú del día"],
        },
        {
            "label": "Transporte",
            "amount_range": (-80.0, -5.0),
            "weight": 12,
            "descriptions": ["Gasolina", "Abono transporte", "Taxi", "Parking", "Peaje autopista"],
        },
        {
            "label": "Ocio",
            "amount_range": (-150.0, -10.0),
            "weight": 10,
            "descriptions": ["Cine", "Concierto", "Spotify", "Netflix", "Videojuegos"],
        },
        {
            "label": "Salud",
            "amount_range": (-200.0, -10.0),
            "weight": 6,
            "descriptions": ["Farmacia", "Médico privado", "Dentista", "Seguro médico"],
        },
        {
            "label": "Ropa",
            "amount_range": (-200.0, -20.0),
            "weight": 6,
            "descriptions": ["Zara", "H&M", "Zapatillas", "Ropa de temporada"],
        },
        {
            "label": "Hogar",
            "amount_range": (-300.0, -30.0),
            "weight": 5,
            "descriptions": ["Alquiler", "IKEA", "Internet + Móvil", "Electricidad"],
        },
        {
            "label": "Educación",
            "amount_range": (-500.0, -50.0),
            "weight": 3,
            "descriptions": ["Matrícula", "Libro de texto", "Curso online", "Material universitario"],
        },
        {
            "label": "Viajes",
            "amount_range": (-800.0, -100.0),
            "weight": 3,
            "descriptions": ["Vuelo", "Hotel", "Airbnb", "Vacaciones de verano"],
        },
    ]

    _INCOME_CATEGORIES: list = [
        {
            "label": "Freelance",
            "amount_range": (200.0, 1_200.0),
            "weight": 20,
            "descriptions": ["Proyecto freelance", "Consultoría", "Factura cliente"],
        },
        {
            "label": "Otros Ingresos",
            "amount_range": (50.0, 500.0),
            "weight": 10,
            "descriptions": ["Venta segunda mano", "Dividendo", "Reembolso seguro", "Regalo"],
        },
    ]

    def __init__(self, db_manager: DatabaseManager) -> None:
        """Initializes the seeder with an injected database manager."""
        self._db = db_manager
        self._fake = Faker("es_ES")

    def _pick_weighted(self, categories: list) -> dict:
        """Randomly selects a category proportional to its configured weight."""
        weights = [cat["weight"] for cat in categories]
        return random.choices(categories, weights=weights, k=1)[0]

    def _build_transaction(self, tx_date: date) -> tuple:
        """Generates a synthetic transaction tuple for a given date."""
        is_expense = random.random() < 0.85

        category = (
            self._pick_weighted(self._EXPENSE_CATEGORIES)
            if is_expense
            else self._pick_weighted(self._INCOME_CATEGORIES)
        )

        amount = round(random.uniform(*category["amount_range"]), 2)
        description = random.choice(category["descriptions"])

        return (tx_date.strftime("%Y-%m-%d"), amount, category["label"], description)

    def _build_monthly_salaries(self, start: date, end: date) -> list:
        """Generates monthly salary credits on the 28th between start and end dates."""
        salaries = []
        current = start.replace(day=1)

        while current <= end:
            payday = current.replace(day=28)
            if payday <= end:
                amount = round(random.uniform(1_600.0, 2_200.0), 2)
                salaries.append((
                    payday.strftime("%Y-%m-%d"),
                    amount,
                    "Nómina",
                    "Nómina mensual",
                ))
            # Advance to the first day of the next month
            if current.month == 12:
                current = current.replace(year=current.year + 1, month=1)
            else:
                current = current.replace(month=current.month + 1)

        return salaries

    def seed(self, num_transactions: int = 500) -> int:
        """Generates and persists synthetic transactions for the last two years."""
        today = date.today()
        two_years_ago = today - timedelta(days=730)

        records: list = []

        for _ in range(num_transactions):
            offset = random.randint(0, 730)
            tx_date = two_years_ago + timedelta(days=offset)
            if tx_date <= today:
                records.append(self._build_transaction(tx_date))

        records.extend(self._build_monthly_salaries(two_years_ago, today))
        self._db.insert_many(records)

        return len(records)
