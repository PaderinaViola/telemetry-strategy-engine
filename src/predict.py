import fastf1 as ff1
import pandas as pd
import joblib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


def prepare_race_data(year, gp, drivers):
    session = ff1.get_session(year, gp, "R")
    session.load(telemetry=False, weather=False)
    laps = session.laps.pick_drivers(drivers).copy()
    if laps.empty:
        raise ValueError(f"No laps found for {gp} in {year}")
    laps["LapTimeSec"] = laps["LapTime"].dt.total_seconds()
    laps["roll_avg"] = (laps.groupby("Driver")["LapTimeSec"].rolling(3, min_periods=1).mean().reset_index(level=0, drop=True))
    laps["prev_lap_time"] = laps.groupby("Driver")["LapTimeSec"].shift(1)
    laps["is_pit_lap"] = laps["PitOutTime"].notna()
    laps = laps.dropna(subset=["LapTimeSec", "roll_avg", "prev_lap_time"]).reset_index(drop=True)

    X = laps[["LapNumber", "LapTimeSec", "roll_avg", "prev_lap_time"]]
    y_true = laps["is_pit_lap"].astype(int)
    return X, y_true, laps



def predict_and_plot(year, gp, drivers, model_path="data/pitstop_model.pkl", threshold=0.7):
    model = joblib.load(model_path)
    X, y_true, laps = prepare_race_data(year, gp, drivers)
    if X is None:
        print(f"⚠️ Skipping {year} {gp} — no data to predict.")
        return
    y_prob = model.predict_proba(X)[:, 1]
    y_pred = (y_prob > threshold).astype(int)
    plt.figure(figsize=(10, 6))
    for driver in drivers:
        drv_laps = laps[laps["Driver"] == driver]
        if drv_laps.empty:
            continue
        pred_pit = drv_laps[y_pred[:len(drv_laps)] == 1]
        pred_normal = drv_laps[y_pred[:len(drv_laps)] == 0]

        if not pred_pit.empty:
            plt.scatter(pred_pit["LapNumber"], [driver] * len(pred_pit), c="red", marker="o", alpha=0.6)

        if not pred_normal.empty:
            plt.scatter(pred_normal["LapNumber"], [driver] * len(pred_normal), c="green", marker="o", alpha=0.6)

        pit_laps = drv_laps[drv_laps["is_pit_lap"] == 1]
        if not pit_laps.empty: plt.scatter(pit_laps["LapNumber"], [driver] * len(pit_laps), c="black", marker="x", s=80)

    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=8, label='Predicted pit'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=8, label='Predicted normal'),
        Line2D([0], [0], marker='x', color='black', markersize=8, label='Actual pit')
    ]
    plt.legend(handles=legend_elements)
    plt.title(f"Predicted vs Actual Pit Stops ({year} {gp})")
    plt.xlabel("Lap Number")
    plt.ylabel("Driver")
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    year = 2024
    gp = "Monza"
    drivers = ["VER", "RUS", "HAM", "SAI"]
    predict_and_plot(year, gp, drivers)
