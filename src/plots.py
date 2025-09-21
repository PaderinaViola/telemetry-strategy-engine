import os
import matplotlib.pyplot as plt
from matplotlib import lines as mlines
from fastf1 import plotting


def plot_lap_times_and_tyres(session, drivers, save_path=None):
    fig, (lap_ax, stint_ax) = plt.subplots(2, 1, figsize=(10, 6), gridspec_kw={'height_ratios': [3, 1]}, sharex=True)
    for drv in drivers:
        drv_laps = session.laps.pick_drivers(drv)
        if drv_laps.empty:
            print(f"⚠️ No laps found for {drv}, skipping...")
            continue
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
            stint_ax.broken_barh([(last_end, length)], (i - 0.4, 0.8), facecolors=col, edgecolors='black')
            last_end += length
    stint_ax.set_yticks(range(len(drivers)))
    stint_ax.set_yticklabels(drivers)
    stint_ax.set_xlabel("Lap Number")

    compounds = stints['Compound'].unique()
    handles = [mlines.Line2D([0], [0], color=plotting.get_compound_color(c, session), lw=6) for c in compounds]
    stint_ax.legend(handles, compounds, title="Tyre Compounds", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()

    if save_path is None:
        os.makedirs("plots", exist_ok=True)
        save_path = os.path.join("plots", "laps_info.png")
    plt.savefig(save_path)
    plt.close()
    print("Available drivers:", session.drivers)
    return save_path 

