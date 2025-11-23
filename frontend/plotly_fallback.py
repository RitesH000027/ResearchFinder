# Quick Fix for Streamlit Plotly Issues
# If you encounter any Plotly errors, use this simplified version

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def create_simple_charts(sample_papers):
    """Create simple charts using matplotlib as fallback"""
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Citation Distribution")
        df = pd.DataFrame(sample_papers)
        
        # Simple bar chart
        fig, ax = plt.subplots(figsize=(10, 6))
        bars = ax.bar(range(len(df)), df['citations'], color='skyblue')
        ax.set_xlabel('Papers')
        ax.set_ylabel('Citations')
        ax.set_title('Citation Distribution')
        ax.set_xticks(range(len(df)))
        ax.set_xticklabels([f"Paper {i+1}" for i in range(len(df))], rotation=45)
        
        # Add value labels on bars
        for bar, citation in zip(bars, df['citations']):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height + 0.5,
                   f'{citation}', ha='center', va='bottom')
        
        plt.tight_layout()
        st.pyplot(fig)
    
    with col2:
        st.subheader("Publication Years")
        year_counts = df['year'].value_counts()
        
        # Simple pie chart
        fig, ax = plt.subplots(figsize=(8, 8))
        ax.pie(year_counts.values, labels=year_counts.index, autopct='%1.1f%%')
        ax.set_title('Publication Years Distribution')
        
        plt.tight_layout()
        st.pyplot(fig)

# Usage instructions:
# If you get Plotly errors, replace the plotly section in streamlit_app.py with:
# create_simple_charts(sample_papers)