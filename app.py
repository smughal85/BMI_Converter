import streamlit as st

# -----------------------------
# Helper functions & constants
# -----------------------------
LB_TO_KG = 0.45359237
IN_TO_M = 0.0254
CM_TO_M = 0.01

def classify_bmi(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25.0:
        return "Normal (Healthy weight)"
    elif bmi < 30.0:
        return "Overweight"
    elif bmi < 35.0:
        return "Obesity class I"
    elif bmi < 40.0:
        return "Obesity class II"
    else:
        return "Obesity class III"

def format_kg(x):
    return f"{x:.1f} kg"

def calculate_bmi(weight_val, weight_unit, height_unit, height_single, height_ft, height_in):
    # Convert weight to kg
    if weight_val <= 0:
        return "Error: weight must be > 0."
    if weight_unit == "lb":
        weight_kg = weight_val * LB_TO_KG
    else:
        weight_kg = weight_val

    # Convert height to meters
    if height_unit == "cm":
        height_m = height_single * CM_TO_M
    elif height_unit == "m":
        height_m = height_single
    elif height_unit == "in":
        height_m = height_single * IN_TO_M
    elif height_unit == "ft+in":
        total_in = height_ft * 12.0 + height_in
        height_m = total_in * IN_TO_M
    else:
        return "Error: unknown height unit."

    if height_m <= 0:
        return "Error: height must be > 0."

    # BMI calculation
    bmi = weight_kg / (height_m ** 2)
    bmi_rounded = round(bmi, 1)
    category = classify_bmi(bmi)

    # Healthy weight range
    min_w = 18.5 * (height_m ** 2)
    max_w = 24.9 * (height_m ** 2)

    out = f"""
### Results
- **BMI:** {bmi_rounded} kg/m²  
- **Category:** {category}  
- **Healthy range for your height:** {format_kg(min_w)} — {format_kg(max_w)}  
(You entered {weight_kg:.1f} kg, height {height_m:.2f} m)

---
**Note:** BMI is a screening tool only. It does not distinguish between muscle and fat.
"""
    return out


# -----------------------------
# Streamlit UI
# -----------------------------
st.title("🩺 BMI Calculator")

st.markdown("Enter your weight and height to calculate BMI (Body Mass Index).")

# Weight input
weight_unit = st.selectbox("Weight unit", ["kg", "lb"])
weight_val = st.number_input("Weight", min_value=0.0, value=70.0)

# Height input
height_unit = st.selectbox("Height unit", ["cm", "m", "in", "ft+in"])

if height_unit in ["cm", "m", "in"]:
    height_single = st.number_input("Height", min_value=0.0, value=170.0 if height_unit=="cm" else 1.70)
    height_ft, height_in = 0.0, 0.0
else:
    height_ft = st.number_input("Height (feet)", min_value=0, value=5)
    height_in = st.number_input("Height (inches)", min_value=0.0, value=7.0)
    height_single = 0.0

if st.button("Calculate BMI"):
    result = calculate_bmi(weight_val, weight_unit, height_unit, height_single, height_ft, height_in)
    st.markdown(result)
