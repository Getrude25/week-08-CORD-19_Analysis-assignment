# app.py
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import streamlit as st
import os

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (10, 6)

def load_data():
    """Load data with memory optimization"""
    try:
        # Load only essential columns
        usecols = ['title', 'abstract', 'publish_time', 'journal', 'authors', 'source_x']
        df = pd.read_csv("data/metadata.csv", usecols=usecols, nrows=20000)
        return df
    except:
        # Create sample data if file not found
        return create_sample_data()

def create_sample_data():
    """Create sample data"""
    np.random.seed(42)
    n_rows = 5000
    dates = pd.date_range('2019-01-01', '2022-12-31', freq='D')
    journals = ['The Lancet', 'Nature', 'Science', 'JAMA', 'NEJM', 'BMJ']
    
    data = {
        'title': [f'COVID-19 Research Paper {i}' for i in range(n_rows)],
        'abstract': [f'Abstract for paper {i} about coronavirus research' for i in range(n_rows)],
        'publish_time': np.random.choice(dates, n_rows),
        'journal': np.random.choice(journals + [None], n_rows),
        'authors': [f'Author {i}' for i in range(n_rows)],
        'source_x': np.random.choice(['PubMed', 'arXiv', 'bioRxiv'], n_rows)
    }
    return pd.DataFrame(data)

def clean_data(df):
    """Clean and prepare data"""
    df_clean = df.copy()
    df_clean['publish_time'] = pd.to_datetime(df_clean['publish_time'], errors='coerce')
    df_clean['year'] = df_clean['publish_time'].dt.year
    df_clean['journal'] = df_clean['journal'].fillna("Unknown")
    df_clean['abstract_word_count'] = df_clean['abstract'].fillna('').str.split().str.len()
    return df_clean

def main():
    st.set_page_config(page_title="CORD-19 Explorer", layout="wide")
    st.title("📊 CORD-19 Research Dataset Explorer")
    
    # Load and clean data
    with st.spinner('Loading data...'):
        df = load_data()
        df_clean = clean_data(df)
    
    # Sidebar filters
    st.sidebar.header("🔧 Filters")
    year_range = st.sidebar.slider("Select Year Range", 
                                  int(df_clean['year'].min()), 
                                  int(df_clean['year'].max()), 
                                  (2020, 2021))
    
    # Filter data
    filtered_df = df_clean[(df_clean['year'] >= year_range[0]) & 
                          (df_clean['year'] <= year_range[1])]
    
    # Metrics
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Total Papers", len(filtered_df))
    with col2: st.metric("Time Range", f"{year_range[0]}-{year_range[1]}")
    with col3: st.metric("Journals", filtered_df['journal'].nunique())
    
    # Visualizations
    tab1, tab2, tab3, tab4 = st.tabs(["📈 Timeline", "📊 Journals", "☁️ Word Cloud", "📝 Data Sample"])
    
    with tab1:
        yearly = filtered_df['year'].value_counts().sort_index()
        fig, ax = plt.subplots()
        sns.barplot(x=yearly.index, y=yearly.values, ax=ax)
        ax.set_title("Publications by Year")
        st.pyplot(fig)
    
    with tab2:
        journals = filtered_df['journal'].value_counts().head(10)
        fig, ax = plt.subplots()
        sns.barplot(y=journals.index, x=journals.values, ax=ax)
        ax.set_title("Top Journals")
        st.pyplot(fig)
    
    with tab3:
        text = " ".join(filtered_df['title'].dropna())
        wordcloud = WordCloud(width=800, height=400).generate(text)
        fig, ax = plt.subplots()
        ax.imshow(wordcloud, interpolation='bilinear')
        ax.axis('off')
        st.pyplot(fig)
    
    with tab4:
        st.dataframe(filtered_df.head(10))
    
    # Insights
    st.header("💡 Key Insights")
    st.write(f"- **Average abstract length**: {filtered_df['abstract_word_count'].mean():.1f} words")
    st.write(f"- **Papers with abstracts**: {filtered_df['abstract'].notnull().sum()} ({(filtered_df['abstract'].notnull().sum()/len(filtered_df)*100):.1f}%)")

if __name__ == "__main__":
    main()
