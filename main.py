from src.data_loader import load_session
from src.plots import plot_lap_times_and_tyres

if __name__ == "__main__":
    from src.data_loader import load_session
    from src.plots import plot_lap_times_and_tyres
    import os

    project_root = os.path.dirname(os.path.abspath(__file__))
    save_path = os.path.join(project_root, "plots", "laps_info.png")

    session = load_session(2024, 'Monza', 'R')
    plot_lap_times_and_tyres(session, ["LEC", "VER", "HAM"], save_path=save_path)

    print(f"Plot saved to {save_path}")

