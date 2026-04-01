import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# ── Page config (must be first st call) ──
st.set_page_config(page_title="EcoFolio", page_icon="🌱", layout="wide")

# ------------------------------
# Profile mappings (same as console version)
# ------------------------------
risk_profile_map = {
    "Cautious": 8,
    "Conservative": 5,
    "Balanced": 3,
    "Assertive": 1.5,
    "Aggressive": 0.75
}

esg_profile_map = {
    "Traditional Investor": 0.1,
    "ESG Aware Investor": 0.3,
    "Balanced Investor": 0.5,
    "Strong ESG Preference Investor": 0.7,
    "ESG-Focused Investor": 0.9
}

# ------------------------------
# Portfolio functions (same as console version)
# ------------------------------
def portfolio_ret(w1, r1, r2):
    return w1 * r1 + (1 - w1) * r2

def portfolio_sd(w1, sd1, sd2, rho):
    return np.sqrt(w1**2 * sd1**2 + (1-w1)**2 * sd2**2 + 2 * rho * w1 * (1-w1) * sd1 * sd2)

# ------------------------------
# ESG classification (same thresholds as console version)
# ------------------------------
def classify_esg(total):
    if total <= 8:
        return ("Traditional Investor",
                "ESG factors are not a primary consideration in your investment decisions. "
                "Your approach focuses mainly on financial performance, with limited emphasis "
                "on environmental, social, or governance aspects.")
    elif total <= 14:
        return ("ESG Aware Investor",
                "ESG factors are considered in your investment decisions, particularly in "
                "identifying and avoiding potential risks. However, they are not a central "
                "driver of your overall investment strategy.")
    elif total <= 20:
        return ("Balanced Investor",
                "ESG factors play a meaningful role in your investment approach alongside "
                "financial considerations. You aim to balance performance objectives with "
                "an interest in sustainability.")
    elif total <= 26:
        return ("Strong ESG Preference Investor",
                "ESG considerations are an important part of your investment decisions. "
                "You tend to favour investments with stronger sustainability characteristics, "
                "while still considering financial outcomes.")
    else:
        return ("ESG-Focused Investor",
                "ESG outcomes are a central component of your investment approach. "
                "Your decisions place significant weight on environmental and social impact, "
                "alongside financial considerations.")

# ------------------------------
# Risk classification (same thresholds as console version)
# ------------------------------
def classify_risk(total):
    if total <= 8:
        return ("Cautious",
                "You place strong importance on stability and are less comfortable with large investment losses.")
    elif total <= 14:
        return ("Conservative",
                "You are willing to take some risk, but protecting your capital remains a higher priority.")
    elif total <= 20:
        return ("Balanced",
                "You seek a middle ground between stability and growth, accepting some volatility for better returns.")
    elif total <= 26:
        return ("Assertive",
                "You are comfortable taking on more risk in pursuit of stronger long term growth.")
    else:
        return ("Aggressive",
                "You are highly comfortable with market fluctuations and prioritise maximising returns over short term stability.")

# ══════════════════════════════════════════════
# STREAMLIT UI
# ══════════════════════════════════════════════

# Header
st.title("🌱 EcoFolio")
st.caption("Sustainable Finance Portfolio Optimiser")
st.markdown("Build a personalised investment portfolio based on your financial risk tolerance **and** ESG preferences.")
st.divider()

# ── SIDEBAR: Asset Parameters ──
with st.sidebar:
    st.header("📊 Asset Parameters")

    st.subheader("Asset 1")
    asset1_name = st.text_input("Name", value="Tech ETF", key="a1n")
    r_h = st.number_input("Expected Return (%)", value=5.0, key="a1r") / 100
    sd_h = st.number_input("Standard Deviation (%)", value=9.0, min_value=0.01, key="a1s") / 100
    esg_h = st.slider("ESG Score (0-100)", 0, 100, 60, key="a1e")

    st.subheader("Asset 2")
    asset2_name = st.text_input("Name", value="Green Bond", key="a2n")
    r_f = st.number_input("Expected Return (%)", value=12.0, key="a2r") / 100
    sd_f = st.number_input("Standard Deviation (%)", value=20.0, min_value=0.01, key="a2s") / 100
    esg_f = st.slider("ESG Score (0-100)", 0, 100, 60, key="a2e")

    st.subheader("Shared Parameters")
    rho_hf = st.slider("Correlation", -1.0, 1.0, -0.20, 0.01)
    r_free = st.number_input("Risk-Free Rate (%)", value=2.0) / 100

# ── TABS ──
tab_home, tab_esg, tab_risk, tab_results, tab_chart = st.tabs(
    ["🏠 Home", "🌿 ESG Questionnaire", "📉 Risk Questionnaire",
     "📋 Portfolio Results", "📈 Visualisation"]
)

