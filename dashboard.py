import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

# Page configuration
st.set_page_config(page_title="Student Performance Dashboard", layout="wide", initial_sidebar_state="expanded")

# Custom title
st.markdown("""
    <style>
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    </style>
    <div class="main-title">📊 Student Performance Dashboard</div>
    """, unsafe_allow_html=True)

# Load data
@st.cache_data
def load_data():
    df = pd.read_csv('StudentsPerformance.csv')
    return df

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")
gender_filter = st.sidebar.multiselect("Select Gender:", options=df['gender'].unique(), default=df['gender'].unique())
race_filter = st.sidebar.multiselect("Select Race/Ethnicity:", options=df['race/ethnicity'].unique(), default=df['race/ethnicity'].unique())
education_filter = st.sidebar.multiselect("Select Parental Education:", options=df['parental level of education'].unique(), default=df['parental level of education'].unique())

# Apply filters
filtered_df = df[
    (df['gender'].isin(gender_filter)) &
    (df['race/ethnicity'].isin(race_filter)) &
    (df['parental level of education'].isin(education_filter))
]

# Key Metrics
st.sidebar.markdown("---")
st.sidebar.subheader("📈 Overall Statistics")
st.sidebar.metric("Total Students", len(filtered_df))
st.sidebar.metric("Avg Math Score", f"{filtered_df['math score'].mean():.1f}")
st.sidebar.metric("Avg Reading Score", f"{filtered_df['reading score'].mean():.1f}")
st.sidebar.metric("Avg Writing Score", f"{filtered_df['writing score'].mean():.1f}")

# Main content tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Overview", "📈 Score Distribution", "🔍 By Demographics", "📉 Correlations", "📋 Data"])

# TAB 1: Overview
with tab1:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        fig_math = go.Figure(data=[go.Box(y=filtered_df['math score'], name='Math Score', marker_color='#1f77b4')])
        fig_math.update_layout(title="Math Score Distribution", height=400, showlegend=False)
        st.plotly_chart(fig_math, use_container_width=True)
    
    with col2:
        fig_reading = go.Figure(data=[go.Box(y=filtered_df['reading score'], name='Reading Score', marker_color='#ff7f0e')])
        fig_reading.update_layout(title="Reading Score Distribution", height=400, showlegend=False)
        st.plotly_chart(fig_reading, use_container_width=True)
    
    with col3:
        fig_writing = go.Figure(data=[go.Box(y=filtered_df['writing score'], name='Writing Score', marker_color='#2ca02c')])
        fig_writing.update_layout(title="Writing Score Distribution", height=400, showlegend=False)
        st.plotly_chart(fig_writing, use_container_width=True)
    
    # Average scores by subject
    avg_scores = {
        'Math': filtered_df['math score'].mean(),
        'Reading': filtered_df['reading score'].mean(),
        'Writing': filtered_df['writing score'].mean()
    }
    
    fig_avg = go.Figure(data=[
        go.Bar(x=list(avg_scores.keys()), y=list(avg_scores.values()), marker_color=['#1f77b4', '#ff7f0e', '#2ca02c'])
    ])
    fig_avg.update_layout(title="Average Scores by Subject", height=400, yaxis_title="Score", xaxis_title="Subject")
    st.plotly_chart(fig_avg, use_container_width=True)

# TAB 2: Score Distribution
with tab2:
    col1, col2 = st.columns(2)
    
    with col1:
        fig_hist_math = px.histogram(filtered_df, x='math score', nbins=20, title="Math Score Distribution", color_discrete_sequence=['#1f77b4'])
        fig_hist_math.update_layout(height=400)
        st.plotly_chart(fig_hist_math, use_container_width=True)
    
    with col2:
        fig_hist_reading = px.histogram(filtered_df, x='reading score', nbins=20, title="Reading Score Distribution", color_discrete_sequence=['#ff7f0e'])
        fig_hist_reading.update_layout(height=400)
        st.plotly_chart(fig_hist_reading, use_container_width=True)
    
    fig_hist_writing = px.histogram(filtered_df, x='writing score', nbins=20, title="Writing Score Distribution", color_discrete_sequence=['#2ca02c'])
    fig_hist_writing.update_layout(height=400)
    st.plotly_chart(fig_hist_writing, use_container_width=True)

# TAB 3: By Demographics
with tab3:
    col1, col2 = st.columns(2)
    
    with col1:
        fig_gender = px.box(filtered_df, x='gender', y='math score', title="Math Score by Gender", color='gender')
        fig_gender.update_layout(height=400)
        st.plotly_chart(fig_gender, use_container_width=True)
    
    with col2:
        fig_race = px.box(filtered_df, x='race/ethnicity', y='reading score', title="Reading Score by Race/Ethnicity", color='race/ethnicity')
        fig_race.update_layout(height=400)
        st.plotly_chart(fig_race, use_container_width=True)
    
    fig_education = px.box(filtered_df, x='parental level of education', y='writing score', title="Writing Score by Parental Education", color='parental level of education')
    fig_education.update_layout(height=400)
    st.plotly_chart(fig_education, use_container_width=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_lunch = px.box(filtered_df, x='lunch', y='math score', title="Math Score by Lunch Type", color='lunch')
        fig_lunch.update_layout(height=400)
        st.plotly_chart(fig_lunch, use_container_width=True)
    
    with col2:
        fig_prep = px.box(filtered_df, x='test preparation course', y='reading score', title="Reading Score by Test Prep", color='test preparation course')
        fig_prep.update_layout(height=400)
        st.plotly_chart(fig_prep, use_container_width=True)

# TAB 4: Correlations
with tab4:
    # Correlation heatmap
    numeric_cols = ['math score', 'reading score', 'writing score']
    corr_matrix = filtered_df[numeric_cols].corr()
    
    fig_corr = px.imshow(corr_matrix, text_auto=True, title="Score Correlations", color_continuous_scale='viridis')
    fig_corr.update_layout(height=400)
    st.plotly_chart(fig_corr, use_container_width=True)
    
    # Scatter plots
    col1, col2 = st.columns(2)
    
    with col1:
        fig_scatter1 = px.scatter(filtered_df, x='math score', y='reading score', color='gender', title="Math vs Reading Scores", trendline="ols")
        fig_scatter1.update_layout(height=400)
        st.plotly_chart(fig_scatter1, use_container_width=True)
    
    with col2:
        fig_scatter2 = px.scatter(filtered_df, x='reading score', y='writing score', color='gender', title="Reading vs Writing Scores", trendline="ols")
        fig_scatter2.update_layout(height=400)
        st.plotly_chart(fig_scatter2, use_container_width=True)
    
    fig_scatter3 = px.scatter(filtered_df, x='math score', y='writing score', color='gender', title="Math vs Writing Scores", trendline="ols")
    fig_scatter3.update_layout(height=400)
    st.plotly_chart(fig_scatter3, use_container_width=True)

# TAB 5: Data Table
with tab5:
    st.subheader("Student Performance Data")
    st.dataframe(filtered_df, use_container_width=True, height=600)
    
    # Download CSV
    csv = filtered_df.to_csv(index=False)
    st.download_button(label="Download as CSV", data=csv, file_name="filtered_students.csv", mime="text/csv")
