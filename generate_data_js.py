#!/usr/bin/env python3
"""
DSE Insight — Data Bridge Script
════════════════════════════════════════════════════════════
Reads the latest scraped CSV files from data/raw/ and
regenerates assets/js/data.js for the web dashboard.

Run this after every scraper session:
    python generate_data_js.py

Author: John Elifuraha Mziray
"""

import os
import re
import sys
import glob
import json
from datetime import datetime
import ml_pipeline

# ── Try importing pandas ─────────────────────────────────────────────────────
try:
    import pandas as pd
except ImportError:
    print("❌  pandas not found. Activate your virtual environment first:")
    print("    .venv\\Scripts\\activate   (Windows PowerShell)")
    sys.exit(1)

# ── Paths ─────────────────────────────────────────────────────────────────────
BASE_DIR      = os.path.dirname(os.path.abspath(__file__))
HISTORICAL_DATA_PATH = os.path.join(BASE_DIR, "data", "historical")
OUTPUT_PATH   = os.path.join(BASE_DIR, "assets", "js", "data.js")

# ── Company Metadata (sector + full name) ─────────────────────────────────────
COMPANY_INFO = {
    "AFRIPRISE":   {"name": "AfriPrise Finance Ltd",          "sector": "Financial Services"},
    "CRDB":        {"name": "CRDB Bank Plc",                  "sector": "Banking"},
    "DCB":         {"name": "DCB Commercial Bank",             "sector": "Banking"},
    "DSE":         {"name": "DSE Plc",                        "sector": "Financial Services"},
    "EABL":        {"name": "East African Breweries Ltd",      "sector": "Beverages"},
    "JATU":        {"name": "Jatu Plc",                       "sector": "Financial Services"},
    "JHL":         {"name": "Jubilee Holdings Ltd",           "sector": "Insurance"},
    "KA":          {"name": "Kenya Airways Ltd",              "sector": "Aviation"},
    "KCB":         {"name": "KCB Group Plc",                  "sector": "Banking"},
    "MBP":         {"name": "Mkombozi Commercial Bank Plc",   "sector": "Banking"},
    "MCB":         {"name": "Mwanga Hakika Bank",             "sector": "Banking"},
    "MKCB":        {"name": "Maendeleo Bank Plc",             "sector": "Banking"},
    "MUCOBA":      {"name": "Mufindi Community Bank",         "sector": "Banking"},
    "NICO":        {"name": "NICO Holdings Ltd",              "sector": "Insurance"},
    "NMB":         {"name": "NMB Bank Plc",                   "sector": "Banking"},
    "NMG":         {"name": "Nation Media Group Ltd",         "sector": "Media"},
    "PAL":         {"name": "Precision Air Services Ltd",     "sector": "Aviation"},
    "SWALA":       {"name": "Swala Oil & Gas Plc",            "sector": "Energy"},
    "SWIS":        {"name": "Swissport Tanzania Ltd",         "sector": "Logistics"},
    "TBL":         {"name": "Tanzania Breweries Ltd",         "sector": "Beverages"},
    "TCC":         {"name": "Tanzania Cigarette Company",     "sector": "Consumer"},
    "TCCL":        {"name": "Tanga Cement Company Ltd",       "sector": "Cement"},
    "TOL":         {"name": "TOL Gases Ltd",                  "sector": "Industrial"},
    "TPCC":        {"name": "Tanzania Portland Cement Co.",   "sector": "Cement"},
    "TTP":         {"name": "Tanzania Tea Packers Ltd",       "sector": "Agriculture"},
    "USL":         {"name": "Urafiki Textile Mill",           "sector": "Textiles"},
    "VODA":        {"name": "Vodacom Tanzania Plc",           "sector": "Telecom"},
    "YETU":        {"name": "Yetu Microfinance Plc",          "sector": "Financial Services"},
    "ITRUST ETF":  {"name": "iShares Trust ETF",              "sector": "ETF"},
    "VERTEX ETF":  {"name": "Vertex Capital ETF",             "sector": "ETF"},
}

# ── Utilities ─────────────────────────────────────────────────────────────────

def parse_change(raw) -> float:
    """Extract numeric % from DSE arrow strings like '+▲ 5.56' or '-▼ -0.74'."""
    try:
        cleaned = re.sub(r"[▲▼⏴⏵⬆⬇+\s]", " ", str(raw)).strip()
        nums = [p for p in cleaned.split() if re.match(r"^-?\d+\.?\d*$", p)]
        if not nums:
            return 0.0
        val = float(nums[-1])
        if "▼" in str(raw) and val > 0:
            val = -val
        return round(val, 2)
    except (ValueError, TypeError):
        return 0.0


def safe_float(val) -> float:
    try:
        return float(str(val).replace(",", "").strip())
    except (ValueError, TypeError):
        return 0.0


def safe_int(val) -> int:
    try:
        return int(safe_float(val))
    except (ValueError, TypeError):
        return 0


def latest_csv(pattern: str) -> str | None:
    files = glob.glob(os.path.join(RAW_DATA_PATH, pattern))
    return sorted(files)[-1] if files else None


def date_from_path(path: str) -> tuple[str, str]:
    # We now read the Date directly from the dataframe, so this is just a fallback.
    now = datetime.now()
    return now.strftime("%Y-%m-%d"), now.strftime("%d %B %Y")

# ── Parsers ───────────────────────────────────────────────────────────────────

