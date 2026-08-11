import os

HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DSE Insight | {title}</title>
    
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    
    <!-- Custom CSS -->
    <link rel="stylesheet" href="assets/css/style.css">
    
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
</head>
<body>
    <!-- Navbar injected here by components.js -->
    <div id="navbar-container"></div>
    
    <div class="container">
"""

FOOTER = """
    </div>

    <!-- Footer injected here by components.js -->
    <div id="footer-container"></div>

    <!-- Data & Scripts -->
    <script src="assets/js/data.js"></script>
    <script src="assets/js/components.js"></script>
    <script src="assets/js/app.js"></script>
</body>
</html>
"""

PAGES = {
    "index.html": {
        "title": "Market Overview",
        "content": """
        <header class="dashboard-header animate-fade">
            <div class="brand">
                <h1>DSE <span>Insight</span></h1>
                <p>Institutional Market Intelligence for the Dar es Salaam Stock Exchange</p>
            </div>
            <div class="market-status" id="market-status">
                <div class="status-badge checking"><div class="indicator"></div> Checking Market Status...</div>
                <div class="time" id="current-time">--:--:--</div>
            </div>
        </header>

        <!-- SUMMARY CARDS -->
        <section class="summary-grid animate-fade" id="summary-grid" style="animation-delay: 0.2s;">
            <div class="summary-card">
                <h3>Total Market Cap</h3>
                <div class="value" id="val-mcap">---</div>
                <div class="subtitle">TZS Billions</div>
            </div>
            <div class="summary-card">
                <h3>Total Turnover</h3>
                <div class="value" id="val-turnover">---</div>
                <div class="subtitle">TZS</div>
            </div>
            <div class="summary-card">
                <h3>Volume Traded</h3>
                <div class="value" id="val-volume">---</div>
                <div class="subtitle">Shares</div>
            </div>
            <div class="summary-card">
                <h3>Companies</h3>
                <div class="value" id="val-companies">---</div>
                <div class="subtitle">Listed Equities</div>
            </div>
        </section>

        <!-- AI INSIGHTS & TOP MOVERS -->
        <section class="animate-fade" style="animation-delay: 0.4s;">
            <div class="section-header">
                <h2>Market Movers & AI Insights</h2>
            </div>
            <div class="movers-grid" style="grid-template-columns: 1fr 1fr 1fr;">
                <div class="glass-card">
                    <h3 style="margin-bottom: 1rem; font-size: 1.1rem; color: var(--status-up);">Top Gainers</h3>
                    <div id="top-gainers-list"></div>
                </div>
                <div class="glass-card">
                    <h3 style="margin-bottom: 1rem; font-size: 1.1rem; color: var(--status-down);">Top Losers</h3>
                    <div id="top-losers-list"></div>
                </div>
                <div class="glass-card" style="border: 1px solid var(--accent-gold);">
                    <h3 style="margin-bottom: 0.5rem; font-size: 1.1rem; color: var(--accent-gold); display: flex; justify-content: space-between;">
                        <span>AI Trend Predictor <i data-lucide="cpu" style="vertical-align: middle;"></i></span>
                    </h3>
                    <p style="font-size: 0.8rem; color: var(--text-secondary); margin-bottom: 1rem;">Machine Learning forecasts for the next 7 days based on momentum and volume.</p>
                    <div id="ai-insights-list">
                        <!-- Populated by JS -->
                    </div>
                </div>
            </div>
        </section>
        
        <!-- MARKET PULSE -->
        <section class="animate-fade" style="animation-delay: 0.6s;">
            <div class="section-header">
                <h2>Market Pulse</h2>
            </div>
            <div class="glass-card">
                <canvas id="volumeChart" height="80"></canvas>
            </div>
        </section>
        """
    },
    "equities.html": {
        "title": "Equities",
        "content": """
        <header class="dashboard-header animate-fade">
            <div class="brand">
                <h1>Equities <span>Market</span></h1>
                <p>Live trading data for all listed companies</p>
            </div>
            <button class="btn-primary" onclick="exportEquitiesCSV()">
                <i data-lucide="download"></i> Export to CSV
            </button>
        </header>
        
        <section class="animate-fade" style="animation-delay: 0.2s;">
            <div class="glass-card table-container">
                <table class="data-table" id="equities-table">
                    <thead>
                        <tr>
                            <th data-sort="symbol">Symbol</th>
                            <th data-sort="name">Company Name</th>
                            <th data-sort="sector">Sector</th>
                            <th data-sort="close" class="text-right">Price (TZS)</th>
                            <th data-sort="changePct" class="text-right">Change</th>
                            <th data-sort="mlTrend" class="text-center tooltip-trigger" data-tooltip="AI forecast based on momentum/volume. Not financial advice.">AI Prediction</th>
                            <th data-sort="volume" class="text-right tooltip-trigger" data-tooltip="Total number of shares traded today">Volume</th>
                            <th data-sort="turnover" class="text-right tooltip-trigger" data-tooltip="Total money (TZS) that changed hands today">Turnover</th>
                            <th data-sort="mcapBillion" class="text-right tooltip-trigger" data-tooltip="Market Capitalization: Total value of the company in Billions">MCAP (TZS 'B) <i data-lucide="chevron-down"></i></th>
                        </tr>
                    </thead>
                    <tbody id="equities-table-body">
                        <!-- Populated by JS -->
                    </tbody>
                </table>
            </div>
        </section>
        """
    },
    "bonds.html": {
        "title": "Fixed Income",
        "content": """
        <header class="dashboard-header animate-fade">
            <div class="brand">
                <h1>Fixed <span>Income</span></h1>
                <p>Government and Corporate Bonds Data</p>
            </div>
        </header>

        <section class="animate-fade" style="animation-delay: 0.2s;">
            <div class="glass-card table-container">
                <table class="data-table">
                    <thead>
                        <tr>
                            <th>Tenor</th>
                            <th>Coupon (%)</th>
                            <th class="text-right">Yield (%)</th>
                        </tr>
                    </thead>
                    <tbody id="bonds-table-body">
                        <!-- Populated by JS -->
                    </tbody>
                </table>
            </div>
        </section>
        """
    },
    "learn.html": {
        "title": "Education Center",
        "content": """
        <header class="dashboard-header animate-fade">
            <div class="brand">
                <h1>Education <span>Center</span></h1>
                <p>Tools and guides for new investors</p>
            </div>
        </header>

        <div class="movers-grid animate-fade" style="animation-delay: 0.2s;">
            <!-- PLAIN ENGLISH -->
            <div class="glass-card" style="grid-column: span 2;">
                <h3 style="margin-bottom: 1rem; font-size: 1.1rem; color: var(--accent-blue);">Market in Plain English</h3>
                <div id="plain-english-text" style="font-size: 1.05rem; line-height: 1.8;">
                    Generating summary...
                </div>
            </div>

            <!-- DSE 101 -->
            <div class="glass-card">
                <h3 style="margin-bottom: 1rem; font-size: 1.1rem; color: var(--accent-gold);">DSE 101: How to Start</h3>
                <div style="font-size: 0.9rem; color: var(--text-secondary);">
                    <p style="margin-bottom: 1rem;"><strong>1. Find a Broker</strong><br>You cannot buy shares directly from the DSE. You need a Licensed Dealing Member (broker) like Orbit Securities, CRDB, or NMB.</p>
                    <p style="margin-bottom: 1rem;"><strong>2. Open a CSD Account</strong><br>Your broker will help you open a Central Depository System account. This is where your digital shares are stored safely.</p>
                    <p><strong>3. Look for Blue Chips <i data-lucide="shield" style="color:var(--accent-gold); width:14px; height:14px;"></i></strong><br>Beginners should look for "Blue Chip" companies (MCAP > 1 Trillion TZS). They are usually safer, well-established companies.</p>
                </div>
            </div>
        </div>

        <section class="animate-fade" style="animation-delay: 0.4s;">
            <div class="section-header">
                <h2>Shares Calculator</h2>
            </div>
            <div class="glass-card" style="max-width: 600px; margin: 0 auto;">
                <p style="color: var(--text-secondary); margin-bottom: 1.5rem; text-align: center;">Find out how many shares you can afford to buy today.</p>
                <form id="investment-form">
                    <div class="form-group" style="margin-bottom: 1rem;">
                        <label for="capital" style="display:block; margin-bottom: 0.5rem; font-size: 0.9rem;">Your Budget (TZS)</label>
                        <input type="number" id="capital" placeholder="e.g. 50000" style="width: 100%; padding: 0.8rem; border-radius: 6px; background: rgba(0,0,0,0.2); border: 1px solid var(--panel-border); color: #fff; font-size: 1rem;">
                    </div>
                    <div class="form-group" style="margin-bottom: 1.5rem;">
                        <label for="calc-ticker" style="display:block; margin-bottom: 0.5rem; font-size: 0.9rem;">Company</label>
                        <select id="calc-ticker" style="width: 100%; padding: 0.8rem; border-radius: 6px; background: rgba(0,0,0,0.2); border: 1px solid var(--panel-border); color: #fff; font-size: 1rem;">
                            <option value="">Select a company...</option>
                        </select>
                    </div>
                    <button type="submit" class="btn-primary" style="width: 100%; justify-content: center;">Calculate</button>
                </form>
                <div id="calc-results" class="calc-result hidden" style="margin-top: 1.5rem; text-align: center; padding: 1rem; background: rgba(0,0,0,0.1); border-radius: 8px;">
                    <!-- Results appear here -->
                </div>
            </div>
        </section>
        """
    },
    "analytics.html": {
        "title": "AI Analytics Hub",
        "content": """
        <header class="dashboard-header animate-fade">
            <div class="brand">
                <h1>AI Predictive <span>Hub</span></h1>
                <p>Machine Learning confidence metrics powered by Scikit-Learn</p>
            </div>
        </header>
        <section class="animate-fade" style="animation-delay: 0.2s;">
            <div class="glass-card" style="text-align: center; padding: 3rem;">
                <i data-lucide="cpu" style="width: 48px; height: 48px; color: var(--accent-gold); margin-bottom: 1rem;"></i>
                <h2 style="margin-bottom: 1rem;">Analytics Hub</h2>
                <p style="color: var(--text-secondary); max-width: 600px; margin: 0 auto;">This section is under construction. It will feature detailed confidence matrix charts, historical model accuracy, and in-depth momentum indicators for the Top 5 predictions.</p>
            </div>
        </section>
        """
    },
    "screener.html": {
        "title": "Stock Screener",
        "content": """
        <header class="dashboard-header animate-fade">
            <div class="brand">
                <h1>Stock <span>Screener</span></h1>
                <p>Filter companies by Sector and Market Cap</p>
            </div>
        </header>
        <section class="animate-fade" style="animation-delay: 0.2s;">
            <div class="glass-card" style="text-align: center; padding: 3rem;">
                <i data-lucide="filter" style="width: 48px; height: 48px; color: var(--accent-gold); margin-bottom: 1rem;"></i>
                <h2 style="margin-bottom: 1rem;">Screener Tool</h2>
                <p style="color: var(--text-secondary); max-width: 600px; margin: 0 auto;">This section is under construction. It will feature advanced filtering controls to find specific equities matching your investment criteria.</p>
            </div>
        </section>
        """
    }
}

def main():
    for filename, data in PAGES.items():
        with open(filename, "w", encoding="utf-8") as f:
            f.write(HEAD.format(title=data["title"]))
            f.write(data["content"])
            f.write(FOOTER)
        print(f"Generated {filename}")

if __name__ == "__main__":
    main()
