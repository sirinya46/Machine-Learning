# -*- coding: utf-8 -*-
"""
Created on Thu Feb 19 15:58:18 2026
@author: BusRmutt
"""

import pickle
import os
import streamlit as st
from streamlit_option_menu import option_menu

# =========================
# Load Models (Safe Path)
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

used_car_model = pickle.load(open(os.path.join(BASE_DIR, 'Used_cars_model.sav'), 'rb'))
riding_model = pickle.load(open(os.path.join(BASE_DIR, 'RidingMowers_model.sav'), 'rb'))
bmi_model = pickle.load(open(os.path.join(BASE_DIR, 'bmi_model.sav'), 'rb'))

# =========================
# Mapping Dictionaries
# =========================
fuel_map = {
    'Diesel': 0,
    'Electric': 1,
    'Petrol': 2
}

engine_map = {
    '800': 0,
    '1000': 1,
    '1200': 2,
    '1500': 3,
    '1800': 4,
    '2000': 5,
    '2500': 6,
    '3000': 7,
    '4000': 8,
    '5000': 9
}

brand_map = {
    'BMW': 0,
    'Chevrolet': 1,
    'Ford': 2,
    'Honda': 3,
    'Hyundai': 4,
    'Kia': 5,
    'Nissan': 6,
    'Tesla': 7,
    'Toyota': 8,
    'Volkswagen': 9
}

transmission_map = {
    'Automatic': 0,
    'Manual': 1
}

# =========================
# Sidebar Menu
# =========================
with st.sidebar:
    selected = option_menu(
        'Prediction Menu',
        ['Ridingmower', 'Used_cars', 'BMI']
    )

# =========================
# Riding Mower Prediction
# =========================
if selected == 'Ridingmower':
    st.title('Riding Mower Classification')

    income = st.text_input('Income')
    lot_size = st.text_input('Lot Size')

    result = ''

    if st.button('Predict Riding'):
        try:
            prediction = riding_model.predict([[
                float(income),
                float(lot_size)
            ]])

            if prediction[0] == 1:
                result = 'Owner'
            else:
                result = 'Non Owner'
        except:
            result = 'กรุณากรอกข้อมูลให้ถูกต้อง'

    st.success(result)


# =========================
# Used Cars Prediction
# =========================
if selected == 'Used_cars':
    st.title('ประเมินราคารถมือ 2')

    make_year = st.text_input('ปีที่ผลิต')
    mileage_kmpl = st.text_input('กินน้ำมันกี่ KM/L')
    engine_cc = st.selectbox('ขนาดเครื่องยนต์ (CC)', list(engine_map.keys()))
    fuel_type = st.selectbox('ประเภทน้ำมัน', list(fuel_map.keys()))
    owner_count = st.text_input('จำนวนเจ้าของเดิม')
    brand = st.selectbox('ยี่ห้อรถ', list(brand_map.keys()))
    transmission = st.selectbox('ประเภทเกียร์', list(transmission_map.keys()))
    accidents_reported = st.text_input('จำนวนอุบัติเหตุที่เคยเกิด')

    price_result = ''

    if st.button('Predict Price'):
        try:
            prediction = used_car_model.predict([[
                float(make_year),
                float(mileage_kmpl),
                engine_map[engine_cc],
                fuel_map[fuel_type],
                float(owner_count),
                brand_map[brand],
                transmission_map[transmission],
                float(accidents_reported)
            ]])

            price_result = round(prediction[0], 2)
        except:
            price_result = 'กรุณากรอกข้อมูลให้ถูกต้อง'

    st.success(price_result)


# =========================
# BMI Prediction
# =========================
if selected == 'BMI':
    st.title('BMI Classification')

    gender = st.selectbox('เพศ', ['Male', 'Female'])
    age = st.text_input('อายุ')
    height = st.text_input('ส่วนสูง (cm)')
    weight = st.text_input('น้ำหนัก (kg)')

    bmi_result = ''

    if st.button('Predict BMI'):
        try:
            # แปลงเพศให้ตรงกับตอน train โมเดล
            gender_val = 1 if gender == 'Male' else 0

            prediction = bmi_model.predict([[
                gender_val,
                float(age),
                float(height),
                float(weight)
            ]])

            bmi_classes = {
                0: 'Underweight',
                1: 'Normal',
                2: 'Overweight',
                3: 'Obese',
                4: 'Extremely Obese'
            }

            bmi_result = bmi_classes.get(prediction[0], "Unknown")

        except:
            bmi_result = 'กรุณากรอกข้อมูลให้ถูกต้อง'

    st.success(bmi_result)
