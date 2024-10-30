transcom = {
    'North American Boreal': {'name':'North American Boreal',
                              'id':[1],
                              'area':9.92914535e+12,
                              'lon_min':75, 'lon_max':155, 'lat_min':75, 'lat_max':120},
    'North American Temperate': {'name':'North American Temperate',
                                 'id':[2],
                                 'area':1.12536480e+13,
                                 'lon_min':-140, 'lon_max':-50, 'lat_min':16, 'lat_max':56},
    'South American Tropical': {'name':'South American Tropical',
                                'id':[3],
                                'area':9.91790982e+12,
                                'lon_min':75, 'lon_max':155, 'lat_min':75, 'lat_max':120},
    'South American Temperate': {'name':'South American Temperate',
                                 'id':[4],
                                 'area':9.14728386e+12,
                                 'lon_min':-180, 'lon_max':180, 'lat_min':-90, 'lat_max':90},
    'Africa': {
                        'name':'Africa',
                        'id':[5,6],
                        'area':1.02476004e+13 + 2.09880079e+13,
                        'lon_min':-20, 'lon_max':52, 'lat_min':-35, 'lat_max':40
    },
    'Central Africa': {
                        'name':'Central Africa',
                        'id':[5,6],
                        'area':10198312017848.516,
                        'lon_min':-20, 'lon_max':52, 'lat_min':-10, 'lat_max':10
    },
    'Northern Africa': {'name':'Northern Africa',
                        'id':[5],
                        'area':2.09880079e+13,
                        'lon_min':-20, 'lon_max':52, 'lat_min':0, 'lat_max':40},
    'Northern Africa itcz': {'name':'Northern Africa itcz',
                        'id':[5],
                        'area':13323488600612.225,
                        'lon_min':-17, 'lon_max':51, 'lat_min':0, 'lat_max':20}, # 51, 15 [-17, 51] [1, 15]
    'Ethiopia':{'name':'Ethiopia',
                        'id':[5],
                        'area':806712302003.494,
                        'lon_min':31, 'lon_max':41, 'lat_min':6, 'lat_max':11
    },
    'Africa 05N20N': {'name':'Africa 05N20N',
                        'id':[5],
                        'area':11483396403538.732,
                        'lon_min':-17, 'lon_max':51, 'lat_min':5, 'lat_max':20}, # 51, 15 [-17, 51] [1, 15]
    'Africa 05N15N': {'name':'Africa 05N15N',
                        'id':[5],
                        'area':8120814109592.613,
                        'lon_min':-17, 'lon_max':51, 'lat_min':5, 'lat_max':15}, # 51, 15 [-17, 51] [1, 15]
    'Africa 05N13N': {'name':'Africa 05N15N',
                        'id':[5],
                        'area':8120814109592.613,
                        'lon_min':-17, 'lon_max':51, 'lat_min':5, 'lat_max':13},
    'Africa 05N20N east': {'name':'Africa 05N20N east',
                        'id':[5],
                        'area':3250080527285.3467,
                        'lon_min':29, 'lon_max':51, 'lat_min':5, 'lat_max':20},
    'Africa 05N20N west': {'name':'Africa 05N20N west',
                        'id':[5],
                        'area':8425828578686.826,
                        'lon_min':-17, 'lon_max':29, 'lat_min':5, 'lat_max':20},
    'Northern Africa itcz west': {
                        'name':'Northern Africa itcz west',
                        'id':[5,6],
                        'area':1,
                        'lon_min':-17, 'lon_max':29, 'lat_min':-10, 'lat_max':7
    },
    'Northern Africa itcz east': {
                        'name':'Northern Africa itcz east',
                        'id':[5,6],
                        'area':1, # 33 LM(SIF)+RM good agreement with ISAM
                        'lon_min':29, 'lon_max':51, 'lat_min':-10, 'lat_max':7
    },
    'Africa 00S20N west': {
                        'name':'Africa 00S20N west',
                        'id':[5,6],
                        'area':1,
                        'lon_min':-17, 'lon_max':29, 'lat_min':0, 'lat_max':20
    },
    'Africa 00S20N east': {
                        'name':'Africa 00S20N east',
                        'id':[5,6],
                        'area':1, # 33 LM(SIF)+RM good agreement with ISAM
                        'lon_min':29, 'lon_max':51, 'lat_min':0, 'lat_max':20
    },
    'Africa 05S15N west': {
                        'name':'Africa 05S15N west',
                        'id':[5,6],
                        'area':1,
                        'lon_min':-17, 'lon_max':29, 'lat_min':-5, 'lat_max':15
    },
    'Africa 05S15N east': {
                        'name':'Africa 05S15N east',
                        'id':[5,6],
                        'area':1, # 33 LM(SIF)+RM good agreement with ISAM
                        'lon_min':29, 'lon_max':51, 'lat_min':-5, 'lat_max':15
    },
    'Africa 10S10N west': {
                        'name':'Africa 10S10N west',
                        'id':[5,6],
                        'area':1,
                        'lon_min':-17, 'lon_max':29, 'lat_min':-10, 'lat_max':10
    },
    'Africa 10S10N east': {
                        'name':'Africa 10S10N east',
                        'id':[5,6],
                        'area':1, # 33 LM(SIF)+RM good agreement with ISAM
                        'lon_min':29, 'lon_max':51, 'lat_min':-10, 'lat_max':10
    },
    'Northern Africa itcz south': {'name':'Northern Africa itcz south', # -17,51
                        'id':[5],
                        'area':1259671597235.4585, #2468264574391.77
                        'lon_min':9, 'lon_max':20, 'lat_min':0, 'lat_max':4}, # 51, 15 [-17, 51] [1, 15]
    'Northern Africa itcz mid': {'name':'Northern Africa itcz mid',
                        'id':[5],
                        'area':4024282813520.953, #4619679467312.458
                        'lon_min':-17, 'lon_max':35, 'lat_min':5, 'lat_max':11}, # 51, 15 [-17, 51] [1, 15]
    'Northern Africa itcz north': {'name':'Northern Africa itcz north', # -17,51
                        'id':[5],
                        'area':5556621979766.517, #2872962264961.8784
                        'lon_min':-17, 'lon_max':35, 'lat_min':12, 'lat_max':20}, # 51, 15 [-17, 51] [1, 15]
    'Northern Africa Mediterranean': {'name':'Northern Africa Mediterranean',
                        'id':[5],
                        'area':2.09880079e+13,
                        'lon_min':-20, 'lon_max':52, 'lat_min':35, 'lat_max':39},
    'Southern Africa': {'name':'Southern Africa',
                        'id':[6],
                        'area':1.02476004e+13,
                        'lon_min':-180, 'lon_max':180, 'lat_min':-90, 'lat_max':-10},
    'Eurasia Boreal': {'name':'Eurasia Boreal',
                       'id':[7],
                       'area':1.35635665e+13,
                       'lon_min':-180, 'lon_max':180, 'lat_min':-90, 'lat_max':90},
    'Eurasia Temperate': {'name':'Eurasia Temperate',
                          'id':[8],
                          'area':2.60175594e+13,
                          'lon_min':-180, 'lon_max':180, 'lat_min':-90, 'lat_max':90},
    'Tropical Asia': {'name':'Tropical Asia',
                      'id':[9],
                      'area':6.47980288e+12,
                      'lon_min':80, 'lon_max':160, 'lat_min':-11, 'lat_max':27,
                      'country':[20.,38.,66.,91.,92.,107.,113.,131.,141.,160.,162.,180.,199.,203.,209.,221.]},
    'Tropical Asia mainland':{'name':'monsoon climate region',
                              'id':[9],
                              'area':3.2144424699063013e12,
                              'lon_min':75, 'lon_max':180, 'lat_min':10, 'lat_max':30, # 10, 90
                              'country':[20,38,92,107,113,131,199,209,221]},
    'Tropical Asia islands':{'name':'rainforest climate region',
                              'id':[9],
                              'area':3.2742918482983364e12,
                              'lon_min':75, 'lon_max':180.0, 'lat_min':-20.0, 'lat_max':10.0,
                             'country':[66.,  91., 141., 160., 162., 180., 203.]},
    'Australia': {'name':'Australia',
                  'id':[10],
                  'area':8.04600923e+12,
                  'lon_min':112, 'lon_max':180, 'lat_min':-50, 'lat_max':-10},
    'Europe': [11, 1.14923051e+13],
    'North Pacific Temperate': [12, 3.74983515e+13],
    'West Pacific Tropical': [13, 3.12908912e+13],
    'East Pacific Tropical': [14, 3.49792988e+13],
    'South Pacific Temperate': [15, 3.74983515e+13],
    'Northern Ocean': [16, 2.14265270e+13],
    'Northern Atlantic Temperate': [17, 2.24065207e+13],
    'Atlantic Tropical': [18, 2.40741779e+13],
    'Southern Atlantic Temperate': [19, 1.85667751e+13],
    'Southern Ocean': [20, 6.29342909e+13],
    'Indian Tropical': [21, 3.14071518e+13],
    'South Indian Temperate': [22, 2.64431293e+13],
    'Not optimized': [23, 1.67106298e+13]
}

