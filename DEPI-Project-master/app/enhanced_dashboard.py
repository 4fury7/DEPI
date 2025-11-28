import streamlit as st
import pandas as pd
import pickle
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from scipy import stats
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import os
from styles import get_custom_css, card_component

# Configuration
st.set_page_config(
    page_title="🎓 Student Performance Dashboard",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Inject Custom CSS
st.markdown(get_custom_css(), unsafe_allow_html=True)


def gradient_header(title, subtitle):
    """Create a beautiful gradient header"""
    return f"""
    <div class="gradient-header">
        <h3 style="font-size: 2rem; font-weight: 800; margin: 0 !important;">{title}</h3>
        <p style="margin: 12px 0 0 0 !important; font-size: 1.05rem;">{subtitle}</p>
    </div>
    """


@st.cache_data
def load_data():
    """Load data from CSV file with proper column mapping for the dashboard."""
    # Get the directory of this script, then go up one level to project root
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(script_dir)
    csv_path = os.path.join(project_root, 'data', 'raw_student_data.csv')
    
    if not os.path.exists(csv_path):
        st.error('❌ Data file not found: data/raw_student_data.csv')
        return pd.DataFrame()
    
    try:
        df = pd.read_csv(csv_path)
        
        df = df.rename(columns={
            'student_id': 'student_name',
            'subject_id': 'subject_name', 
            'teacher_id': 'teacher_name',
            'attendance': 'total_attendance',
            'final_score': 'total_mark',
            'date': 'exam_date'
        })
        
        if 'subject_name' in df.columns:
            df['subject_name'] = df['subject_name'].apply(
                lambda x: str(x).replace('SUB_', '').replace('_', ' ').title()[:20] if pd.notna(x) else 'Unknown'
            )
        
        if 'student_name' in df.columns:
            df['student_name'] = df['student_name'].apply(
                lambda x: 'Student ' + str(x).replace('STU_', '').replace('_', '')[:10] if pd.notna(x) else 'Unknown'
            )
        
        if 'teacher_name' in df.columns:
            df['teacher_name'] = df['teacher_name'].apply(
                lambda x: 'Teacher ' + str(x).replace('TCH_', '').replace('_', '')[:10] if pd.notna(x) else 'Unknown'
            )
        
        if 'class' not in df.columns:
            np.random.seed(42)
            classes = ['Class A', 'Class B', 'Class C', 'Class D']
            df['class'] = np.random.choice(classes, size=len(df))
        
        if 'gender' not in df.columns:
            np.random.seed(42)
            df['gender'] = np.random.choice(['Male', 'Female'], size=len(df))
        
        if 'score_id' not in df.columns:
            df['score_id'] = range(1, len(df) + 1)
        
        for col in ['exam_1', 'exam_2', 'exam_3', 'total_attendance', 'total_mark']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        if 'exam_date' in df.columns:
            df['exam_date'] = pd.to_datetime(df['exam_date'], errors='coerce')
        
        return df
        
    except Exception as e:
        st.error(f'❌ Error loading data: {str(e)}')
        return pd.DataFrame()


# Load data
df = load_data()

# Sidebar Navigation with icons
st.sidebar.title("🎯 Navigation")
page = st.sidebar.radio("Go to", [
    "📊 Overview", 
    "📈 Advanced Insights", 
    "🧬 Statistical Analysis", 
    "🔮 Predictive Analytics",
    "🎯 Risk Analysis",
    "🏆 Performance Benchmarking",
    "📄 Raw Data"
])
page = page.split(" ", 1)[1]

st.sidebar.markdown("---")
st.sidebar.markdown("### 🔍 Filters")

# Validate data
if df is None or df.empty:
    st.error("❌ No data available. Please ensure data/raw_student_data.csv exists.")
    st.stop()

required_cols = {'subject_name', 'class', 'total_mark', 'total_attendance', 'student_name'}
available_cols = set(df.columns)
missing_cols = required_cols - available_cols

if missing_cols:
    st.error(f"❌ Missing required columns: {', '.join(sorted(missing_cols))}")
    st.info(f"📋 Available columns: {', '.join(sorted(df.columns))}")
    st.stop()

# Filters
selected_subject = st.sidebar.multiselect(
    "📚 Select Subject", 
    sorted(df['subject_name'].unique()), 
    default=sorted(df['subject_name'].unique())[:5] if len(df['subject_name'].unique()) > 5 else sorted(df['subject_name'].unique())
)
selected_class = st.sidebar.multiselect(
    "🎓 Select Class", 
    sorted(df['class'].unique()), 
    default=sorted(df['class'].unique())
)

# Filter Data
if selected_subject and selected_class:
    filtered_df = df[df['subject_name'].isin(selected_subject) & df['class'].isin(selected_class)]
else:
    filtered_df = df.copy()

if filtered_df.empty:
    st.warning("⚠️ No data matches the selected filters. Please adjust your selection.")
    st.stop()


# Updated chart styling for glassmorphic theme
def update_chart_layout(fig, title=""):
    """Apply consistent glassmorphic styling to charts"""
    fig.update_layout(
        plot_bgcolor='rgba(255, 255, 255, 0.1)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#ffffff', family='Inter', size=13),
        title=dict(
            text=title,
            font=dict(size=20, color='#ffffff', family='Inter'),
            x=0.05
        ),
        xaxis=dict(
            showgrid=True, 
            gridcolor='rgba(255, 255, 255, 0.1)',
            color='rgba(255, 255, 255, 0.9)'
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            color='rgba(255, 255, 255, 0.9)'
        ),
        margin=dict(l=40, r=40, t=60, b=40),
        showlegend=True,
        legend=dict(
            bgcolor='rgba(255, 255, 255, 0.1)',
            bordercolor='rgba(255, 255, 255, 0.2)',
            font=dict(color='white')
        )
    )
    return fig


