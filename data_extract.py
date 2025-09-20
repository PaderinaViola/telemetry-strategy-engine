import fastf1 as ff1
from fastf1 import plotting
from fastf1 import utils
import fastf1.legacy
import fastf1 as ff1
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib import cm
import matplotlib.font_manager as fm
import numpy as np
import pandas as pd
import os


# Enable the cache by providing the name of the cache folder
ff1.Cache.enable_cache('Cache')
plotting.setup_mpl()


def load_race_session(year, gp_name, event):
    session_race = ff1.get_session(year, gp_name, event)
    session_race.load()
    return session_race

def plot_lap_times(year, gp_name, drivers):
    """
    Extract lap times for top 3 drivers (or given driver list)
    in the given race and plot LapNumber vs LapTime.
    """
    session = load_race_session(year, gp_name, 'R')
    laps = session.laps
    laps_top = laps[laps['Driver'].isin(drivers)].copy()
    laps_top['LapTimeSec'] = laps_top['LapTime'].dt.total_seconds()
    
    plt.figure(figsize=(10,6))
    for drv in drivers:
        drv_laps = laps_top[laps_top['Driver'] == drv]
        # Sort by lap number just in case
        drv_laps = drv_laps.sort_values('LapNumber')
        plt.plot(drv_laps['LapNumber'], drv_laps['LapTimeSec'], marker='o', label=drv)
    
    plt.xlabel('Lap Number')
    plt.ylabel('Lap Time (s)')
    plt.title(f'Lap Times for {", ".join(drivers)} in {gp_name} {year}')
    plt.legend()
    plt.grid(True)
    plt.show()
    if not os.path.exists("./laps"):
        os.mkdir("./laps")
    plt.savefig(f"./laps/laps_info.png")
    plt.close()

if __name__ == "__main__":
    year= 2025
    gp = 'Abu Dhabi'
    drivers = "LEC"

