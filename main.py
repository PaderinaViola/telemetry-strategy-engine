from test import plot_lap_times, plot_pitstop_strategy, export_pitstop_summary

if __name__ == "__main__":
    year = 2021
    gp = "Abu Dhabi"
    drivers = ["VER", "HAM", "SAI"]

    plot_lap_times(year, gp, drivers)
    plot_pitstop_strategy(year, gp, drivers)
    export_pitstop_summary(year, gp, drivers)