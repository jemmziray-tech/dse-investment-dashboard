# DSE Insight

## Intelligent Investment Analytics Platform for the Dar es Salaam Stock Exchange

DSE Insight is a data-driven investment intelligence platform designed to simplify stock market analysis by combining financial analytics, data visualization, and machine learning.

The platform collects, processes, and analyzes market and company financial data to help investors understand trends, evaluate company performance, compare investment opportunities, and make data-informed decisions.

The goal of this project is to transform raw stock market data into meaningful insights through automation, analytics, and artificial intelligence.

---

# Project Vision

Traditional stock analysis requires investors to manually collect financial reports, study historical trends, calculate valuation metrics, and compare companies.

DSE Insight aims to automate this process by creating a centralized intelligence system that provides:

- Real-time market monitoring
- Automated financial analysis
- Company performance evaluation
- Historical trend analysis
- Investment scoring
- Predictive analytics

---

# Key Features

## Market Overview Dashboard

Provides a high-level view of the Dar es Salaam Stock Exchange including:

- Market movements
- Top gainers and losers
- Trading volumes
- Market capitalization
- Sector performance

---

## Company Analysis

Analyze individual listed companies through:

- Historical share price trends
- Revenue growth
- Profitability analysis
- Dividend history
- Financial health indicators
- Valuation metrics

---

## Company Comparison

Compare multiple companies based on:

- Profit growth
- Revenue performance
- Dividend yield
- Risk indicators
- Valuation ratios

---

## Automated Data Pipeline

The system is designed to automatically:

1. Collect updated market data
2. Clean and transform raw information
3. Store historical records
4. Update analytical models
5. Refresh dashboard insights

---

## Machine Learning Intelligence

Future development includes machine learning models for:

- Revenue forecasting
- Financial trend prediction
- Company scoring
- Risk analysis
- Pattern detection

---

# Technology Stack

## Programming Language

- Python

## Data Processing

- Pandas
- NumPy

## Data Visualization

- Streamlit
- Plotly
- Matplotlib

## Database

- PostgreSQL
- SQL

## Machine Learning

- Scikit-learn

## Development Tools

- Git
- GitHub
- Visual Studio Code

---

# System Architecture

```
Data Sources
     |
     v
Data Collection Layer
     |
     v
Data Cleaning & Processing
     |
     v
Database Storage
     |
     v
Financial Analytics Engine
     |
     v
Machine Learning Models
     |
     v
Streamlit Interactive Dashboard
```

---

# Project Structure

```
dse-investment-dashboard/

├── app.py

├── data/
│   ├── raw/
│   ├── processed/
│   └── database/

├── scraper/
│   ├── scraper.py
│   ├── downloader.py
│   └── parser.py

├── preprocessing/
│   ├── clean_data.py
│   ├── transform.py
│   └── validation.py

├── database/
│   ├── database.py
│   └── models.py

├── analysis/
│   ├── financial_analysis.py
│   ├── indicators.py
│   └── statistics.py

├── ml/
│   ├── forecasting.py
│   ├── scoring.py
│   └── train_model.py

├── dashboard/
│   ├── home.py
│   ├── company.py
│   ├── comparison.py
│   ├── forecast.py
│   └── alerts.py

├── charts/
│   ├── line_chart.py
│   ├── bar_chart.py
│   └── candlestick.py

└── utils/
    ├── config.py
    ├── helper.py
    └── logger.py
```

---

# Development Roadmap

## Phase 1: Foundation

- [x] Project architecture setup
- [x] Git repository initialization
- [ ] Environment configuration
- [ ] Database setup

## Phase 2: Data Engineering

- [ ] Automated data collection
- [ ] Data cleaning pipeline
- [ ] Historical data storage

## Phase 3: Analytics Platform

- [ ] Financial ratio calculations
- [ ] Company comparison tools
- [ ] Interactive dashboards

## Phase 4: Machine Learning

- [ ] Forecasting models
- [ ] Investment scoring system
- [ ] Risk prediction models

## Phase 5: Deployment

- [ ] Cloud deployment
- [ ] Automated daily updates
- [ ] Monitoring system

---

# Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/dse-insight.git
```

Navigate into the project:

```bash
cd dse-investment-dashboard
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate the environment:

Windows:

```bash
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
streamlit run app.py
```

---

# Future Improvements

Planned improvements include:

- Live market data integration
- Mobile-friendly dashboard
- Portfolio tracking
- Automated investment reports
- News sentiment analysis
- AI-powered financial assistant

---

# Disclaimer

DSE Insight is an educational and research project designed to demonstrate financial analytics and machine learning applications.

It does not provide financial advice or guarantee investment returns. Investment decisions should always involve independent research and professional guidance.

---

# Author

John Elifuraha Mziray

Data Science | Artificial Intelligence | Machine Learning

GitHub:
https://github.com/jemmziray-tech

LinkedIn:
https://linkedin.com/in/john-mziray