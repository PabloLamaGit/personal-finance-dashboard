# FinDash — Personal Finance Analytics Dashboard

An interactive web application for personal finance tracking and visual analytics, built in Python using Object-Oriented Programming (OOP) and a clean layered architecture.

## Key Features

- **Executive KPIs:** Real-time calculation of Total Income, Total Expenses, Net Balance, and Savings Rate.
- **Interactive Data Visualization:** Tabbed navigation powered by Plotly to explore cumulative wealth evolution, expense distribution by category, and monthly income vs. expense comparisons.
- **Transaction Management:** Clean sidebar interface to log manual transactions or populate the database with 500 realistic synthetic records spanning two years.
- **Local Persistence:** Zero-configuration embedded SQLite3 database with automatic schema initialization.

## Tech Stack

- **Language:** Python 3.10+
- **Frontend & UI:** Streamlit
- **Data Processing:** Pandas (vectorized aggregations)
- **Visualization:** Plotly Express
- **Database:** SQLite3
- **Mock Data Generation:** Faker

## Architecture & Design Patterns

The codebase follows a strict **Layered / MVC Architecture** to separate data persistence, business logic, and UI rendering:

```text
dashboard_finanzas/
├── .streamlit/
│   └── config.toml             # Custom dark theme configuration
├── src/
│   ├── data/
│   │   ├── database.py         # DatabaseManager (SQLite CRUD & parameterized queries)
│   │   └── seeder.py           # DataSeeder (synthetic data generator)
│   ├── services/
│   │   └── analytics.py        # FinancialAnalytics (pure Pandas transformations)
│   └── presentation/
│       ├── charts.py           # ChartFactory (standardized Plotly figures)
│       └── dashboard.py        # DashboardApp (Streamlit UI orchestrator)
├── main.py                     # Application entry point
└── requirements.txt            # Project dependencies
```

- **Single Responsibility Principle (SRP):** `FinancialAnalytics` operates exclusively on Pandas DataFrames without importing UI or plotting libraries, making the core logic independently testable.
- **Factory Pattern:** `ChartFactory` centralizes chart styling, color palettes, and layout configurations.
- **Dependency Injection:** `DataSeeder` receives a `DatabaseManager` instance rather than instantiating connections directly.

## Getting Started

### 1. Clone the repository
```bash
git clone [https://github.com/YOUR_USERNAME/dashboard-finanzas.git](https://github.com/YOUR_USERNAME/dashboard-finanzas.git)
cd dashboard-finanzas
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# On Windows:
venv\Scripts\activate

# On macOS / Linux:
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the application
```bash
streamlit run main.py
```

Once the browser opens, click **Generate Test Data** in the sidebar to populate the local database and explore the dashboard.