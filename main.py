# main.py
import streamlit as st
import os

from src.data_loader import load_session
from src.plots import plot_lap_times_and_tyres
from src.ml_models import build_dataset, train_model
from src.predict import predict_and_plot


def main():
    st.title("🏎️ Formula 1 Data & Pit Stop Predictor")

    menu = ["Visualize Race", "Train ML Model", "Predict Pit Stops"]
    choice = st.sidebar.selectbox("Choose Action", menu)

    if choice == "Visualize Race":
        st.header("📊 Lap Times & Tyre Stints")

        year = st.number_input("Year", min_value=2018, max_value=2024, value=2024)
        gp = st.text_input("Grand Prix (e.g. Monza, Miami)", "Monza")
        drivers = st.text_input("Drivers (comma-separated abbreviations)", "VER,LEC,HAM")

        if st.button("Generate Plot"):
            session = load_session(year, gp, "R")
            save_path = plot_lap_times_and_tyres(session, drivers.split(","))
            st.image(save_path, caption=f"Lap Times & Tyre Stints: {gp} {year}")

    elif choice == "Train ML Model":
        st.header("🤖 Train Pit Stop Prediction Model")

        year = st.number_input("Training Year", min_value=2018, max_value=2024, value=2023)
        gps = st.text_area("Grand Prix list (comma-separated)", "Sakhir,Jeddah,Melbourne,Baku,Miami,Imola,Monte Carlo,Barcelona,Montreal,Red Bull Ring,Silverstone,Hungaroring,Spa,Zandvoort,Monza,Marina Bay,Suzuka,Losail,Austin,Mexico City,Interlagos,Las Vegas,Yas Marina")
        drivers = ["VER", "LEC", "HAM", "RUS", "SAI"]
        drivers = st.text_input("Drivers (comma-separated abbreviations)", "VER, LEC, HAM, RUS, SAI")

        if st.button("Train Model"):
            gps_list = [gp.strip() for gp in gps.split(",")]
            drivers_list = [d.strip() for d in drivers.split(",")]

            X, y = build_dataset(year, gps_list, drivers_list)
            model_path = "data/pitstop_model.pkl"
            train_model(X, y, model_path=model_path)

            st.success(f"✅ Model trained and saved to {model_path}")

    elif choice == "Predict Pit Stops":
        st.header("🔮 Predict Pit Stops")

        year = st.number_input("Prediction Year", min_value=2018, max_value=2024, value=2024)
        gp = st.text_input("Grand Prix (e.g. Miami, Monza)", "Miami")
        drivers = st.text_input("Drivers (comma-separated abbreviations)", "VER,HAM,SAI")

        if st.button("Run Prediction"):
            predict_and_plot(year, gp, [d.strip() for d in drivers.split(",")])
            st.pyplot()  # show matplotlib plot directly


if __name__ == "__main__":
    main()

