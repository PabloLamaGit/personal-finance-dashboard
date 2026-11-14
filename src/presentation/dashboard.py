"""Streamlit dashboard presentation layer."""

import streamlit as st

from src.data.database import DatabaseManager
from src.data.seeder import DataSeeder
from src.presentation.charts import ChartFactory
from src.services.analytics import FinancialAnalytics


class DashboardApp:
    """Coordinates and renders the Streamlit financial dashboard interface."""

    def __init__(
        self,
        db_manager: DatabaseManager,
        seeder: DataSeeder,
        analytics: FinancialAnalytics,
    ) -> None:
        """Initializes the dashboard with database, seeder, and analytics instances."""
        self._db = db_manager
        self._seeder = seeder
        self._analytics = analytics

    def run(self) -> None:
        """Executes the main dashboard rendering pipeline."""
        self._inject_css()
        self._render_sidebar()
        self._render_header()

        if self._analytics.is_empty():
            self._render_empty_state()
            st.stop()
            return

        self._render_kpis()
        st.markdown("<br>", unsafe_allow_html=True)
        self._render_interactive_charts()
        st.markdown("<br>", unsafe_allow_html=True)
        self._render_transactions_table()
        self._render_footer()

    def _inject_css(self) -> None:
        """Injects custom CSS styling for dashboard components."""
        st.markdown(
            """
            <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

            /* ── Global typography ── */
            html, body, [class*="css"] {
                font-family: 'Inter', -apple-system, BlinkMacSystemFont,
                             'Segoe UI', Roboto, sans-serif;
            }

            /* ── Remove Streamlit chrome ── */
            #MainMenu, footer, .stDeployButton { visibility: hidden; }

            /* ── Main content area ── */
            .main .block-container {
                padding-top: 1.75rem;
                padding-bottom: 2.5rem;
                max-width: 1440px;
            }

            /* ── Sidebar typography and borders ── */
            [data-testid="stSidebar"] hr {
                border-color: rgba(255, 255, 255, 0.08) !important;
                margin: 1rem 0 !important;
            }
            [data-testid="stSidebar"] label,
            [data-testid="stSidebar"] label p,
            label,
            label p {
                color: #CBD5E1 !important;
                font-size: 0.8rem !important;
                font-weight: 500 !important;
            }

            /* ── Inputs: clear crisp light text on dark background ── */
            [data-testid="stSidebar"] input,
            [data-testid="stSidebar"] textarea,
            [data-testid="stSidebar"] [data-testid="stNumberInput"] input,
            [data-testid="stSidebar"] [data-testid="stTextInput"] input,
            [data-testid="stSidebar"] [data-testid="stDateInput"] input,
            [data-testid="stSidebar"] [data-baseweb="input"] input,
            [data-testid="stSidebar"] [data-baseweb="base-input"] input,
            input,
            textarea {
                background-color: #0A1128 !important;
                background: #0A1128 !important;
                color: #F8FAFC !important;
                -webkit-text-fill-color: #F8FAFC !important;
                caret-color: #00D2A0 !important;
                font-weight: 500 !important;
                font-size: 0.875rem !important;
                border-radius: 6px !important;
            }
            [data-testid="stSidebar"] [data-baseweb="input"],
            [data-testid="stSidebar"] [data-baseweb="base-input"],
            [data-testid="stSidebar"] [data-testid="stNumberInput"] > div,
            [data-testid="stSidebar"] [data-testid="stTextInput"] > div,
            [data-baseweb="input"],
            [data-baseweb="base-input"] {
                background-color: #0A1128 !important;
                background: #0A1128 !important;
                border: 1px solid rgba(255, 255, 255, 0.16) !important;
                border-radius: 6px !important;
            }
            [data-testid="stSidebar"] [data-baseweb="input"]:focus-within,
            [data-testid="stSidebar"] [data-baseweb="base-input"]:focus-within,
            [data-baseweb="input"]:focus-within {
                border-color: #00D2A0 !important;
                box-shadow: 0 0 0 1px #00D2A0 !important;
            }
            input::placeholder,
            textarea::placeholder,
            input::-webkit-input-placeholder,
            textarea::-webkit-input-placeholder {
                color: #64748B !important;
                -webkit-text-fill-color: #64748B !important;
                opacity: 1 !important;
                font-weight: 400 !important;
            }
            [data-testid="stSidebar"] [data-testid="stNumberInput"] button,
            [data-testid="stSidebar"] [data-testid="stNumberInput"] button * {
                color: #F8FAFC !important;
                fill: #F8FAFC !important;
                -webkit-text-fill-color: #F8FAFC !important;
            }
            [data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"],
            [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] {
                background-color: #0A1128 !important;
                background: #0A1128 !important;
                border: 1px solid rgba(255, 255, 255, 0.16) !important;
                border-radius: 6px !important;
            }
            [data-testid="stSidebar"] [data-testid="stSelectbox"] [data-baseweb="select"] *,
            [data-testid="stSidebar"] .stSelectbox [data-baseweb="select"] * {
                color: #F8FAFC !important;
                -webkit-text-fill-color: #F8FAFC !important;
                font-weight: 500 !important;
            }
            [data-testid="stSidebar"] [data-testid="stDateInput"] [data-baseweb="input"] {
                background-color: #0A1128 !important;
                background: #0A1128 !important;
                border-radius: 6px !important;
            }

            /* ── KPI Metric Cards ── */
            [data-testid="metric-container"] {
                background: #101F42 !important;
                border: 1px solid rgba(255, 255, 255, 0.08) !important;
                border-radius: 12px;
                padding: 1.25rem 1.5rem;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.25);
                transition: box-shadow 0.2s ease, transform 0.2s ease;
            }
            [data-testid="metric-container"]:hover {
                box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
                transform: translateY(-2px);
                border-color: rgba(0, 210, 160, 0.35) !important;
            }
            [data-testid="stMetricLabel"] > div,
            [data-testid="stMetricLabel"] p {
                font-size: 0.7rem !important;
                font-weight: 700 !important;
                letter-spacing: 0.07em !important;
                text-transform: uppercase !important;
                color: #94A3B8 !important;
            }
            [data-testid="stMetricValue"],
            [data-testid="stMetricValue"] div {
                font-size: 1.7rem !important;
                font-weight: 700 !important;
                color: #F8FAFC !important;
                letter-spacing: -0.5px !important;
            }

            /* ── Section labels ── */
            .fin-section-label {
                font-size: 0.68rem;
                font-weight: 700;
                letter-spacing: 0.1em;
                text-transform: uppercase;
                color: #94A3B8;
                margin-bottom: 0.85rem;
                padding-bottom: 0.6rem;
                border-bottom: 1px solid rgba(255, 255, 255, 0.08);
            }

            /* ── Tabs ── */
            .stTabs [data-baseweb="tab-list"] {
                gap: 0;
                border-bottom: 1px solid rgba(255, 255, 255, 0.1);
                background: transparent;
                margin-bottom: 1rem;
            }
            .stTabs [data-baseweb="tab"] {
                font-size: 0.83rem;
                font-weight: 500;
                color: #94A3B8;
                padding: 0.6rem 1.2rem;
                border-radius: 0;
                border-bottom: 2px solid transparent;
                margin-bottom: -1px;
                background: transparent;
                letter-spacing: 0.01em;
            }
            .stTabs [aria-selected="true"] {
                color: #F8FAFC !important;
                border-bottom: 2px solid #00D2A0 !important;
                font-weight: 600 !important;
                background: transparent !important;
            }

            /* ── Data table ── */
            [data-testid="stDataFrame"] {
                border: 1px solid rgba(255, 255, 255, 0.08);
                border-radius: 12px;
                overflow: hidden;
            }

            /* ── Buttons ── */
            .stButton > button {
                border-radius: 8px;
                font-weight: 600;
                font-size: 0.83rem;
                letter-spacing: 0.02em;
                padding: 0.55rem 1rem;
                transition: all 0.2s ease;
            }

            /* Primary button */
            [data-testid="stSidebar"] button[data-testid="baseButton-primary"],
            [data-testid="stSidebar"] button[kind="primary"],
            [data-testid="stSidebar"] div.stButton > button,
            [data-testid="stSidebar"] div[class*="st-key-btn_seed"] button,
            button[data-testid="baseButton-primary"] {
                background-color: #00D2A0 !important;
                background: #00D2A0 !important;
                border: none !important;
                color: #0A1128 !important;
                -webkit-text-fill-color: #0A1128 !important;
                font-weight: 700 !important;
                box-shadow: 0 2px 8px rgba(0, 210, 160, 0.3) !important;
            }
            [data-testid="stSidebar"] button[data-testid="baseButton-primary"] *,
            [data-testid="stSidebar"] button[data-testid="baseButton-primary"] p,
            [data-testid="stSidebar"] button[kind="primary"] *,
            [data-testid="stSidebar"] button[kind="primary"] p,
            [data-testid="stSidebar"] div.stButton > button *,
            [data-testid="stSidebar"] div.stButton > button p,
            [data-testid="stSidebar"] div[class*="st-key-btn_seed"] button *,
            [data-testid="stSidebar"] div[class*="st-key-btn_seed"] button p,
            button[data-testid="baseButton-primary"] *,
            button[data-testid="baseButton-primary"] p {
                color: #0A1128 !important;
                -webkit-text-fill-color: #0A1128 !important;
                font-weight: 700 !important;
                font-size: 0.875rem !important;
            }
            [data-testid="stSidebar"] button[data-testid="baseButton-primary"]:hover,
            [data-testid="stSidebar"] div.stButton > button:hover,
            [data-testid="stSidebar"] div[class*="st-key-btn_seed"] button:hover {
                background-color: #00B88C !important;
                background: #00B88C !important;
                transform: translateY(-1px);
                box-shadow: 0 4px 14px rgba(0, 210, 160, 0.45) !important;
            }

            /* Secondary / Form submit button */
            [data-testid="stSidebar"] div[data-testid="stFormSubmitButton"] button,
            [data-testid="stSidebar"] button[data-testid="baseButton-secondary"],
            [data-testid="stSidebar"] button[kind="secondary"],
            div[data-testid="stFormSubmitButton"] button,
            button[data-testid="baseButton-secondary"] {
                background-color: rgba(255, 255, 255, 0.08) !important;
                background: rgba(255, 255, 255, 0.08) !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                color: #F8FAFC !important;
                -webkit-text-fill-color: #F8FAFC !important;
                box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2) !important;
            }
            [data-testid="stSidebar"] div[data-testid="stFormSubmitButton"] button *,
            [data-testid="stSidebar"] div[data-testid="stFormSubmitButton"] button p,
            [data-testid="stSidebar"] button[data-testid="baseButton-secondary"] *,
            [data-testid="stSidebar"] button[data-testid="baseButton-secondary"] p,
            [data-testid="stSidebar"] button[kind="secondary"] *,
            [data-testid="stSidebar"] button[kind="secondary"] p,
            div[data-testid="stFormSubmitButton"] button *,
            div[data-testid="stFormSubmitButton"] button p {
                color: #F8FAFC !important;
                -webkit-text-fill-color: #F8FAFC !important;
                font-weight: 600 !important;
                font-size: 0.875rem !important;
            }
            [data-testid="stSidebar"] div[data-testid="stFormSubmitButton"] button:hover,
            [data-testid="stSidebar"] button[data-testid="baseButton-secondary"]:hover,
            [data-testid="stSidebar"] button[kind="secondary"]:hover,
            div[data-testid="stFormSubmitButton"] button:hover {
                background-color: rgba(0, 210, 160, 0.15) !important;
                background: rgba(0, 210, 160, 0.15) !important;
                border-color: #00D2A0 !important;
                transform: translateY(-1px);
                box-shadow: 0 3px 10px rgba(0, 210, 160, 0.2) !important;
            }
            [data-testid="stSidebar"] div[data-testid="stFormSubmitButton"] button:hover *,
            [data-testid="stSidebar"] div[data-testid="stFormSubmitButton"] button:hover p,
            div[data-testid="stFormSubmitButton"] button:hover *,
            div[data-testid="stFormSubmitButton"] button:hover p {
                color: #00D2A0 !important;
                -webkit-text-fill-color: #00D2A0 !important;
            }

            /* ── Alerts ── */
            .stAlert {
                border-radius: 10px;
                font-size: 0.875rem;
            }
            [data-testid="stSidebar"] .stAlert {
                background: rgba(0, 210, 160, 0.1) !important;
                border: 1px solid rgba(0, 210, 160, 0.25) !important;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

    def _render_sidebar(self) -> None:
        """Renders the sidebar controls for data management and manual transaction entry."""
        with st.sidebar:
            st.markdown(
                "<h2 style='margin:0 0 0.1rem; letter-spacing:-0.5px; "
                "color:#F1F5F9 !important;'>FinDash</h2>"
                "<p style='font-size:0.75rem; margin:0 0 1rem; "
                "color:#64748B !important;'>Personal Finance Analytics</p>",
                unsafe_allow_html=True,
            )
            st.markdown("---")

            st.markdown(
                "<p style='font-size:0.65rem; font-weight:700; "
                "letter-spacing:0.1em; text-transform:uppercase; "
                "color:#64748B !important; margin-bottom:0.5rem;'>"
                "Data Management</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                "<p style='font-size:0.78rem; line-height:1.6; "
                "color:#94A3B8 !important; margin-bottom:0.75rem;'>"
                "Populate the database with 2 years of synthetic "
                "transactions to explore the dashboard.</p>",
                unsafe_allow_html=True,
            )

            if st.button(
                "Generate Test Data",
                use_container_width=True,
                type="primary",
                key="btn_seed",
            ):
                with st.spinner("Generating records..."):
                    self._db.clear_database()
                    total = self._seeder.seed(num_transactions=500)
                st.success(f"{total:,} records inserted.")
                st.rerun()

            st.markdown("---")

            st.markdown(
                "<p style='font-size:0.65rem; font-weight:700; "
                "letter-spacing:0.1em; text-transform:uppercase; "
                "color:#64748B !important; margin-bottom:0.5rem;'>"
                "Add Transaction</p>",
                unsafe_allow_html=True,
            )

            with st.form("form_transaction", clear_on_submit=True):
                f_date = st.date_input("Date")
                f_description = st.text_input(
                    "Description",
                    placeholder="e.g. Weekly grocery run",
                )
                f_category = st.selectbox(
                    "Category",
                    options=[
                        "Supermercado", "Restaurantes", "Transporte",
                        "Ocio", "Salud", "Ropa", "Hogar", "Educación",
                        "Viajes", "Nómina", "Freelance", "Otros Ingresos",
                    ],
                )
                f_amount = st.number_input(
                    "Amount (€)",
                    step=0.01,
                    format="%.2f",
                    help="Negative values indicate expenses (e.g. -45.00).",
                )
                submitted = st.form_submit_button(
                    "Save Transaction",
                    use_container_width=True,
                )

                if submitted:
                    if f_description.strip() and f_amount != 0.0:
                        self._db.insert_transaction(
                            date=f_date.strftime("%Y-%m-%d"),
                            amount=float(f_amount),
                            category=f_category,
                            description=f_description.strip(),
                        )
                        st.success("Transaction saved.")
                        st.rerun()
                    else:
                        st.error("Provide a description and non-zero amount.")

    def _render_header(self) -> None:
        """Renders the main page title and contextual subtitle."""
        st.markdown(
            "<h1 style='font-size:1.8rem; font-weight:700; color:#F8FAFC; "
            "letter-spacing:-0.5px; margin-bottom:0.15rem;'>"
            "Financial Overview</h1>"
            "<p style='color:#94A3B8; font-size:0.875rem; margin-top:0;'>"
            "Personal finance analytics — last 24 months</p>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<hr style='border:none; border-top:1px solid rgba(255,255,255,0.08); "
            "margin:0.75rem 0 1.5rem;'>",
            unsafe_allow_html=True,
        )

    def _render_empty_state(self) -> None:
        """Renders an informational notice when no transactions exist in the database."""
        st.info(
            "The database is currently empty. "
            "Click **Generate Test Data** in the sidebar to populate it "
            "with 500+ realistic transactions, or add entries manually.",
        )

    def _render_kpis(self) -> None:
        """Renders headline metric cards for income, expenses, balance, and savings rate."""
        kpis = self._analytics.get_kpis()

        st.markdown(
            "<p class='fin-section-label'>Executive Summary</p>",
            unsafe_allow_html=True,
        )

        col1, col2, col3, col4 = st.columns(4, gap="medium")

        with col1:
            st.metric(
                label="Total Income",
                value=f"€ {kpis['total_income']:,.2f}",
            )
        with col2:
            st.metric(
                label="Total Expenses",
                value=f"€ {kpis['total_expenses']:,.2f}",
            )
        with col3:
            balance = kpis["balance"]
            st.metric(
                label="Net Balance",
                value=f"€ {balance:,.2f}",
                delta=f"€ {balance:,.2f}",
            )
        with col4:
            rate = kpis["savings_rate"]
            st.metric(
                label="Savings Rate",
                value=f"{rate:.1f}%",
                delta=f"{rate:.1f}% of gross income",
            )

    def _render_interactive_charts(self) -> None:
        """Renders analytical charts inside interactive tabs."""
        st.markdown(
            "<p class='fin-section-label'>Analytics</p>",
            unsafe_allow_html=True,
        )

        tab_trend, tab_donut, tab_comparison = st.tabs([
            "Balance Trend",
            "Category Breakdown",
            "Monthly Comparison",
        ])

        with tab_trend:
            monthly_df = self._analytics.get_monthly_trends()
            fig = ChartFactory.create_balance_trend(monthly_df)
            st.plotly_chart(fig, use_container_width=True)

        with tab_donut:
            cat_df = self._analytics.get_category_distribution()
            fig = ChartFactory.create_category_donut(cat_df)
            st.plotly_chart(fig, use_container_width=True)

        with tab_comparison:
            comp_df = self._analytics.get_monthly_comparison()
            fig = ChartFactory.create_monthly_comparison(comp_df)
            st.plotly_chart(fig, use_container_width=True)

    def _render_transactions_table(self) -> None:
        """Renders the table containing recent transactions."""
        st.markdown(
            "<p class='fin-section-label'>Recent Transactions</p>",
            unsafe_allow_html=True,
        )

        df_display = self._analytics.get_recent_transactions(n=20)
        st.dataframe(df_display, use_container_width=True, hide_index=True)

    def _render_footer(self) -> None:
        """Renders a minimal bottom footer with stack credits."""
        st.markdown(
            "<hr style='border:none; border-top:1px solid rgba(255, 255, 255, 0.08); margin:2rem 0 1rem;'>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align:center; font-size:0.7rem; color:#CBD5E1; "
            "letter-spacing:0.02em;'>"
            "FinDash &nbsp;·&nbsp; Personal Finance Dashboard &nbsp;·&nbsp; "
            "Python &nbsp;·&nbsp; Streamlit &nbsp;·&nbsp; SQLite3 &nbsp;·&nbsp; "
            "Pandas &nbsp;·&nbsp; Plotly</p>",
            unsafe_allow_html=True,
        )
