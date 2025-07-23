from fastapi import APIRouter
import app.services
from app.models import schema


router = APIRouter()



@router.post("/daily-peak", response_model=schema.ResultDataDailyPeak)
def daily_peak(data: schema.FilterDataDailyPeak):
    return  app.services.analyze_max_daily_usage(data)



@router.post("/daily-profile", response_model=schema.ResultDataDailyProfile)
def daily_profile(data: schema.FilterDataDailyProfile):
    return app.services.analyze_24h_usage(data)




@router.post("/long-term", response_model=schema.ResultDataLongTerm)
def long_term(data: schema.FilterDataLongTerm):
    return app.services.long_term(data)


@router.post("/Load-continuity", response_model=schema.ResultDataToziBar)
def load_continuity(data: schema.FilterDataToziBar):
    return app.services.tozi_bar(data)

@router.post("/weekly-peak", response_model=schema.ResultDataWeeklyPeak)
def weekly_peak(data: schema.FilterDataWeeklyPeak):
    return app.services.analize_week(data)

@router.post("/consumption-distribution", response_model=schema.ResultDataTariffShare)
def consumption_distribution(data: schema.FilterDataTariffShare):
    return app.services.tariff_share_analyze(data)

@router.post("/compare-energetic", response_model=schema.ResultDataEnergyCompare)
def compare_energetic(data: schema.FilterDataEnergyCompare):
    return app.services.compare_energetic(data)

@router.post("/consumption-limitation", response_model=schema.ResultDataConsumptionReductionFactor)
def compare_energetic(data: schema.FilterDataConsumptionReductionFactor):
    return app.services.consumption_reduction_factor(data)


# Sample
# @router.post("/calculate", response_model=ResultData)
# def calculate(data: FilterData):
#     return calculate_consumption(data)