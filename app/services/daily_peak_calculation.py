from app.datafetch import Database
from app.models.schema import FilterDataDailyPeak, ResultDataDailyPeak
from persiantools.jdatetime import JalaliDate



def analyze_max_daily_usage(data: FilterDataDailyPeak)-> ResultDataDailyPeak:
    # Load filtered data from extract_power_data (returns Jalali date as string in 'YYYY-MM-DD')
    extractor = Database(
    host="178.236.33.157",
    port=3306,
    user="team_data",
    password="StrongPassword123!",
    database="electrodata"
    )


    df = extractor.extract(start_date=data.start_date, end_date=data.end_date, areas=data.region_code, fidder_ids=data.fidder_code , company_ids=data.company_id)


    if df.empty or 'date' not in df.columns:
        return ResultDataDailyPeak (
        region_code= data.region_code,
        fidder_code= data.fidder_code ,
        status= "Failed" ,
        result = {}
    )

    # Ensure we only have valid hour columns
    hour_cols = [f'H{i}' for i in range(1, 25) if f'H{i}' in df.columns]

    # Group by 'date' and find the max for each hour across all rows of that day
    grouped = df.groupby('date')[hour_cols].max()

    # Then take the maximum across the 24 hours for each day
    grouped['amount'] = grouped.max(axis=1)

    # Reset index to get 'date' as a column again
    grouped = grouped.reset_index()

    # Convert Gregorian to Jalali if needed
    result = []
    for _, row in grouped.iterrows():
        try:
            jdate = JalaliDate.strptime(row['date'], "%Y-%m-%d").isoformat()
        except Exception as e:
            print(e)
            jdate = row['date']  # fallback
        result.append({
            'date': jdate,
            'amount': float(row['amount'])
        })
    return ResultDataDailyPeak (
        region_code= data.region_code,
        fidder_code= data.fidder_code ,
        status= "success" ,
        company_id = data.company_id,
        result = result
    )

