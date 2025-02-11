import streamlit as st
import requests

# 🎨 Custom Streamlit Styles
st.set_page_config(
    page_title="AI-Driven Insurance Recommendation",
    page_icon="🔍",
    layout="centered"
)

st.markdown(
    """
    <style>
        body {
            background-color: #f4f4f4;
        }
        .stTextInput, .stNumberInput, .stButton {
            font-size: 18px !important;
        }
        .stButton>button {
            background-color: #007BFF !important;
            color: white !important;
            border-radius: 10px;
            padding: 10px 20px;
        }
        .stButton>button:hover {
            background-color: #0056b3 !important;
        }
        .stTitle, .stHeader, .stSubheader {
            color: #007BFF;
        }
        .stMarkdown {
            font-size: 18px;
        }
    </style>
    """,
    unsafe_allow_html=True
)

# 🌟 Streamlit UI
st.title("🔍 AI-Driven Insurance Recommendation")
st.markdown("### Get Personalized Policy Recommendations")

# Input for Customer ID
customer_id = st.number_input("Enter Customer ID:", min_value=1, step=1)

# API URL
FASTAPI_URL = "http://127.0.0.1:8000/recommend/"

# Fetch recommendations when button is clicked
if st.button("📌 Get My Recommendations"):
    with st.spinner("Fetching recommendations..."):
        try:
            response = requests.get(f"{FASTAPI_URL}{customer_id}")
            if response.status_code == 200:
                data = response.json()
                recommended_policies = data.get("recommended_policies", [])
                if recommended_policies:
                    st.success("✅ Recommended Policies:")
                    for policy in recommended_policies:
                        st.markdown(f"- 🏆 **Policy ID:** `{policy}`")
                else:
                    st.warning("⚠ No recommendations found for this customer.")
            else:
                st.error("❌ Unable to fetch recommendations. Please check the Customer ID.")
        except requests.exceptions.RequestException as e:
            st.error(f"🚨 API Connection Error: {e}")

# Add a footer
st.markdown(
    """
    <br><br>
    <p style="text-align: center; font-size: 14px; color: grey;">
        Developed with ❤️ using Streamlit & FastAPI
    </p>
    """,
    unsafe_allow_html=True
)