# ── HOME TAB ──
with tab_home:
    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("🌿 ESG Questionnaire")
        st.write("Discover your sustainability profile through 3 quick questions.")
    with c2:
        st.subheader("📉 Risk Questionnaire")
        st.write("Find out your risk tolerance and investment style.")
    with c3:
        st.subheader("📋 Results & 📈 Chart")
        st.write("See your optimal portfolio, comparison table, and interactive chart.")

# ── ESG QUESTIONNAIRE TAB ──
with tab_esg:
    st.header("🌿 ESG Questionnaire")
    st.write("Rate each factor from **1** (not important at all) to **10** (extremely important).")

    env_score = st.slider(
        "1. How important is environmental sustainability "
        "(e.g. carbon reduction, pollution control, resource efficiency) "
        "when making your investment decisions, even if it reduces your returns?",
        1, 10, 5, key="eq1")

    social_score = st.slider(
        "2. How important are social factors "
        "(e.g. labour practices, diversity, community impact) "
        "when making your investment decisions, even if it reduces your returns?",
        1, 10, 5, key="eq2")

    gov_score = st.slider(
        "3. How important is strong corporate governance "
        "(e.g. transparency, accountability, ethical leadership) "
        "when making your investment decisions, even if it reduces your returns?",
        1, 10, 5, key="eq3")

    total_esg_score = env_score + social_score + gov_score
    esg_profile, esg_description = classify_esg(total_esg_score)
    lambda_esg = esg_profile_map[esg_profile]

    st.divider()
    st.metric("Your ESG Score", "{} / 30".format(total_esg_score))
    st.success("**{}** — {}".format(esg_profile, esg_description))
    st.caption("ESG preference coefficient (lambda) = {}".format(lambda_esg))

# ── RISK QUESTIONNAIRE TAB ──
with tab_risk:
    st.header("📉 Risk Profile Questionnaire")
    st.write("Rate each statement from **1** to **10**.")

    q1 = st.slider(
        "1. If your investment fell by 10% in a short period, how would you react? "
        "(1 = Sell immediately · 10 = Hold / invest more)",
        1, 10, 5, key="rq1")

    q2 = st.slider(
        "2. Which matters more to you when investing? "
        "(1 = Minimise risk & protect capital · 10 = Maximise returns even with higher risk)",
        1, 10, 5, key="rq2")

    q3 = st.slider(
        "3. How comfortable are you with significant price fluctuations? "
        "(1 = Very uncomfortable · 10 = Very comfortable)",
        1, 10, 5, key="rq3")

    total_risk_score = q1 + q2 + q3
    risk_profile, risk_description = classify_risk(total_risk_score)
    gamma_risk = risk_profile_map[risk_profile]

    st.divider()
    st.metric("Your Risk Score", "{} / 30".format(total_risk_score))
    st.info("**{}** — {}".format(risk_profile, risk_description))
    st.caption("Risk aversion coefficient (gamma) = {}".format(gamma_risk))

# ══════════════════════════════════════════════
# COMPUTATION (same logic as console version)
# ══════════════════════════════════════════════

# --- Tangency Portfolio ---
weights_frontier = np.linspace(0, 1, 1000)
sharpe_ratios = []

for w in weights_frontier:
    ret = portfolio_ret(w, r_h, r_f)
    sd = portfolio_sd(w, sd_h, sd_f, rho_hf)
    if sd > 0:
        sharpe_ratios.append((ret - r_free) / sd)
    else:
        sharpe_ratios.append(-np.inf)

max_idx = np.argmax(sharpe_ratios)
w1_tangency = weights_frontier[max_idx]
w2_tangency = 1 - w1_tangency
ret_tangency = portfolio_ret(w1_tangency, r_h, r_f)
sd_tangency = portfolio_sd(w1_tangency, sd_h, sd_f, rho_hf)

# --- Optimal Portfolio (Utility Maximisation with ESG) ---
weights_cml = np.linspace(0, 1.5, 1000)
utilities = []
returns_list = []
risks_list = []
esg_scores_list = []

for w in weights_cml:
    w1 = w * w1_tangency
    w2 = w * w2_tangency
    w_rf = 1 - w
    ret = r_free + w * (ret_tangency - r_free)
    sd = abs(w) * sd_tangency
    esg = w1 * esg_h + w2 * esg_f
    utility = ret - 0.5 * gamma_risk * sd**2 + lambda_esg * (esg / 100)
    utilities.append(utility)
    returns_list.append(ret)
    risks_list.append(sd)
    esg_scores_list.append(esg)

