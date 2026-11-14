"""Factory creating styled Plotly figures for financial metrics."""

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


class ChartFactory:
    """Stateless factory creating configured Plotly charts with a unified style."""

    _ACCENT: str = "#00D2A0"
    _POSITIVE: str = "#43A047"
    _NEGATIVE: str = "#EF5350"

    _PALETTE: list = [
        "#00D2A0", "#38BDF8", "#818CF8", "#A78BFA",
        "#F472B6", "#FB923C", "#FACC15", "#4ADE80",
        "#2DD4BF", "#94A3B8",
    ]

    _BASE_LAYOUT: dict = dict(
        font=dict(
            family="Inter, -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
            size=12,
            color="#F8FAFC",
        ),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=8, r=8, t=40, b=8),
        hoverlabel=dict(
            bgcolor="#101F42",
            font_color="#F8FAFC",
            font_size=12,
            bordercolor="#00D2A0",
        ),
    )

    @staticmethod
    def create_balance_trend(df: pd.DataFrame) -> go.Figure:
        """Creates an area-line chart showing cumulative balance over time."""
        fig = px.line(
            df,
            x="month",
            y="cumulative_balance",
            markers=True,
            labels={
                "month": "Month",
                "cumulative_balance": "Cumulative Balance (€)",
            },
            color_discrete_sequence=[ChartFactory._ACCENT],
            title="Cumulative Net Balance",
        )

        fig.update_traces(
            line=dict(width=2.5),
            marker=dict(
                size=6,
                line=dict(width=1.5, color="#FFFFFF"),
            ),
            fill="tozeroy",
            fillcolor="rgba(0,191,165,0.07)",
            hovertemplate="<b>%{x}</b><br>%{y:,.2f} €<extra></extra>",
        )

        fig.update_xaxes(
            tickangle=-40,
            showgrid=False,
            zeroline=False,
            linecolor="rgba(255, 255, 255, 0.15)",
            tickfont=dict(size=10, color="#94A3B8"),
        )
        fig.update_yaxes(
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.08)",
            zeroline=True,
            zerolinecolor="rgba(255, 255, 255, 0.2)",
            zerolinewidth=1.5,
            tickformat=",.0f",
            ticksuffix=" €",
            tickfont=dict(color="#94A3B8"),
        )

        fig.update_layout(**ChartFactory._BASE_LAYOUT, hovermode="x unified")
        return fig

    @staticmethod
    def create_category_donut(df: pd.DataFrame) -> go.Figure:
        """Creates a donut chart showing expense distribution by category."""
        fig = px.pie(
            df,
            values="total",
            names="category",
            hole=0.52,
            color_discrete_sequence=ChartFactory._PALETTE,
            title="Expense Breakdown by Category",
        )

        fig.update_traces(
            textposition="outside",
            textinfo="label+percent",
            hovertemplate=(
                "<b>%{label}</b><br>"
                "%{value:,.2f} €  ·  %{percent}<extra></extra>"
            ),
            marker=dict(line=dict(color="#0A1128", width=2)),
        )

        fig.update_layout(
            **ChartFactory._BASE_LAYOUT,
            showlegend=False,
        )
        return fig

    @staticmethod
    def create_monthly_comparison(df: pd.DataFrame) -> go.Figure:
        """Creates a grouped bar chart comparing monthly income versus expenses."""
        fig = px.bar(
            df,
            x="month",
            y="total",
            color="type",
            barmode="group",
            labels={
                "month": "Month",
                "total": "Amount (€)",
                "type": "",
            },
            color_discrete_map={
                "Income": ChartFactory._POSITIVE,
                "Expenses": ChartFactory._NEGATIVE,
            },
            title="Monthly Income vs Expenses",
        )

        fig.update_traces(
            marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>%{y:,.2f} €<extra></extra>",
        )

        fig.update_xaxes(
            tickangle=-40,
            showgrid=False,
            linecolor="rgba(255, 255, 255, 0.15)",
            tickfont=dict(size=10, color="#94A3B8"),
        )
        fig.update_yaxes(
            showgrid=True,
            gridcolor="rgba(255, 255, 255, 0.08)",
            zeroline=False,
            tickformat=",.0f",
            ticksuffix=" €",
            tickfont=dict(color="#94A3B8"),
        )

        fig.update_layout(
            **ChartFactory._BASE_LAYOUT,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1,
                title_text="",
                font=dict(size=12),
            ),
        )
        return fig
