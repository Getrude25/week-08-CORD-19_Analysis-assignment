# CORD-19 Data Analysis Assignment

## 📋 Project Overview
This project analyzes the CORD-19 research dataset containing metadata about COVID-19 research papers. The analysis includes data exploration, cleaning, visualization, and an interactive Streamlit application.

## 🚀 Features
- Data loading and cleaning
- Publication trend analysis
- Journal and author analysis
- Word cloud generation
- Interactive Streamlit dashboard

## 🛠️ Installation
```bash
pip install -r requirements.txt
```

## 📊 Usage ##
1. Data Analysis: Run the Jupyter notebook CORD19_Analysis.ipynb
2. Streamlit App: Run streamlit run app.py

## 📈 Key Findings ##
- COVID-19 publications peaked in 2020-2021
- Major medical journals dominated publications
- Average abstract length: ~250 words
- Significant increase in preprint servers usage

## 🎯 Challenges & Solutions ##
- Memory Error: Solved by chunk loading and selective column reading
- Missing Data: Handled with appropriate filling strategies
- Large Dataset: Used sampling for visualization

## 📁 Project Structure ##
``` 
Framework_Assignment/
├── data/
│   └── metadata.csv
├── notebooks/
│   └── CORD19_Analysis.ipynb
├──app.py
├── requirements.txt
└── README.md
```

## 👨‍💻 Author ##
Getruda Vitus

## 📄 License ##
This project is for educational purposes.