trendy_names = [
        'CABLE-POP',  # 1
           'CLASSIC',  # 2
           'CLM5.0',  # 3
           'DLEM',  # 4
           'IBIS',  # 5
           'ISAM',  # 6
           'ISBA-CTRIP',  # 7
           'JSBACH',  # 8
           'JULES-ES-1p0',  # 9
           'LPJ',  # 10
           'LPX-Bern',  # 11
           'OCN',  # 12
           'ORCHIDEE-CNP',  # 13
           'ORCHIDEEv3',  # 14
           'ORCHIDEE',  # 15
           'SDGVM',  # 16
           'VISIT',  # 17
           'YIBs'    # 18
     ]

trendy_names_v11 = [   # 17 models, no permission to download CARDAMOM, LPJ-GUESS no monthly data
    'CABLE-POP'
    , 'CLASSIC'
    , 'CLM5.0'
    , 'DLEM'
    , 'IBIS'
    , 'ISAM'
    , 'ISBA-CTRIP'
    , 'JULES'
    , 'JSBACH'
    , 'LPJ'
    , 'LPX-Bern'
    , 'OCN'
    , 'ORCHIDEE'
    , 'SDGVM'
    , 'VISIT-NIES'
    , 'VISIT'
    , 'YIBs'
]

tm5gosat_names = [
        'RemoTeC',
        'ACOS',
    ]