optimal_idx = np.argmax(utilities)
w_optimal = weights_cml[optimal_idx]
w1_optimal = w_optimal * w1_tangency
w2_optimal = w_optimal * w2_tangency
w_rf_optimal = 1 - w_optimal
ret_optimal = returns_list[optimal_idx]
sd_optimal = risks_list[optimal_idx]
esg_optimal = esg_scores_list[optimal_idx]
utility_optimal = utilities[optimal_idx]

# --- Derived Metrics ---
pri_score = (esg_optimal / 100) * 100
sharpe_optimal = (ret_optimal - r_free) / sd_optimal if sd_optimal > 0 else 0
sharpe_esg = (ret_optimal + lambda_esg * (esg_optimal / 100) - r_free) / sd_optimal if sd_optimal > 0 else 0

if esg_optimal >= 70:
    esg_level = "High ESG Impact"
elif esg_optimal >= 40:
    esg_level = "Medium ESG Impact"
else:
    esg_level = "Low ESG Impact"

esg_tangency = w1_tangency * esg_h + w2_tangency * esg_f
delta_ret = ret_tangency - ret_optimal
delta_esg = esg_optimal - esg_tangency

# --- Frontier data for chart ---
frontier_returns = []
frontier_risks = []
frontier_esg = []
for w in weights_frontier:
    ret = portfolio_ret(w, r_h, r_f)
    sd = portfolio_sd(w, sd_h, sd_f, rho_hf)
    esg = w * esg_h + (1 - w) * esg_f
    frontier_returns.append(ret * 100)
    frontier_risks.append(sd * 100)
    frontier_esg.append(esg)

frontier_returns = np.array(frontier_returns)
frontier_risks = np.array(frontier_risks)
frontier_esg = np.array(frontier_esg)
max_esg_frontier_idx = np.argmax(frontier_esg)

# ══════════════════════════════════════════════
# RESULTS TAB
# ══════════════════════════════════════════════

with tab_results:
    st.header("📋 ESG-Aware Optimal Portfolio")

    # --- Portfolio Weights ---
    st.subheader("Portfolio Weights")
    c1, c2, c3 = st.columns(3)
    c1.metric("Risk-Free Asset", "{:.2f}%".format(w_rf_optimal * 100))
    c2.metric(asset1_name, "{:.2f}%".format(w1_optimal * 100))
    c3.metric(asset2_name, "{:.2f}%".format(w2_optimal * 100))

    st.divider()

    # --- Financial Performance ---
    st.subheader("Financial Performance")
    m1, m2, m3, m4, m5 = st.columns(5)
    m1.metric("Utility Score", "{:.4f}".format(utility_optimal))
    m2.metric("Expected Return", "{:.2f}%".format(ret_optimal * 100))
    m3.metric("Risk (Std Dev)", "{:.2f}%".format(sd_optimal * 100))
    m4.metric("Sharpe Ratio", "{:.3f}".format(sharpe_optimal))
    m5.metric("ESG-adj Sharpe", "{:.3f}".format(sharpe_esg))

    st.divider()

    # --- Sustainability Metrics ---
    st.subheader("Sustainability Metrics")
    s1, s2, s3 = st.columns(3)
    s1.metric("Portfolio ESG Score", "{:.2f}".format(esg_optimal))
    s2.metric("PRI Score", "{:.2f}".format(pri_score))
    s3.metric("Impact Level", esg_level)

    st.divider()

    # --- Trade-off ---
    st.subheader("Return vs Sustainability Trade-off")
    if delta_ret > 0 and delta_esg > 0:
        st.warning(
            "You sacrifice **{:.2f}% return** for **+{:.2f} ESG points** "
            "compared to the Max Sharpe portfolio.".format(delta_ret * 100, delta_esg))
    elif delta_ret > 0 and delta_esg <= 0:
        st.info(
            "Return difference vs tangency: **{:.2f}%**. "
            "ESG difference: **{:.2f} points**.".format(-delta_ret * 100, delta_esg))
    else:
        st.success(
            "Your optimal portfolio gains **+{:.2f}% return** and **+{:.2f} ESG points** "
            "vs the tangency portfolio.".format(-delta_ret * 100, delta_esg))

    st.divider()

    # --- Interpretation ---
    st.subheader("📖 Portfolio Interpretation")

    st.markdown(
        "The recommended portfolio reflects your selected risk tolerance "
        "and sustainability preferences."
    )
    st.markdown(
        "Based on your preferences, the model maximises a utility function "
        "that balances expected return, portfolio risk, and ESG impact."
    )
    st.markdown(
        "The portfolio delivers an expected return of **{:.2f}%** "
        "with a volatility of **{:.2f}%**.".format(ret_optimal * 100, sd_optimal * 100)
    )
    st.markdown(
        "The Sharpe ratio of **{:.2f}** indicates the "
        "risk-adjusted financial performance of the portfolio.".format(sharpe_optimal)
    )
    st.markdown(
        "When ESG preferences are incorporated, the ESG-adjusted Sharpe ratio "
        "is **{:.2f}**, reflecting sustainability-adjusted performance.".format(sharpe_esg)
    )
    st.markdown(
        "The portfolio ESG score is **{:.2f}**, "
        "corresponding to a **{}**.".format(esg_optimal, esg_level.lower())
    )
    st.markdown(
        "This produces a PRI score of **{:.2f}**, "
        "indicating the overall sustainability alignment of the portfolio.".format(pri_score)
    )
    if delta_ret > 0:
        st.markdown(
            "Relative to the maximum Sharpe ratio portfolio, you sacrifice "
            "**{:.2f}%** of expected return in exchange for "
            "an ESG improvement of **{:.2f}** points.".format(delta_ret * 100, delta_esg)
        )
    st.markdown(
        "Overall, the allocation balances financial performance "
        "with sustainability preferences in line with your questionnaire responses."
    )

