import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from PIL import Image

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="LSV Pricing Engine | Quant Research",
    page_icon="📉",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS (Institutional & Readable)
# ==========================================
st.markdown("""
    <style>
    /* Main container width and font stack */
    .main { max-width: 1100px; margin: 0 auto; font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    h1 { text-align: center; font-size: 2.8rem !important; font-weight: 900 !important; margin-bottom: 0.5rem !important; line-height: 1.25 !important; color: var(--text-color) !important; opacity: 0.95 !important; letter-spacing: -0.02em !important; }
    .subtitle { text-align: center; font-size: 1.3rem !important; color: var(--text-color) !important; opacity: 0.75 !important; font-style: italic !important; margin-bottom: 1.8rem !important; font-weight: 400 !important; }
    h2 { font-weight: 800 !important; font-size: 2.2rem !important; margin-top: 2.8rem !important; border-bottom: 1px solid rgba(128, 128, 128, 0.2) !important; padding-bottom: 0.5rem !important; margin-bottom: 1.5rem !important; color: var(--text-color) !important; opacity: 0.95 !important; letter-spacing: -0.01em !important; }
    .section-badge {
        background-color: #2563EB;
        color: #FFFFFF !important;
        padding: 8px 16px;              
        border-radius: 8px;             
        font-size: 1.65rem;             
        font-weight: 800;
        letter-spacing: 0.06em;
        text-transform: uppercase;
        display: inline-block;
        vertical-align: middle;   
        margin-right: 12px;
    }
    .h2-text {
        position: relative;
        top: 3px;
    }
    h3 { font-weight: 700 !important; font-size: 1.6rem !important; margin-top: 2rem !important; margin-bottom: 1rem !important; color: var(--text-color) !important; opacity: 0.95 !important; }
    div[data-testid="stMarkdownContainer"] p, div[data-testid="stMarkdownContainer"] li { font-size: 1.25rem !important; line-height: 1.6 !important; font-weight: 400 !important; color: var(--text-color) !important; opacity: 0.9 !important; } 
    div[data-testid="stMarkdownContainer"] li { margin-bottom: 0.5rem !important; }
    div[data-testid="stMarkdownContainer"] strong { font-weight: 700 !important; color: var(--text-color) !important; opacity: 1.0 !important; }
    
    .hero-box { background-color: var(--secondary-background-color); border: 1px solid rgba(128, 128, 128, 0.2); border-radius: 6px; padding: 20px 25px; margin: 1.5rem 0 2.5rem 0; }
    .hero-box-title { font-size: 1.2rem; font-weight: 700; color: #3B82F6; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.05em; }
    .math-box { text-align: center; font-size: 1.05rem; color: var(--text-color); opacity: 0.6; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: -10px; margin-top: 1.5rem; font-weight: 600; }
    .findings-box { border-left: 5px solid #10B981 !important; padding: 1.2rem !important; margin: 2rem 0 !important; background-color: var(--secondary-background-color) !important; border-radius: 0 6px 6px 0 !important; }
    .findings-title { font-size: 1.25rem; font-weight: 700; margin-bottom: 10px; color: #10B981; text-transform: uppercase; letter-spacing: 0.05em; }
    .pipeline-container { display: flex; justify-content: space-between; align-items: center; margin: 2rem 0; gap: 8px; }
    .pipeline-block { background-color: var(--secondary-background-color); padding: 12px; border-radius: 6px; text-align: center; flex: 1; border: 1px solid rgba(128, 128, 128, 0.2); }
    .pipeline-block-title { font-size: 0.85rem; font-weight: 700; text-transform: uppercase; margin-bottom: 4px; color: #3B82F6; }
    .pipeline-block-desc { font-size: 0.9rem; opacity: 0.8; }
    .pipeline-arrow { font-size: 1.2rem; opacity: 0.3; }
    
    .mechanism-box { border-left: 5px solid #3B82F6 !important; padding: 1.25rem !important; margin: 1.5rem 0 !important; background-color: var(--secondary-background-color) !important; color: var(--text-color) !important; border-radius: 0 6px 6px 0 !important; }
    .mechanism-title { color: #3B82F6; font-size: 1.25rem; font-weight: 800; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em; }
    
    .insight-box { border-left: 5px solid #8B5CF6 !important; padding: 1.25rem !important; margin: 1.5rem 0 !important; background-color: var(--secondary-background-color) !important; color: var(--text-color) !important; border-radius: 0 6px 6px 0 !important; }
    .insight-title { color: #8B5CF6; font-size: 1.25rem; font-weight: 800; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.05em; }
    
    .stat-box { background-color: var(--secondary-background-color) !important; border: 1px solid rgba(128, 128, 128, 0.2) !important; border-radius: 6px !important; padding: 15px !important; text-align: center !important; margin-bottom: 15px !important; }
    .stat-value { font-size: 2.0rem !important; font-weight: 700 !important; color: var(--text-color) !important; margin-bottom: 2px !important; line-height: 1 !important;}
    .stat-label { font-size: 0.85rem !important; font-weight: 600 !important; color: var(--text-color) !important; opacity: 0.6 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important;}
    .toc-link { text-decoration: none !important; font-size: 1rem !important; display: block !important; padding: 4px 0 !important; font-weight: 500 !important; color: var(--text-color) !important; opacity: 0.8 !important; transition: opacity 0.2s ease-in-out !important; }
    .toc-link:hover { opacity: 1.0 !important; text-decoration: none !important; }
    /* Mobile-Only Sidebar Hint */
    .mobile-sidebar-hint { display: none; }
    @media (max-width: 768px) {
        .mobile-sidebar-hint {
            display: block !important;
            background-color: rgba(59, 130, 246, 0.1);
            color: #3B82F6;
            padding: 12px;
            border-radius: 8px;
            text-align: center;
            font-weight: 500;
            font-size: 0.95rem;
            margin-top: 25px;
            border: 1px solid rgba(59, 130, 246, 0.3);
            line-height: 1.4;
        }
        
        /* Floating Pointer to the Hamburger Menu */
        .mobile-menu-badge {
            display: block !important;
            position: fixed;
            top: 14px;
            left: 55px; 
            background-color: #2563EB;
            color: white;
            padding: 4px 10px;
            border-radius: 12px;
            font-size: 0.85rem;
            font-weight: 800;
            letter-spacing: 0.05em;
            text-transform: uppercase;
            z-index: 999; /* FIX 1: Lowered so the open sidebar covers it */
            box-shadow: 0 2px 5px rgba(0,0,0,0.2);
            /* FIX 2: Pulses 4 times, then completely fades away after 8 seconds */
            animation: pulse 2s 4, fadeOut 0.5s 8s forwards; 
            pointer-events: none; 
        }
        @keyframes pulse {
            0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(37, 99, 235, 0.7); }
            70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(37, 99, 235, 0); }
            100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(37, 99, 235, 0); }
        }
        @keyframes fadeOut {
            to { opacity: 0; visibility: hidden; }
        }
    }
    .mobile-menu-badge { display: none; } /* Hides it entirely on desktop */
    </style>
""", unsafe_allow_html=True)

