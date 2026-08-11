// Formatters
const formatMoney = (val) => new Intl.NumberFormat('en-TZ', { maximumFractionDigits: 0 }).format(val);
const formatDecimal = (val, maxDecimals=2) => new Intl.NumberFormat('en-TZ', { minimumFractionDigits: 2, maximumFractionDigits: maxDecimals }).format(val);
const formatCompact = (val) => new Intl.NumberFormat('en-TZ', { notation: "compact", maximumFractionDigits: 1 }).format(val);

// State
let sortCol = 'mcapBillion';
let sortAsc = false;

document.addEventListener("DOMContentLoaded", () => {
    initClock();
    if(document.getElementById('market-status')) checkMarketStatus();
    
    // Overview Page
    if(document.getElementById('summary-grid')) populateSummary();
    if(document.getElementById('plain-english-text')) generatePlainEnglish();
    if(document.getElementById('top-gainers-list')) populateMovers();
    if(document.getElementById('ai-insights-list')) populateAIInsights();
    
    // Equities Page
    if(document.getElementById('equities-table-body')) renderEquitiesTable();
    
    // Bonds Page
    if(document.getElementById('bonds-table-body')) renderBondsTable();
    
    // Charts (Overview or Analytics)
    if(document.getElementById('volumeChart')) initCharts();
    
    // Learn Page
    if(document.getElementById('investment-form')) initCalculator();
    
    // Initialize Lucide icons
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }

    // Setup sorting listeners
    document.querySelectorAll('#equities-table th[data-sort]').forEach(th => {
        th.addEventListener('click', () => {
            const field = th.getAttribute('data-sort');
            if (sortCol === field) {
                sortAsc = !sortAsc;
            } else {
                sortCol = field;
                sortAsc = false;
            }
            renderEquitiesTable();
        });
    });
});

function initClock() {
    const clockEl = document.getElementById('live-clock');
    
    function update() {
        // EAT is UTC+3
        const d = new Date();
        const utc = d.getTime() + (d.getTimezoneOffset() * 60000);
        const eat = new Date(utc + (3600000 * 3));
        
        clockEl.innerText = eat.toLocaleTimeString('en-US', { hour12: false }) + ' EAT';
    }
    
    update();
    setInterval(update, 1000);
}

function checkMarketStatus() {
    const statusEl = document.getElementById('market-status-badge');
    const statusText = document.getElementById('market-status-text');
    
    const d = new Date();
    const utc = d.getTime() + (d.getTimezoneOffset() * 60000);
    const eat = new Date(utc + (3600000 * 3));
    
    const day = eat.getDay(); // 0=Sun, 6=Sat
    const hour = eat.getHours();
    
    // DSE is typically open Mon-Fri 10:00 to 14:00 (simplifying to 9-15 for safety/demo)
    const isOpen = (day >= 1 && day <= 5) && (hour >= 9 && hour < 15);
    
    if (isOpen) {
        statusEl.className = 'status-badge open';
        statusText.innerText = 'Market Open';
    } else {
        statusEl.className = 'status-badge closed';
        statusText.innerText = 'Market Closed';
    }
}

function populateSummary() {
    document.getElementById('display-date').innerText = DSE_DATA.meta.displayDate;
    
    document.getElementById('sum-turnover').innerText = 'TZS ' + formatCompact(DSE_DATA.summary.totalTurnover);
    document.getElementById('sum-volume').innerText = formatCompact(DSE_DATA.summary.totalVolume);
    document.getElementById('sum-deals').innerText = formatMoney(DSE_DATA.summary.totalDeals);
    document.getElementById('sum-mcap').innerText = 'TZS ' + formatDecimal(DSE_DATA.summary.totalMcapBillion) + ' B';
}

function getChangeClass(change) {
    if (change > 0) return 'up';
    if (change < 0) return 'down';
    return 'neutral';
}

function getChangeBgClass(change) {
    if (change > 0) return 'bg-up';
    if (change < 0) return 'bg-down';
    return '';
}

