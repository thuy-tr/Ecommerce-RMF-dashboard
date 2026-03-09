# E-Commerce Data Analysis & RFM Customer Segmentation: EDA, RFM & Dashboard

You can view and interact with the interactive dashboard on Streamlit app via this link:
https://thuy-ecommerce-dashboard1.streamlit.app/

This project is an end-to-end data analytics portfolio piece that demonstrates exploratory data analysis (EDA), customer segmentation using the RFM (Recency, Frequency, Monetary) framework, and the creation of an interactive business dashboard.

## 📌 Project Overview

The goal of this project is to analyze transactional data from an online retail store, extract actionable business insights, and segment customers to provide targeted marketing recommendations. 

The project consists of three main components:
1. **Exploratory Data Analysis (EDA):** Cleaning the data, handling missing values, and analyzing trends in revenue, geography, and product performance.
2. **RFM Analysis:** Segmenting customers into 6 distinct groups (Champions, Loyal, Potential, At Risk, Lost, Other) based on their purchasing behavior.
3. **Interactive Dashboard:** A Streamlit web application that allows stakeholders to view high-level business metrics and look up specific customers to see their RFM profile and tailored recommendations.

## 📊 Key Insights

- **Strong revenue concentration:** "Champions" (22% of customers) generate **67% of total revenue**.
- **Churn risk:** The "At Risk" segment still contributes ~11% of revenue but has an average recency of over 140 days. Win-back campaigns are highly recommended here.
- **Lost customers:** Make up the largest headcount (22%) but contribute less than 3% of revenue, indicating a large pool of one-off buyers.

## 🛠️ Tech Stack

- **Python** (Data manipulation and analysis)
- **Pandas & NumPy** (Data cleaning, aggregation, and RFM calculation)
- **Plotly** (Interactive data visualizations)
- **Streamlit** (Web dashboard creation)
- **Jupyter Notebook** (Step-by-step analytical documentation)

## 📂 Repository Structure

- `retail_data_analysis.ipynb`: Jupyter notebook containing the initial data cleaning, EDA, and business trend analysis.
- `rfm_analysis.ipynb`: Jupyter notebook detailing the RFM scoring logic, segment definitions, and priority matrix.
- `dashboard.py`: The Streamlit application script that powers the interactive dashboard.
- `Online Retail.xlsx`: The dataset used for this analysis.
- `requirements.txt`: List of Python dependencies required to run the project.

## 🚀 How to Run Locally

1. **Clone the repository:**
   ```bash
   git clone https://github.com/thuy-tr/Ecommerce-RMF-dashboard.git
   cd Ecommerce-RMF-dashboard
   ```

2. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the Streamlit Dashboard:**
   ```bash
   streamlit run dashboard.py
   ```
   The dashboard will automatically open in your default web browser at `http://localhost:8501`.

## 💡 Future Enhancements

- Connect the dashboard to a live SQL database instead of a static Excel file.
- Implement Machine Learning (e.g., K-Means clustering) to dynamically create customer segments.
- Deploy the dashboard to Streamlit Community Cloud for public access.