# Helper function to load images safely
def render_image(image_path, caption):
    try:
        img = Image.open(image_path)
        st.image(img, caption=caption, use_container_width=True)
    except FileNotFoundError:
        st.error(f"⚠️ Missing Plot: Please ensure `{image_path}` is saved in the directory.")

# ==========================================
# STATIC DATA (From Official Results)
# ==========================================
@st.cache_data
def load_oos_summary():
    return pd.DataFrame({
        'Model': ['Pure Heston (SV)', 'Pure Dupire (LV)', 'Full LSV (SV + LV)'],
        'RMSE ($)': [17.84, 490.11, 19.42],
        'MAE ($)': [12.14, 336.24, 15.78],
        'MAPE (%)': [48.03, 1498.24, 120.68],
        'R² Score': [0.9935, -3.8757, 0.9923]
    })

@st.cache_data
def load_barrier_exotics():
    return pd.DataFrame({
        'Barrier (B)': ['3660', '3660', '3875', '3875'],
        'Maturity': ['0.5y', '1.0y', '0.5y', '1.0y'],
        'LSV (Fair Value)': ['$248.19', '$354.84', '$229.21', '$316.87'],
        'Dupire (LV)': ['$843.95', '$1102.59', '$750.43', '$966.58'],
        'Heston (SV)': ['$255.75', '$358.88', '$237.52', '$320.30'],
        'LV Pricing Error': ['+240.0%', '+210.7%', '+227.4%', '+205.0%'],
        'SV Pricing Error': ['+3.0%', '+1.1%', '+3.6%', '+1.1%']
    })

