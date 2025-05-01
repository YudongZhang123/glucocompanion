import streamlit as st

# Streamlit Interface
st.title("GlucoCompanion - Blood Glucose Prediction Tool")

st.write("""
**Purpose:** This tool is designed to help users adjust their rapid-acting insulin dose to maintain blood glucose levels within the target range of **4.4 - 8.0 mmol/L** after meals.

**Disclaimer:** This tool provides general recommendations based on standard diabetes management guidelines. It is not a substitute for professional medical advice. Always consult a healthcare provider for personalized treatment.

**About ICR (Insulin-to-Carbohydrate Ratio):**
- A typical ICR for adults is between **10–15 g/unit**.
- Children or insulin-sensitive individuals may have ICRs of **15–20 g/unit** or more.
- People with insulin resistance (e.g., during puberty or with obesity) may need a lower ICR, such as **5–10 g/unit**.
- This value is individualized and often determined based on total daily insulin dose or clinical experience.
""")

# User Inputs
icr = st.number_input("Insulin-to-Carbohydrate Ratio (g/unit)", min_value=1.0, step=0.1, help="How many grams of carbohydrates 1 unit of rapid-acting insulin covers.")
carbs = st.number_input("Carbohydrate Intake (g)", min_value=0.0, step=1.0)
pre_meal_glucose = st.number_input("Pre-meal Blood Glucose (mmol/L)", min_value=0.0, step=0.1)

# Define constants
sensitivity_factor = 2  # 1 unit of insulin lowers blood glucose by 2 mmol/L
natural_increase_2hr = 1.5  # natural 2-hour post-meal rise in blood glucose
continued_decrease_4hr = 1.0  # estimated further blood glucose drop by 4 hours due to insulin action

# Prediction button
if st.button("Predict"):
    # Calculate recommended insulin dose
    insulin_dose = carbs / icr
    insulin_dose = round(insulin_dose, 1)

    # Estimate 2-hour post-meal glucose
    expected_glucose_rise = (carbs / 10) * 2
    expected_glucose_drop = insulin_dose * sensitivity_factor
    post_meal_2hr = pre_meal_glucose + expected_glucose_rise - expected_glucose_drop + natural_increase_2hr
    post_meal_2hr = round(post_meal_2hr, 1)

    # Estimate 4-hour post-meal glucose
    post_meal_4hr = post_meal_2hr - continued_decrease_4hr
    post_meal_4hr = round(post_meal_4hr, 1)

    # Determine glucose level feedback
    def interpret_glucose(value):
        if value < 4.4:
            return "⚠️ Low blood glucose detected. Please consume fast-acting carbohydrates immediately."
        elif value > 8.0:
            return "⚠️ High blood glucose detected. Consider taking corrective insulin and monitor for symptoms."
        else:
            return "✅ Blood glucose is within the target range. Keep up the good work!"

    # Display Results
    st.success(f"Recommended Rapid-acting Insulin Dose: {insulin_dose} units")
    st.success(f"Predicted 2-hour Post-meal Blood Glucose: {post_meal_2hr} mmol/L\n{interpret_glucose(post_meal_2hr)}")
    st.success(f"Predicted 4-hour Post-meal Blood Glucose: {post_meal_4hr} mmol/L\n{interpret_glucose(post_meal_4hr)}")
