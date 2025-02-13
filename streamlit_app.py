import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# 🎨 Streamlit Page Configuration
st.set_page_config(
    page_title="AI-Driven Insurance Dashboard",
    page_icon="📊",
    layout="wide"
)

# 🌟 Custom Streamlit CSS for styling
st.markdown(
    """
    <style>
        body { background-color: #f4f4f4; }
        .stTextInput, .stNumberInput, .stButton { font-size: 18px !important; }
        .stButton>button {
            background-color: #007BFF !important;
            color: white !important;
            border-radius: 10px;
            padding: 10px 20px;
        }
        .stButton>button:hover { background-color: #0056b3 !important; }
        .stTitle, .stHeader, .stSubheader { color: #007BFF; }
        .stMarkdown { font-size: 18px; }
    </style>
    """,
    unsafe_allow_html=True
)

# 🌍 API Endpoints
FASTAPI_RECOMMEND_URL = "http://127.0.0.1:8000/recommend/"
FASTAPI_CHURN_URL = "http://127.0.0.1:8000/churn/"

# 📌 Sidebar with user input
st.sidebar.title("🔍 AI-Powered Insurance Dashboard")
customer_id = st.sidebar.number_input("Enter Customer ID:", min_value=1, step=1)

# 📌 Fetch Data Button
if st.sidebar.button("📌 Get My Recommendations"):
    with st.spinner("Fetching recommendations..."):
        try:
            response = requests.get(f"{FASTAPI_RECOMMEND_URL}{customer_id}")
            churn_response = requests.get(f"{FASTAPI_CHURN_URL}{customer_id}")

            if response.status_code == 200 and churn_response.status_code == 200:
                rec_data = response.json()
                churn_data = churn_response.json()

                recommended_policies = rec_data.get("recommended_policies", [])
                churn_prediction = churn_data.get("churn_prediction", False)

                # ✅ Display Recommendations
                st.subheader("📜 Recommended Policies")
                if recommended_policies:
                    for policy in recommended_policies:
                        st.success(f"🏆 **Policy ID:** `{policy}`")
                else:
                    st.warning("⚠ No recommendations found.")

                # 🔥 Churn Prediction
                st.subheader("🔮 Churn Prediction")
                if churn_prediction:
                    st.error("🚨 High Risk: Customer is likely to churn!")
                else:
                    st.success("✅ Low Risk: Customer is unlikely to churn.")

            else:
                st.error("❌ API Error. Check Customer ID.")

        except requests.exceptions.RequestException as e:
            st.error(f"🚨 API Connection Error: {e}")

# 📊 Sample Data Visualization
st.subheader("📈 Customer Insights")

# Load Sample Data
df = pd.read_csv("data/processed/cleaned_customer_data.csv")

# 🎨 Engagement Score Distribution
fig1 = px.histogram(df, x="engagement_score", nbins=20, title="📊 Customer Engagement Distribution", color_discrete_sequence=["#007BFF"])
st.plotly_chart(fig1, use_container_width=True)

# 💰 Income vs. Policy Claims
fig2 = px.scatter(df, x="income", y="past_claims", color="engagement_score", title="💰 Income vs. Policy Claims", size_max=15, color_continuous_scale="blues")
st.plotly_chart(fig2, use_container_width=True)

# 📉 Churn Risk Heatmap
st.subheader("⚠ Churn Risk Analysis")
plt.figure(figsize=(10, 6))
corr = df.corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
st.pyplot(plt)

# 🎯 Footer
st.markdown(
    """
    <br><br>
    <p style="text-align: center; font-size: 14px; color: grey;">
        Built with ❤️ by Anurag Mishra
    </p>
    """,
    unsafe_allow_html=True
)
