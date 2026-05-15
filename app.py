import streamlit as st
import pandas as pd
import os
from dotenv import load_dotenv

# LangChain & Mistral Integrations
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# Machine Learning Core
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.preprocessing import LabelEncoder

# 1. PAGE CONFIG & THEME-AWARE STYLING
st.set_page_config(page_title="DIU Sleep Health Dashboard", page_icon="🌙", layout="wide")

# This CSS fixes the "Blank Box" issue by using semi-transparent backgrounds
st.markdown("""
    <style>
    [data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.05); 
        border: 1px solid rgba(151, 166, 195, 0.2);
        padding: 15px;
        border-radius: 10px;
    }
    [data-testid="stMetricLabel"] {
        color: #7f8c8d !important;
        font-weight: 600;
    }
    .status-high {
        color: #ff4b4b;
        font-weight: bold;
        background: rgba(255, 75, 75, 0.1);
        padding: 2px 6px;
        border-radius: 4px;
    }
    .status-low {
        color: #00d488;
        font-weight: bold;
        background: rgba(0, 212, 136, 0.1);
        padding: 2px 6px;
        border-radius: 4px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. SYSTEM INITIALIZATION (With Path Solver)
@st.cache_resource
def initialize_system():
    load_dotenv()
    
    # Path Solver: Checks current and parent directories
    filename = 'Detection of Sleep Disorders Among University Students at DIU Using Machine Learning Algorithms (Responses) dataset.xlsx'
    possible_paths = [
        os.path.join('data', filename),
        os.path.join('..', 'data', filename),
        filename
    ]
    
    path = None
    for p in possible_paths:
        if os.path.exists(p):
            path = p
            break
            
    if path is None:
        return None, None, None, None

    df = pd.read_excel(path)
    df.columns = df.columns.str.strip().str.replace('\n', ' ')
    
    clusters = {
        "Insomnia": [7, 11, 12, 20],
        "Sleep Deprivation": [5, 10, 23, 25],
        "Sleep Apnea": [27, 28],
        "Circadian Rhythm": [6, 17, 14],
        "Stress & Anxiety": [19, 20, 21, 22]
    }
    
    y = pd.DataFrame()
    for name, idxs in clusters.items():
        scores = df.iloc[:, idxs].apply(lambda x: LabelEncoder().fit_transform(x.astype(str))).mean(axis=1)
        y[name] = (scores > scores.median()).astype(int)
    
    X = df.drop(columns=['Timestamp']).copy()
    for col in X.columns:
        X[col] = LabelEncoder().fit_transform(X[col].astype(str))
        
    model = MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42))
    model.fit(X, y)
    
    return df, X, y, model

df, X, y, ml_model = initialize_system()

if df is None:
    st.error("❌ Dataset not found. Please ensure the 'data' folder is in the correct directory.")
    st.stop()

# 3. SIDEBAR NAVIGATION
with st.sidebar:
    st.title("Research Hub")
    menu = st.radio("Navigation", ["Dashboard", "Dataset Explorer"])
    st.markdown("---")
    student_idx = st.number_input("Select Student ID", min_value=0, max_value=len(df)-1, value=10)

# 4. MAIN CONTENT AREA
if menu == "Dashboard":
    st.title("🌙 DIU Sleep Health Analysis")
    
    # Header Metrics
    m1, m2, m3 = st.columns(3)
    m1.metric("Age Group", df.iloc[student_idx, 1])
    m2.metric("Gender", df.iloc[student_idx, 2])
    m3.metric("Academic Year", df.iloc[student_idx, 3])

    st.markdown("---")

    # Prediction Logic
    student_row = X.iloc[[student_idx]]
    prediction = ml_model.predict(student_row)[0]
    risks = {y.columns[i]: ("High Risk" if val == 1 else "Low Risk") for i, val in enumerate(prediction)}

    left_col, right_col = st.columns(2)

    with left_col:
        st.subheader("📊 ML Diagnostic Summary")
        for disorder, status in risks.items():
            icon = "🚨" if status == "High Risk" else "✅"
            color = "status-high" if status == "High Risk" else "status-low"
            st.markdown(f"**{icon} {disorder}:** <span class='{color}'>{status}</span>", unsafe_allow_html=True)

    with right_col:
        st.subheader("💡 AI Research Insights")
        if st.button("Generate Recommendations"):
            api_key = os.getenv("MISTRAL_API_KEY")
            if not api_key:
                st.warning("⚠️ API Key missing in .env file.")
            else:
                with st.spinner("Analyzing..."):
                    try:
                        llm = ChatMistralAI(model='mistral-small-2603', temperature=0.7, mistral_api_key=api_key)
                        prompt = ChatPromptTemplate.from_messages([
                            ("system", "You are a DIU Sleep Researcher. Give 3 professional medical lifestyle interventions."),
                            ("user", "High Risks Identified: {risks}")
                        ])
                        chain = prompt | llm | StrOutputParser()
                        high_risks = [k for k, v in risks.items() if v == "High Risk"]
                        response = chain.invoke({"risks": str(high_risks)})
                        st.success(response)
                    except Exception as e:
                        st.error(f"Mistral Error: {str(e)}")

elif menu == "Dataset Explorer":
    st.title("📂 Data Analysis")
    st.dataframe(df, use_container_width=True)
    st.bar_chart(y.sum())