from api.app.datafetch import Database
from api.app.models.schema import FilterDataDailyProfile , ResultDataDailyProfile



def analyze_24h_usage(data: FilterDataDailyProfile)-> ResultDataDailyProfile:

    # Initialize database connection
    db = Database(
        host="178.236.33.157",
        port=3306,
        user="team_data",
        password="StrongPassword123!",
        database="electrodata"
    )

    # Extract filtered data
    df = db.extract(
        start_date=data.start_date,
        end_date=data.end_date,
        fidder_ids=data.fidder_code,
        areas=data.region_code,
        company_ids=data.company_id
    )
    if df.empty:
        return ResultDataDailyProfile (
        region_code= data.region_code,
        fidedr_code= data.fidder_code ,
        status= "Failed" ,
        method=data.method,
        result = []
    )

    # Compute hourly summary
    hour_cols = [f'H{i}' for i in range(1, 25)]

    if data.method == 'max':
        hour_values = df[hour_cols].max()
    else:  # method == 'mean'
        hour_values = df[hour_cols].mean()

    result = [{'hour': hour, 'amount': float(round(hour_values[hour], 3))} for hour in hour_cols]

    return ResultDataDailyProfile (
        region_code= data.region_code,
        fidder_code= data.fidder_code ,
        status= "success" ,
        method=data.method,
        company_id = data.company_id,
        result = result
    )