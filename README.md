<div align="center">

# 🇹🇿 DSE Insight Dashboard
### Intelligent Investment Analytics & Predictive AI Platform

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-yellow.svg?style=for-the-badge&logo=javascript&logoColor=white)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![GitHub Actions](https://img.shields.io/badge/Automated-GitHub_Actions-2088FF.svg?style=for-the-badge&logo=github-actions&logoColor=white)](https://github.com/features/actions)
[![Scikit-Learn](https://img.shields.io/badge/AI-Scikit_Learn-F7931E.svg?style=for-the-badge&logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)](https://opensource.org/licenses/MIT)

**DSE Insight** is a premium, zero-cost, serverless web application that transforms raw data from the Dar es Salaam Stock Exchange (DSE) into a stunning, beginner-friendly analytics dashboard powered by Machine Learning.

[Explore the Live Dashboard](https://jemmziray-tech.github.io/dse-investment-dashboard) *(Insert your live URL here)*

---
</div>

## ✨ Key Features

- **🤖 AI Trend Predictor:** A Scikit-Learn Random Forest model analyzes historical momentum and trading volume to forecast the short-term trend (🟢 Bullish, 🔴 Bearish, ⚪ Neutral) for every listed company.
- **💎 Premium Glassmorphism UI:** A stunning, dark-themed, Tanzanian-inspired interface designed to rival professional Bloomberg terminals, built entirely in Vanilla HTML/CSS/JS.
- **🎓 Beginner-Friendly Tools:** Breaks down financial jargon with an interactive "Shares Calculator", simple "Market in Plain English" summaries, tooltips, and ⭐ Blue Chip badges to guide first-time investors.
- **🌍 Zero-Cost Serverless Automation:** The entire data pipeline (Scraping ➔ AI Inference ➔ Data Compilation ➔ Website Deployment) runs automatically every day using GitHub Actions and GitHub Pages. No servers, no databases, zero hosting costs.

---

## 🏗️ System Architecture

The project utilizes a highly efficient "Scraper-to-Static" architecture. It completely bypasses the need for an expensive backend server or database by generating a statically servable JavaScript data payload.

```mermaid
graph TD
    subgraph "1. Data Acquisition (Python)"
        A[DSE Website] -->|Requests / BeautifulSoup| B(scraper.py)
        B -->|Saves| C[data/raw/*.csv]
    end

    subgraph "2. Machine Learning Engine (Python)"
        C -->|Historical Data| D(ml_pipeline.py)
        D -->|Feature Engineering| E{Random Forest Model}
        E -->|Output| F[AI Trend Predictions]
    end

    subgraph "3. Data Bridge (Python)"
        C --> G(generate_data_js.py)
        F --> G
        G -->|Compiles & Formats| H[assets/js/data.js]
    end

    subgraph "4. Client-Side Application (HTML/JS)"
        H -->|Loads via <script>| I(index.html)
        I -->|Renders UI| J[DOM / CSS]
        I -->|Renders Charts| K[Chart.js]
    end

    subgraph "5. Cloud Automation (GitHub)"
        L((Daily Cron Job\n4:00 PM EAT)) -->|Triggers Action| A
        H -->|Auto-Commits| M[GitHub Repo]
        M -->|Deploys| N[GitHub Pages Live URL]
    end
    
    style A fill:#2d3748,stroke:#d4a843,stroke-width:2px,color:#fff
    style E fill:#00c896,stroke:#d4a843,stroke-width:2px,color:#fff
    style H fill:#3b82f6,stroke:#d4a843,stroke-width:2px,color:#fff
    style N fill:#e53e3e,stroke:#d4a843,stroke-width:2px,color:#fff
```

### Architecture Breakdown
1. **Scraper (`scraper.py`)**: Fetches the daily market reports from the DSE and saves them locally as CSV files.
2. **ML Pipeline (`ml_pipeline.py`)**: Consumes the historical CSV data, calculates momentum/volume features, and runs a Scikit-Learn Random Forest Classifier to generate confidence scores for future trends.
3. **Data Bridge (`generate_data_js.py`)**: Bridges the gap between local Python processing and the browser. It merges the latest CSV data with the ML predictions and outputs a pure JavaScript object file (`data.js`).
4. **The Frontend (`index.html` & `app.js`)**: A completely static, client-side application that reads `data.js` to render the UI, populate tables, and draw Chart.js visualizations.

---

## 🚀 Getting Started Locally

### Prerequisites
- Python 3.10+
- A modern web browser

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/jemmziray-tech/dse-investment-dashboard.git
   cd dse-investment-dashboard
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # Mac/Linux:
   source .venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Pipeline
To manually run the pipeline and update the data:
1. Run the scraper to get today's data:
   ```bash
   python scraper/scraper.py
   ```
2. Run the data bridge (which automatically triggers the ML pipeline):
   ```bash
   python generate_data_js.py
   ```
3. Open `index.html` in your browser to view the updated dashboard!

---

## ☁️ Setting Up Cloud Automation

You can set this project to scrape, predict, and host itself completely for free.

1. **Push to GitHub**: Push this repository to your GitHub account.
2. **Enable GitHub Pages**:
   - Go to your repository **Settings** > **Pages**.
   - Under "Build and deployment", set the source to **Deploy from a branch**.
   - Select the `main` (or `master`) branch.
3. **The Magic**: The included `.github/workflows/daily_scraper.yml` file is pre-configured to run every Monday-Friday at 4:00 PM EAT. It will automatically run the scraper, execute the AI model, and push the new data to your live website. 

---

## ⚠️ Disclaimer
**Educational Purposes Only.** The data presented on this dashboard and the predictions generated by the AI models do not constitute financial advice. Always consult a licensed financial advisor before making investment decisions on the Dar es Salaam Stock Exchange.

---

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
<div align="center">
<i>Built with ❤️ by <a href="https://github.com/jemmziray-tech">John Elifuraha Mziray</a></i>
</div>