import name_dic
import numpy as np
import matplotlib.dates as mdates
class VisualLines:
    def __init__(self,ax,time):
        self.ax   = ax
        self.time = time
    def tm5_4dvar_prior(self,data):
        self.ax.plot(self.time, data['TM5-4DVAR_prior']
                     , color='k', linestyle='--', label='TM5 4DVAR$_{prior}$')
        return self
    def cams_prior(self,data):
        self.ax.plot(self.time, data['CAMS_prior']
                     , color='b', linestyle='--', label='CAMS$_{prior}$')
        return self
    def ct_cms_prior(self,data):
        self.ax.plot(self.time, data['CT_pri_cms']
                     , color='b', linestyle='--', label='CT2022$_{GFED cms}$')
        return self
    def ct_4p1s_prior(self,data):
        self.ax.plot(self.time, data['CT_pri_4p1s']
                     , color='b', linestyle='--', label='CT2022$_{GFED 4.1s}$')
        return self
    def tm5_4dvar_insitu(self,data):
        self.ax.plot(self.time, data['TM5-4DVAR']
                     , color='royalblue', label='TM5 4DVAR$_{in-situ}$')
        return self
    def cams(self,data):
        self.ax.plot(self.time, data['CAMS']
                     , color='royalblue', label='CAMS$_{in-situ}$')
        return self
    def ct(self,data):
        self.ax.plot(self.time, data['CarbonTracker']
                     , color='royalblue', label='CT2022$_{in-situ}$')
        return self
    def remotec(self,data):
        self.ax.plot(self.time, data['RemoTeC']
                     , color='r', label='TM5 4DVAR$_{+GOSAT/RemoTeC}$')
        return self
    def acos(self,data):
        self.ax.plot(self.time, data['ACOS']
                     , color='chocolate', label='TM5 4DVAR$_{+GOSAT/ACOS}$')
        return self
    def inv_sat(self,data,*range):
        #print(type(self.ax))
        self.ax.plot(self.time, data['mean']
                     ,color='firebrick',label='TM5 4DVAR$_{+GOSAT}$')
        if range:
            lb = data[name_dic.tm5gosat_names].min(axis=1)
            ub = data[name_dic.tm5gosat_names].max(axis=1)
            self.ax.fill_between(self.time, lb, ub,
                                 color='firebrick', alpha=0.4, edgecolor='none')
        return self
    def inv_insitu(self,data,*range):
        self.ax.plot(self.time, data['mean'],
                     color='royalblue',label='Inverse Model$_{in-situ}$')
        if range:
            lb = data[name_dic.tm5is_names].min(axis=1)
            ub = data[name_dic.tm5is_names].max(axis=1)
            self.ax.fill_between(self.time, lb, ub,
                                 color='royalblue', alpha=0.4, edgecolor='none')
        return self
    def trendy_all(self,data,*range):
        self.ax.plot(self.time, -data['mean']
                     ,color='grey', label='TRENDY$_{all}$')
        if range:
            lb = -(data['mean'] - data['SD'])
            ub = -(data['mean'] + data['SD'])
            self.ax.fill_between(self.time, lb, ub,
                                 color='grey', alpha=0.4, edgecolor='none')
        return self
    def trendy_sel(self,data,group_list,*range):
        self.ax.plot(self.time, data[group_list].mean(axis=1)
                     ,color='k', label='TRENDY$_{selection}$')
        if range:
            lb = -(data[group_list].mean(axis=1) - data[group_list].std(axis=1))
            ub = -(data[group_list].mean(axis=1) + data[group_list].std(axis=1))
            self.ax.fill_between(self.time, lb, ub,
                                 color='k', alpha=0.3, edgecolor='none')
        return self
    def trendy_bad(self,data,group_list,*range):
        self.ax.plot(self.time, data[group_list].mean(axis=1)
                     , color='grey', label='TRENDY$_{selection}$')
        if range:
            lb = -(data[group_list].mean(axis=1) - data[group_list].std(axis=1))
            ub = -(data[group_list].mean(axis=1) + data[group_list].std(axis=1))
            self.ax.fill_between(self.time, lb, ub,
                                 color='grey', alpha=0.3, edgecolor='none')
        return self
    def trendy_gpp(self,data,group_list,*range):
        mean = data[group_list].mean(axis=1)
        std  = data[group_list].std(axis=1)
        self.ax.plot(self.time, mean, color='green', linewidth=1, label='GPP')
        """
        self.ax.fill_between(self.time, mean, y2=0,
                         interpolate=True, color='none', hatch='//', alpha=0.5, edgecolor='green', label='GPP')
        """
        if range:
            lb = (mean - std)
            ub = (mean + std)
            self.ax.fill_between(self.time, lb, ub,
                                 color='green', alpha=0.3, edgecolor='none')
        return self
    def trendy_nee(self,ter,gpp,group_list,*range):
        nee = ter[group_list]-gpp[group_list]
        mean = nee[group_list].mean(axis=1)
        std = nee[group_list].std(axis=1)
        self.ax.plot(self.time, mean, color='k', linewidth=1, label='TER-GPP')
        if range:
            lb = (mean - std)
            ub = (mean + std)
            self.ax.fill_between(self.time, lb, ub,
                                 color='k', alpha=0.3, edgecolor='none')
        return self
    def trendy_ter(self, data, group_list, *range):
        mean = data[group_list].mean(axis=1)
        std = data[group_list].std(axis=1)
        self.ax.plot(self.time, mean, color='purple', linewidth=1, label='TER')
        """
        self.ax.fill_between(self.time, mean, y2=0,
                             interpolate=True, color='none', hatch='\\\\', alpha=0.5, edgecolor='purple', label='TER')
        """
        if range:
            lb = (mean - std)
            ub = (mean + std)
            self.ax.fill_between(self.time, lb, ub,
                                 color='purple', alpha=0.3, edgecolor='none')
        return self
    def trendy_nbp(self, data, group_list, *range):
        mean = data[group_list].mean(axis=1)
        std = data[group_list].std(axis=1)
        self.ax.plot(self.time, mean, color='k', linewidth=1, label='TRENDY NBP')
        """
        self.ax.fill_between(self.time, mean, y2=0,
                             interpolate=True, color='none', hatch='\\\\', alpha=0.5, edgecolor='purple', label='TER')
        """
        if range:
            lb = (mean - std)
            ub = (mean + std)
            self.ax.fill_between(self.time, lb, ub,
                                 color='k', alpha=0.3, edgecolor='none')
        return self
    def fill_with_color(self,data1,data2,cond,color):
        self.ax.fill_between(self.time, data1, data2,
                                where=cond,
                                interpolate=True, color=color, alpha=0.5)
        return self
    def fill_with_crosslin(self, data1,data2,cond, color):
        self.ax.fill_between(self.time, data1, data2,
                             where=cond,
                             interpolate=True, color='none', alpha=0.5, hatch='////', edgecolor=color)
        self.ax.fill_between(self.time, data1, data2,
                             where=cond,
                             interpolate=True, color='none', alpha=0.5, hatch='\\\\', edgecolor=color)
        return self
    def gfed(self,data):
        self.ax.plot(self.time, data['gfed']
                     , color='orange', label='GFED')
        return self
    def gfas(self,data):
        self.ax.plot(self.time, data['gfas']
                     , color='hotpink', label='GFAS')
        return self
    def finn(self,data):
        self.ax.plot(self.time, data['finn']
                     , color='purple', label='FINN')
        return self
    def fluxcom_and_fire(self,fluxcom,fire,firename):
        """
        :param fluxcom:
        :param fire:
        :param firename:'GFED','GFAS','FINN'
        :return:
        """
        self.ax.plot(self.time, fluxcom['NEE']+fire[firename.lower()]
                     , color='gold', label=f'FLUXCOM+{firename}')
        return self
    def gosif_gpp(self, data):
        self.ax.plot(self.time, data, color='green', label='GOSIF GPP',linewidth=3, linestyle='--')
        return self
    def nirv_gpp(self, data):
        self.ax.plot(self.time, data, color='r', label='NIRv GPP',linewidth=3, linestyle='--')
        return self
    def precipitation(self, data, label):
        # change gap to adjust the distance between bars
        gap = 1
        if self.time.dtype != np.int64:
            time = mdates.date2num(self.time)
        else:
            time = self.time
        time_diffs = np.diff(time)
        min_time_diff = np.min(time_diffs)
        adaptive_width = min_time_diff * gap
        self.ax.bar(time, data,
                width=adaptive_width, linewidth=0.7, align='edge', color='white', edgecolor='k', label=label)
        return self

    def temp(self, data, label):
        self.ax.plot(self.time, data,
                    color='r', label=label, marker='s', markersize=3)
        return self