# ══════════════════════════════════════════════
# CHART TAB
# ══════════════════════════════════════════════

with tab_chart:
    st.header("📈 Portfolio Visualisation")

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6.5))

    # ── LEFT: ESG-Efficient Frontier ──
    scatter = ax1.scatter(frontier_risks, frontier_returns, c=frontier_esg,
                          cmap="RdYlGn", s=8, zorder=2, label="Frontier portfolios")
    cbar = fig.colorbar(scatter, ax=ax1, pad=0.02)
    cbar.set_label("ESG Score", fontsize=10)

    # CML
    max_sharpe_ratio = (ret_tangency - r_free) / sd_tangency if sd_tangency > 0 else 0
    cml_x_max = max(frontier_risks) * 1.2
    ax1.plot([0, cml_x_max],
             [r_free * 100, r_free * 100 + max_sharpe_ratio * cml_x_max],
             "--", color="grey", linewidth=1, alpha=0.7, label="CML", zorder=1)

    # Risk-free
    ax1.scatter([0], [r_free * 100], color="blue", s=100, marker="o",
                edgecolors="black", zorder=5,
                label="Risk-Free ({:.1f}%)".format(r_free * 100))

    # Tangency / Max Sharpe
    ax1.scatter([sd_tangency * 100], [ret_tangency * 100], color="gold", s=180,
                marker="D", edgecolors="black", linewidths=0.8, zorder=5,
                label="Tangency / Max Sharpe")

    # Max ESG
    ax1.scatter([frontier_risks[max_esg_frontier_idx]],
                [frontier_returns[max_esg_frontier_idx]],
                color="green", s=180, marker="^", edgecolors="black",
                linewidths=0.8, zorder=5, label="Max ESG")

    # Optimal
    ax1.scatter([sd_optimal * 100], [ret_optimal * 100], color="red", s=280,
                marker="*", edgecolors="black", linewidths=0.8, zorder=6,
                label="Optimal (w1={:.1f}%)".format(w1_optimal * 100))

    ax1.set_xlabel("Portfolio Std Dev (%)", fontsize=11)
    ax1.set_ylabel("Expected Return (%)", fontsize=11)
    ax1.set_title("ESG-Efficient Frontier: Risk vs Return", fontsize=13, fontweight="bold")
    ax1.legend(loc="upper left", fontsize=7.5, framealpha=0.9)
    ax1.grid(True, alpha=0.3)

    # ── RIGHT: Utility vs Weight ──
    weights_pct = np.linspace(0, 1.5, 1000) * 100
    ax2.plot(weights_pct, utilities, color="#1f77b4", linewidth=2, label="Utility")

    opt_w_pct = w_optimal * 100
    ax2.axvline(x=opt_w_pct, color="red", linestyle="--", linewidth=1,
                label="Optimal w = {:.1f}%".format(opt_w_pct))
    ax2.scatter([opt_w_pct], [utility_optimal], color="red", s=200, marker="*",
                edgecolors="black", linewidths=0.8, zorder=5)

    ax2.set_xlabel("Weight in {} (%)".format(asset1_name), fontsize=11)
    ax2.set_ylabel("Utility (ESG-adjusted)", fontsize=11)
    ax2.set_title("Utility Function vs Portfolio Weight", fontsize=13, fontweight="bold")
    ax2.legend(loc="best", fontsize=9)
    ax2.grid(True, alpha=0.3)

    fig.tight_layout()
    st.pyplot(fig, use_container_width=True)
    plt.close(fig)
