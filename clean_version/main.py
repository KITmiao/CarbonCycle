from data_processor import (
    process_trendy_nbp,
    process_trendy_ra,
    process_trendy_rh,
    process_trendy_gpp,
    process_trendy_fLuc,
    process_trendy_fFire,
    process_trendy_lai,
    ProcessTM5GOSAT,
    ProcessTRENDY,
    ProcessTM5IS,
    ProcessFire,
    ProcessFluxcom,
    ProcessFluxcomX,
    ProcessTM5Prior,
    ProcessLai,
    ProcessSIF,
    ProcessERA5,
    ProcessOCO,
    ProcessOCO2MIP,
    ProcessSIFbaseGPP,
    ProcessNIRvGPP,
    ProcessAll
)
import settings
if settings.check_study_region:
    import plots.latlon_studyregion
if settings.check_study_region_glb:
    import plots.latlon_studyregion_glbview
if settings.check_concentration:
    import plots.plot_concentration
if settings.check_invs:
    import plots.plot_invs
if settings.check_invs_2region_diff:
    import plots.plot_2region_diff
if settings.check_IAV:
    import plots.plot_IAV
if settings.check_IAV_nbps:
    import plots.plot_IAV_nbps
if settings.check_hovmollers:
    import plots.hovmoller
if settings.check_obs_spatial:
    import plots.latlon_gosat_points
if settings.check_prior:
    import plots.plot_prior
if settings.check_gosat:
    import plots.plot_GOSAT
if settings.check_insitu:
    import plots.plot_Insitu
if settings.check_fires_role:
    import plots.compare_fire
if settings.check_individual_trendy:
    import plots.trendy_indiv
if settings.check_individual_nbp:
    import plots.plot_trendy_nbp_compo
if settings.check_nbp:
    import plots.plot_NBP
if settings.check_nee:
    import plots.plot_NEE
if settings.check_meteo:
    import plots.plot_meteo
if settings.check_gpp_with_gosif_gpp:
    import plots.plot_GPPGOSIF
if settings.check_gpp_with_nirv_gpp:
    import plots.plot_NIRvGPP
if settings.check_invs_spatial:
    import plots.latlon_inversions
if settings.check_invs_insitu_spatial:
    import plots.latlon_inversion_insitu
if settings.check_invs_gosat_spatial:
    import plots.latlon_inversion_gosat
if settings.check_invs_fire_spatial:
    import plots.latlon_inversions_fire
if settings.check_fire_spatial:
    import plots.latlon_fire
if settings.check_meteo_spatial:
    import plots.latlon_meteo
if settings.check_SV_meteo_spatial:
    import plots.latlon_SV_era5
if settings.check_SV_invs_gosat_spatial:
    import plots.latlon_SV_invs
if settings.check_SV_trendy_spatial:
    import plots.latlon_SV_trendy
if settings.check_SV_gpp_spatial:
    import plots.latlon_SV_gpps
if settings.check_elevation_spatial:
    import plots.latlon_elevation
if settings.check_gpp_spatial:
    import plots.latlon_gpps
if settings.check_ter_spatial:
    import plots.latlon_re_TER
if settings.check_soc_spatial:
    import plots.latlon_soc
if settings.check_trendy_nbp_spatial:
    import plots.latlon_trendy_nbp
if settings.check_trendy_gpp_spatial:
    import plots.latlon_trendy_gpp
if settings.check_pearson_gpp_meteo:
    import plots.pearson_gpp_meteo
if settings.check_pearson_ter_meteo:
    import plots.pearson_ter_meteo
if settings.scatter_MAP_MAT_NBP:
    import statistical.scatter_meteo_nbp
if settings.scatter_MAP_MAT_GPP:
    import statistical.scatter_meteo_gpp
if settings.nbp_with_PCFpcs:
    import statistical.pc_with_PCFnbp
