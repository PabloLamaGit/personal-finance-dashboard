"""Financial analytics and aggregation service."""

import pandas as pd


class FinancialAnalytics:
    """Computes financial metrics and aggregations from transaction data."""

    def __init__(self, df: pd.DataFrame) -> None:
        """Initializes the analytics engine with a transactions DataFrame."""
        self._df = df

    def is_empty(self) -> bool:
        """Returns True if the underlying DataFrame has no records."""
        return self._df.empty

    def get_kpis(self) -> dict:
        """Calculates headline financial KPIs (income, expenses, balance, savings rate)."""
        if self._df.empty:
            return {
                "total_income": 0.0,
                "total_expenses": 0.0,
                "balance": 0.0,
                "savings_rate": 0.0,
                "num_transactions": 0,
            }

        income_mask = self._df["amount"] > 0
        expense_mask = self._df["amount"] < 0

        total_income: float = float(self._df.loc[income_mask, "amount"].sum())
        total_expenses_raw: float = float(self._df.loc[expense_mask, "amount"].sum())
        balance: float = total_income + total_expenses_raw
        savings_rate: float = (balance / total_income * 100) if total_income > 0 else 0.0

        return {
            "total_income": total_income,
            "total_expenses": abs(total_expenses_raw),  # Positive for display
            "balance": balance,
            "savings_rate": savings_rate,
            "num_transactions": len(self._df),
        }

    def get_monthly_trends(self) -> pd.DataFrame:
        """Groups transactions by month and calculates net and cumulative balance."""
        if self._df.empty:
            return pd.DataFrame(
                columns=["month", "net_monthly", "cumulative_balance"]
            )

        df = self._df.copy()

        # Group by calendar month and aggregate net amounts
        df["month"] = df["date"].dt.to_period("M")

        monthly = (
            df.groupby("month")["amount"]
            .sum()
            .reset_index()
            .rename(columns={"amount": "net_monthly"})
            .sort_values("month")
        )

        # Calculate running cumulative balance over time
        monthly["cumulative_balance"] = monthly["net_monthly"].cumsum()
        monthly["month"] = monthly["month"].astype(str)

        return monthly

    def get_category_distribution(self) -> pd.DataFrame:
        """Aggregates total expenditure per category for expense transactions."""
        if self._df.empty:
            return pd.DataFrame(columns=["category", "total"])

        expenses = self._df[self._df["amount"] < 0].copy()
        expenses["amount"] = expenses["amount"].abs()

        # Aggregate spend totals grouped by expense category

        return (
            expenses.groupby("category")["amount"]
            .sum()
            .reset_index()
            .rename(columns={"amount": "total"})
            .sort_values("total", ascending=False)
        )

    def get_monthly_comparison(self) -> pd.DataFrame:
        """Aggregates income and expenses separately by month."""
        if self._df.empty:
            return pd.DataFrame(columns=["month", "type", "total"])

        df = self._df.copy()
        df["month"] = df["date"].dt.to_period("M").astype(str)
        df["type"] = df["amount"].apply(
            lambda x: "Income" if x > 0 else "Expenses"
        )
        df["amount_abs"] = df["amount"].abs()

        # Group by month and transaction type to compare aggregate flows

        return (
            df.groupby(["month", "type"])["amount_abs"]
            .sum()
            .reset_index()
            .rename(columns={"amount_abs": "total"})
            .sort_values(["month", "type"])
        )

    def get_recent_transactions(self, n: int = 20) -> pd.DataFrame:
        """Returns the n most recent transactions formatted for UI display."""
        if self._df.empty:
            return pd.DataFrame()

        df = self._df.head(n).copy()

        # Format dates and currency values for presentation

        df["date"] = df["date"].dt.strftime("%d/%m/%Y")
        df["amount"] = df["amount"].apply(
            lambda x: f"+{x:,.2f} €" if x > 0 else f"{x:,.2f} €"
        )

        return (
            df[["date", "category", "description", "amount"]]
            .rename(columns={
                "date": "Date",
                "category": "Category",
                "description": "Description",
                "amount": "Amount",
            })
        )
