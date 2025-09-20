import fastf1 as ff1 
from fastf1 import plotting 
import pandas as pd 
import matplotlib.pyplot as plt
import os

ff1.Cache.enable_cache('Cache')
ff1.plotting.setup_mpl()

def load_session(year: int, gp: str, session_type: str, telemetry=False, weather=False):
    """
    Load a FastF1 session and return it.
    """
    session = ff1.get_session(year, gp, session_type)
    session.load(telemetry=telemetry, weather=weather)
    return session
