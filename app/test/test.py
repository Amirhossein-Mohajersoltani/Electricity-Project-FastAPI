# Daily Peak
# from app.models.schema import FilterDataDailyPeak
# from app.services import analyze_max_daily_usage
#
# data = FilterDataDailyPeak(
#     start_date="1401-01-01",
#     end_date="1403-04-10",
#     region_code=[1,10],
#     fidder_code = [1,20,30,50,100],
#     company_id = [3]
# )
# result = analyze_max_daily_usage(data)
# print(result)

# --------------------------------------------------------------

# Daily Profile
# from app.models.schema import FilterDataDailyProfile
# from app.services import analyze_24h_usage
#
# data = FilterDataDailyProfile(
#     start_date="1401-01-01",
#     end_date="1403-01-31",
#     region_code=[1,10],
#     fidder_code = [1,137,142,149],
#     method="max", # Also max
#     company_id = [3]
# )
#
# result = analyze_24h_usage(data)
# print(result)

# --------------------------------------------------------------

# Compare Energetic
# from app.models.schema import FilterDataEnergyCompare
# from app.services import compare_energetic
#
# data = FilterDataEnergyCompare(
#     year=[1401,1402],
#     region_code=[1,2,3],
#     fidder_code = [1,137,142,149],
#     company_id = [3],
# )
#
# result = compare_energetic(data)
# print(result)

# --------------------------------------------------------------

# # Long Term
# from app.models.schema import FilterDataLongTerm
# from app.services import long_term
#
# data = FilterDataLongTerm(
#     year=[1401,1402,1403 ],
#     region_code=[1,2,3],
#     fidder_code = [1,137,142,149],
#     company_id = [3]
# )
#
# result = long_term(data)
# print(result)

# --------------------------------------------------------------

# consumption distribution
# from api.app.models.schema import FilterDataTariffShare
# from api.app.services import tariff_share_analyze
#
# data = FilterDataTariffShare(
#     start_date="1401-01-01",
#     end_date="1401-01-31",
#     region_code=[13,12],
#     fidder_code = [454],
#     company_id = [3]
# )
#
# result = tariff_share_analyze(data)
# print(result)

# --------------------------------------------------------------

## Load continuity
from app.models.schema import FilterDataToziBar
from app.services import tozi_bar

data = FilterDataToziBar(
    start_date="1401-01-01",
    end_date="1401-04-31",
    region_code=[1],
    # fidder_code=[1],
    company_id = [3]
)
#
result = tozi_bar(data)
# print(result.region_code)
# print(result.fidder_code)
print(len(result.result[0]['sort_value']))
# print(result.result[0]["area"])


# print(result)

# --------------------------------------------------------------

# Weekly Peak
# from app.models.schema import FilterDataWeeklyPeak
# from app.services import analize_week
#
# data = FilterDataWeeklyPeak(
#     start_date="1401-01-01",
#     end_date="1407-01-31",
#     region_code=[1],
#     fidder_code = [1],
#     company_id=[3]
# )
#
# result = analize_week(data)
# print(result)
#
#








# ------------------------------------------------
# from app.models.schema import FilterDataConsumptionReductionFactor
# from app.services import consumption_reduction_factor
#
# data = FilterDataConsumptionReductionFactor(
#     fidder_code=[1,137,142,149],
#     region_code=[1,2,3],
#     No_limitation_start_date="1401-07-01",
#     No_limitation_end_date="1405-08-30",
#     limitation_start_date="1401-04-01",
#     limitation_end_date="1408-05-31",
#     company_id = [3]
# )
#
# result = consumption_reduction_factor(data)
# print(result.model_dump())


# -------------------------------------------------
# # compare energy for private company
# from api.app.models.schema import FilterDataCompareEnergPCompany
# from api.app.services.energy_comparision_Pcompany_calculation import compare_ernergic_for_private_company

# data = FilterDataCompareEnergPCompany(
#     start_date="1403-01-01",
#     end_date="1403-04-10",
#     region_code=[1],
#     fidder_code = [1],
#     company_id = [101],
#     window=15
# )

# result = compare_ernergic_for_private_company(data)
# print(result)




# ------------------------------------------------

# from api.app.datafetch import Database
#
#
#
# db = Database(
#         host="178.236.33.157",
#         port=3306,
#         user="team_data",
#         password="StrongPassword123!",
#         database="electrodata"
#     )
#
#
# df = db.extract(
#     start_date= "1401-01-01",
#     end_date= "1401-01-31",
#     areas=[2, 6],
#     fidder_ids=[12]
# )
#
# print(df)

#        feeder code        date     H1     H2  ...    H22    H23    H24  area
# 0               12  1401-01-01  3.278  2.895  ...  3.503  3.501  3.431     2
# 1               12  1401-01-02  0.000  3.257  ...  3.635  3.634  3.558     2
# 2               12  1401-01-03  3.384  3.263  ...  3.668  3.711  3.577     2
# 3               12  1401-01-04  3.433  3.043  ...  3.606  3.675  3.635     2
# 4               12  1401-01-05  3.409  3.069  ...  3.556  3.596  3.502     2
# ...            ...         ...    ...    ...  ...    ...    ...    ...   ...
# 28081          357  1401-01-27  3.149  2.778  ...  4.136  3.931  3.626     6
# 28082          357  1401-01-28  3.147  2.749  ...  4.076  3.875  3.521     6
# 28083          357  1401-01-29  3.051  2.659  ...  4.131  3.909  3.527     6
# 28084          357  1401-01-30  3.066  2.676  ...  4.094  3.913  3.591     6
# 28085          357  1401-01-31  3.155  2.720  ...  4.097  3.870  3.615     6
#
# [28086 rows x 27 columns]

