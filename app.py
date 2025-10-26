import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from data_generator import generate_energy_data
from model import prepare_data, train_model, predict_future, load_model, save_model
import os

st.set_page_config(page_title="EcoWatt: Smart Energy Consumption Forecasting", page_icon="⚡")

st.title("⚡ EcoWatt: Smart Energy Consumption Forecasting")

st.markdown("""
Welcome to EcoWatt! This application forecasts energy consumption using machine learning.
Upload your data or use our synthetic data generator to get started.
""")

# Sidebar for controls
st.sidebar.header("Controls")

# Option to generate or upload data
data_option = st.sidebar.selectbox("Data Source", ["Generate Synthetic Data", "Upload CSV"])

if data_option == "Generate Synthetic Data":
    periods = st.sidebar.slider("Number of days", 365, 365*5, 730)
    if st.sidebar.button("Generate Data"):
        with st.spinner("Generating data..."):
            data = generate_energy_data(periods=periods)
            data.to_csv('energy_data.csv', index=False)
            st.sidebar.success("Data generated!")
            st.session_state.data = data
else:
    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type="csv")
    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file)
        # Check if required columns exist
        if 'date' not in data.columns or 'consumption_kwh' not in data.columns:
            st.sidebar.error("CSV must contain 'date' and 'consumption_kwh' columns. Please check your file format.")
            st.sidebar.info("Required columns: date, consumption_kwh")
            st.sidebar.info("Optional: time (HH:MM:SS format)")
            st.sidebar.info("Example: date=2023-01-01, time=14:30:00, consumption_kwh=150.5")
        else:
            try:
                # Handle date and optional time columns
                if 'time' in data.columns:
                    # Combine date and time if time column exists
                    data['date'] = pd.to_datetime(data['date'] + ' ' + data['time'], format='%Y-%m-%d %H:%M:%S')
                else:
                    # Use date only
                    data['date'] = pd.to_datetime(data['date'])

                # Sort by date to ensure chronological order
                data = data.sort_values('date').reset_index(drop=True)

                st.session_state.data = data
                st.sidebar.success("Data uploaded successfully!")
                if 'time' in data.columns:
                    st.sidebar.info("Date and time columns combined successfully.")
                else:
                    st.sidebar.info("Date column processed successfully.")
            except Exception as e:
                st.sidebar.error(f"Error processing date/time columns: {str(e)}")
                st.sidebar.info("Date format: YYYY-MM-DD (e.g., 2023-01-01)")
                st.sidebar.info("Time format (optional): HH:MM:SS (e.g., 14:30:00)")

# Load or train model
if 'model' not in st.session_state:
    st.session_state.model = load_model()

if st.sidebar.button("Train Model") and 'data' in st.session_state:
    with st.spinner("Training model..."):
        data = st.session_state.data
        X, y = prepare_data(data)
        model = train_model(X, y)
        save_model(model)
        st.session_state.model = model
        st.sidebar.success("Model trained!")

# Main content
if 'data' in st.session_state:
    data = st.session_state.data

    st.subheader("Energy Consumption Data")
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(data['date'], data['consumption_kwh'])
    ax.set_xlabel('Date')
    ax.set_ylabel('Consumption (kWh)')
    ax.set_title('Historical Energy Consumption')
    st.pyplot(fig)

    st.subheader("Data Statistics")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total Days", len(data))
    with col2:
        st.metric("Average Consumption", f"{data['consumption_kwh'].mean():.1f} kWh")
    with col3:
        st.metric("Max Consumption", f"{data['consumption_kwh'].max():.1f} kWh")

    # Forecasting
    if st.session_state.model is not None:
        st.subheader("Energy Consumption Forecast")

        days_ahead = st.slider("Days to forecast", 1, 90, 30)

        if st.button("Generate Forecast"):
            with st.spinner("Generating forecast..."):
                # Get last known data for prediction
                last_known = data['consumption_kwh'].values[-7:]  # Last 7 days
                predictions = predict_future(st.session_state.model, last_known, days_ahead)

                # Create forecast dates
                last_date = data['date'].max()
                forecast_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=days_ahead)

                forecast_df = pd.DataFrame({
                    'date': forecast_dates,
                    'predicted_consumption': predictions
                })

                st.session_state.forecast = forecast_df

        if 'forecast' in st.session_state:
            forecast_df = st.session_state.forecast

            # Plot historical + forecast
            fig, ax = plt.subplots(figsize=(12, 6))
            ax.plot(data['date'], data['consumption_kwh'], label='Historical', color='blue')
            ax.plot(forecast_df['date'], forecast_df['predicted_consumption'], label='Forecast', color='red', linestyle='--')
            ax.set_xlabel('Date')
            ax.set_ylabel('Consumption (kWh)')
            ax.legend()
            ax.set_title('Energy Consumption Forecast')
            st.pyplot(fig)

            st.subheader("Forecast Data")
            st.dataframe(forecast_df)

            # Download forecast
            csv = forecast_df.to_csv(index=False)
            st.download_button(
                label="Download Forecast as CSV",
                data=csv,
                file_name="energy_forecast.csv",
                mime="text/csv"
            )
    else:
        st.info("Please train the model first to enable forecasting.")
else:
    st.info("Please generate or upload data to get started.")

st.markdown("---")
st.markdown("Built with ❤️ using Streamlit and scikit-learn")