function getChangeSymbol(change) {
    if (change > 0) return '<i data-lucide="trending-up"></i>';
    if (change < 0) return '<i data-lucide="trending-down"></i>';
    return '<i data-lucide="minus"></i>';
}

function populateMovers() {
    const gainersList = document.getElementById('top-gainers-list');
    const losersList = document.getElementById('top-losers-list');
    
    const gainers = DSE_DATA.equities.filter(e => e.changePct > 0).sort((a,b) => b.changePct - a.changePct).slice(0, 5);
    const losers = DSE_DATA.equities.filter(e => e.changePct < 0).sort((a,b) => a.changePct - b.changePct).slice(0, 5);
    
    gainersList.innerHTML = gainers.length ? gainers.map(g => createMoverRow(g, 'up')).join('') : '<div class="mover-item">No gainers today</div>';
    losersList.innerHTML = losers.length ? losers.map(l => createMoverRow(l, 'down')).join('') : '<div class="mover-item">No losers today</div>';
    if (typeof lucide !== 'undefined') lucide.createIcons();
}

function createMoverRow(item, type) {
    const bgClass = type === 'up' ? 'bg-up' : 'bg-down';
    const icon = type === 'up' ? 'trending-up' : 'trending-down';
    
    return `
        <div class="mover-item">
            <div class="mover-info">
                <div class="ticker">${item.symbol}</div>
                <div class="name">${item.name}</div>
            </div>
            <div class="mover-stats">
                <div class="price">${formatMoney(item.close)}</div>
                <div class="change ${bgClass}"><i data-lucide="${icon}"></i> ${Math.abs(item.changePct).toFixed(2)}%</div>
            </div>
        </div>
    `;
}

function renderEquitiesTable() {
    const tbody = document.getElementById('equities-table-body');
    let data = [...DSE_DATA.equities];
    
    data.sort((a, b) => {
        let valA = a[sortCol];
        let valB = b[sortCol];
        
        if (typeof valA === 'string') {
            return sortAsc ? valA.localeCompare(valB) : valB.localeCompare(valA);
        }
        return sortAsc ? (valA - valB) : (valB - valA);
    });
    
    tbody.innerHTML = data.map(row => {
        const cClass = getChangeClass(row.changePct);
        const cSym = getChangeSymbol(row.changePct);
        
        // Define Blue Chip (e.g. MCAP > 1000 Billion TZS)
        const isBlueChip = row.mcapBillion >= 1000;
        const nameHtml = row.name + (isBlueChip ? ' <span class="blue-chip tooltip-trigger" data-tooltip="Blue Chip"><i data-lucide="shield"></i></span>' : '');

        // AI Prediction Badge
        let aiBadge = `<span class="ai-badge neutral"><i data-lucide="minus"></i> Neutral</span>`;
        if (row.mlTrend === "Bullish") aiBadge = `<span class="ai-badge bullish"><i data-lucide="trending-up"></i> Bullish <small>(${row.mlConfidence}%)</small></span>`;
        if (row.mlTrend === "Bearish") aiBadge = `<span class="ai-badge bearish"><i data-lucide="trending-down"></i> Bearish <small>(${row.mlConfidence}%)</small></span>`;

        return `
            <tr>
                <td class="ticker">${row.symbol}</td>
                <td>${nameHtml}</td>
                <td>${row.sector}</td>
                <td class="text-right">${formatMoney(row.close)}</td>
                <td class="text-right ${cClass}">${cSym} ${Math.abs(row.changePct).toFixed(2)}%</td>
                <td class="text-center">${aiBadge}</td>
                <td class="text-right">${formatCompact(row.volume)}</td>
                <td class="text-right">${formatCompact(row.turnover)}</td>
                <td class="text-right">${formatDecimal(row.mcapBillion)}</td>
            </tr>
        `;
    }).join('');
    
    // Update header icons
    document.querySelectorAll('#equities-table th i').forEach(i => i.remove());
    const activeTh = document.querySelector(`#equities-table th[data-sort="${sortCol}"]`);
    if (activeTh) activeTh.innerHTML += sortAsc ? ' <i data-lucide="chevron-up"></i>' : ' <i data-lucide="chevron-down"></i>';
    if (typeof lucide !== 'undefined') lucide.createIcons();
}

