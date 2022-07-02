import fastf1 as ff1
from fastf1.core import Laps
from fastf1 import plotting
from timple.timedelta import strftimedelta
import pandas as pd

plotting.setup_mpl()
ff1.Cache.enable_cache('data/cache')


class session_data:

    def __init__(self, year, race_number, session_type):
        self.session = ff1.get_session(year, race_number, session_type)
        self.session.load()
    
    def get_fastest_laps(self, drivers):
        list_fastest_laps = list()
        for drv in drivers:
            drvs_fastest_lap = self.session.laps.pick_driver(drv).pick_fastest()
            list_fastest_laps.append(drvs_fastest_lap)
        return Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)

    def get_all_drivers(self):
        return pd.unique(self.session.laps['Driver'])

    def get_team_colors(self):
        return self.session.results.groupby('TeamName').first()['TeamColor']