@st.cache_data
def load_real_3d_leverage_surface():
    """Loads the actual 3D leverage surface exported from the research notebook."""
    try:
        df = pd.read_csv("leverage_surface.csv")
        grid_size = int(np.sqrt(len(df)))
        
        K = df['Strike'].values.reshape(grid_size, grid_size)
        T = df['Expiry'].values.reshape(grid_size, grid_size)
        Z = df['Leverage'].values.reshape(grid_size, grid_size)
        
        fig = go.Figure(data=[go.Surface(
            z=Z, x=K, y=T, 
            colorscale='Viridis', 
            opacity=0.95,
            hovertemplate='Strike: %{x:.0f}<br>Expiry: %{y:.2f}y<br>Leverage: %{z:.3f}<extra></extra>'
        )])
        
        fig.update_layout(
            scene=dict(
                xaxis_title='Strike (K)',
                yaxis_title='Time to Expiry (T)',
                zaxis_title='Leverage L(K, t)',
                camera=dict(eye=dict(x=1.6, y=-1.6, z=0.8))
            ),
            margin=dict(l=0, r=0, b=0, t=20),
            height=550,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        return fig
    except FileNotFoundError:
        return None

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================
with st.sidebar:
    st.title("Research Outline")
    st.markdown("""
    <a href="#0-the-market-problem" target="_self" class="toc-link">0. The Market Problem</a>
    <a href="#1-engine-math-model" target="_self" class="toc-link">1. Engine & Math model</a>
    <a href="#2-markovian-projection" target="_self" class="toc-link">2. Calibration Diagnostics</a>
    <a href="#3-out-of-sample-results" target="_self" class="toc-link">3. Out-Of-Sample Results</a>
    <a href="#4-exotic-barrier-arbitrage" target="_self" class="toc-link">4. Arbitrage & Exotics</a>
    
    
    <div class="mobile-sidebar-hint">
        <strong>Tap outside</strong> or <strong>swipe left</strong> to close menu.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.info(
        "**Author:** Jayesh Chaudhary\n\n"
        "**Role:** Quantitative Researcher\n\n"
    )

# ==========================================
# MAIN DOCUMENT: TITLE & HERO
# ==========================================

# Mobile Tooltip pointing to the Sidebar
st.markdown('<div class="mobile-menu-badge">👈 Topics Menu</div>', unsafe_allow_html=True)

st.markdown("<h1>Local Stochastic Volatility (LSV)</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Bridging Heston and Dupire models for exotic derivatives pricing under realistic volatility dynamics.</p>", unsafe_allow_html=True)

# Small, muted author line under the subtitle
st.markdown("""
    <div style='text-align: center; margin-top: -1.0rem; margin-bottom: 3rem;'>
        <span style='font-size: 1.0rem; color: var(--text-color); opacity: 0.5; font-weight: 400; letter-spacing: 0.15em; text-transform: uppercase;'>
            Research by <strong>Jayesh Chaudhary</strong>
        </span>
    </div>
""", unsafe_allow_html=True)

# Quick Stats Bar (Simplified)
col_a, col_b = st.columns(2)

# Reusable green style templates for a pleasant, eye-friendly look
box_css = "background-color: rgba(16, 185, 129, 0.05); border: 1px solid rgba(16, 185, 129, 0.2); border-radius: 8px; padding: 20px 15px; text-align: center; margin-bottom: 20px;"
val_css = "font-size: 1.8rem; font-weight: 800; color: #10B981; margin-bottom: 6px; line-height: 1;"
lbl_css = "font-size: 0.95rem; font-weight: 700; color: var(--text-color); opacity: 0.7; text-transform: uppercase; letter-spacing: 0.05em;"

with col_a:
    st.markdown(f"<div style='{box_css}'><div style='{lbl_css}'>Underlying Asset</div><div style='{val_css}'>SPX Options</div></div>", unsafe_allow_html=True)
with col_b:
    st.markdown(f"<div style='{box_css}'><div style='{lbl_css}'>Resolution</div><div style='{val_css}'>End-of-Day</div></div>", unsafe_allow_html=True)

    
st.markdown("""
<div class="hero-box">
    <div class="hero-box-title">Project Overview</div>
    <ul>
        <li><strong>Objective:</strong> Standard models Option traders face a persistent model trade-off. Heston gets the future skew right but fails to perfectly match today's prices (introducing basis risk into static hedges). Dupire matches today's prices perfectly but assumes volatility is deterministic (causing massive mispricing on path-dependent exotics).</li>
        <li><strong>Implementation:</strong> Built a vectorized <strong>Quadratic-Exponential (QE) Monte Carlo engine</strong> and calibrated a 2D leverage surface via exact <strong>Gyöngy (1986) Markovian Projection to get the best of both worlds.</strong></li>
        <li><strong>The Stress Test:</strong> Instead of recalibrating daily like a production desk would, I intentionally forced a static Day-1 calibration grid through a 1-week forward market drift. This isolates and measures the structural "grid decay" of the models.</li>
        <li><strong>Use Case:</strong> Priced OTC Down-and-Out Barrier Options, showing how deterministic volatility assumptions (Dupire) lead to significant pricing errors.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ==========================================
# SECTION 0: INTUITION
# ==========================================
st.markdown("<h2 id='0-the-market-problem'><span class='section-badge'>0.</span><span class='h2-text'> The Market Problem</span></h2>", unsafe_allow_html=True)

st.markdown("""
Pricing standard vanilla options is a solved problem. But when pricing Over-The-Counter (OTC) exotics, you need a model that accurately captures **both** today's market prices (for static hedging) and the dynamic evolution of volatility in the future (for dynamic hedging).

### Model Limitations
* **Heston (Stochastic Volatility):** A parametric model that lets variance evolve randomly. It does a great job capturing how volatility dynamically spikes when markets sell off. However, because it only has 5 parameters, it lacks the flexibility to perfectly fit the initial Day 1 market smile.
* **Dupire (Local Volatility):** A non-parametric model that acts like a highly flexible grid, perfectly fitting today's market prices. The catch? It assumes future volatility is 100% determined by time and spot price. When the market actually drops, Dupire's grid fails to capture the sudden dynamic spike in volatility, leaving exotics severely mispriced.

### The LSV model
Think of Local Stochastic Volatility (LSV) as a "multiplier map" overlaid on top of a Heston model. We let Heston run its random variance paths, but at every time-step and strike, we apply a calibrated Leverage Function (the multiplier). This forces the final Monte Carlo distribution to perfectly match today's market prices, while keeping Heston's realistic volatility dynamics alive for the path-dependent future.
""")

st.divider()

# ==========================================
# SECTION 1 & 2: THE ENGINE & CALIBRATION
# ==========================================
st.markdown("<h2 id='1-engine-math-model'><span class='section-badge'>1.</span><span class='h2-text'> Engine & Math model</span></h2>", unsafe_allow_html=True)

col_math1, col_math2 = st.columns(2)
with col_math1:
    render_image("plots/spx_iv_smile.png", "SPX Implied Volatility Smiles (Input Data)")
with col_math2:
    render_image("plots/spx_term_structure.png", "SPX ATM Volatility Term Structure")
    
    

st.markdown("""
Standard Euler discretization is unstable for Heston processes because the variance component ($v_t$) can drift negative. This implementation uses the Andersen (2008) Quadratic-Exponential (QE) scheme to preserve boundary conditions.
The engine is vectorized in NumPy. By replacing SciPy statistical calls with pre-allocated random normal arrays, the engine achieves efficient execution of 15,000 Monte Carlo paths across discrete time steps.
""")

st.markdown("<h2 id='2-markovian-projection'><span class='section-badge'>2.</span><span class='h2-text'> Markovian Projection</span></h2>", unsafe_allow_html=True)

st.markdown("""
LSV relies on calibrating a Leverage Function $L(K, t)$. This is achieved using the **Gyöngy (1986) Theorem**.

The algorithm bins simulated paths to estimate the conditional expectation of variance. Leverage is then defined as the ratio between the target local volatility and this conditional expectation:
""")
st.markdown("""
<div class="math-box">
Gyöngy Projection Formula
</div>
""", unsafe_allow_html=True)
st.latex(r"L(K,t) = \frac{\sigma_{LV}(K,t)}{\sqrt{\mathbb{E}[v_t \mid S_t = K]}}")

col_calib1, col_calib2 = st.columns(2)
with col_calib1:
    render_image("plots/dupire_surface.png", "Dupire Local Volatility Surface (Target)")
with col_calib2:
    render_image("plots/calibration_convergence.png", "L2 Norm Convergence of Leverage Function")

st.markdown("""
<div class="mechanism-box">
<div class="mechanism-title">Calibration & Numerical Stability</div>
<p>To calibrate the engine, we use the <strong>Gyöngy (1986) Theorem</strong>. The engine simulates thousands of paths, estimates the variance, and applies a multiplier to match the Dupire target.</p>
<p><strong>The Heatmap (Left):</strong> This is the theoretical "target" surface we are trying to replicate.<br>
<strong>The Convergence Plot (Right):</strong> This tracks our calibration error over 5 iterations. The sharp downward slope proves the engine is successfully learning the target surface.</p>
<p><strong>The Engineering Challenge:</strong> The Dupire equation requires dividing by the second derivative of call prices. Deep Out-Of-The-Money, this approaches zero, causing local volatility estimates to explode. By applying strict localization and bounds clipping, the engine ensures valid inputs into the Monte Carlo paths without destabilizing.</p>
</div>
""", unsafe_allow_html=True)

# 3D Visual & Density Match
st.markdown("### Calibrated Leverage Function & Density Matching")
col_3d, col_density = st.columns([1.2, 1])
with col_3d:
    fig_3d = load_real_3d_leverage_surface()
    if fig_3d:
        st.plotly_chart(fig_3d, use_container_width=True)
    else:
        st.info("⚠️ Please run the CSV export script in the notebook to generate the 3D leverage surface data (`leverage_surface.csv`).")

with col_density:
    st.markdown("<br>", unsafe_allow_html=True)
    render_image("plots/density_match.png", "Density Matching (LSV MC vs. Dupire Target)")

st.markdown("""
The 3D surface represents the calibrated `Leverage Function`—the spatial multiplier applied to the underlying Heston paths. 

The density chart on the right visualizes a critical production decision. The solid blue Dupire target is highly jagged; taking second derivatives of real-world bid/ask quotes creates extreme microstructure noise. Instead of violently overfitting to these quoting artifacts, our LSV engine applies a 1D Gaussian kernel filter (`sigma=1.5`). The dashed orange line shows the result: the Monte Carlo paths successfully capture the core probability mass of the target distribution while actively filtering out the numerical noise that would otherwise crash the engine.
""")

st.divider()

# ==========================================
# SECTION 3: OUT OF SAMPLE VALIDATION
# ==========================================
st.markdown("<h2 id='3-out-of-sample-results'><span class='section-badge'>3.</span><span class='h2-text'> Out-of-Sample Results</span></h2>", unsafe_allow_html=True)

st.markdown("""
In a production environment, LSV grids are recalculated every morning. However, to truly evaluate the structural integrity of the models, we intentionally "froze" the calibration on **August 16, 2022**, and pushed the models forward across 5 days of unseen market data. This allows us to observe the mechanical degradation of the grids.
""")

st.dataframe(load_oos_summary(), use_container_width=True, hide_index=True)


# Visualizing OOS Errors
st.markdown("### Out-of-Sample Bias & Error Distribution")
col_oos1, col_oos2 = st.columns(2)
with col_oos1:
    render_image("plots/oos_residual_kde.png", "Residual Distribution (Model Bias)")
with col_oos2:
    render_image("plots/oos_error_smile.png", "Pricing Error Smile across Strikes")

st.markdown("""
The plots above reveal the exact nature of the errors. The **Residual KDE (left)** shows that while Dupire suffers from a massive systemic overpricing bias as the market drifts, LSV and Heston residuals remain tightly centered near zero. The **Error Smile (right)** confirms this holds true across the entire strike spectrum.
""")

st.markdown("""
<div class="insight-box">
<div class="insight-title">The Parametric Trade-off</div>
<p>You might notice Heston slightly outperforms LSV out-of-sample on vanillas (RMSE of $17.84 vs $19.42). This is a standard parametric vs. non-parametric trade-off.</p>
<p>Heston's 5 parameters act as a structural regularizer, allowing the model to naturally shift alongside spot price movements ("Sticky Moneyness"). Conversely, LSV relies on a dense grid calibrated specifically to Day 1. As the market drifts, this grid ages (the "Sticky Strike" effect).</p>
<p>Trading desks generally accept this minor multi-day degradation and recalculate the LSV grid daily because an exact fit to the Day 1 smile is mandatory for pricing complex path-dependent exotics.</p>
</div>
""", unsafe_allow_html=True)

st.divider()

# ==========================================
# SECTION 4: EXOTIC ARBITRAGE (THE CONCLUSION)
# ==========================================
st.markdown("<h2 id='4-exotic-barrier-arbitrage'><span class='section-badge'>4.</span><span class='h2-text'> Exotic Barrier Pricing</span></h2>", unsafe_allow_html=True)

st.markdown("""
For OTC derivatives like Down-and-Out Barrier Calls, there is no centralized order book to observe a "true" market price. A reliable internal model is required for quoting and risk management. 

In this analysis, Full LSV is used as the internal benchmark, as it matches observed vanilla prices while retaining stochastic variance dynamics.
""")

st.dataframe(load_barrier_exotics(), use_container_width=True, hide_index=True)

st.markdown("""
Across all configurations, Dupire overprices barrier options by more than 200%, while Heston and LSV remain within a few percent of each other.
""")

st.markdown("""
<div class="mechanism-box">
<div class="mechanism-title">The Cost of Deterministic Volatility</div>
<p>Equity indices generally exhibit a negative spot-volatility correlation. If the SPX drops toward the barrier, market volatility structurally increases. This higher volatility raises the probability that the asset price breaches the knock-out level, rendering the option worthless.</p>
<p>LSV captures this dynamic, resulting in a lower option premium. Dupire LV, assuming deterministic volatility, underestimates the probability of a barrier breach. Utilizing a pure Local Volatility model in this context leads to systematic overpricing, exposing the desk to adverse selection and persistent hedging losses.</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")


st.markdown("""
<div class="findings-box">
<div class="findings-title">Conclusion</div>
<ul>
<li><strong>LSV Efficacy:</strong> The LSV model successfully matches execution-day vanilla prices while maintaining necessary forward volatility dynamics.</li>
<li><strong>Engine Stability:</strong> Exact Gyöngy Markovian Projection with boundary controls is required to prevent leverage function degradation.</li>
<li><strong>Production Use:</strong> While parametric models show slight out-of-sample resilience for vanillas, the non-parametric LSV grid is critical to avoid structural pricing errors in OTC exotics.</li>
</ul>
</div>
""", unsafe_allow_html=True)


st.markdown("""
<div style='text-align: center; margin-top: 50px; padding-top: 20px; border-bottom: 1px solid rgba(128, 128, 128, 0.2);'>
    <p style='font-size: 1.15rem; color: #6B7280; font-style: italic;'>
        If you made it all the way to the end, thank you for viewing my work. <br>
        I am always looking to refine these projects, so if you have critiques, suggestions, or just want to talk market dynamics, I'd love to hear them:
    </p>
    <a href='mailto:jayeshchaudharyofficial@gmail.com' style='font-size: 1.15rem; font-weight: 700; color: #FFFFFF; background-color: #3B82F6; padding: 10px 24px; border-radius: 6px; text-decoration: none; display: inline-block; transition: all 0.2s; margin-bottom: 30px;'>
        ✉️ Email Me
    </a>
</div>
""", unsafe_allow_html=True)
