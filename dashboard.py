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

    # --- THE FIX IS HERE ---
    # Instead of looking for the EXACT millisecond, we look for data
    # from the last 30 minutes.
    # This captures all stations, even if they reported a few seconds apart.
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
        # 1. Let the user Pick a Station (The Fix!)
        # We get a list of all unique station names
        all_stations = df['station_name'].unique()
        selected_station_name = st.selectbox("Select a Station", all_stations)

    with col2:
        # 2. Let the user Pick an Hour
        input_hour = st.slider("Select Hour (0-23)", 0, 23, 12)

    # Get the specific latitude/longitude/empty_slots for the selected station
    # We take the most recent data for that station to be accurate
    station_data = df[df['station_name'] == selected_station_name].tail(1).iloc[0]

    # Prepare the input for the AI
    # It needs: [latitude, longitude, empty_slots, hour]
    input_data = pd.DataFrame([[
        station_data['latitude'],
        station_data['longitude'],
        input_hour
    ]], columns=['latitude', 'longitude', 'hour'])

    # ASK THE ROBOT
    prediction = model.predict(input_data)

    # Show the result
    st.success(f"🔮 At {input_hour}:00, I predict **{int(prediction[0])}** bikes at **{selected_station_name}**.")

    # Show a mini chart of that station's history
    st.write(f"📉 History for {selected_station_name}:")
    history_data = df[df['station_name'] == selected_station_name]
    st.line_chart(history_data.set_index('timestamp')['free_bikes'])

else:
    st.error("❌ I can't find the brain (bike_predictor.pkl). Run train_model.py!")