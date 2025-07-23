import pandas as pd
from datetime import timedelta
import jdatetime
from app.datafetch import Database
from app.models.schema import FilterDataCompareEnergPCompany , ResultDataCompareEnergPCompany

def compare_ernergic_for_private_company( data : FilterDataCompareEnergPCompany ) -> ResultDataCompareEnergPCompany :
    """
    Divide the input solar date range into batches of 'window' days,
    sum total consumption per batch, and return a summary DataFrame.
    """
    # Initialize database connection
    db = Database(
        host="178.236.33.157",
        port=3306,
        user="team_data",
        password="StrongPassword123!",
        database="electrodata"
    )

    # Extract filtered data
    df = db.extract_total_consumption(
        start_date=data.start_date,
        end_date=data.end_date,
        fidder_ids=data.fidder_code,
        areas=data.region_code,
        company_ids=data.company_id
    )

    if df.empty:
        return ResultDataCompareEnergPCompany(
                region_code = data.region_code,
                fidder_code=data.fidder_code,
                company_id=data.company_id,
                status ="Empty Data frame" ,
                result = []
        )

    # Step 2: Convert Jalali dates (string) to Gregorian dates
    df['gregorian_date'] = df['date'].apply(lambda x: jdatetime.date(*map(int, x.split('-'))).togregorian())
    df.sort_values('gregorian_date', inplace=True)

    # Determine the Gregorian start/end dates from input
    start_g = jdatetime.date(*map(int, data.start_date.split('-'))).togregorian()
    end_g = jdatetime.date(*map(int, data.end_date.split('-'))).togregorian()

    # Step 3: Iterate in window-sized chunks and sum consumption
    results = []
    current_start = start_g
    while current_start <= end_g:
        current_end = min(current_start + timedelta(days=data.window - 1), end_g)

        # Filter rows for the current window
        mask = (df['gregorian_date'] >= current_start) & (df['gregorian_date'] <= current_end)
        total = df.loc[mask, 'total_consumption'].sum()

        # Format window start/end as Jalali again for result clarity
        solar_start = jdatetime.date.fromgregorian(date=current_start).strftime('%Y-%m-%d')
        solar_end = jdatetime.date.fromgregorian(date=current_end).strftime('%Y-%m-%d')

        results.append({
            'window_start': solar_start,
            'window_end': solar_end,
            'total_consumption': total
        })

        current_start = current_end + timedelta(days=1)

    return  ResultDataCompareEnergPCompany(
                region_code = data.region_code,
                fidder_code=data.fidder_code,
                company_id=data.company_id,
                status ="success" ,
                result = results
        )
