import streamlit as st
import requests
import pandas as pd
import plotly.express as px

# 🎨 Streamlit Page Configuration
st.set_page_config(
    page_title="AI-Driven Insurance Dashboard",
    page_icon="📊",
    layout="wide"
)

# 🌍 API Endpoints
FASTAPI_RECOMMEND_URL = "http://127.0.0.1:8000/recommend/"
FASTAPI_CHURN_URL = "http://127.0.0.1:8000/churn/"

# 📌 Sidebar with user input
st.sidebar.title("🔍 AI-Powered Insurance Dashboard")
customer_id = st.sidebar.number_input("Enter Customer ID:", min_value=1, step=1)

# 📌 Fetch Data Button
if st.sidebar.button("📌 Get My Insights"):
    with st.spinner("Fetching data..."):
        try:
            # 🔄 Fetch Data from APIs
            rec_response = requests.get(f"{FASTAPI_RECOMMEND_URL}{customer_id}")
            churn_response = requests.get(f"{FASTAPI_CHURN_URL}{customer_id}")

            # ✅ Check API Status
            if rec_response.status_code == 200 and churn_response.status_code == 200:
                rec_data = rec_response.json()
                churn_data = churn_response.json()

                recommended_policies = rec_data.get("recommended_policies", [])
                churn_prediction = churn_data.get("churn_prediction", False)
                shap_values = churn_data.get("shap_values", [])

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

                # 📊 Feature Importance (SHAP)
                if shap_values:
                    st.subheader("⚡ Feature Importance for Churn Prediction")
                    shap_df = pd.DataFrame({
                        "Feature": [f"Feature {i+1}" for i in range(len(shap_values[0]))],
                        "SHAP Value": [abs(value[0]) for value in shap_values[0]]
                    })
                    shap_df = shap_df.sort_values(by="SHAP Value", ascending=False)

                    try:
                        # Create SHAP Feature Importance Graph
                        fig = px.bar(
                            shap_df,
                            x="SHAP Value",
                            y="Feature",
                            orientation="h",
                            title="🔍 SHAP Feature Importance",
                            color="SHAP Value",
                            color_continuous_scale="blues"
                        )
                        st.plotly_chart(fig, use_container_width=True)
                    except Exception as e:
                        st.error(f"🚨 Error in SHAP Visualization: {e}")

            else:
                st.error(f"❌ API Error: {rec_response.status_code} or {churn_response.status_code}")

        except requests.exceptions.RequestException as e:
            st.error(f"🚨 API Connection Error: {e}")

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
