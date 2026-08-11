// components.js - Injects Navbar and Footer across all pages

const NAVBAR_HTML = `
<nav class="navbar">
    <div class="nav-brand">
        <i data-lucide="bar-chart-2"></i>
        <span>DSE Insight</span>
    </div>
    <ul class="nav-links">
        <li><a href="index.html" class="nav-link" id="nav-index">Overview</a></li>
        <li><a href="equities.html" class="nav-link" id="nav-equities">Equities</a></li>
        <li><a href="bonds.html" class="nav-link" id="nav-bonds">Fixed Income</a></li>
        <li><a href="analytics.html" class="nav-link" id="nav-analytics">AI Analytics</a></li>
        <li><a href="screener.html" class="nav-link" id="nav-screener">Screener</a></li>
        <li><a href="learn.html" class="nav-link" id="nav-learn">Education</a></li>
    </ul>
</nav>
`;

const FOOTER_HTML = `
<footer>
    <div class="footer-content">
        <p>&copy; 2026 DSE Insight. Not financial advice.</p>
        <div class="footer-links">
            <a href="https://github.com/jemmziray-tech/dse-investment-dashboard" target="_blank">
                <i data-lucide="github"></i> View Source
            </a>
        </div>
    </div>
</footer>
`;

function injectComponents() {
    // Inject Navbar
    const navContainer = document.getElementById('navbar-container');
    if (navContainer) {
        navContainer.innerHTML = NAVBAR_HTML;
        
        // Highlight active link
        const currentPath = window.location.pathname.split('/').pop() || 'index.html';
        const activeLink = document.getElementById('nav-' + currentPath.replace('.html', ''));
        if (activeLink) {
            activeLink.classList.add('active');
        }
    }

    // Inject Footer
    const footerContainer = document.getElementById('footer-container');
    if (footerContainer) {
        footerContainer.innerHTML = FOOTER_HTML;
    }

    // Initialize Lucide icons for the newly injected HTML
    if (typeof lucide !== 'undefined') {
        lucide.createIcons();
    }
}

// Run injection when DOM is loaded
document.addEventListener('DOMContentLoaded', injectComponents);
