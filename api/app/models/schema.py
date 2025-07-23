from pydantic import BaseModel


class FilterDataDailyPeak(BaseModel):
    start_date: str
    end_date: str
    region_code: list
    fidder_code: list | None = None
    company_id : list | None = None


class ResultDataDailyPeak(BaseModel):
    region_code: list
    fidder_code: list | None = None
    status: str
    company_id : list | None = None
    result : list

class FilterDataDailyProfile(BaseModel):
    start_date: str
    end_date: str
    region_code: list
    fidder_code: list | None = None
    method : str
    company_id : list | None = None

class ResultDataDailyProfile(BaseModel):
    region_code: list
    fidder_code: list | None = None
    status: str
    method : str
    company_id : list | None = None
    result : list

class FilterDataWeeklyPeak(BaseModel):
    table: str | None = None
    start_date: str
    end_date: str
    region_code: list
    fidder_code: list | None = None
    company_id : list | None = None



class ResultDataWeeklyPeak(BaseModel):
    region_code: list
    fidder_code: list | None = None
    status: str
    company_id : list | None = None
    result : list

class FilterDataLongTerm(BaseModel):
    table: str | None = None
    year : list
    region_code: list
    fidder_code: list | None = None
    company_id : list | None = None


class ResultDataLongTerm(BaseModel):
    region_code: list
    fidder_code: list | None = None
    status: str
    company_id : list | None = None
    result : list

class FilterDataTariffShare(BaseModel):
    table: str | None = None
    start_date: str
    end_date: str
    region_code: list
    fidder_code: list | None = None
    company_id : list | None = None


class ResultDataTariffShare(BaseModel):
    region_code: list
    fidder_code: list | None = None
    status: str
    company_id : list | None = None
    result : list

class FilterDataToziBar(BaseModel):
    table: str | None = None
    start_date: str
    end_date: str
    region_code: list
    fidder_code: list | None = None
    company_id : list | None = None


class ResultDataToziBar(BaseModel):
    region_code: list
    fidder_code: list | None = None
    status: str
    company_id : list | None = None
    result : list

class FilterDataEnergyCompare(BaseModel):
    table: str | None = None
    year : list
    region_code: list
    fidder_code: list | None = None
    company_id : list | None = None


class ResultDataEnergyCompare(BaseModel):
    region_code: list
    fidder_code: list | None = None
    status: str
    company_id : list | None = None
    result : list

class FilterDataConsumptionReductionFactor(BaseModel):
    No_limitation_start_date: str
    No_limitation_end_date: str
    limitation_start_date : str
    limitation_end_date:str
    region_code: list
    fidder_code: list | None = None
    company_id : list | None = None

class ResultDataConsumptionReductionFactor(BaseModel):
    region_code: list
    fidder_code: list | None = None
    status: str
    company_id : list | None = None
    result : list

class FilterDataCompareEnergPCompany(BaseModel):
    table: str | None = None
    start_date: str
    end_date: str
    region_code: list
    fidder_code: list | None = None
    company_id : list | None = None
    window : int

class ResultDataCompareEnergPCompany(BaseModel):
    region_code: list
    fidder_code: list | None = None
    company_id : list | None = None
    status: str
    result : list
    