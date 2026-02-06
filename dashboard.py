import streamlit as st
import pandas as pd
import pickle  # To load the brain

# 1. Load the Brain!
try:
    with open("bike_predictor.pkl", "rb") as f:
        model = pickle.load(f)
    brain_available = True
except FileNotFoundError:
    brain_available = False

st.title("🚴 Frankfurt Bike AI Manager")

# 2. Show Current Status (Business Analyst Stuff)
try:
    df = pd.read_csv("frankfurt_bikes.csv")

    # Convert 'timestamp' to real datetime objects
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # Get the very latest time found in the file
    latest_timestamp_in_file = df['timestamp'].max()

    # Filter: Keep rows that are within 30 minutes of the latest time
    current_data = df[df['timestamp'] > (latest_timestamp_in_file - pd.Timedelta(minutes=30))]

    st.write(f"Data snapshot from: {latest_timestamp_in_file}")

    col1, col2 = st.columns(2)
    with col1:
        total_bikes = current_data['free_bikes'].sum()
        st.metric("Total Free Bikes", total_bikes)
    with col2:
        total_stations = len(current_data)
        st.metric("Active Stations", total_stations)

    st.map(current_data)
except:
    st.warning("⚠️ No data found yet. Run fetch_data.py first!")

# 3. THE AI SECTION (Machine Learning Stuff)
st.divider()
st.header("🤖 Ask the AI Prediction Model")

if brain_available:
    st.write("I can guess how many bikes will be available based on the time.")

    col1, col2 = st.columns(2)

    with col1:
        # 1. Let the user Pick a Station
        all_stations = df['station_name'].unique()
        selected_station_name = st.selectbox("Select a Station", all_stations)

    with col2:
        # 2. Let the user Pick an Hour
        input_hour = st.slider("Select Hour (0-23)", 0, 23, 12)

    # Get the specific latitude/longitude for the selected station
    station_data = df[df['station_name'] == selected_station_name].tail(1).iloc[0]

    # Prepare the input for the AI
    # It needs: [latitude, longitude, hour]
    input_data = pd.DataFrame([[
        station_data['latitude'],
        station_data['longitude'],
        input_hour
    ]], columns=['latitude', 'longitude', 'hour'])

    # ASK THE ROBOT
    prediction = model.predict(input_data)
    predicted_count = int(prediction[0])

    # --- DYNAMIC PRICING LOGIC ---
    base_price = 3.00  # 3 Euros per hour normally

    if predicted_count < 3:
        # SCARCITY! Very few bikes. Raise price.
        price_factor = 1.5  # +50%
        condition = "🔥 High Demand (Surge Pricing)"
    elif predicted_count > 15:
        # OVERSUPPLY! Too many bikes. Lower price.
        price_factor = 0.8  # -20%
        condition = "💰 Oversupply (Discount)"
    else:
        # NORMAL
        price_factor = 1.0
        condition = "⚖️ Normal Demand"

    final_price = round(base_price * price_factor, 2)

    # Show the prediction AND the Price
    st.divider()
    st.subheader(f"Strategy: {condition}")

    c1, c2, c3 = st.columns(3)
    c1.metric("Predicted Bikes", predicted_count)
    c2.metric("Suggested Hourly Price", f"€{final_price}")
    c3.metric("Price Adjustment", f"{int((price_factor - 1) * 100)}%")

    if price_factor > 1:
        st.warning(f"⚠️ Recommendation: Move bikes to {selected_station_name} before {input_hour}:00 to capture high revenue!")
    elif price_factor < 1:
        st.success(f"✅ Recommendation: Run a marketing campaign to encourage rides from {selected_station_name}.")

else:
    st.error("❌ I can't find the brain (bike_predictor.pkl). Run train_model.py!")