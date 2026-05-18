import streamlit as st
import pandas as pd
import plotly.express as px

# ─── Page Config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="The State of Hiring",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─── Custom CSS — Dark Theme ──────────────────────────────────────────────────
st.markdown("""
<style>
    .block-container { padding: 2rem 2.5rem; }

    .metric-card {
        background: #1E293B;
        border-radius: 12px;
        padding: 1.2rem 1.5rem;
        box-shadow: 0 2px 12px rgba(0,0,0,0.3);
        border-left: 4px solid #2E86AB;
        margin-bottom: 1rem;
    }
    .metric-label {
        font-size: 11px;
        color: #94A3B8;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 6px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 800;
        color: #F1F5F9;
        line-height: 1.2;
    }
    .metric-sub {
        font-size: 12px;
        color: #64748B;
        margin-top: 4px;
    }
    .section-header {
        font-size: 18px;
        font-weight: 700;
        color: #F1F5F9;
        margin: 1.2rem 0 0.6rem 0;
        padding-bottom: 0.4rem;
        border-bottom: 2px solid #334155;
    }
    .page-title {
        font-size: 32px;
        font-weight: 800;
        color: #F1F5F9;
        margin-bottom: 4px;
    }
    .page-subtitle {
        font-size: 14px;
        color: #94A3B8;
        margin-bottom: 1.5rem;
    }
    .insight-box {
        background: #1E3A5F;
        border-left: 4px solid #2E86AB;
        border-radius: 8px;
        padding: 0.75rem 1rem;
        font-size: 13px;
        color: #93C5FD;
        margin-top: 0.5rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# ─── Load Data ────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    job_demand  = pd.read_csv("new_csv_files/job_in_demand.csv")
    remote      = pd.read_csv("new_csv_files/remote_vs_nonremote.csv")
    trend       = pd.read_csv("new_csv_files/hire_trend_month.csv")
    companies   = pd.read_csv("new_csv_files/top_companies.csv")
    salary_pct  = pd.read_csv("new_csv_files/salary_percent.csv")
    skill_type  = pd.read_csv("new_csv_files/skill_type_analysis.csv")
    top_skills  = pd.read_csv("new_csv_files/top_paying_skills.csv")
    top_jobs    = pd.read_csv("new_csv_files/top_paying_jobs.csv")
    return job_demand, remote, trend, companies, salary_pct, skill_type, top_skills, top_jobs

job_demand, remote, trend, companies, salary_pct, skill_type, top_skills, top_jobs = load_data()

# ─── Shared Dark Plot Layout ──────────────────────────────────────────────────
def dark_layout(**kwargs):
    layout = dict(
        plot_bgcolor="#0F172A",
        paper_bgcolor="#0F172A",
        font=dict(family="Arial", size=12, color="#F1F5F9"),
        margin=dict(l=10, r=10, t=20, b=10),
        xaxis=dict(
            gridcolor="#1E293B",
            linecolor="#334155",
            tickfont=dict(color="#F1F5F9"),
            title_font=dict(color="#F1F5F9")
        ),
        yaxis=dict(
            gridcolor="#1E293B",
            linecolor="#334155",
            tickfont=dict(color="#F1F5F9"),
            title_font=dict(color="#F1F5F9")
        ),
        legend=dict(
            font=dict(color="#F1F5F9"),
            bgcolor="#1E293B",
            bordercolor="#334155"
        ),
        coloraxis_colorbar=dict(
            tickfont=dict(color="#F1F5F9"),
            title_font=dict(color="#F1F5F9")
        )
    )
    layout.update(kwargs)
    return layout

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## Job Market Intel")
    st.markdown("---")

    page = st.selectbox(
        "Navigate to",
        ["Overview", "Salary Analysis", "Skills Analysis", "Trends", "Companies", "Salary Predictor"]
    )

    st.markdown("---")
    st.markdown("### Filter by Role")
    all_roles = sorted(job_demand["job_title_short"].tolist())
    selected_roles = st.multiselect(
        "Select Job Roles",
        options=all_roles,
        default=all_roles
    )

    st.markdown("---")
    st.markdown("### Filter by Avg Salary")
    sal_min = int(job_demand["avg_salary"].min())
    sal_max = int(job_demand["avg_salary"].max())
    salary_range = st.slider(
        "Salary Range ($)",
        min_value=sal_min,
        max_value=sal_max,
        value=(sal_min, sal_max),
        step=1000,
        format="$%d"
    )

    st.markdown("---")
    st.markdown("""
    **Data Source**  
    787k+ worldwide job postings  
    across 10 data roles · 2023
    """)

# ─── Apply Filters ────────────────────────────────────────────────────────────
job_filtered = job_demand[
    (job_demand["job_title_short"].isin(selected_roles)) &
    (job_demand["avg_salary"] >= salary_range[0]) &
    (job_demand["avg_salary"] <= salary_range[1])
]
sal_filtered  = salary_pct[salary_pct["job_title_short"].isin(selected_roles)]
rem_filtered  = remote[remote["Job"].isin(selected_roles)]
comp_filtered = companies[companies["Job Name"].isin(selected_roles)]

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 1 — OVERVIEW
# ─────────────────────────────────────────────────────────────────────────────
if page == "Overview":
    st.markdown('<div class="page-title">The State of Hiring</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Worldwide data jobs analysis — salary, demand, skills & trends</div>', unsafe_allow_html=True)

    # KPI Cards
    c1, c2, c3, c4 = st.columns(4)
    total_jobs = int(job_filtered["total_jobs"].sum()) if not job_filtered.empty else 0
    avg_sal    = int(job_filtered["avg_salary"].mean()) if not job_filtered.empty else 0
    top_role   = job_filtered.loc[job_filtered["avg_salary"].idxmax(), "job_title_short"] if not job_filtered.empty else "N/A"
    top_sal    = int(job_filtered["avg_salary"].max()) if not job_filtered.empty else 0

    with c1:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Total Job Postings</div>
            <div class="metric-value">{total_jobs:,}</div>
            <div class="metric-sub">Filtered selection</div>
        </div>""", unsafe_allow_html=True)
    with c2:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Avg Market Salary</div>
            <div class="metric-value">${avg_sal:,}</div>
            <div class="metric-sub">Across selected roles</div>
        </div>""", unsafe_allow_html=True)
    with c3:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Highest Paying Role</div>
            <div class="metric-value" style="font-size:18px;">{top_role}</div>
            <div class="metric-sub">${top_sal:,} avg salary</div>
        </div>""", unsafe_allow_html=True)
    with c4:
        st.markdown(f"""<div class="metric-card">
            <div class="metric-label">Data Period</div>
            <div class="metric-value" style="font-size:20px;">2023</div>
            <div class="metric-sub">Jan 2023 — Dec 2023</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Job Roles — Demand vs Salary</div>', unsafe_allow_html=True)
        if job_filtered.empty:
            st.warning("No data for selected filters.")
        else:
            df = job_filtered.sort_values("avg_salary", ascending=True)
            fig = px.bar(df, x="avg_salary", y="job_title_short", orientation="h",
                         color="total_jobs", color_continuous_scale="Teal",
                         hover_data=["min_salary", "max_salary", "total_jobs"])
            fig.update_layout(**dark_layout(
                xaxis_title="Average Salary ($)", yaxis_title="Job Role",
                coloraxis_colorbar=dict(title="Total Jobs",
                    tickfont=dict(color="#F1F5F9"),
                    title_font=dict(color="#F1F5F9"))
            ))
            st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box">Senior Data Scientist pays the most ($154k avg). Data Analyst has the highest demand (9,756 jobs).</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">Monthly Hiring Trend</div>', unsafe_allow_html=True)
        fig2 = px.line(trend, x="Periods", y="Total Jobs",
                       markers=True, line_shape="spline",
                       color_discrete_sequence=["#2E86AB"])
        fig2.update_layout(**dark_layout(
            xaxis_title="Month", yaxis_title="Total Jobs", xaxis_tickangle=-45
        ))
        fig2.update_traces(line=dict(width=3), marker=dict(size=8))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('<div class="insight-box">Jan & Jun 2023 had peak hiring. Sharp drop from Sep 2023 onwards.</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 2 — SALARY ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Salary Analysis":
    st.markdown('<div class="page-title">Salary Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Deep dive into salary distributions across roles and work types</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Remote vs Onsite Salary Comparison</div>', unsafe_allow_html=True)
    if rem_filtered.empty:
        st.warning("No data for selected filters.")
    else:
        df_r = rem_filtered.sort_values("Difference", ascending=False)
        fig = px.bar(df_r, x="Job", y=["Remote Pay", "Onsite Pay"], barmode="group",
                     color_discrete_map={"Remote Pay": "#2E86AB", "Onsite Pay": "#E84855"})
        fig.update_layout(**dark_layout(
            xaxis_title="Job Role", yaxis_title="Average Salary ($)",
            xaxis_tickangle=-45, legend_title="Work Type",
            margin=dict(l=10, r=10, t=20, b=100)
        ))
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="insight-box">Cloud Engineer gets highest remote premium (+$41k). Only Senior Data Analyst pays slightly more onsite.</div>', unsafe_allow_html=True)

    st.markdown("---")

    st.markdown('<div class="section-header">Salary Percentile by Job Role (P25 / P50 / P75 / P90)</div>', unsafe_allow_html=True)
    if sal_filtered.empty:
        st.warning("No data for selected filters.")
    else:
        df_p = sal_filtered.sort_values("p50", ascending=False)
        fig2 = px.bar(df_p, x="job_title_short", y=["p25", "p50", "p75", "p90"],
                      barmode="group",
                      color_discrete_sequence=["#2E86AB", "#A23B72", "#F18F01", "#C73E1D"],
                      labels={"value": "Salary ($)", "variable": "Percentile",
                              "job_title_short": "Job Role"})
        fig2.update_layout(**dark_layout(
            xaxis_title="Job Role", yaxis_title="Salary ($)",
            xaxis_tickangle=-45, legend_title="Percentile",
            margin=dict(l=10, r=10, t=20, b=100)
        ))
        st.plotly_chart(fig2, use_container_width=True)
    st.markdown('<div class="insight-box">Senior roles have P25 above $125k. ML Engineer has the biggest salary gap — experience matters most here.</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 3 — SKILLS ANALYSIS
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Skills Analysis":
    st.markdown('<div class="page-title">Skills Analysis</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Which skills pay the most and are in highest demand?</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Top Paying Skills</div>', unsafe_allow_html=True)
        df_s = top_skills.sort_values("avg_salary", ascending=True)
        fig = px.bar(df_s, x="avg_salary", y="skills", orientation="h",
                     color="avg_salary", color_continuous_scale="Teal",
                     labels={"avg_salary": "Avg Salary ($)", "skills": "Skill"})
        fig.update_layout(**dark_layout(
            xaxis_title="Average Salary ($)", yaxis_title="Skill",
            showlegend=False, margin=dict(l=100, r=10, t=20, b=10),
            coloraxis_colorbar=dict(title="Avg Salary",
                tickfont=dict(color="#F1F5F9"),
                title_font=dict(color="#F1F5F9"))
        ))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('<div class="insight-box">SVN ($400k) and Solidity ($179k) pay the most — niche skills command premium salaries.</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="section-header">Skill Type — Demand vs Salary</div>', unsafe_allow_html=True)
        df_t = skill_type.sort_values("avg_salary", ascending=True)
        fig2 = px.bar(df_t, x="avg_salary", y="skill_type", orientation="h",
                      color="total_jobs", color_continuous_scale="Blues",
                      labels={"avg_salary": "Avg Salary ($)", "skill_type": "Skill Type",
                              "total_jobs": "Total Jobs"})
        fig2.update_layout(**dark_layout(
            xaxis_title="Average Salary ($)", yaxis_title="Skill Type",
            margin=dict(l=120, r=10, t=20, b=10),
            coloraxis_colorbar=dict(title="Total Jobs",
                tickfont=dict(color="#F1F5F9"),
                title_font=dict(color="#F1F5F9"))
        ))
        st.plotly_chart(fig2, use_container_width=True)
        st.markdown('<div class="insight-box">Libraries (AI/ML) pay most ($139k). Programming has highest demand (47k jobs) but average salary.</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 4 — TRENDS
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Trends":
    st.markdown('<div class="page-title">Hiring Trends</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Monthly hiring patterns and salary trends across 2023</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Total Jobs by Month</div>', unsafe_allow_html=True)
        fig = px.line(trend, x="Periods", y="Total Jobs",
                      markers=True, line_shape="spline",
                      color_discrete_sequence=["#2E86AB"])
        fig.update_layout(**dark_layout(
            xaxis_title="Month", yaxis_title="Total Jobs", xaxis_tickangle=-45
        ))
        fig.update_traces(line=dict(width=3), marker=dict(size=8))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown('<div class="section-header">Avg Salary by Month</div>', unsafe_allow_html=True)
        fig2 = px.line(trend, x="Periods", y="AVG Salary",
                       markers=True, line_shape="spline",
                       color_discrete_sequence=["#E84855"])
        fig2.update_layout(**dark_layout(
            xaxis_title="Month", yaxis_title="Avg Salary ($)", xaxis_tickangle=-45
        ))
        fig2.update_traces(line=dict(width=3), marker=dict(size=8))
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown('<div class="insight-box">Jan & Jun 2023 had peak hiring. Salary stayed stable (~$120k-$125k) throughout the year despite job count dropping sharply in H2 2023.</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-header">Jobs Distribution by Month</div>', unsafe_allow_html=True)
    fig3 = px.bar(trend, x="Periods", y="Total Jobs",
                  color="Total Jobs", color_continuous_scale="Teal")
    fig3.update_layout(**dark_layout(
        xaxis_title="Month", yaxis_title="Total Jobs",
        xaxis_tickangle=-45, margin=dict(l=10, r=10, t=20, b=80),
        coloraxis_colorbar=dict(title="Total Jobs",
            tickfont=dict(color="#F1F5F9"),
            title_font=dict(color="#F1F5F9"))
    ))
    st.plotly_chart(fig3, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 5 — COMPANIES
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Companies":
    st.markdown('<div class="page-title">Top Paying Companies</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Which companies pay the most for data roles?</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">Top Companies by Role & Salary</div>', unsafe_allow_html=True)
    if comp_filtered.empty:
        st.warning("No data for selected filters.")
    else:
        df_c = comp_filtered.sort_values("AVG Salary", ascending=True)
        fig = px.bar(df_c, x="AVG Salary", y="Company Name", orientation="h",
                     color="Job Name", hover_data=["Total Jobs"],
                     labels={"AVG Salary": "Avg Salary ($)",
                             "Company Name": "Company", "Job Name": "Job Role"})
        fig.update_layout(**dark_layout(
            xaxis_title="Average Salary ($)", yaxis_title="Company",
            legend_title="Job Role",
            margin=dict(l=250, r=10, t=20, b=10), height=600
        ))
        st.plotly_chart(fig, use_container_width=True)
    st.markdown('<div class="insight-box">Algo Capital Group and Anthropic are among top payers. Anthropic pays $295k for Data Analyst roles!</div>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown('<div class="section-header">Top 10 Highest Paying Jobs</div>', unsafe_allow_html=True)
    df_j = top_jobs[["Job", "Name of Company", "AVG Salary", "Schedule"]].copy()
    df_j["AVG Salary"] = df_j["AVG Salary"].apply(lambda x: f"${x:,.0f}")
    df_j.columns = ["Job Title", "Company", "Avg Salary", "Schedule"]
    st.dataframe(df_j, use_container_width=True, hide_index=True)

# ─────────────────────────────────────────────────────────────────────────────
# PAGE 6 — SALARY PREDICTOR
# ─────────────────────────────────────────────────────────────────────────────
elif page == "Salary Predictor":
    import joblib
    import numpy as np

    st.markdown('<div class="page-title">Salary Predictor</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Predict your expected salary based on role, location & preferences</div>', unsafe_allow_html=True)

    # Load models
    rf_model    = joblib.load('models/salary_model.pkl')
    le_role     = joblib.load('models/le_role.pkl')
    le_country  = joblib.load('models/le_country.pkl')
    le_schedule = joblib.load('models/le_schedule.pkl')

    st.markdown("---")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-header">Your Profile</div>', unsafe_allow_html=True)

        role      = st.selectbox("Job Role", sorted(le_role.classes_))
        country   = st.selectbox("Country", sorted(le_country.classes_))
        schedule  = st.selectbox("Job Type", sorted([str(x) for x in le_schedule.classes_]))
        remote    = st.radio("Work Type", ["Remote", "Onsite"])
        degree    = st.radio("Degree Required", ["Not Required", "Required"])
        insurance = st.radio("Health Insurance", ["Yes", "No"])

    with col2:
        st.markdown('<div class="section-header">Predicted Salary</div>', unsafe_allow_html=True)

        # Encode inputs
        role_enc      = le_role.transform([role])[0]
        country_enc   = le_country.transform([country])[0]
        schedule_enc  = le_schedule.transform([schedule])[0]
        remote_val    = 1 if remote == "Remote" else 0
        degree_val    = 1 if degree == "Not Required" else 0
        insurance_val = 1 if insurance == "Yes" else 0

        features = np.array([[
            role_enc, country_enc, remote_val,
            degree_val, insurance_val, schedule_enc
        ]])

        predicted = rf_model.predict(features)[0]
        lower     = predicted * 0.85
        upper     = predicted * 1.15

        st.markdown(f"""
        <div class="metric-card" style="margin-top:2rem;">
            <div class="metric-label">Predicted Salary</div>
            <div class="metric-value">${predicted:,.0f}</div>
            <div class="metric-sub">Range: ${lower:,.0f} — ${upper:,.0f}</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-label">Model Info</div>
            <div class="metric-value" style="font-size:16px;">Random Forest</div>
            <div class="metric-sub">R²: 0.208 · MAE: $31,323</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="insight-box">Prediction based on 787k+ worldwide job postings. Salary may vary based on experience and company size.</div>', unsafe_allow_html=True)