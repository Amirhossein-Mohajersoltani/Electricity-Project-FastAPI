import numpy as np
from app.datafetch import Database
from app.models.schema import FilterDataDailyPeak, ResultDataDailyPeak



def analyze_max_daily_usage(data: FilterDataDailyPeak)-> ResultDataDailyPeak:
    # Load filtered data from extract_power_data (returns Jalali date as string in 'YYYY-MM-DD')
    extractor = Database(
    host="178.236.33.157",
    port=3306,
    user="team_data",
    password="StrongPassword123!",
    database="electrodata"
    )

    df = extractor.extract(start_date=data.start_date, end_date=data.end_date, area=data.region_code, feeder_id=data.fidder_code, table=data.table)

    if df.empty or 'date' not in df.columns:
        return ResultDataDailyPeak (
        region_code= data.region_code,
        fider_code= data.fidder_code ,
        status= "Failed" ,
        result = {}
    )

    # Extract month and day from 'date' column in format 'YYYY-MM-DD'
    df['ماه'] = df['date'].str.split('-').str[1].astype(int)
    df['روز'] = df['date'].str.split('-').str[2].astype(int)

    # Calculate روز سال (day of year) in Jalali calendar
    month_lengths = [31]*6 + [30]*5 + [29]
    cumulative_days = [0] + list(np.cumsum(month_lengths[:-1]))
    df['روز سال'] = df.apply(lambda row: cumulative_days[row['ماه'] - 1] + row['روز'], axis=1)

    # Aggregate maximum hourly usage per day
    hour_cols = [f'H{i}' for i in range(1, 25) if f'H{i}' in df.columns]
    daily_sum = df.groupby('روز سال')[hour_cols].sum()
    daily_peak = daily_sum.max(axis=1).dropna()

    # Return result as dictionary {روز سال: ماکسیمم مصرف}
    result = {int(day): float(val) for day, val in daily_peak.items()}
    return ResultDataDailyPeak (
        region_code= data.region_code,
        fider_code= data.fider_code ,
        status= "success" ,
        result = result
    )

