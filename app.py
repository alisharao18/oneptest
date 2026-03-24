# Function for 1 sample p-test
import numpy as np
from scipy.stats import norm
import streamlit as st

st.set_page_config(page_title="Alisha's 1-Sample Proportion Z-Test", page_icon="📊")

def oneptest(n,p,p_hat,sig,alternative):
    q = 1-p
    se = np.sqrt((p*q)/n)
    z_cal = (p_hat - p) / se
    #df = n-1

    if(alternative == 'two-sided'):
        z_pos = norm.ppf(1 - (sig/2))
        z_neg = norm.ppf((sig/2))
        p_value = 2 * (1 - norm.cdf(abs(z_cal)))
        dictt = {'z_calculated':z_cal,'z_positive':z_pos,'z_negative':z_neg,'p-value':p_value}
        return dictt
    elif(alternative == 'lesser'):
        z_neg = norm.ppf(sig)
        p_value = norm.cdf(z_cal)
        dictt = {'z_calculated':z_cal,'z_negative':z_neg,'p-value':p_value}
        return dictt
    elif(alternative == 'greater'):
        z_pos = norm.ppf(1-sig)
        p_value = 1 - norm.cdf(z_cal)
        dictt = {'z_calculated':z_cal,'z_positive':z_pos,'p-value':p_value}
        return dictt
    
# ── UI ────────────────────────────────────────────────────────────────────────
st.title("📊 1-Sample Proportion Z-Test")
st.markdown("Test whether a population proportion equals a hypothesized value.")
 
st.divider()
 
# inputs
col1, col2 = st.columns(2)
 
with col1:
    n = st.number_input("Sample Size (n)", min_value=1, value=6000, step=1)
    p = st.number_input("Hypothesized Proportion (p₀)", min_value=0.0, max_value=1.0, value=0.05, step=0.01)
 
with col2:
    x = st.number_input("Number of Successes (x)", min_value=0, value=335, step=1)
    sig = st.number_input("Significance Level (α)", min_value=0.01, max_value=0.20, value=0.05, step=0.01)
 
alternative = st.selectbox(
    "Alternative Hypothesis (Hₐ)",
    options=['two-sided', 'greater', 'lesser'],
    format_func=lambda x: {
        'two-sided': 'Two-sided: p ≠ p₀',
        'greater':   'Right-tailed: p > p₀',
        'lesser':    'Left-tailed: p < p₀'
    }[x]
)
 
st.divider()
 
# ── run test ──────────────────────────────────────────────────────────────────
if st.button("Run Z-Test", type="primary", use_container_width=True):
 
    p_hat = x / n
 
    # check np >= 5 and nq >= 5
    if n * p < 5 or n * (1 - p) < 5:
        st.warning("⚠️ Condition np ≥ 5 and nq ≥ 5 not met. Z-test may not be valid.")
 
    result = oneptest(n, p, p_hat, sig, alternative)
 
    # ── metrics ───────────────────────────────────────────────────────────────
    st.subheader("Results")
 
    m1, m2, m3 = st.columns(3)
    m1.metric("Sample Proportion (p̂)", f"{p_hat:.4f}")
    m2.metric("Z Calculated", f"{result['z_calculated']:.4f}")
    m3.metric("P-Value", f"{result['p-value']:.4f}")
 
    # ── critical values ───────────────────────────────────────────────────────
    st.subheader("Critical Values")
    cv1, cv2 = st.columns(2)
    if 'z_positive' in result:
        cv1.metric("Z positive", f"{result['z_positive']:.4f}")
    if 'z_negative' in result:
        cv2.metric("Z negative", f"{result['z_negative']:.4f}")
 
    # ── decision ──────────────────────────────────────────────────────────────
    st.subheader("Decision")
    p_value = result['p-value']
 
    if p_value < sig:
        st.success(f"✅ Reject H₀  —  p-value ({p_value:.4f}) < α ({sig})")
    else:
        st.error(f"❌ Fail to Reject H₀  —  p-value ({p_value:.4f}) ≥ α ({sig})")
 
    # ── hypotheses reminder ───────────────────────────────────────────────────
    with st.expander("Hypotheses"):
        st.markdown(f"**H₀ :** p = {p}")
        labels = {
            'two-sided': f"p ≠ {p}",
            'greater':   f"p > {p}",
            'lesser':    f"p < {p}"
        }
        st.markdown(f"**Hₐ :** {labels[alternative]}")