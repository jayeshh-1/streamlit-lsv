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
    .main { max-width: 1100px; margin: 0 auto; font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; }
    h1 { text-align: center; font-size: 2.6rem !important; font-weight: 800 !important; margin-bottom: 0.5rem !important; line-height: 1.25 !important; color: var(--text-color) !important; letter-spacing: -0.02em !important; }
    .subtitle { text-align: center; font-size: 1.15rem !important; color: var(--text-color) !important; opacity: 0.75 !important; font-style: italic !important; margin-bottom: 2.5rem !important; font-weight: 400 !important; }
    h2 { font-weight: 700 !important; font-size: 1.8rem !important; margin-top: 3.5rem !important; border-bottom: 2px solid var(--secondary-background-color) !important; padding-bottom: 0.5rem !important; margin-bottom: 1.5rem !important; color: var(--text-color) !important; letter-spacing: -0.01em !important; }
    h3 { font-weight: 600 !important; font-size: 1.3rem !important; margin-top: 2rem !important; margin-bottom: 1rem !important; color: var(--text-color) !important; opacity: 0.9 !important; }
    div[data-testid="stMarkdownContainer"] p, div[data-testid="stMarkdownContainer"] li { font-size: 1.1rem !important; line-height: 1.6 !important; font-weight: 400 !important; color: var(--text-color) !important; opacity: 0.85 !important; } 
    div[data-testid="stMarkdownContainer"] li { margin-bottom: 0.5rem !important; }
    div[data-testid="stMarkdownContainer"] strong { font-weight: 600 !important; color: var(--text-color) !important; opacity: 1.0 !important; }
    .section-badge { background-color: #3B82F6; color: #FFFFFF !important; padding: 4px 12px; border-radius: 4px; font-size: 1.0rem; vertical-align: middle; margin-right: 12px; font-weight: 700; letter-spacing: 0.05em; text-transform: uppercase; display: inline-block; transform: translateY(-2px); }
    .hero-box { background-color: var(--secondary-background-color); border: 1px solid rgba(128, 128, 128, 0.2); border-radius: 6px; padding: 20px 25px; margin: 1.5rem 0 2.5rem 0; }
    .hero-box-title { font-size: 1.2rem; font-weight: 700; color: #3B82F6; margin-bottom: 10px; text-transform: uppercase; letter-spacing: 0.05em; }
    .math-box { text-align: center; font-size: 0.95rem; color: var(--text-color); opacity: 0.6; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: -10px; margin-top: 1.5rem; font-weight: 600; }
    .findings-box { border-left: 4px solid #10B981 !important; padding: 1.2rem !important; margin: 2rem 0 !important; background-color: var(--secondary-background-color) !important; border-radius: 0 6px 6px 0 !important; }
    .findings-title { font-size: 1.2rem; font-weight: 700; margin-bottom: 10px; color: #10B981; text-transform: uppercase; letter-spacing: 0.05em; }
    .pipeline-container { display: flex; justify-content: space-between; align-items: center; margin: 2rem 0; gap: 8px; }
    .pipeline-block { background-color: var(--secondary-background-color); padding: 12px; border-radius: 6px; text-align: center; flex: 1; border: 1px solid rgba(128, 128, 128, 0.2); }
    .pipeline-block-title { font-size: 0.85rem; font-weight: 700; text-transform: uppercase; margin-bottom: 4px; color: #3B82F6; }
    .pipeline-block-desc { font-size: 0.9rem; opacity: 0.8; }
    .pipeline-arrow { font-size: 1.2rem; opacity: 0.3; }
    .mechanism-box { border-left: 4px solid #3B82F6 !important; padding: 1.2rem !important; margin: 1.5rem 0 !important; background-color: var(--secondary-background-color) !important; border-radius: 0 6px 6px 0 !important; }
    .insight-box { border-left: 4px solid #8B5CF6 !important; padding: 1.2rem !important; margin: 1.5rem 0 !important; background-color: rgba(139, 92, 246, 0.05) !important; color: #6d28d9 !important; border-radius: 0 6px 6px 0 !important; }
    .stat-box { background-color: var(--secondary-background-color) !important; border: 1px solid rgba(128, 128, 128, 0.2) !important; border-radius: 6px !important; padding: 15px !important; text-align: center !important; margin-bottom: 15px !important; }
    .stat-value { font-size: 2.0rem !important; font-weight: 700 !important; color: var(--text-color) !important; margin-bottom: 2px !important; line-height: 1 !important;}
    .stat-label { font-size: 0.85rem !important; font-weight: 600 !important; color: var(--text-color) !important; opacity: 0.6 !important; text-transform: uppercase !important; letter-spacing: 0.05em !important;}
    .toc-link { text-decoration: none !important; font-size: 0.95rem !important; display: block !important; padding: 4px 0 !important; font-weight: 500 !important; color: var(--text-color) !important; opacity: 0.8 !important; transition: opacity 0.2s ease-in-out !important; }
    .toc-link:hover { opacity: 1.0 !important; text-decoration: none !important; }
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
    <a href="#0-the-market-problem" class="toc-link">0. The Market Problem</a>
    <a href="#1-engine-math-model" class="toc-link">1. Engine & Math model</a>
    <a href="#2-markovian-projection" class="toc-link">2. Calibration Diagnostics</a>
    <a href="#3-out-of-sample-results" class="toc-link">3. Out-Of-Sample Results</a>
    <a href="#4-exotic-barrier-arbitrage" class="toc-link">4. Arbitrage & Exotics</a>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.info(
        "**Author:** Jayesh Chaudhary\n\n"
        "**Role:** Quantitative Researcher\n\n"
    )

# ==========================================
# MAIN DOCUMENT: TITLE & HERO
# ==========================================
st.markdown("<h1>Local Stochastic Volatility (LSV)</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Bridging Heston and Dupire models for exotic derivatives pricing under realistic volatility dynamics.</p>", unsafe_allow_html=True)

st.markdown("""
<div class="hero-box">
    <div class="hero-box-title">Project Overview</div>
    <ul>
        <li><strong>Objective:</strong> Standard models face a structural trade-off. Heston misprices initial static hedges, while Dupire fails to capture forward volatility dynamics. We build an LSV model to reconcile the mismatch between static smile fit and forward volatility dynamics.</li>
        <li><strong>Implementation:</strong> Built a vectorized <strong>Quadratic-Exponential (QE) Monte Carlo engine</strong> and calibrated a 2D leverage surface via exact <strong>Gyöngy (1986) Markovian Projection</strong>.</li>
        <li><strong>Validation:</strong> Evaluated the model across 5 out-of-sample days, confirming the expected parametric resilience of Heston versus the grid decay of Local Volatility.</li>
        <li><strong>Use Case:</strong> Priced OTC Down-and-Out Barrier Options, showing how deterministic volatility assumptions (Dupire) lead to significant pricing errors.</li>
    </ul>
</div>
""", unsafe_allow_html=True)

# ==========================================
# SECTION 0: INTUITION
# ==========================================
st.markdown("<h2 id='0-the-market-problem'><span class='section-badge'>Phase 0</span> The Market Problem</h2>", unsafe_allow_html=True)

st.markdown("""
Vanilla option pricing is a well-understood problem. However, pricing Over-The-Counter (OTC) exotics requires models that accurately capture both the current market surface and future volatility dynamics.

### Model Limitations
* **Heston (Stochastic Volatility):** Captures forward skew by allowing variance to evolve stochastically. However, its 5-parameter formulation limits its ability to exactly fit the Day 1 vanilla smile, introducing basis risk into static hedging portfolios.
* **Dupire (Local Volatility):** Provides an exact fit to the initial market smile via a non-parametric grid. However, it assumes volatility is deterministic, flattening the forward skew and misestimating tail risks during market sell-offs.

### The LSV model
Local Stochastic Volatility (LSV) calibrates a spatial leverage function over an underlying Heston process. This combination forces the model's marginal distributions to match the market's vanilla prices today, while maintaining realistic variance dynamics for the future.
""")


st.divider()

# ==========================================
# SECTION 1 & 2: THE ENGINE & CALIBRATION
# ==========================================
st.markdown("<h2 id='1-engine-math-model'><span class='section-badge'>Phase 1</span> Engine & Math model</h2>", unsafe_allow_html=True)

col_math1, col_math2 = st.columns(2)
with col_math1:
    render_image("plots/spx_iv_smile.png", "SPX Implied Volatility Smiles (Input Data)")
with col_math2:
    render_image("plots/spx_term_structure.png", "SPX ATM Volatility Term Structure")

st.markdown("""
Standard Euler discretization is unstable for Heston processes because the variance component ($v_t$) can drift negative. This implementation uses the Andersen (2008) Quadratic-Exponential (QE) scheme to preserve boundary conditions.
The engine is vectorized in NumPy. By replacing SciPy statistical calls with pre-allocated random normal arrays, the engine achieves efficient execution of 80,000 Monte Carlo paths across discrete time steps.
""")

st.markdown("<h2 id='2-markovian-projection'><span class='section-badge'>Phase 2</span> Markovian Projection</h2>", unsafe_allow_html=True)

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
<strong>Numerical Stability Control</strong><br>
The Dupire equation requires dividing by the second derivative of call prices with respect to strike. Deep Out-Of-The-Money, this approaches zero, causing local volatility estimates to destabilize. The engine applies strict localization and bounds clipping to ensure valid inputs into the Monte Carlo paths.
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

st.markdown("The 3D surface represents the calibrated multiplier applied to the stochastic variance process. The density matching chart confirms that the Markovian projection successfully aligns the Monte Carlo terminal distributions with the theoretical target.")

st.divider()

# ==========================================
# SECTION 3: OUT OF SAMPLE VALIDATION
# ==========================================
st.markdown("<h2 id='3-out-of-sample-results'><span class='section-badge'>Phase 3</span> Out-of-Sample Results</h2>", unsafe_allow_html=True)

st.markdown("""
To evaluate model stability, the Leverage Function was calibrated on **August 16, 2022**, and then tested out-of-sample against market prices over the following 5 trading sessions.
""")

st.dataframe(load_oos_summary(), use_container_width=True, hide_index=True)

st.markdown("""
<div class="insight-box">
<strong>The Parametric Trade-off</strong><br>
You might notice Heston slightly outperforms LSV out-of-sample on vanillas (RMSE of $17.84 vs $19.42). This is a standard parametric vs. non-parametric trade-off.<br><br>
Heston's 5 parameters act as a structural regularizer, allowing the model to naturally shift alongside spot price movements ("Sticky Moneyness"). Conversely, LSV relies on a dense grid calibrated specifically to Day 1. As the market drifts, this grid ages (the "Sticky Strike" effect).<br><br>
Trading desks generally accept this minor multi-day degradation—and recalculate the LSV grid daily—because an exact fit to the Day 1 smile is mandatory for pricing complex path-dependent exotics.
</div>
""", unsafe_allow_html=True)

st.divider()

# ==========================================
# SECTION 4: EXOTIC ARBITRAGE (THE CONCLUSION)
# ==========================================
st.markdown("<h2 id='4-exotic-barrier-arbitrage'><span class='section-badge'>Phase 4</span> Exotic Barrier Pricing</h2>", unsafe_allow_html=True)

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
<strong>The Cost of Deterministic Volatility:</strong><br>
Equity indices generally exhibit a negative spot-volatility correlation. If the SPX drops toward the barrier, market volatility structurally increases. This higher volatility raises the probability that the asset price breaches the knock-out level, rendering the option worthless.<br><br>
LSV captures this dynamic, resulting in a lower option premium. Dupire LV, assuming deterministic volatility, underestimates the probability of a barrier breach. Utilizing a pure Local Volatility model in this context leads to systematic overpricing, exposing the desk to adverse selection and persistent hedging losses.
</div>
""", unsafe_allow_html=True)

st.markdown("### Key Takeaways")


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
