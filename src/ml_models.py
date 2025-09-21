import joblib
import fastf1 as ff1
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report

ff1.Cache.enable_cache("Cache")

def build_dataset(year, gps, drivers):
    all_laps = []
    for gp in gps:
        session = ff1.get_session(year, gp, "R")
        session.load(telemetry=False, weather=False)
        laps = session.laps.pick_drivers(drivers).copy()
        if laps.empty:
            print(f"⚠️ No laps for {gp}, skipping...")
            continue
        laps["LapTimeSec"] = laps["LapTime"].dt.total_seconds()
        laps["roll_avg"] = (laps.groupby("Driver")["LapTimeSec"].rolling(3, min_periods=1).mean().reset_index(level=0, drop=True))
        laps["prev_lap_time"] = laps.groupby("Driver")["LapTimeSec"].shift(1)
        laps["is_pit_lap"] = laps["PitOutTime"].notna()
        laps["GP"] = gp
        laps = laps.dropna(subset=["LapTimeSec", "roll_avg", "prev_lap_time"])
        all_laps.append(laps)
    if not all_laps:
        raise ValueError("❌ No valid laps found for given races/drivers")
    laps = pd.concat(all_laps, ignore_index=True)
    X = laps[["LapNumber", "LapTimeSec", "roll_avg", "prev_lap_time"]]
    y = laps["is_pit_lap"].astype(int)
    return X, y

def train_model(X, y, model_path="data/pitstop_model.pkl"):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    model = RandomForestClassifier(n_estimators=100, max_depth=5, class_weight="balanced", random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    print("Classification Report:")
    print(classification_report(y_test, y_pred))
    joblib.dump(model, model_path)
    print(f"✅ Model saved to {model_path}")


if __name__ == "__main__":
    year = 2023
    gps = ["Sakhir", "Jeddah", "Melbourne", "Baku", "Miami", "Imola", "Monte Carlo", "Barcelona", "Montreal", "Red Bull Ring", "Silverstone", "Hungaroring", "Spa", "Zandvoort", "Monza", "Marina Bay", "Suzuka", "Losail", "Austin", "Mexico City", "Interlagos", "Las Vegas", "Yas Marina"]
    drivers = ["VER", "LEC", "HAM", "RUS", "SAI"]
    X, y = build_dataset(year, gps, drivers)
    print("Dataset size:", X.shape, "Pit laps:", y.sum())
    train_model(X, y)