# ============== PAGE: OVERVIEW ==============
if page == "Overview":
    st.title("🎓 Student Performance Dashboard")
    st.markdown("### 📈 Key Performance Indicators")
    
    col1, col2, col3, col4 = st.columns(4)
    
    avg_score = filtered_df['total_mark'].mean()
    avg_attendance = filtered_df['total_attendance'].mean()
    total_students = filtered_df['student_name'].nunique()
    
    if not filtered_df.empty and 'total_mark' in filtered_df.columns:
        top_idx = filtered_df['total_mark'].idxmax()
        top_performer = filtered_df.loc[top_idx, 'student_name'] if pd.notna(top_idx) else "N/A"
    else:
        top_performer = "N/A"
    
    with col1:
        st.markdown(card_component("Average Score", f"{avg_score:.1f}", "Across all subjects"), unsafe_allow_html=True)
    with col2:
        st.markdown(card_component("Avg Attendance", f"{avg_attendance:.1f}/10", "Lectures attended"), unsafe_allow_html=True)
    with col3:
        st.markdown(card_component("Total Students", f"{total_students}", "Active students"), unsafe_allow_html=True)
    with col4:
        display_name = str(top_performer).split()[1] if len(str(top_performer).split()) > 1 else str(top_performer)[:10]
        st.markdown(card_component("Top Performer", display_name, "Highest score"), unsafe_allow_html=True)

    st.markdown("### 📊 Performance Trends & Analytics")
    
    # Chart: Average Score by Subject
    subject_avg = filtered_df.groupby('subject_name')['total_mark'].mean().reset_index()
    fig_bar = px.bar(
        subject_avg,
        x='subject_name',
        y='total_mark',
        title="📊 Average Score by Subject"
    )
    fig_bar.update_traces(
        marker_color='rgba(139, 92, 246, 0.8)',
        marker_line_color='rgba(255, 255, 255, 0.5)',
        marker_line_width=1.5
    )
    fig_bar = update_chart_layout(fig_bar)
    st.plotly_chart(fig_bar, use_container_width=True)
    
    # Two column charts
    col1, col2 = st.columns(2)
    
    with col1:
        fig_hist = px.histogram(filtered_df, x='total_mark', nbins=20, title="📈 Score Distribution")
        fig_hist.update_traces(marker_color='rgba(96, 165, 250, 0.7)')
        fig_hist = update_chart_layout(fig_hist)
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        fig_scatter = px.scatter(
            filtered_df, 
            x='total_attendance', 
            y='total_mark',
            color='subject_name',
            title="📉 Attendance vs Score",
            opacity=0.7
        )
        fig_scatter = update_chart_layout(fig_scatter)
        st.plotly_chart(fig_scatter, use_container_width=True)


