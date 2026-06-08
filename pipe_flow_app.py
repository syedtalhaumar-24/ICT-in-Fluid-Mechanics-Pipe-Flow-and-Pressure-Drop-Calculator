import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(
    page_title="Pipe Flow & Pressure Drop Calculator",
    page_icon="💧",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cinzel:wght@400;600;700;900&family=Crimson+Text:ital,wght@0,400;0,600;1,400&display=swap');

.stApp { background: linear-gradient(135deg, #060D1A 0%, #0A1628 50%, #0D1F3C 100%); color: #F0E6CC; }
[data-testid="stSidebar"] { background: linear-gradient(180deg, #060D1A 0%, #0A1628 100%); border-right: 1px solid #C9A84C44; }

.main-title { font-family: 'Cinzel', serif; font-size: 2.4rem; font-weight: 900;
    background: linear-gradient(90deg, #C9A84C, #F0C040, #C9A84C);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;
    text-align: center; letter-spacing: 4px; padding-top: 10px; }

.sub-title { font-family: 'Crimson Text', serif; font-size: 1.05rem; color: #A08840;
    text-align: center; letter-spacing: 5px; font-style: italic; margin-bottom: 20px; }

.section-header { font-family: 'Cinzel', serif; font-size: 0.88rem; color: #C9A84C;
    letter-spacing: 3px; border-left: 3px solid #C9A84C; padding-left: 10px;
    margin: 18px 0 12px 0; text-transform: uppercase; }

.metric-card { background: linear-gradient(135deg, #0D1F3C, #112244);
    border: 1px solid #C9A84C; border-radius: 10px; padding: 16px;
    text-align: center; box-shadow: 0 4px 20px rgba(201,168,76,0.1); }

.metric-value { font-family: 'Cinzel', serif; font-size: 1.8rem; font-weight: 700; color: #F0C040; }
.metric-label { font-family: 'Crimson Text', serif; font-size: 0.82rem; color: #A08840;
    letter-spacing: 2px; text-transform: uppercase; }
.metric-unit  { font-family: 'Crimson Text', serif; font-size: 0.78rem; color: #806830; }

.info-box { background: rgba(201,168,76,0.06); border: 1px solid #C9A84C44;
    border-radius: 8px; padding: 14px 18px; margin: 10px 0;
    font-family: 'Crimson Text', serif; font-size: 0.95rem; color: #D4C090; }

.result-box { background: linear-gradient(135deg, #0D1F3C, #0A1628);
    border: 1px solid #C9A84C; border-top: 3px solid #C9A84C;
    border-radius: 8px; padding: 14px 18px; margin: 8px 0; }

.formula-box { background: linear-gradient(135deg, #060D1A, #0D1F3C);
    border: 1px solid #C9A84C; border-radius: 8px; padding: 12px 18px; margin: 8px 0;
    font-family: 'Cinzel', serif; color: #F0C040; font-size: 1rem;
    text-align: center; letter-spacing: 1px; }

.team-card { background: linear-gradient(135deg, #0D1F3C, #060D1A);
    border: 1px solid #C9A84C33; border-radius: 8px; padding: 10px 14px; margin: 5px 0; }

.gold-divider { border: none; height: 1px;
    background: linear-gradient(90deg, transparent, #C9A84C, transparent); margin: 20px 0; }

.status-good { background: linear-gradient(90deg, #0a2a0a, #0d3d0d);
    border: 1px solid #00cc44; color: #00ff66; padding: 6px 16px;
    border-radius: 20px; font-family: 'Cinzel', serif; font-size: 0.85rem; display: inline-block; }
.status-warn { background: linear-gradient(90deg, #2a1a00, #3d2800);
    border: 1px solid #ccaa00; color: #ffdd00; padding: 6px 16px;
    border-radius: 20px; font-family: 'Cinzel', serif; font-size: 0.85rem; display: inline-block; }
.status-bad  { background: linear-gradient(90deg, #2a0000, #3d0000);
    border: 1px solid #cc2200; color: #ff4422; padding: 6px 16px;
    border-radius: 20px; font-family: 'Cinzel', serif; font-size: 0.85rem; display: inline-block; }

label { font-family: 'Crimson Text', serif !important; color: #A08840 !important; }
.stNumberInput input { background: #0D1F3C !important; border: 1px solid #C9A84C55 !important; color: #F0C040 !important; }
.stSelectbox > div > div { background: #0D1F3C !important; border: 1px solid #C9A84C55 !important; color: #F0C040 !important; }
.stTextInput input { background: #0D1F3C !important; border: 1px solid #C9A84C55 !important; color: #F0C040 !important; }

.stTabs [data-baseweb="tab-list"] { background: #060D1A; border-radius: 10px; padding: 4px; border: 1px solid #C9A84C33; }
.stTabs [data-baseweb="tab"] { background: transparent; color: #A08840; font-family: 'Cinzel', serif; font-size: 0.78rem; border-radius: 8px; }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg, #1B3A6B, #112244) !important; color: #F0C040 !important; border: 1px solid #C9A84C !important; }

.stButton > button { background: linear-gradient(135deg, #1B3A6B, #112244); color: #F0C040;
    border: 1px solid #C9A84C; border-radius: 8px; font-family: 'Cinzel', serif;
    font-size: 0.9rem; letter-spacing: 2px; padding: 10px 28px; }
.stButton > button:hover { box-shadow: 0 0 20px rgba(201,168,76,0.3); }

#MainMenu {visibility: hidden;} footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ── CONSTANTS ─────────────────────────────────────────────────────────────────
FLUIDS = {
    "Water (20°C)":        {"rho": 998.2,  "mu": 0.001002, "color": "#00AAFF"},
    "Water (60°C)":        {"rho": 983.2,  "mu": 0.000467, "color": "#0088DD"},
    "Engine Oil (40°C)":   {"rho": 876.0,  "mu": 0.210,    "color": "#C9A84C"},
    "Air (20°C)":          {"rho": 1.204,  "mu": 0.0000181,"color": "#AADDFF"},
    "Gasoline":            {"rho": 737.0,  "mu": 0.000600, "color": "#FFCC44"},
    "Mercury":             {"rho": 13546.0,"mu": 0.001526, "color": "#AAAAAA"},
    "Glycerin (25°C)":     {"rho": 1259.0, "mu": 0.950,    "color": "#88FFAA"},
    "Crude Oil":           {"rho": 870.0,  "mu": 0.007,    "color": "#664422"},
}

PIPE_MATERIALS = {
    "Commercial Steel":     0.000046,
    "Cast Iron":            0.00026,
    "Concrete":             0.0030,
    "PVC / Plastic":        0.0000015,
    "Copper":               0.0000015,
    "Galvanized Iron":      0.00015,
    "Wrought Iron":         0.000046,
}

FITTINGS = {
    "Globe Valve (fully open)": 10.0,
    "Gate Valve (fully open)":  0.2,
    "90° Elbow (standard)":     0.9,
    "90° Elbow (long radius)":  0.6,
    "45° Elbow":                0.4,
    "Tee (flow through run)":   0.6,
    "Tee (flow through branch)":1.8,
    "Check Valve":              2.5,
    "Sudden Expansion":         1.0,
    "Sudden Contraction":       0.5,
    "Entry (sharp-edged)":      0.5,
    "Exit Loss":                1.0,
}

PLOT_CFG = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(10,20,40,0.8)",
    font=dict(color="#A08840", family="Georgia"),
    title_font=dict(color="#C9A84C", size=14, family="Georgia"),
)

TEAM = [
    ("Abdul Hakeem", "24-ME-006"),
    ("Sana Ullah",   "24-ME-114"),
    ("Mahad Saeed",  "24-ME-122"),
]

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="section-header">Fluid Selection</div>', unsafe_allow_html=True)
    fluid_choice = st.selectbox("Select Fluid", list(FLUIDS.keys()))
    fluid = FLUIDS[fluid_choice]
    rho = fluid["rho"]
    mu  = fluid["mu"]

    st.markdown(f"""<div class="info-box">
    <b style="color:#F0C040;">Density (ρ)</b> = {rho} kg/m³<br>
    <b style="color:#F0C040;">Viscosity (μ)</b> = {mu:.6f} Pa·s
    </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Group 10 — Team</div>', unsafe_allow_html=True)
    for name, reg in TEAM:
        st.markdown(f"""<div class="team-card">
            <span style="font-family:'Crimson Text',serif;color:#D4C090;font-weight:600;">💧 {name}</span><br>
            <span style="font-family:'Courier New',monospace;color:#C9A84C;font-size:0.82rem;">{reg}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    st.markdown('<div style="font-family:Georgia;color:#604820;font-size:0.78rem;text-align:center;font-style:italic;">ICT in Fluid Mechanics<br>Mechanical Engineering<br>UET Taxila · 2025</div>', unsafe_allow_html=True)

# ── HEADER ────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">💧 PIPE FLOW CALCULATOR</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Fluid Mechanics — Pressure Drop & Flow Analysis Tool</div>', unsafe_allow_html=True)
st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

# ── TABS ──────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "PRESSURE DROP",
    "FLOW REGIME",
    "PIPE NETWORK",
    "FLOW CHARTS",
    "THEORY",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — PRESSURE DROP CALCULATOR (Darcy-Weisbach)
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">Darcy-Weisbach Pressure Drop Calculator</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">Calculate pressure drop in a pipe using the Darcy-Weisbach equation. Includes major (friction) and minor (fittings) losses.</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-header">Pipe Parameters</div>', unsafe_allow_html=True)
        D = st.number_input("Pipe Diameter D (m)",      min_value=0.001, value=0.05,  step=0.005)
        L = st.number_input("Pipe Length L (m)",        min_value=0.1,   value=100.0, step=5.0)
        e = st.selectbox("Pipe Material (Roughness)",   list(PIPE_MATERIALS.keys()))
        roughness = PIPE_MATERIALS[e]

    with col2:
        st.markdown('<div class="section-header">Flow Parameters</div>', unsafe_allow_html=True)
        V = st.number_input("Flow Velocity V (m/s)",    min_value=0.001, value=2.0,   step=0.1)
        elev = st.number_input("Elevation Change Δz (m)", value=0.0, step=1.0,
                               help="Positive = uphill, Negative = downhill")

    st.markdown('<div class="section-header">Minor Losses (Fittings)</div>', unsafe_allow_html=True)
    st.markdown('<div class="info-box">Select fittings present in the pipe system:</div>', unsafe_allow_html=True)

    fitting_cols = st.columns(3)
    selected_fittings = {}
    fitting_list = list(FITTINGS.keys())
    for i, fitting in enumerate(fitting_list):
        with fitting_cols[i % 3]:
            count = st.number_input(f"{fitting}", min_value=0, value=0, step=1, key=f"fit_{i}")
            if count > 0:
                selected_fittings[fitting] = count

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

    if st.button("CALCULATE PRESSURE DROP", use_container_width=True):
        g = 9.81
        A = np.pi * D**2 / 4
        Q = V * A

        # Reynolds number
        Re = rho * V * D / mu

        # Friction factor (Colebrook-White)
        eps_D = roughness / D
        if Re < 2300:
            f = 64 / Re
            flow_type = "Laminar"
        else:
            f = 0.02
            for _ in range(100):
                f = (-2 * np.log10(eps_D/3.7 + 2.51/(Re * np.sqrt(f))))**-2
            flow_type = "Turbulent"

        # Major loss
        hf_major = f * (L / D) * (V**2 / (2*g))
        dP_major = rho * g * hf_major

        # Minor losses
        K_total = sum(FITTINGS[fit] * cnt for fit, cnt in selected_fittings.items())
        hf_minor = K_total * V**2 / (2*g)
        dP_minor = rho * g * hf_minor

        # Elevation head
        dP_elev = rho * g * elev

        # Total
        hf_total = hf_major + hf_minor + elev
        dP_total = dP_major + dP_minor + dP_elev

        # Power
        Power = rho * g * Q * hf_total

        # Results
        st.markdown('<div class="section-header">Results</div>', unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        with c1: st.markdown(f'<div class="metric-card"><div class="metric-value">{Re:,.0f}</div><div class="metric-unit">—</div><div class="metric-label">Reynolds Number</div></div>', unsafe_allow_html=True)
        with c2: st.markdown(f'<div class="metric-card"><div class="metric-value">{f:.5f}</div><div class="metric-unit">—</div><div class="metric-label">Friction Factor (f)</div></div>', unsafe_allow_html=True)
        with c3: st.markdown(f'<div class="metric-card"><div class="metric-value">{dP_total/1000:.2f}</div><div class="metric-unit">kPa</div><div class="metric-label">Total Pressure Drop</div></div>', unsafe_allow_html=True)
        with c4: st.markdown(f'<div class="metric-card"><div class="metric-value">{Power:.1f}</div><div class="metric-unit">W</div><div class="metric-label">Pump Power Req.</div></div>', unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        c5, c6, c7, c8 = st.columns(4)
        with c5: st.markdown(f'<div class="metric-card"><div class="metric-value">{hf_major:.3f}</div><div class="metric-unit">m</div><div class="metric-label">Major Head Loss</div></div>', unsafe_allow_html=True)
        with c6: st.markdown(f'<div class="metric-card"><div class="metric-value">{hf_minor:.3f}</div><div class="metric-unit">m</div><div class="metric-label">Minor Head Loss</div></div>', unsafe_allow_html=True)
        with c7: st.markdown(f'<div class="metric-card"><div class="metric-value">{hf_total:.3f}</div><div class="metric-unit">m</div><div class="metric-label">Total Head Loss</div></div>', unsafe_allow_html=True)
        with c8: st.markdown(f'<div class="metric-card"><div class="metric-value">{Q*1000:.3f}</div><div class="metric-unit">L/s</div><div class="metric-label">Flow Rate Q</div></div>', unsafe_allow_html=True)

        # Flow regime status
        st.markdown("<br>", unsafe_allow_html=True)
        if Re < 2300:
            st.markdown(f'<div style="text-align:center"><span class="status-good">LAMINAR FLOW — Re = {Re:,.0f}</span></div>', unsafe_allow_html=True)
        elif Re < 4000:
            st.markdown(f'<div style="text-align:center"><span class="status-warn">TRANSITIONAL FLOW — Re = {Re:,.0f}</span></div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="text-align:center"><span class="status-bad">TURBULENT FLOW — Re = {Re:,.0f}</span></div>', unsafe_allow_html=True)

        # Loss breakdown chart
        if hf_major > 0 or hf_minor > 0:
            loss_labels = ["Major Friction Loss", "Minor Fitting Loss", "Elevation Head"]
            loss_values = [hf_major, hf_minor, abs(elev)]
            loss_values = [v for v in loss_values if v > 0]
            loss_labels = [l for l, v in zip(loss_labels, [hf_major, hf_minor, abs(elev)]) if v > 0]

            fig = go.Figure(go.Pie(
                labels=loss_labels, values=loss_values, hole=0.45,
                marker=dict(colors=["#C9A84C", "#F0C040", "#1B3A6B"])
            ))
            fig.update_layout(**PLOT_CFG, title="Head Loss Breakdown", height=300)
            st.plotly_chart(fig, use_container_width=True)

        st.session_state["last_calc"] = {"Re": Re, "f": f, "dP": dP_total, "hf": hf_total, "Q": Q, "V": V, "D": D}

# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — FLOW REGIME ANALYZER
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-header">Flow Regime & Reynolds Number Analyzer</div>', unsafe_allow_html=True)
    st.markdown('<div class="formula-box">Re = ρVD / μ</div>', unsafe_allow_html=True)

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        V_r = st.number_input("Velocity V (m/s)",       min_value=0.001, value=1.0, step=0.1, key="vr")
        D_r = st.number_input("Pipe Diameter D (m)",    min_value=0.001, value=0.05, step=0.005, key="dr")
    with col_r2:
        Re_val = rho * V_r * D_r / mu
        color  = "#00FF88" if Re_val < 2300 else ("#FFDD00" if Re_val < 4000 else "#FF4422")
        regime = "LAMINAR" if Re_val < 2300 else ("TRANSITIONAL" if Re_val < 4000 else "TURBULENT")

        st.markdown(f'<div class="metric-card" style="margin-top:20px;"><div class="metric-value" style="color:{color}">{Re_val:,.0f}</div><div class="metric-unit">Reynolds Number</div><div class="metric-label" style="color:{color};">{regime} FLOW</div></div>', unsafe_allow_html=True)

    # Re vs Velocity chart
    V_range = np.linspace(0.01, 10, 300)
    Re_range = rho * V_range * D_r / mu

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=V_range, y=Re_range, line=dict(color="#C9A84C", width=3), name="Reynolds Number"))
    fig.add_hline(y=2300, line_dash="dash", line_color="#00FF88", annotation_text="Laminar Limit (2300)", annotation_font_color="#00FF88")
    fig.add_hline(y=4000, line_dash="dash", line_color="#FF4422", annotation_text="Turbulent Limit (4000)", annotation_font_color="#FF4422")
    fig.add_trace(go.Scatter(x=[V_r], y=[Re_val], mode="markers", marker=dict(size=12, color="#F0C040"), name=f"Current (Re={Re_val:,.0f})"))
    fig.update_layout(**PLOT_CFG, title="Reynolds Number vs Flow Velocity",
        xaxis=dict(title="Velocity (m/s)", gridcolor="#1B3A6B", color="#A08840"),
        yaxis=dict(title="Reynolds Number", gridcolor="#1B3A6B", color="#A08840"), height=380)
    st.plotly_chart(fig, use_container_width=True)

    # Velocity profile
    st.markdown('<div class="section-header">Velocity Profile Across Pipe Cross-Section</div>', unsafe_allow_html=True)
    r_range = np.linspace(-D_r/2, D_r/2, 300)
    if Re_val < 2300:
        V_profile = V_r * 2 * (1 - (r_range/(D_r/2))**2)
        profile_label = "Parabolic (Laminar)"
    else:
        n = 7
        V_profile = V_r * 1.22 * (1 - np.abs(r_range/(D_r/2)))**(1/n)
        profile_label = "Turbulent (1/7 Power Law)"

    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(x=r_range*1000, y=V_profile, line=dict(color="#C9A84C", width=3), name=profile_label, fill="tozeroy", fillcolor="rgba(201,168,76,0.1)"))
    fig2.update_layout(**PLOT_CFG, title=f"Velocity Profile — {profile_label}",
        xaxis=dict(title="Radial Position (mm)", gridcolor="#1B3A6B", color="#A08840"),
        yaxis=dict(title="Velocity (m/s)", gridcolor="#1B3A6B", color="#A08840"), height=300)
    st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — PIPE NETWORK
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Series & Parallel Pipe Network Calculator</div>', unsafe_allow_html=True)

    network_type = st.radio("Network Type", ["Series Pipes", "Parallel Pipes"], horizontal=True)

    st.markdown('<div class="info-box">Enter up to 4 pipe segments. The calculator finds total head loss and flow distribution.</div>', unsafe_allow_html=True)

    num_pipes = st.slider("Number of Pipes", 2, 4, 3)
    pipe_data = []
    cols = st.columns(num_pipes)
    for i, col in enumerate(cols[:num_pipes]):
        with col:
            st.markdown(f'<div style="color:#C9A84C;font-family:Georgia;font-weight:bold;text-align:center;">Pipe {i+1}</div>', unsafe_allow_html=True)
            d_i = st.number_input(f"D{i+1} (m)",  min_value=0.001, value=0.05,  step=0.005, key=f"d{i}")
            l_i = st.number_input(f"L{i+1} (m)",  min_value=1.0,   value=50.0,  step=5.0,   key=f"l{i}")
            f_i = st.number_input(f"f{i+1}",       min_value=0.001, value=0.02,  step=0.001, key=f"f{i}")
            pipe_data.append({"D": d_i, "L": l_i, "f": f_i})

    Q_total = st.number_input("Total Flow Rate Q (m³/s)", min_value=0.0001, value=0.01, step=0.001)

    if st.button("ANALYZE NETWORK", use_container_width=True):
        g = 9.81
        results = []

        if "Series" in network_type:
            # Same Q through all pipes
            for p in pipe_data[:num_pipes]:
                A_i = np.pi * p["D"]**2 / 4
                V_i = Q_total / A_i
                hf_i = p["f"] * (p["L"] / p["D"]) * (V_i**2 / (2*g))
                results.append({"V": V_i, "hf": hf_i, "Q": Q_total})
            total_hf = sum(r["hf"] for r in results)

            st.markdown('<div class="section-header">Series Network Results</div>', unsafe_allow_html=True)
            for i, r in enumerate(results):
                st.markdown(f'<div class="result-box"><b style="color:#F0C040;">Pipe {i+1}:</b> V = {r["V"]:.3f} m/s &nbsp;|&nbsp; Head Loss = {r["hf"]:.3f} m &nbsp;|&nbsp; Q = {r["Q"]*1000:.3f} L/s</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card" style="margin-top:12px;"><div class="metric-value">{total_hf:.3f} m</div><div class="metric-label">Total Head Loss</div></div>', unsafe_allow_html=True)

        else:
            # Parallel: same head loss, find Q distribution
            R_vals = [p["f"] * p["L"] / (p["D"] * 2 * g * (np.pi * p["D"]**2 / 4)**2) for p in pipe_data[:num_pipes]]
            sqrt_R = [1/np.sqrt(r) for r in R_vals]
            sum_sqrt_R = sum(sqrt_R)
            hf_common = (Q_total / sum_sqrt_R)**2

            st.markdown('<div class="section-header">Parallel Network Results</div>', unsafe_allow_html=True)
            for i, (p, sr) in enumerate(zip(pipe_data[:num_pipes], sqrt_R)):
                Q_i = sr / sum_sqrt_R * Q_total
                A_i = np.pi * p["D"]**2 / 4
                V_i = Q_i / A_i
                st.markdown(f'<div class="result-box"><b style="color:#F0C040;">Pipe {i+1}:</b> Q = {Q_i*1000:.3f} L/s &nbsp;|&nbsp; V = {V_i:.3f} m/s</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="metric-card" style="margin-top:12px;"><div class="metric-value">{hf_common:.3f} m</div><div class="metric-label">Common Head Loss</div></div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — FLOW CHARTS
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">Flow Analysis Charts & Moody Diagram</div>', unsafe_allow_html=True)

    chart_type = st.selectbox("Select Chart", [
        "Pressure Drop vs Velocity",
        "Pressure Drop vs Pipe Diameter",
        "Moody Diagram (f vs Re)",
        "Flow Rate vs Pipe Diameter",
    ])

    D_c  = st.number_input("Pipe Diameter (m)",   min_value=0.001, value=0.05,  step=0.005, key="Dc")
    L_c  = st.number_input("Pipe Length (m)",     min_value=1.0,   value=100.0, step=10.0,  key="Lc")
    f_c  = 0.02

    if "Pressure Drop vs Velocity" in chart_type:
        V_vals = np.linspace(0.1, 10, 200)
        Re_vals = rho * V_vals * D_c / mu
        f_vals  = np.where(Re_vals < 2300, 64/Re_vals, 0.02)
        dP_vals = f_vals * (L_c/D_c) * rho * V_vals**2 / 2 / 1000

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=V_vals, y=dP_vals, line=dict(color="#C9A84C", width=3), fill="tozeroy", fillcolor="rgba(201,168,76,0.08)"))
        fig.update_layout(**PLOT_CFG, title=f"Pressure Drop vs Velocity (D={D_c}m, L={L_c}m)",
            xaxis=dict(title="Velocity (m/s)", gridcolor="#1B3A6B", color="#A08840"),
            yaxis=dict(title="Pressure Drop (kPa)", gridcolor="#1B3A6B", color="#A08840"), height=420)
        st.plotly_chart(fig, use_container_width=True)

    elif "Pressure Drop vs Pipe Diameter" in chart_type:
        V_fixed = st.number_input("Fixed Velocity (m/s)", min_value=0.1, value=2.0, step=0.1)
        D_vals = np.linspace(0.01, 0.3, 200)
        Re_vals = rho * V_fixed * D_vals / mu
        f_vals  = np.where(Re_vals < 2300, 64/Re_vals, 0.02)
        dP_vals = f_vals * (L_c/D_vals) * rho * V_fixed**2 / 2 / 1000

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=D_vals*1000, y=dP_vals, line=dict(color="#C9A84C", width=3)))
        fig.update_layout(**PLOT_CFG, title=f"Pressure Drop vs Pipe Diameter (V={V_fixed} m/s, L={L_c}m)",
            xaxis=dict(title="Diameter (mm)", gridcolor="#1B3A6B", color="#A08840"),
            yaxis=dict(title="Pressure Drop (kPa)", gridcolor="#1B3A6B", color="#A08840"), height=420)
        st.plotly_chart(fig, use_container_width=True)

    elif "Moody" in chart_type:
        Re_range = np.logspace(3, 8, 500)
        eps_vals = [0.0, 0.0001, 0.001, 0.01]
        colors   = ["#C9A84C", "#F0C040", "#00AAFF", "#FF6B35"]
        labels   = ["Smooth", "ε/D=0.0001", "ε/D=0.001", "ε/D=0.01"]

        fig = go.Figure()
        for eps_D, color, label in zip(eps_vals, colors, labels):
            f_vals = []
            for Re in Re_range:
                if Re < 2300:
                    f_vals.append(64/Re)
                else:
                    f = 0.02
                    for _ in range(50):
                        if eps_D == 0:
                            f = (0.790 * np.log(Re) - 1.64)**-2
                        else:
                            f = (-2*np.log10(eps_D/3.7 + 2.51/(Re*np.sqrt(f))))**-2
                    f_vals.append(f)
            fig.add_trace(go.Scatter(x=Re_range, y=f_vals, mode="lines", line=dict(color=color, width=2), name=label))

        fig.update_layout(**PLOT_CFG, title="Moody Diagram — Friction Factor vs Reynolds Number",
            xaxis=dict(type="log", title="Reynolds Number (Re)", gridcolor="#1B3A6B", color="#A08840"),
            yaxis=dict(type="log", title="Friction Factor (f)",  gridcolor="#1B3A6B", color="#A08840"),
            legend=dict(font=dict(color="#A08840")), height=450)
        st.plotly_chart(fig, use_container_width=True)

    else:  # Flow Rate vs Diameter
        V_fixed2 = st.number_input("Fixed Velocity (m/s)", min_value=0.1, value=2.0, step=0.1, key="vf2")
        D_vals2  = np.linspace(0.01, 0.5, 300)
        Q_vals   = V_fixed2 * np.pi * D_vals2**2 / 4 * 1000

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=D_vals2*1000, y=Q_vals, line=dict(color="#C9A84C", width=3), fill="tozeroy", fillcolor="rgba(201,168,76,0.08)"))
        fig.update_layout(**PLOT_CFG, title=f"Flow Rate vs Pipe Diameter (V={V_fixed2} m/s)",
            xaxis=dict(title="Diameter (mm)", gridcolor="#1B3A6B", color="#A08840"),
            yaxis=dict(title="Flow Rate (L/s)", gridcolor="#1B3A6B", color="#A08840"), height=420)
        st.plotly_chart(fig, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# TAB 5 — THEORY
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-header">Key Formulas & Theory</div>', unsafe_allow_html=True)

    formulas = [
        ("Reynolds Number",          "Re = ρVD / μ",                    "Determines flow regime: < 2300 Laminar, > 4000 Turbulent"),
        ("Darcy-Weisbach Equation",  "ΔP = f · (L/D) · (ρV²/2)",       "Main equation for pressure drop due to friction"),
        ("Friction Factor (Laminar)","f = 64 / Re",                     "Only valid for laminar flow (Re < 2300)"),
        ("Colebrook-White Equation", "1/√f = -2 log(ε/3.7D + 2.51/Re√f)", "Implicit equation for turbulent friction factor"),
        ("Continuity Equation",      "Q = V · A = V · πD²/4",           "Flow rate — constant in steady incompressible flow"),
        ("Bernoulli Equation",       "P/ρg + V²/2g + z = constant",     "Energy conservation along a streamline"),
        ("Head Loss (Major)",        "hf = f · (L/D) · V²/2g",         "Friction head loss along the pipe length"),
        ("Head Loss (Minor)",        "hm = K · V²/2g",                  "Loss due to fittings, bends, valves"),
    ]

    col_t1, col_t2 = st.columns(2)
    for i, (name, formula, desc) in enumerate(formulas):
        with (col_t1 if i % 2 == 0 else col_t2):
            st.markdown(f"""<div style="margin-bottom:10px;">
                <div style="font-family:Georgia;color:#A08840;font-size:0.85rem;letter-spacing:1px;">{name}</div>
                <div class="formula-box" style="font-size:0.9rem;padding:8px 14px;">{formula}</div>
                <div style="font-family:Georgia;color:#806830;font-size:0.82rem;margin-top:4px;font-style:italic;">{desc}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Flow Regimes</div>', unsafe_allow_html=True)
    regimes = [
        ("Laminar Flow",      "Re < 2300",   "Smooth, orderly flow in layers. Parabolic velocity profile. f = 64/Re."),
        ("Transitional Flow", "2300–4000",   "Unstable flow switching between laminar and turbulent. Unpredictable."),
        ("Turbulent Flow",    "Re > 4000",   "Chaotic, mixing flow. Flat velocity profile. Use Colebrook equation."),
    ]
    for regime, re_range, desc in regimes:
        color = "#00FF88" if "Laminar" in regime else ("#FFDD00" if "Trans" in regime else "#FF4422")
        st.markdown(f"""<div class="result-box" style="margin-bottom:8px;">
            <b style="color:{color};font-family:Georgia;">{regime}</b>
            <span style="color:#C9A84C;font-family:Georgia;margin-left:12px;">{re_range}</span><br>
            <span style="color:#A08840;font-family:Georgia;font-size:0.92rem;">{desc}</span>
        </div>""", unsafe_allow_html=True)

    st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
    st.markdown('<div class="section-header">Group 10 — Project Team</div>', unsafe_allow_html=True)
    for name, reg in TEAM:
        st.markdown(f"""<div class="team-card" style="padding:14px 18px;">
            <span style="font-family:Georgia;color:#D4C090;font-size:1.05rem;font-weight:600;">💧 {name}</span>
            <span style="font-family:'Courier New',monospace;color:#C9A84C;font-size:0.9rem;float:right;">{reg}</span>
        </div>""", unsafe_allow_html=True)

# ── FOOTER ────────────────────────────────────────────────────────────────────
st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
st.markdown("""<div style="text-align:center;font-family:Georgia;color:#604820;font-size:0.8rem;letter-spacing:2px;padding:10px 0;font-style:italic;">
    ICT in Fluid Mechanics  |  Pipe Flow & Pressure Drop Calculator  |  Mechanical Engineering  |  UET Taxila  |  2025
</div>""", unsafe_allow_html=True)