tm5oco_names = [
    'OCO'
]

tm5is_names = [
        'CAMS',
        'CarbonTracker',
        'TM5-4DVAR'
    ]
prior_names = [
        'CAMS_prior',
        'CT_pri_cms',
        'CT_pri_4p1s',
        'TM5-4DVAR_prior'
    ]

oco2mip_names = [
    'Ames',
    'Baker',
    'CAMS',
    'CMS-Flux',
    'COLA',
    'CSU',
    'CT',
    'JHU',
    'LoFI',
    'NIES',
    'OU',
    'TM5-4DVAR',
    'UT',
    'WOMBAT',
    'EnsMean',
    'EnsStd'
]

fire_names = [
              'finn',
              'gfas',
              'gfed'
       ]

fFire_names = [
    'CLASSIC',
    'ISBA-CTRIP',
    'LPX-Bern',
    'ORCHIDEE',
    'VISIT',
    'CLM5.0',
    'JSBACH',
    'LPJ',
    'ORCHIDEE-CNP',
    'SDGVM'
]

sif_names = [
    'GOME'
]

fluxcom_x_vars = [
    'NEE',
    'GPP'
]

fluxcom_vars = [
    'NEE',
    'TER'
]

ERA5_vars = [
    'tp',
    't2m',
    'e',
    'swvl1',
    'u10',
    'v10',
    'sst'
]

MODIS_vars = [
    'lai',
    'fpar',
    'ndvi',
    'evi'
]

est_GPP = [
    'GOME',
    'GOSIF',
]

FLUXNET = [
    'AR-SLu',
    'AR-Vir',
    'BR-Sa1',
    'BR-Sa3',
    'CG-Tch',
    'GF-Guy',
    'GH-Ank',
    'MY-PSO',
    'PA-SPn',
    'PA-SPs',
    'SD-Dem',
    'SN-Dhr',
    'ZM-Mon'
]

months = ['Jan.', 'Feb.', 'Mar.', 'Apr.', 'May.', 'Jun.', 'Jul.', 'Aug.', 'Sep.', 'Oct.', 'Nov.', 'Dec.']