import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

# Page Configuration (Optional, makes the dashboard wider)
st.set_page_config(page_title="Student Dashboard", layout="wide")

# --- Data Loading ---
@st.cache_data  # Caches the data to prevent reloading on every interaction
def load_data():
    # Connect to the SQLite database
    conn = sqlite3.connect('school_data.db')
    
    # Read data into Pandas DataFrame
    query = "SELECT * FROM student_performance"
    df = pd.read_sql(query, conn)
    
    # Close connection
    conn.close()
    return df

try:
    df = load_data()
except Exception as e:
    st.error(f"Error loading database. Make sure 'school_data.db' exists. Error: {e}")
    st.stop()

# --- Sidebar: Filter Options ---
st.sidebar.header("Filter Options")

# Multi-select for Subject
# Get unique subjects for the list
unique_subjects = df['subject'].unique() if not df.empty else []
selected_subjects = st.sidebar.multiselect(
    "Select Subject(s):",
    options=unique_subjects,
    default=[] # Default is empty, which we handle as "Select All" logic below
)

# Apply Filter
if selected_subjects:
    df_filtered = df[df['subject'].isin(selected_subjects)]
else:
    df_filtered = df # If nothing selected, show all

# --- Main Dashboard Layout ---
st.title("Student Performance Dashboard")

# Check if dataframe is empty after filtering
if df_filtered.empty:
    st.warning("No data available for the selected filters.")
else:
    # --- KPI Row ---
    # Calculate metrics
    total_students = len(df_filtered)
    avg_score = df_filtered['score'].mean()
    avg_attendance = df_filtered['attendance'].mean()

    # Display metrics in columns
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Students", total_students)
    col2.metric("Average Score", f"{avg_score:.1f}")
    col3.metric("Average Attendance", f"{avg_attendance:.1f}%")

    st.markdown("---") # Divider

    # --- Charts ---
    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        st.subheader("Average Score by Grade")
        # Group by Grade and calculate mean score
        # Note: This uses the 'grade' column (A, B, C, etc.) from your database
        avg_score_grade = df_filtered.groupby('grade')['score'].mean().reset_index()
        
        fig_bar = px.bar(
            avg_score_grade, 
            x='grade', 
            y='score', 
            color='grade',
            title="Avg Score per Grade",
            template="plotly_white"
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with chart_col2:
        st.subheader("Attendance vs. Score")
        fig_scatter = px.scatter(
            df_filtered, 
            x='attendance', 
            y='score', 
            color='subject', # Color points by subject for better visibility
            title="Correlation: Attendance vs Score",
            hover_data=['name'],
            template="plotly_white"
        )
        st.plotly_chart(fig_scatter, use_container_width=True)

    # --- Raw Data ---
    st.subheader("Raw Data")
    st.dataframe(df_filtered, use_container_width=True)