def parse_equities(path: str) -> tuple[list, str, str]:
    df = pd.read_csv(path)
    if 'Date' in df.columns:
        latest_date = df['Date'].max()
        df = df[df['Date'] == latest_date]
        dt = datetime.strptime(latest_date, "%Y-%m-%d")
        report_date = dt.strftime("%Y-%m-%d")
        display_date = dt.strftime("%d %B %Y")
    else:
        report_date, display_date = date_from_path(path)
        
    rows = []
    for _, row in df.iterrows():
        sym = str(row.get("Symbol", "")).strip()
        if not sym or sym.lower() == "nan":
            continue
        info = COMPANY_INFO.get(sym, {"name": sym, "sector": "Other"})
        rows.append({
            "symbol":      sym,
            "name":        info["name"],
            "sector":      info["sector"],
            "open":        safe_float(row.get("Open", 0)),
            "prevClose":   safe_float(row.get("Prev Close", 0)),
            "close":       safe_float(row.get("Close", 0)),
            "high":        safe_float(row.get("High", 0)),
            "low":         safe_float(row.get("Low", 0)),
            "changePct":   parse_change(row.get("Change", 0)),
            "turnover":    safe_float(row.get("Turn over", 0)),
            "deals":       safe_int(row.get("Deals", 0)),
            "volume":      safe_int(row.get("Volume", 0)),
            "mcapBillion": safe_float(row.get("MCAP (TZS 'B)", 0)),
        })
    return rows, report_date, display_date


def parse_bonds(path: str) -> list:
    if not os.path.exists(path):
        return []
    df = pd.read_csv(path)
    if 'Date' in df.columns:
        latest_date = df['Date'].max()
        df = df[df['Date'] == latest_date]
        
    rows = []
    for _, row in df.iterrows():
        tenor = str(row.get("Tenor", "")).strip()
        num   = str(row.get("Bond Number", "")).strip()
        if not tenor or tenor.lower() == "nan":
            continue
        coupon = None
        m = re.search(r"-(\d{1,2}\.\d{1,2})-", num)
        if m:
            coupon = float(m.group(1))
        rows.append({"tenor": tenor, "bondNumber": num, "couponRate": coupon})
    return rows


def compute_summary(equities: list) -> dict:
    gainers  = [e for e in equities if e["changePct"] > 0]
    losers   = [e for e in equities if e["changePct"] < 0]
    top_g    = max(gainers, key=lambda x: x["changePct"], default=None)
    top_l    = min(losers,  key=lambda x: x["changePct"], default=None)
    return {
        "totalTurnover":    round(sum(e["turnover"]    for e in equities)),
        "totalDeals":       sum(e["deals"]             for e in equities),
        "totalVolume":      sum(e["volume"]            for e in equities),
        "totalMcapBillion": round(sum(e["mcapBillion"] for e in equities), 1),
        "gainersCount":     len(gainers),
        "losersCount":      len(losers),
        "unchangedCount":   len(equities) - len(gainers) - len(losers),
        "topGainer":        top_g["symbol"]   if top_g else None,
        "topGainerPct":     top_g["changePct"] if top_g else None,
        "topLoser":         top_l["symbol"]   if top_l else None,
        "topLoserPct":      top_l["changePct"] if top_l else None,
    }

# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    print("\n🔄  DSE Insight — Data Bridge")
    print("─" * 44)

    eq_file   = os.path.join(HISTORICAL_DATA_PATH, "dse_table_3_historical.csv")
    bond_file = os.path.join(HISTORICAL_DATA_PATH, "dse_table_4_historical.csv")

    if not os.path.exists(eq_file):
        print("❌  No historical equity CSV found. Run the scraper first.")
        sys.exit(1)

    print(f"📄  Equity : {os.path.basename(eq_file)}")
    print(f"📄  Bonds  : {os.path.basename(bond_file) if os.path.exists(bond_file) else 'not found'}")

    equities, report_date, display_date = parse_equities(eq_file)
    bonds    = parse_bonds(bond_file)
    summary  = compute_summary(equities)

    print("🤖  Running AI Trend Predictor...")
    symbols = [e['symbol'] for e in equities]
    ml_preds = ml_pipeline.run_predictions(symbols)
    
    # Inject AI predictions into equities
    for e in equities:
        sym = e['symbol']
        pred = ml_preds.get(sym, {"trend": "Neutral", "confidence": 50})
        e['mlTrend'] = pred['trend']
        e['mlConfidence'] = pred['confidence']

    payload = {
        "meta": {
            "exchange":    "Dar es Salaam Stock Exchange",
            "currency":    "TZS",
            "reportDate":  report_date,
            "displayDate": display_date,
            "dataSource":  "dse.co.tz",
            "generatedAt": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        },
        "summary":  summary,
        "equities": equities,
        "bonds":    bonds,
    }

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"// DSE Insight — Market Data (auto-generated {ts} EAT)\n")
        f.write(f"// Report date : {display_date}\n")
        f.write(f"// Source      : {eq_file}\n\n")
        f.write(f"const DSE_DATA = {json.dumps(payload, indent=2, ensure_ascii=False)};\n")

    print(f"\n✅  Generated  : assets/js/data.js")
    print(f"📊  Companies  : {len(equities)}")
    print(f"📈  Gainers    : {summary['gainersCount']}")
    print(f"📉  Losers     : {summary['losersCount']}")
    print(f"💰  Total MCAP : TZS {summary['totalMcapBillion']:,.1f} B")
    print("─" * 44)
    print("✨  Open index.html in your browser to view the dashboard.\n")


if __name__ == "__main__":
    main()
