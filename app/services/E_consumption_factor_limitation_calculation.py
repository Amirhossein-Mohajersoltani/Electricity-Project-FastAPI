from app.datafetch import Database
from app.models.schema import FilterDataConsumptionReductionFactor, ResultDataConsumptionReductionFactor
from persiantools.jdatetime import JalaliDate

def consumption_reduction_factor(
data : FilterDataConsumptionReductionFactor
)-> ResultDataConsumptionReductionFactor:
    """
    Calculates the consumption reduction factor for feeders
    comparing periods with and without consumption limitations.

    Parameters:
        region_code (list[str], optional): region codes to filter.
        fider_code (list[str], optional): feeder codes to filter.
        No_limitation_start_date (str): start date of no-limit period (YYYY-MM-DD).
        No_limitation_end_date (str): end date of no-limit period (YYYY-MM-DD).
        limitation_start_date (str): start date of limitation period (YYYY-MM-DD).
        limitation_end_date (str): end date of limitation period (YYYY-MM-DD).

    Returns:
        List[dict]: List of dictionaries, each with:
            - start date limit
            - end date limit
            - start date no limit
            - end date no limit
            - feeder code
            - consumption reduction factor
    """

    # Connect to the database
    extractor = Database(
        host="178.236.33.157",
        port=3306,
        user="team_data",
        password="StrongPassword123!",
        database="electrodata"
    )
    
    # --- Fetch data for limitation period
    df_limitation = extractor.extract_total_consumption(
        start_date=data.limitation_start_date, 
        end_date=data.limitation_end_date,
        areas=data.region_code,
        fidder_ids=data.fidder_code,
        company_ids=data.company_id
    )
    
    if df_limitation.empty:
        return ResultDataConsumptionReductionFactor (
        region_code= data.region_code,
        fidder_code= data.fidder_code ,
        status= "No data found for limitation period." ,
        company_id = data.company_id ,
        result = {}
    )
    
    # --- Fetch data for no-limitation period
    df_nolimitation = extractor.extract_total_consumption(
        start_date=data.No_limitation_start_date, 
        end_date=data.No_limitation_end_date,
        areas=data.region_code,
        fidder_ids=data.fidder_code,
        company_ids=data.company_id
    )
    
    if df_nolimitation.empty:
        return ResultDataConsumptionReductionFactor (
        region_code= data.region_code,
        fidder_code= data.fidder_code ,
        status= "No data found for no-limitation period." ,
        company_id = data.company_id ,
        result = {}
    )
    
    # --- Calculate mean consumption in both periods
    mean_limit = df_limitation.groupby("feeder code")["total_consumption"].mean()
    mean_nolimit = df_nolimitation.groupby("feeder code")["total_consumption"].mean()

    
    # Find common feeder codes present in both
    common_feeders = mean_limit.index.intersection(mean_nolimit.index)
    
    if len(common_feeders) == 0:
        return ResultDataConsumptionReductionFactor (
        region_code= data.region_code,
        fidder_code= data.fidder_code ,
        status= "No common fidder codes found between limitation and no-limitation periods" ,
        company_id = data.company_id ,
        result = {}
    )
    
    results = []
    
    for feeder in common_feeders:
        mean_limit_value = mean_limit.loc[feeder]
        mean_nolimit_value = mean_nolimit.loc[feeder]
        
        # Handle division by zero
        if mean_nolimit_value == 0:
            reduction_factor = None
            print(f"Skipping fidder {feeder}: mean consumption during no-limitation period is zero.")
        else:
            reduction_factor = mean_limit_value / mean_nolimit_value
        
        result = {
            "start date limit": data.limitation_start_date,
            "end date limit": data.limitation_end_date,
            "start date no limit": data.No_limitation_start_date,
            "end date no limit": data.No_limitation_end_date,
            "fidder code": feeder,
            "consumption reduction factor": float(reduction_factor)
        }
        
        results.append(result)
    
    return ResultDataConsumptionReductionFactor (
        region_code= data.region_code,
        fidder_code= data.fidder_code ,
        status= "success" ,
        company_id = data.company_id ,
        result = results
    )

# print(consumption_reduction_factor(fider_code=[1,4,10,13] , No_limitation_start_date="1401-07-01", No_limitation_end_date="1401-08-30" , 
#                              limitation_start_date="1401-04-01", limitation_end_date="1401-05-31"))