import os
import joblib
import pandas as pd
import streamlit as st

# Configure page
st.set_page_config(
    page_title="Health Insurance Cost Estimator",
    page_icon="🛡️",
    layout="centered",
)

# Display Project Icon / Banner
icon_path = os.path.join("C:\\Users\\bhargav\\OneDrive\\Documents\\Onedrive1\\OneDrive\\Desktop\\Insurance Predictor\\assets\\icon.png")
col1, col2 = st.columns([1, 4])
with col1:
  if os.path.exists(icon_path):
    st.image(icon_path, width=90)
  else:
    st.markdown("## 🛡️")
with col2:
  st.title("Insurance Cost Estimator")
  st.caption("Predict estimated annual medical charges using Machine Learning")

st.markdown("---")


# Load the serialized model pipeline
@st.cache_resource
def load_model():
  artifact_path = os.path.join("C:\\Users\\bhargav\\OneDrive\\Documents\\Onedrive1\\OneDrive\\Desktop\\Insurance Predictor\\best_model", "best_model_pipeline.pkl")
  return joblib.load(artifact_path)


try:
  model = load_model()
except Exception as e:
  st.error(
      "Trained model not found in `artifacts/`. Please run the training notebook"
      f" first.\nDetails: {e}"
  )
  st.stop()

# User Input Form
st.subheader("Applicant Details")
col_a, col_b = st.columns(2)

with col_a:
  age = st.slider("Age", min_value=18, max_value=65, value=30, step=1)
  bmi = st.number_input(
      "BMI (Body Mass Index)",
      min_value=12.0,
      max_value=55.0,
      value=24.5,
      step=0.1,
  )
  children = st.selectbox(
      "Number of Children / Dependents", options=[0, 1, 2, 3, 4, 5], index=0
  )

with col_b:
  sex = st.selectbox("Sex", options=["male", "female"])
  smoker = st.selectbox(
      "Smoking Status", options=["no", "yes"], help="Major pricing factor"
  )
  region = st.selectbox(
      "Region (US)",
      options=["northwest", "northeast", "southwest", "southeast"],
  )

# Assemble DataFrame matching model column format
input_df = pd.DataFrame({
    "age": [age],
    "sex": [sex],
    "bmi": [bmi],
    "children": [children],
    "smoker": [smoker],
    "region": [region],
})

# Prediction trigger
if st.button("Calculate Estimated Premium", type="primary"):
  prediction = model.predict(input_df)[0]

  st.success(f"### Estimated Annual Charge: **${prediction:,.2f}**")

  # Key insights indicator
  if smoker == "yes" and bmi >= 30:
    st.warning(
        "⚠️ Note: High BMI combined with smoking significantly scales up risk"
        " loadings."
    )
  elif smoker == "yes":
    st.info(
        "ℹ️ Smoking status is the highest-weight driver in this risk model."
    )