# ============== PAGE: ADVANCED INSIGHTS ==============
elif page == "Advanced Insights":
    st.title("📈 Advanced Analytics & Insights")
    
    st.markdown("### 🎯 Subject Performance Analysis")
    
    subject_stats = filtered_df.groupby('subject_name').agg({
        'total_mark': ['mean', 'std', 'min', 'max', 'count'],
        'total_attendance': 'mean'
    }).round(2)
    subject_stats.columns = ['Avg Score', 'Std Dev', 'Min Score', 'Max Score', 'Count', 'Avg Attendance']
    subject_stats = subject_stats.reset_index()
    
    st.dataframe(subject_stats, use_container_width=True, hide_index=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_box = px.box(filtered_df, x='subject_name', y='total_mark', title="📊 Score Distribution by Subject")
        fig_box.update_traces(marker_color='rgba(167, 139, 250, 0.7)')
        fig_box = update_chart_layout(fig_box)
        st.plotly_chart(fig_box, use_container_width=True)
    
    with col2:
        class_stats = filtered_df.groupby('class')['total_attendance'].mean().reset_index()
        fig_att = px.bar(class_stats, x='class', y='total_attendance', title="📅 Avg Attendance by Class")
        fig_att.update_traces(marker_color='rgba(52, 211, 153, 0.7)')
        fig_att = update_chart_layout(fig_att)
        st.plotly_chart(fig_att, use_container_width=True)
    
    # Performance Heatmap
    st.markdown("### 🌡️ Subject Performance Heatmap")
    
    if 'exam_date' in filtered_df.columns and filtered_df['exam_date'].notna().any():
        filtered_df['month'] = filtered_df['exam_date'].dt.to_period('M').astype(str)
        pivot_data = filtered_df.groupby(['subject_name', 'month'])['total_mark'].mean().reset_index()
        pivot_table = pivot_data.pivot(index='subject_name', columns='month', values='total_mark')
        
        if not pivot_table.empty:
            fig_heat = px.imshow(
                pivot_table,
                labels=dict(x="Month", y="Subject", color="Avg Score"),
                color_continuous_scale='Turbo'
            )
            fig_heat = update_chart_layout(fig_heat)
            st.plotly_chart(fig_heat, use_container_width=True)
    
    # Gender comparison
    st.markdown("### 👥 Performance by Gender")
    gender_stats = filtered_df.groupby('gender')['total_mark'].agg(['mean', 'count']).round(2)
    gender_stats.columns = ['Average Score', 'Count']
    
    col1, col2 = st.columns([1, 2])
    with col1:
        st.dataframe(gender_stats, use_container_width=True)
    with col2:
        fig_gender = px.bar(
            filtered_df.groupby('gender')['total_mark'].mean().reset_index(),
            x='gender', y='total_mark', color='gender',
            title="Average Score by Gender"
        )
        fig_gender = update_chart_layout(fig_gender)
        fig_gender.update_layout(showlegend=False)
        st.plotly_chart(fig_gender, use_container_width=True)


# ============== PAGE: STATISTICAL ANALYSIS ==============
elif page == "Statistical Analysis":
    st.title("🧬 Statistical Analysis")
    
    st.markdown(gradient_header(
        "📊 Hypothesis Testing & Deep Analytics",
        "Advanced statistical methods for data-driven decisions"
    ), unsafe_allow_html=True)
    
    st.markdown("### 📊 Descriptive Statistics")
    numeric_cols = ['exam_1', 'exam_2', 'exam_3', 'total_attendance', 'total_mark']
    available_numeric = [col for col in numeric_cols if col in filtered_df.columns]
    
    if available_numeric:
        desc_stats = filtered_df[available_numeric].describe().round(2)
        st.dataframe(desc_stats, use_container_width=True)
    
    st.markdown("### 🔗 Correlation Matrix")
    
    if len(available_numeric) >= 2:
        corr_matrix = filtered_df[available_numeric].corr()
        fig_corr = px.imshow(
            corr_matrix, 
            text_auto='.2f', 
            color_continuous_scale='RdBu_r',
            title="Correlation Heatmap"
        )
        fig_corr = update_chart_layout(fig_corr)
        st.plotly_chart(fig_corr, use_container_width=True)
    
    # Hypothesis Testing: Gender
    st.markdown("### 🔬 Hypothesis Testing: Gender vs Performance")
    
    male_scores = filtered_df[filtered_df['gender'] == 'Male']['total_mark']
    female_scores = filtered_df[filtered_df['gender'] == 'Female']['total_mark']
    
    if len(male_scores) > 1 and len(female_scores) > 1:
        t_stat, p_value = stats.ttest_ind(male_scores, female_scores)
        
        col1, col2 = st.columns(2)
        with col1:
            st.metric("T-Statistic", f"{t_stat:.4f}")
        with col2:
            significance = "✅ Significant" if p_value < 0.05 else "❌ Not Significant"
            st.metric("P-Value", f"{p_value:.4f}", delta=significance)
        
        if p_value < 0.05:
            st.info("🔍 There IS a statistically significant difference between male and female performance.")
        else:
            st.info("🔍 There is NO statistically significant difference between male and female performance.")
        
        # Box plot comparison
        fig_box = go.Figure()
        fig_box.add_trace(go.Box(y=male_scores, name='Male', marker_color='rgba(96, 165, 250, 0.7)', boxmean='sd'))
        fig_box.add_trace(go.Box(y=female_scores, name='Female', marker_color='rgba(244, 114, 182, 0.7)', boxmean='sd'))
        fig_box = update_chart_layout(fig_box, "Score Distribution by Gender")
        st.plotly_chart(fig_box, use_container_width=True)
    
    # Distribution Analysis
    st.markdown("### 📈 Distribution Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_hist = go.Figure()
        fig_hist.add_trace(go.Histogram(x=filtered_df['total_mark'], nbinsx=25, marker_color='rgba(139, 92, 246, 0.7)'))
        fig_hist = update_chart_layout(fig_hist, "Score Distribution Histogram")
        st.plotly_chart(fig_hist, use_container_width=True)
    
    with col2:
        if len(filtered_df) >= 20:
            sample_size = min(5000, len(filtered_df))
            stat, p_value = stats.shapiro(filtered_df['total_mark'].sample(sample_size, random_state=42))
            st.metric("Shapiro-Wilk p-value", f"{p_value:.4f}")
            if p_value > 0.05:
                st.success("✅ Data appears normally distributed (p > 0.05)")
            else:
                st.info("ℹ️ Data may not be normally distributed (p ≤ 0.05)")


# ============== PAGE: PREDICTIVE ANALYTICS ==============
elif page == "Predictive Analytics":
    st.title("🔮 Predictive Analytics")
    
    st.markdown(gradient_header(
        "🚀 Performance Prediction & Segmentation",
        "ML-powered insights for proactive interventions"
    ), unsafe_allow_html=True)
    
    # Trend Analysis
    st.markdown("### 📈 Trend Analysis")
    
    if 'exam_date' in filtered_df.columns and filtered_df['exam_date'].notna().any():
        monthly = filtered_df.groupby(filtered_df['exam_date'].dt.to_period('M'))['total_mark'].mean()
        monthly_df = monthly.reset_index()
        monthly_df['exam_date'] = monthly_df['exam_date'].astype(str)
        
        fig_trend = px.line(monthly_df, x='exam_date', y='total_mark', title="📈 Monthly Average Score Trend", markers=True)
        fig_trend.update_traces(line_color='rgba(96, 165, 250, 0.9)', line_width=3)
        fig_trend = update_chart_layout(fig_trend)
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("📅 Date-based trend analysis not available")
    
    # Clustering
    st.markdown("### 🎯 Student Clustering (K-Means)")
    
    if len(filtered_df) >= 10:
        features = ['total_mark', 'total_attendance']
        X = filtered_df[features].dropna()
        
        if len(X) >= 10:
            n_clusters = st.slider("Number of Clusters", 2, 5, 3)
            
            scaler = StandardScaler()
            X_scaled = scaler.fit_transform(X)
            
            kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
            clusters = kmeans.fit_predict(X_scaled)
            
            cluster_df = X.copy()
            cluster_df['Cluster'] = clusters
            
            fig_cluster = px.scatter(
                cluster_df,
                x='total_attendance',
                y='total_mark',
                color='Cluster',
                title="🎯 Student Clusters",
                color_continuous_scale='Viridis'
            )
            fig_cluster = update_chart_layout(fig_cluster)
            st.plotly_chart(fig_cluster, use_container_width=True)
            
            # Cluster statistics
            st.markdown("#### 📊 Cluster Characteristics")
            cluster_stats = cluster_df.groupby('Cluster')[features].mean().round(2)
            cluster_stats['Count'] = cluster_df.groupby('Cluster').size()
            st.dataframe(cluster_stats, use_container_width=True)
            
            st.info("""
            💡 **How to use this:**
            - **High performers** (high score, high attendance) → Advanced programs
            - **At-risk students** (low score, low attendance) → Intensive support
            - **Inconsistent performers** → Motivation programs
            """)
    else:
        st.warning("⚠️ Not enough data for clustering (need at least 10 records)")


# ============== PAGE: RISK ANALYSIS ==============
elif page == "Risk Analysis":
    st.title("🎯 Student Risk Analysis")
    
    st.markdown(gradient_header(
        "⚠️ Proactive Student Support System",
        "Identify at-risk students early"
    ), unsafe_allow_html=True)
    
    # Calculate Risk Score
    risk_df = filtered_df.copy()
    risk_df['attendance_risk'] = (10 - risk_df['total_attendance']) * 10
    risk_df['score_risk'] = 100 - risk_df['total_mark']
    risk_df['risk_score'] = (risk_df['attendance_risk'] * 0.4 + risk_df['score_risk'] * 0.6).clip(0, 100)
    
    def categorize_risk(score):
        if score >= 70:
            return "🔴 Critical"
        elif score >= 50:
            return "🟠 High"
        elif score >= 30:
            return "🟡 Medium"
        else:
            return "🟢 Low"
    
    risk_df['risk_category'] = risk_df['risk_score'].apply(categorize_risk)
    
    # Summary Cards
    col1, col2, col3, col4 = st.columns(4)
    
    critical = len(risk_df[risk_df['risk_category'] == "🔴 Critical"])
    high = len(risk_df[risk_df['risk_category'] == "🟠 High"])
    medium = len(risk_df[risk_df['risk_category'] == "🟡 Medium"])
    low = len(risk_df[risk_df['risk_category'] == "🟢 Low"])
    
    with col1:
        st.markdown(card_component("CRITICAL RISK", str(critical), "Immediate attention needed"), unsafe_allow_html=True)
    
    with col2:
        st.markdown(card_component("HIGH RISK", str(high), "Needs monitoring"), unsafe_allow_html=True)
    
    with col3:
        st.markdown(card_component("MEDIUM RISK", str(medium), "Watch closely"), unsafe_allow_html=True)
    
    with col4:
        st.markdown(card_component("LOW RISK", str(low), "On track"), unsafe_allow_html=True)
    
    # Risk distribution charts
    st.markdown("### 📊 Risk Distribution")
    risk_counts = risk_df['risk_category'].value_counts().reset_index()
    risk_counts.columns = ['Category', 'Count']
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_risk = px.pie(risk_counts, values='Count', names='Category', title="Risk Category Distribution", hole=0.4)
        fig_risk = update_chart_layout(fig_risk)
        st.plotly_chart(fig_risk, use_container_width=True)
    
    with col2:
        fig_scatter_risk = px.scatter(
            risk_df,
            x='total_attendance',
            y='total_mark',
            color='risk_category',
            title="Risk by Score & Attendance",
            opacity=0.7
        )
        fig_scatter_risk = update_chart_layout(fig_scatter_risk)
        st.plotly_chart(fig_scatter_risk, use_container_width=True)
    
    # High-risk students table
    st.markdown("### 📋 High-Risk Students (Top 20)")
    at_risk = risk_df[risk_df['risk_score'] >= 50][
        ['student_name', 'subject_name', 'total_mark', 'total_attendance', 'risk_score', 'risk_category']
    ].sort_values('risk_score', ascending=False).head(20)
    
    if not at_risk.empty:
        st.dataframe(at_risk, use_container_width=True, hide_index=True)
    else:
        st.success("✅ No high-risk students found!")


# ============== PAGE: PERFORMANCE BENCHMARKING ==============
elif page == "Performance Benchmarking":
    st.title("🏆 Performance Benchmarking")
    
    st.markdown(gradient_header(
        "📊 Multi-Dimensional Performance Analysis",
        "Compare performance across subjects, classes, and time periods"
    ), unsafe_allow_html=True)
    
    # Subject Difficulty Analysis
    st.markdown("### 📚 Subject Difficulty Analysis")
    
    subject_perf = filtered_df.groupby('subject_name').agg({
        'total_mark': 'mean',
        'student_name': 'count'
    }).round(2)
    subject_perf.columns = ['Avg Score', 'Students']
    subject_perf['Difficulty'] = (100 - subject_perf['Avg Score']).clip(0, 100)
    subject_perf = subject_perf.sort_values('Difficulty', ascending=False).reset_index()
    
    fig_diff = px.bar(
        subject_perf,
        x='subject_name',
        y='Difficulty',
        color='Difficulty',
        color_continuous_scale='RdYlGn_r',
        title="📚 Subject Difficulty Index (Higher = More Difficult)"
    )
    fig_diff = update_chart_layout(fig_diff)
    fig_diff.update_layout(showlegend=False)
    st.plotly_chart(fig_diff, use_container_width=True)
    
    # Top Performers
    st.markdown("### 🏅 Top Performers")
    
    top_students = filtered_df.groupby('student_name')['total_mark'].mean().sort_values(ascending=False).head(10).reset_index()
    top_students.columns = ['Student', 'Avg Score']
    top_students['Rank'] = range(1, len(top_students) + 1)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig_top = px.bar(top_students, x='Student', y='Avg Score', title="🏆 Top 10 Students by Average Score")
        fig_top.update_traces(marker_color='rgba(251, 191, 36, 0.8)')
        fig_top = update_chart_layout(fig_top)
        st.plotly_chart(fig_top, use_container_width=True)
    
    with col2:
        st.dataframe(top_students[['Rank', 'Student', 'Avg Score']], use_container_width=True, hide_index=True)
    
    # Class Comparison
    st.markdown("### 🎓 Class Performance Comparison")
    
    class_perf = filtered_df.groupby('class').agg({
        'total_mark': ['mean', 'std'],
        'total_attendance': 'mean',
        'student_name': 'nunique'
    }).round(2)
    class_perf.columns = ['Avg Score', 'Std Dev', 'Avg Attendance', 'Students']
    class_perf = class_perf.reset_index()
    
    st.dataframe(class_perf, use_container_width=True, hide_index=True)
    
    fig_class = px.bar(class_perf, x='class', y='Avg Score', color='Avg Attendance',
                       title="Class Performance Overview", color_continuous_scale='Blues')
    fig_class = update_chart_layout(fig_class)
    st.plotly_chart(fig_class, use_container_width=True)


# ============== PAGE: RAW DATA ==============
elif page == "Raw Data":
    st.title("📄 Raw Data Explorer")
    
    st.markdown(f"### 📊 Dataset Overview ({len(filtered_df):,} records)")
    
    # Search
    search = st.text_input("🔍 Search in data", "")
    
    if search:
        mask = filtered_df.astype(str).apply(lambda x: x.str.contains(search, case=False, na=False)).any(axis=1)
        display_df = filtered_df[mask]
        st.info(f"Found {len(display_df):,} matching records")
    else:
        display_df = filtered_df
    
    st.dataframe(display_df, use_container_width=True, hide_index=True, height=500)
    
    # Column info
    with st.expander("📋 Column Information"):
        col_info = pd.DataFrame({
            'Column': display_df.columns,
            'Type': display_df.dtypes.astype(str),
            'Non-Null': display_df.count().values,
            'Unique': display_df.nunique().values
        })
        st.dataframe(col_info, use_container_width=True, hide_index=True)
    
    # Download button
    csv = display_df.to_csv(index=False)
    st.download_button(
        label="📥 Download as CSV",
        data=csv,
        file_name="student_performance_data.csv",
        mime="text/csv"
    )


# ============== FOOTER ==============
st.markdown("---")
st.markdown("""
<div style="text-align: center; padding: 24px; color: rgba(255, 255, 255, 0.7);">
    <p style="margin: 0; font-size: 1rem;">Built with ❤️ using <strong style="color: rgba(255, 255, 255, 0.95);">Streamlit</strong></p>
    <p style="margin: 8px 0 0 0; font-size: 0.9rem;">🎓 Student Performance Analytics Dashboard © 2025</p>
</div>
""", unsafe_allow_html=True)
