import pandas as pd
from statistical_analysis import change_order
from settings import order
class SeasonPlot:
    def __init__(self,ax):
        months = [3, 6, 9, 12]
        self.hline = ax.axhline(0, color='grey', linestyle='-', linewidth=2, alpha=0.3)
        for mn in months:
            ax.axvline(mn,
                       color='gray', linestyle='-', linewidth=0.8, alpha=0.5)
        ax.set_xlabel('month')
        ax.set_xticks([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        ax.set_xticklabels(order)
        ax.set_xlim(1, 15)
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
    def remove_hline(self):
        self.hline.remove()
        return self