"""
BerkleyCore Loss Analysis Platform
Streamlit Edition

A comprehensive commercial insurance claims analysis tool for loss control consultants.
"""

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Configure page
st.set_page_config(
    page_title="BerkleyCore Loss Analysis Platform",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for BerkleyCore branding
st.markdown("""
<style>
    /* Main theme */
    .stApp {
        background: linear-gradient(135deg, #1e3a8a 0%, #3730a3 100%);
    }
    
    /* Cards */
    .metric-card {
        background: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 16px;
    }
    
    /* Headers */
    h1, h2, h3 {
        color: #1e293b;
    }
    
    /* Metric styling */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: #1e3a8a;
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #64748b;
    }
    
    /* Risk score colors */
    .risk-critical { color: #dc2626; }
    .risk-high { color: #f59e0b; }
    .risk-moderate { color: #3b82f6; }
    .risk-low { color: #10b981; }
    
    /* Priority badges */
    .priority-critical {
        background: #fee2e2;
        color: #dc2626;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    .priority-high {
        background: #fed7aa;
        color: #c2410c;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    .priority-moderate {
        background: #dbeafe;
        color: #1e40af;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(255, 255, 255, 0.98);
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Import utilities
from utils.data_processing import load_file, process_claims_data, generate_sample_data
from utils.calculations import (
    calculate_summary, calculate_risk_score, generate_recommendations,
    group_by_dimension, format_currency, format_percent
)
from utils.visualizations import (
    create_loss_cause_chart, create_trend_chart, create_weekday_chart,
    create_status_pie, create_lob_chart, create_severity_distribution,
    create_lag_histogram, create_monthly_trend, create_state_map
)


def init_session_state():
    """Initialize session state variables."""
    if 'claims_data' not in st.session_state:
        st.session_state.claims_data = None
    if 'summary' not in st.session_state:
        st.session_state.summary = None
    if 'risk_score' not in st.session_state:
        st.session_state.risk_score = None
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = None
    if 'format_type' not in st.session_state:
        st.session_state.format_type = None


def sidebar():
    """Render sidebar with navigation and upload."""
    with st.sidebar:
        st.image("https://via.placeholder.com/200x50/1e3a8a/ffffff?text=BerkleyCore", width=200)
        st.markdown("### Loss Analysis Platform")
        st.markdown("---")
        
        # File upload
        st.markdown("#### 📁 Data Upload")
        uploaded_file = st.file_uploader(
            "Upload claims data",
            type=['csv', 'xlsx', 'xls'],
            help="Supports CSV, Excel, and Tableau exports"
        )
        
        if uploaded_file:
            with st.spinner("Processing file..."):
                try:
                    df, format_type = load_file(uploaded_file)
                    df = process_claims_data(df)
                    st.session_state.claims_data = df
                    st.session_state.format_type = format_type
                    
                    # Calculate summary and risk
                    st.session_state.summary = calculate_summary(df)
                    st.session_state.risk_score = calculate_risk_score(df, st.session_state.summary)
                    recs, savings, avg_roi = generate_recommendations(df, st.session_state.summary)
                    st.session_state.recommendations = {
                        'items': recs,
                        'total_savings': savings,
                        'avg_roi': avg_roi
                    }
                    
                    st.success(f"✅ Loaded {len(df):,} claims ({format_type})")
                except Exception as e:
                    st.error(f"Error loading file: {str(e)}")
        
        # Sample data option
        st.markdown("---")
        if st.button("📊 Load Sample Data", use_container_width=True):
            with st.spinner("Generating sample data..."):
                df = generate_sample_data(500)
                df = process_claims_data(df)
                st.session_state.claims_data = df
                st.session_state.format_type = "Sample Data"
                
                st.session_state.summary = calculate_summary(df)
                st.session_state.risk_score = calculate_risk_score(df, st.session_state.summary)
                recs, savings, avg_roi = generate_recommendations(df, st.session_state.summary)
                st.session_state.recommendations = {
                    'items': recs,
                    'total_savings': savings,
                    'avg_roi': avg_roi
                }
                
                st.success("✅ Sample data loaded!")
        
        # Data info
        if st.session_state.claims_data is not None:
            st.markdown("---")
            st.markdown("#### 📋 Data Summary")
            summary = st.session_state.summary
            st.metric("Total Claims", f"{summary.total_claims:,}")
            st.metric("Total Incurred", format_currency(summary.total_incurred))
            st.metric("Format", st.session_state.format_type)
        
        # Footer
        st.markdown("---")
        st.markdown(
            "<div style='text-align: center; color: #64748b; font-size: 12px;'>"
            "BerkleyCore v2.0<br>Streamlit Edition"
            "</div>",
            unsafe_allow_html=True
        )


def dashboard_page():
    """Render main dashboard."""
    st.title("📊 Dashboard")
    
    if st.session_state.claims_data is None:
        st.info("👆 Upload claims data using the sidebar to get started, or load sample data for a demo.")
        
        # Show feature overview
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("""
            ### 📁 Easy Data Import
            - CSV and Excel files
            - Tableau exports
            - Universal field mapping
            - Auto-format detection
            """)
        with col2:
            st.markdown("""
            ### 📈 Advanced Analytics
            - KPI dashboards
            - Trend analysis
            - Risk scoring
            - ROI calculations
            """)
        with col3:
            st.markdown("""
            ### 🛡️ Risk Control
            - Mitigation strategies
            - Payback analysis
            - Priority rankings
            - Action plans
            """)
        return
    
    df = st.session_state.claims_data
    summary = st.session_state.summary
    risk = st.session_state.risk_score
    
    # Top metrics row
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.metric(
            "Total Claims",
            f"{summary.total_claims:,}",
            help="Total number of claims in dataset"
        )
    
    with col2:
        st.metric(
            "Total Incurred",
            format_currency(summary.total_incurred),
            help="Sum of all incurred losses"
        )
    
    with col3:
        st.metric(
            "Average Claim",
            format_currency(summary.avg_claim),
            help="Average incurred per claim"
        )
    
    with col4:
        st.metric(
            "Open Claims",
            f"{summary.open_claims:,}",
            delta=f"{(summary.open_claims/summary.total_claims*100):.1f}%",
            delta_color="inverse",
            help="Claims still open"
        )
    
    with col5:
        risk_color = {
            'Critical': '🔴',
            'High': '🟠',
            'Moderate': '🟡',
            'Low': '🟢'
        }
        st.metric(
            "Risk Score",
            f"{risk_color.get(risk.level, '')} {risk.total_score}",
            delta=risk.level,
            delta_color="off",
            help="Overall risk assessment (0-100)"
        )
    
    st.markdown("---")
    
    # Charts row 1
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_loss_cause_chart(df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_trend_chart(df), use_container_width=True)
    
    # Charts row 2
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(create_weekday_chart(df), use_container_width=True)
    
    with col2:
        st.plotly_chart(create_status_pie(df), use_container_width=True)


def analysis_page():
    """Render detailed analysis page."""
    st.title("🔍 Detailed Analysis")
    
    if st.session_state.claims_data is None:
        st.warning("Please upload data first.")
        return
    
    df = st.session_state.claims_data
    
    # Analysis tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🗺️ Geography", "📊 Distributions", "📋 Data Table"])
    
    with tab1:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_monthly_trend(df), use_container_width=True)
        with col2:
            st.plotly_chart(create_lob_chart(df), use_container_width=True)
    
    with tab2:
        st.plotly_chart(create_state_map(df), use_container_width=True)
        
        # State breakdown table
        if 'state' in df.columns:
            state_data = group_by_dimension(df, 'state')
            st.dataframe(
                state_data.head(10).style.format({
                    'total': '${:,.0f}',
                    'average': '${:,.0f}'
                }),
                use_container_width=True
            )
    
    with tab3:
        col1, col2 = st.columns(2)
        with col1:
            st.plotly_chart(create_severity_distribution(df), use_container_width=True)
        with col2:
            st.plotly_chart(create_lag_histogram(df), use_container_width=True)
    
    with tab4:
        # Data table with filters
        st.markdown("### Claims Data")
        
        # Filters
        col1, col2, col3 = st.columns(3)
        with col1:
            if 'policy_year' in df.columns:
                years = ['All'] + sorted(df['policy_year'].dropna().unique().tolist())
                selected_year = st.selectbox("Policy Year", years)
        with col2:
            if 'status' in df.columns:
                statuses = ['All'] + df['status'].dropna().unique().tolist()
                selected_status = st.selectbox("Status", statuses)
        with col3:
            if 'loss_cause' in df.columns:
                causes = ['All'] + sorted(df['loss_cause'].dropna().unique().tolist())
                selected_cause = st.selectbox("Loss Cause", causes)
        
        # Apply filters
        filtered_df = df.copy()
        if 'policy_year' in df.columns and selected_year != 'All':
            filtered_df = filtered_df[filtered_df['policy_year'] == selected_year]
        if 'status' in df.columns and selected_status != 'All':
            filtered_df = filtered_df[filtered_df['status'] == selected_status]
        if 'loss_cause' in df.columns and selected_cause != 'All':
            filtered_df = filtered_df[filtered_df['loss_cause'] == selected_cause]
        
        st.dataframe(filtered_df, use_container_width=True, height=400)
        
        # Download button
        csv = filtered_df.to_csv(index=False)
        st.download_button(
            "📥 Download Filtered Data",
            csv,
            "claims_data.csv",
            "text/csv",
            use_container_width=True
        )


def risk_control_page():
    """Render risk control recommendations page."""
    st.title("🛡️ Risk Control Recommendations")
    
    if st.session_state.claims_data is None:
        st.warning("Please upload data first.")
        return
    
    risk = st.session_state.risk_score
    recs = st.session_state.recommendations
    
    # Risk score header
    risk_colors = {
        'Critical': '#dc2626',
        'High': '#f59e0b',
        'Moderate': '#3b82f6',
        'Low': '#10b981'
    }
    
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #1e3a8a, #3730a3); 
                color: white; padding: 30px; border-radius: 12px; margin-bottom: 24px;">
        <h2 style="margin: 0; color: white;">Risk Assessment</h2>
        <div style="display: flex; gap: 40px; margin-top: 20px; flex-wrap: wrap;">
            <div style="text-align: center;">
                <div style="font-size: 48px; font-weight: bold; color: {risk_colors[risk.level]};">
                    {risk.total_score}
                </div>
                <div style="font-size: 14px; opacity: 0.9;">Risk Score ({risk.level})</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 32px; font-weight: bold; color: #10b981;">
                    {format_currency(recs['total_savings'])}
                </div>
                <div style="font-size: 14px; opacity: 0.9;">Potential Savings</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 32px; font-weight: bold;">
                    {len(recs['items'])}
                </div>
                <div style="font-size: 14px; opacity: 0.9;">Recommendations</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 32px; font-weight: bold; color: #10b981;">
                    {recs['avg_roi']:.0f}%
                </div>
                <div style="font-size: 14px; opacity: 0.9;">Average ROI</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Risk factors breakdown
    with st.expander("📊 Risk Factor Breakdown"):
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Severity Factor", f"{risk.factors.get('severity', 0)}/25")
        with col2:
            st.metric("Frequency Factor", f"{risk.factors.get('frequency', 0)}/25")
        with col3:
            st.metric("Open Rate Factor", f"{risk.factors.get('open_rate', 0)}/25")
        with col4:
            st.metric("Lag Time Factor", f"{risk.factors.get('lag', 0)}/25")
    
    # Recommendations
    st.markdown("### 💡 Prioritized Recommendations")
    
    if not recs['items']:
        st.info("No specific recommendations generated. Consider implementing general safety improvements.")
    else:
        for i, rec in enumerate(recs['items'], 1):
            priority_class = f"priority-{rec.priority}"
            
            with st.container():
                st.markdown(f"""
                <div style="background: white; border-radius: 12px; padding: 20px; 
                            margin-bottom: 20px; border-left: 4px solid 
                            {'#dc2626' if rec.priority == 'critical' else '#f59e0b' if rec.priority == 'high' else '#3b82f6'};">
                    <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 15px;">
                        <h4 style="margin: 0; color: #1e293b;">{rec.strategy_name}</h4>
                        <span class="{priority_class}">{rec.priority.upper()} PRIORITY</span>
                    </div>
                    <p style="color: #64748b; margin-bottom: 15px;">
                        Addresses: <strong>{rec.cause}</strong> 
                        ({rec.frequency} claims, {format_currency(rec.total_loss)} total loss)
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                # ROI metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Implementation Cost", format_currency(rec.implementation_cost))
                with col2:
                    st.metric("Potential Savings", format_currency(rec.potential_savings))
                with col3:
                    st.metric("ROI", f"{rec.roi:.0f}%")
                with col4:
                    st.metric("Payback Period", f"{rec.payback_months} months")
                
                # Actions
                with st.expander(f"📋 Implementation Actions"):
                    for action in rec.actions:
                        st.markdown(f"→ {action}")
                    
                    st.markdown(f"""
                    ---
                    **Expected Impact:** {rec.reduction_rate*100:.0f}% reduction potential  
                    **Confidence:** {'Low' if rec.confidence_factor < 0.7 else 'Moderate' if rec.confidence_factor < 0.9 else 'High'}  
                    **Net Annual Benefit:** {format_currency(rec.net_benefit)}
                    """)
                
                st.markdown("---")


def reports_page():
    """Render reports and export page."""
    st.title("📄 Reports & Export")
    
    if st.session_state.claims_data is None:
        st.warning("Please upload data first.")
        return
    
    df = st.session_state.claims_data
    summary = st.session_state.summary
    risk = st.session_state.risk_score
    recs = st.session_state.recommendations
    
    st.markdown("### Executive Summary Report")
    
    # Generate report content
    report_date = datetime.now().strftime("%B %d, %Y")
    
    report_md = f"""
# BerkleyCore Loss Analysis Report
**Generated:** {report_date}  
**Data Source:** {st.session_state.format_type}  
**Analysis Period:** {df['policy_year'].min() if 'policy_year' in df.columns else 'N/A'} - {df['policy_year'].max() if 'policy_year' in df.columns else 'N/A'}

---

## Executive Summary

| Metric | Value |
|--------|-------|
| Total Claims | {summary.total_claims:,} |
| Total Incurred | {format_currency(summary.total_incurred)} |
| Total Paid | {format_currency(summary.total_paid)} |
| Total Reserve | {format_currency(summary.total_reserve)} |
| Average Claim | {format_currency(summary.avg_claim)} |
| Open Claims | {summary.open_claims:,} ({summary.open_claims/summary.total_claims*100:.1f}%) |
| Closed Claims | {summary.closed_claims:,} ({summary.closed_claims/summary.total_claims*100:.1f}%) |
| Average Report Lag | {summary.avg_lag_time:.1f} days |

---

## Risk Assessment

**Overall Risk Score:** {risk.total_score}/100 ({risk.level})

### Risk Factors
- Severity Factor: {risk.factors.get('severity', 0)}/25
- Frequency Factor: {risk.factors.get('frequency', 0)}/25
- Open Rate Factor: {risk.factors.get('open_rate', 0)}/25
- Lag Time Factor: {risk.factors.get('lag', 0)}/25

---

## Risk Mitigation Recommendations

**Total Potential Savings:** {format_currency(recs['total_savings'])}  
**Average ROI:** {recs['avg_roi']:.0f}%  
**Priority Actions:** {len([r for r in recs['items'] if r.priority in ['critical', 'high']])}

"""
    
    for i, rec in enumerate(recs['items'][:5], 1):
        report_md += f"""
### {i}. {rec.strategy_name} ({rec.priority.upper()} Priority)

- **Target:** {rec.cause}
- **Frequency:** {rec.frequency} claims
- **Total Loss:** {format_currency(rec.total_loss)}
- **Implementation Cost:** {format_currency(rec.implementation_cost)}
- **Potential Savings:** {format_currency(rec.potential_savings)}
- **ROI:** {rec.roi:.0f}%
- **Payback:** {rec.payback_months} months

"""
    
    report_md += """
---

*Report generated by BerkleyCore Loss Analysis Platform v2.0*
"""
    
    st.markdown(report_md)
    
    # Export options
    st.markdown("---")
    st.markdown("### Export Options")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.download_button(
            "📄 Download Report (Markdown)",
            report_md,
            "berkleycore_report.md",
            "text/markdown",
            use_container_width=True
        )
    
    with col2:
        csv_data = df.to_csv(index=False)
        st.download_button(
            "📊 Download Claims Data (CSV)",
            csv_data,
            "claims_data.csv",
            "text/csv",
            use_container_width=True
        )
    
    with col3:
        # Recommendations CSV
        if recs['items']:
            recs_data = pd.DataFrame([{
                'Strategy': r.strategy_name,
                'Priority': r.priority,
                'Loss Cause': r.cause,
                'Frequency': r.frequency,
                'Total Loss': r.total_loss,
                'Implementation Cost': r.implementation_cost,
                'Potential Savings': r.potential_savings,
                'ROI': f"{r.roi:.0f}%",
                'Payback Months': r.payback_months
            } for r in recs['items']])
            
            st.download_button(
                "💡 Download Recommendations (CSV)",
                recs_data.to_csv(index=False),
                "recommendations.csv",
                "text/csv",
                use_container_width=True
            )


def main():
    """Main application entry point."""
    init_session_state()
    sidebar()
    
    # Navigation
    page = st.radio(
        "Navigation",
        ["📊 Dashboard", "🔍 Analysis", "🛡️ Risk Control", "📄 Reports"],
        horizontal=True,
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    if page == "📊 Dashboard":
        dashboard_page()
    elif page == "🔍 Analysis":
        analysis_page()
    elif page == "🛡️ Risk Control":
        risk_control_page()
    elif page == "📄 Reports":
        reports_page()


if __name__ == "__main__":
    main()