function renderBondsTable() {
    const tbody = document.getElementById('bonds-table-body');
    tbody.innerHTML = DSE_DATA.bonds.map(b => `
        <tr>
            <td>${b.tenor}</td>
            <td style="font-family: monospace;">${b.bondNumber}</td>
            <td class="text-right">${b.couponRate ? b.couponRate.toFixed(2) + '%' : '-'}</td>
        </tr>
    `).join('');
}

// Global defaults for Chart.js
Chart.defaults.color = '#a0aec0';
Chart.defaults.font.family = "'Inter', sans-serif";

function initCharts() {
    // 1. Sector Composition (MCAP)
    const sectorCtx = document.getElementById('sectorChart').getContext('2d');
    
    let sectorMcap = {};
    DSE_DATA.equities.forEach(e => {
        if(!sectorMcap[e.sector]) sectorMcap[e.sector] = 0;
        sectorMcap[e.sector] += e.mcapBillion;
    });
    
    // Sort and keep top 5 + other
    let sectors = Object.entries(sectorMcap).sort((a,b) => b[1] - a[1]);
    let topSectors = sectors.slice(0, 5);
    let otherMcap = sectors.slice(5).reduce((sum, item) => sum + item[1], 0);
    if(otherMcap > 0) topSectors.push(['Other', otherMcap]);
    
    new Chart(sectorCtx, {
        type: 'doughnut',
        data: {
            labels: topSectors.map(s => s[0]),
            datasets: [{
                data: topSectors.map(s => s[1]),
                backgroundColor: [
                    '#00c896', '#d4a843', '#3b82f6', '#8b5cf6', '#ef4444', '#718096'
                ],
                borderWidth: 0,
                hoverOffset: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: { position: 'right', labels: { color: '#f0f2f5', boxWidth: 12 } },
                tooltip: { 
                    callbacks: { 
                        label: (ctx) => ' ' + ctx.label + ': TZS ' + formatDecimal(ctx.raw) + 'B'
                    } 
                }
            },
            cutout: '70%'
        }
    });

    // 2. Top Traded by Volume (Bar)
    const volCtx = document.getElementById('volumeChart').getContext('2d');
    let topVol = [...DSE_DATA.equities].sort((a,b) => b.volume - a.volume).slice(0, 5);
    
    new Chart(volCtx, {
        type: 'bar',
        data: {
            labels: topVol.map(v => v.symbol),
            datasets: [{
                label: 'Volume',
                data: topVol.map(v => v.volume),
                backgroundColor: 'rgba(212, 168, 67, 0.6)',
                borderColor: '#d4a843',
                borderWidth: 1,
                borderRadius: 4
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                y: { beginAtZero: true, grid: { color: 'rgba(255,255,255,0.05)' } },
                x: { grid: { display: false } }
            },
            plugins: {
                legend: { display: false },
                tooltip: { callbacks: { label: (ctx) => ' Volume: ' + formatMoney(ctx.raw) } }
            }
        }
    });
}

// --- Beginner Features ---

function populateAIInsights() {
    const list = document.getElementById('ai-insights-list');
    
    // Sort equities by AI confidence where trend is Bullish
    const bullish = DSE_DATA.equities.filter(e => e.mlTrend === 'Bullish').sort((a,b) => b.mlConfidence - a.mlConfidence);
    
    let html = "";
    if (bullish.length > 0) {
        html += `<div style="font-size: 0.9rem; color: var(--text-secondary); margin-bottom: 0.5rem;">Top Bullish Signals:</div>`;
        bullish.slice(0, 3).forEach(b => {
            html += `
                <div class="mover-item" style="padding: 0.5rem 0;">
                    <div class="mover-info"><span class="ticker">${b.symbol}</span></div>
                    <div class="mover-stats"><span class="ai-badge bullish"><i data-lucide="trending-up"></i> ${b.mlConfidence}%</span></div>
                </div>
            `;
        });
    } else {
        html = `<div style="text-align: center; color: var(--text-muted); padding: 1rem 0;">No strong bullish signals today.</div>`;
    }
    
    list.innerHTML = html;
    if (typeof lucide !== 'undefined') lucide.createIcons();
}

function generatePlainEnglish() {
    const textEl = document.getElementById('plain-english-text');
    const s = DSE_DATA.summary;
    
    if (s.totalVolume === 0) {
        textEl.innerHTML = "The market is currently quiet with no trading volume yet today.";
        return;
    }

    let intro = "";
    if (s.gainersCount > s.losersCount) {
        intro = "Today was a positive day on the DSE! ";
    } else if (s.losersCount > s.gainersCount) {
        intro = "It was a tough day on the market today. ";
    } else {
        intro = "The market was balanced today. ";
    }

    let gainerText = "";
    if (s.topGainer) {
        gainerText = `${s.gainersCount} companies gained value, led by <strong>${s.topGainer}</strong> which went up <strong>${s.topGainerPct}%</strong>. `;
    }

    // Find most traded by turnover
    let mostTraded = [...DSE_DATA.equities].sort((a,b) => b.turnover - a.turnover)[0];
    let tradedText = "";
    if (mostTraded && mostTraded.turnover > 0) {
        tradedText = `The most actively traded stock by value was <strong>${mostTraded.symbol}</strong>, seeing TZS ${formatCompact(mostTraded.turnover)} change hands.`;
    }

    textEl.innerHTML = intro + gainerText + tradedText;
}

function initCalculator() {
    const calcForm = document.getElementById('investment-form');
    if (!calcForm) return;

    // Populate dropdown
    const select = document.getElementById('calc-ticker');
    let availableEquities = DSE_DATA.equities.filter(e => e.close > 0).sort((a,b) => a.name.localeCompare(b.name));
    select.innerHTML += availableEquities.map(e => `<option value="${e.symbol}">${e.name} (${e.symbol})</option>`).join('');

    calcForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const capital = parseFloat(document.getElementById('capital').value);
        const ticker = select.value;
        
        const eq = DSE_DATA.equities.find(e => e.symbol === ticker);
        if(!eq || isNaN(capital) || capital <= 0) return;
        
        const shares = Math.floor(capital / eq.close);
        const actualCost = shares * eq.close;
        const remainder = capital - actualCost;
        
        let resHtml = `
            <p>With <strong>TZS ${formatMoney(capital)}</strong>, you can afford:</p>
            <div style="font-size: 2rem; color: var(--accent-gold); font-weight: 700; margin: 1rem 0;">
                ${shares.toLocaleString()} Shares
            </div>
            <p>of ${eq.name} (${ticker}) at TZS ${formatMoney(eq.close)} each.</p>
            <p style="color: var(--text-secondary); font-size: 0.9rem; margin-top: 1rem;">
                Total cost: TZS ${formatMoney(actualCost)}<br>
                Change left over: TZS ${formatMoney(remainder)}
            </p>
            <p style="color: var(--status-down); font-size: 0.8rem; margin-top: 0.5rem;">
                *Note: This excludes broker fees and CSDR fees (usually ~2% total).
            </p>
        `;
        
        document.getElementById('calc-results').innerHTML = resHtml;
    });
}

// --- Professional Features ---

function exportEquitiesCSV() {
    if (!DSE_DATA || !DSE_DATA.equities) return;
    
    // Define headers
    const headers = ["Symbol", "Name", "Sector", "Price (TZS)", "Change (%)", "Volume", "Turnover (TZS)", "Market Cap (TZS B)", "AI Trend", "AI Confidence"];
    
    // Map rows
    const rows = DSE_DATA.equities.map(e => [
        e.symbol,
        `"${e.name}"`,
        e.sector,
        e.close,
        e.changePct,
        e.volume,
        e.turnover,
        e.mcapBillion,
        e.mlTrend,
        e.mlConfidence
    ]);
    
    // Combine
    const csvContent = [
        headers.join(","),
        ...rows.map(r => r.join(","))
    ].join("\n");
    
    // Trigger download
    const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.setAttribute("href", url);
    link.setAttribute("download", `DSE_Equities_${new Date().toISOString().split('T')[0]}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}
