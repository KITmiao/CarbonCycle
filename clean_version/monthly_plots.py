import pandas as pd
import matplotlib.pyplot as plt
from input import years
class MonthlyPlot:
    def __init__(self,ax):
        self.hline=ax.axhline(0, color='grey', linestyle='-', linewidth=2, alpha=0.3)
        for year in years:
            ax.axvline(pd.to_datetime(f'{year}-01-01'),
                       color='gray', linestyle='-', linewidth=0.8, alpha=0.5)
        ax.set_xlabel('Year')
        self.ax = ax
    def co2_flux(self):
        self.ax.set_ylabel('CO$_2$ flux (Tg/month)')
        return self
    def co2_conc(self):
        self.ax.set_ylabel('Detrended CO$_2$ (ppm)', labelpad=-5)
        return self
    def rain(self):
        self.ax.set_ylabel('Mean monthly\nprecipitation (mm)')
        return self
    def obs_num(self):
        self.ax.set_ylabel('Observation\nnumber')
        return self
    def temp(self):
        self.ax.set_ylabel('Mean monthly\n2m temperature (\u00B0C)')
        return self
    def lats(self):
        self.ax.set_ylabel('Latitude')
        return self
    def lons(self):
        self.ax.set_xlabel('Longitude')
        self.ax.set_ylabel('time')
        return self
    def remove_hline(self):
        self.hline.remove()
        return self
