import fastf1 as ff1
from fastf1.core import Laps
from fastf1 import plotting
from timple.timedelta import strftimedelta
import pandas as pd
import numpy as np


plotting.setup_mpl()
ff1.Cache.enable_cache('data/cache')


class session_data:

    loaded_data = {}
    current_session = None

    def __init__(self, year, race_number, session_type):
        self.session = ff1.get_session(year, race_number, session_type)
        self.year = year
        self.race_number = race_number
        self.session_type = session_type
        self.selected_drivers = []
        # key is concatenation of year, race_number and session_type

        self.loaded_data.setdefault(str(year) + str(race_number) + session_type , self)
        print(self.loaded_data)
    
    # TODO Download only needed data
    def load_session(self):
        self.session.load()
        return self.session

    def get_fastest_lap(self, driver):
        return self.session.laps.pick_driver(driver).pick_fastest()

    def get_fastest_laps(self, drivers):
        list_fastest_laps = list()
        for drv in drivers:
            drvs_fastest_lap = self.session.laps.pick_driver(drv).pick_fastest()
            if(not pd.isna(drvs_fastest_lap['LapTime'])):
                list_fastest_laps.append(drvs_fastest_lap)
        return Laps(list_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)

    def get_all_drivers(self):
        return pd.unique(self.session.results['Abbreviation'])

    def get_team_colors(self):
        print(self.session.results)
        return self.session.results.groupby('TeamName').first()['TeamColor']
    
    @classmethod
    def get_session(cls, year, race_number, session_type):
        key = str(year) + str(race_number) + session_type
        if key in cls.loaded_data:
            return cls.loaded_data[str(year) + str(race_number) + session_type]

    @classmethod
    def set_current(cls, data):
        cls.current_session = data