import fastf1 as ff1
from fastf1 import plotting
import pandas as pd
import matplotlib.pyplot as plt
import os

ff1.Cache.enable_cache('Cache')
plotting.setup_mpl()

def plot_lap_times_and_tyres(year, gp, session_type, drivers, save_path="./laps/laps_info.png"):
    """
    Plots lap times and tyre stints for selected drivers in a given F1 session.
    Parameters:
    - year: int, e.g., 2023
    - gp: str, Grand Prix name, e.g., 'Monaco'
    - session_type: str, e.g., 'R', 'Q', 'S'
    - drivers: list of str, e.g., ['LEC', 'PIA', 'SAI']
    - save_path: str, file path to save the figure
    """
   
    session = ff1.get_session(year, gp, session_type)
    session.load(telemetry=False, weather=False)

    fig, (lap_ax, stint_ax) = plt.subplots(2, 1, figsize=(10, 6), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)

    for drv in drivers:
        drv_laps = session.laps.pick_drivers(drv)
        abb = drv_laps["Driver"].iloc[0]
        color = plotting.get_driver_color(abb, session)
        lap_ax.plot(drv_laps['LapNumber'], drv_laps['LapTime'], label=abb, color=color)

    lap_ax.set_ylabel("Lap Time")
    lap_ax.legend()

    stints = session.laps[["Driver", "Stint", "Compound", "LapNumber"]]
    stints = stints.groupby(["Driver", "Stint", "Compound"]).count().reset_index()
    stints = stints.rename(columns={"LapNumber": "StintLength"})

    for i, drv in enumerate(drivers):
        drv_stints = stints.loc[stints['Driver'] == drv]
        last_end = 0
        for _, row in drv_stints.iterrows():
            compound = row['Compound']
            length = row['StintLength']
            col = plotting.get_compound_color(compound, session)
            stint_ax.broken_barh([(last_end, length)], (i - 0.4, 0.8),
                                 facecolors=col, edgecolors='black')
            last_end += length

    stint_ax.set_yticks(range(len(drivers)))
    stint_ax.set_yticklabels(drivers)
    stint_ax.set_xlabel("Lap Number")

    compounds = stints['Compound'].unique()
    handles = [plt.Line2D([0], [0], color=plotting.get_compound_color(c, session), lw=6) for c in compounds]
    stint_ax.legend(handles, compounds, title="Tyre Compounds", bbox_to_anchor=(1.05, 1), loc='upper left')
    

    plt.tight_layout()
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    plt.savefig(save_path)
    plt.close()

if __name__ == "__main__":
    year = 2024
    gp = 'Monza'
    session_type = 'R'
    drivers = ["LEC", "PIA", "NOR"]  # list of drivers
    plot_lap_times_and_tyres(year, gp, session_type, drivers)