import fastf1 as ff1
from fastf1 import plotting
import pandas as pd
import matplotlib.pyplot as plt
import os

def ensure_dir_exists(path):
    os.makedirs(path, exist_ok=True)

# If you need a common color mapping or wrapper, you could add:
def get_compound_color(compound, session):
    return plotting.get_compound_color(compound, session)