"""Application entry point and dependency wiring."""

import streamlit as st

from src.data.database import DatabaseManager
from src.data.seeder import DataSeeder
from src.presentation.dashboard import DashboardApp
from src.services.analytics import FinancialAnalytics

st.set_page_config(
    page_title="FinDash · Personal Finance",
    page_icon="💹",
    layout="wide",
    initial_sidebar_state="expanded",
)

db_manager = DatabaseManager(db_path="finanzas.db")
db_manager.init_db()

df = db_manager.get_all_transactions()
analytics = FinancialAnalytics(df=df)

seeder = DataSeeder(db_manager=db_manager)

app = DashboardApp(db_manager=db_manager, seeder=seeder, analytics=analytics)
app.run()
