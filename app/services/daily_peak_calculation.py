from app.datafetch import Database
from app.models.schema import FilterDataDailyPeak, ResultDataDailyPeak
from persiantools.jdatetime import JalaliDate
import pandas as pd

def analyze_max_daily_usage(data: FilterDataDailyPeak) -> ResultDataDailyPeak:
    # Load filtered data
    extractor = Database(
        host="178.236.33.157",
        port=3306,
        user="team_data",
        password="StrongPassword123!",
        database="electrodata"
    )

    df = extractor.extract(
        start_date=data.start_date,
        end_date=data.end_date,
        areas=data.region_code,
        fidder_ids=data.fidder_code,
        company_ids=data.company_id
    )

    if df.empty or 'date' not in df.columns:
        return ResultDataDailyPeak(
            region_code=data.region_code,
            fidder_code=data.fidder_code,
            status="Failed",
            result={}
        )

    # Valid hour columns
    hour_cols = [f'H{i}' for i in range(1, 25)]
    for col in hour_cols:
        if col not in df.columns:
            df[col] = 0

    # Generate full Jalali date range
    start = JalaliDate.strptime(data.start_date, "%Y-%m-%d")
    end = JalaliDate.strptime(data.end_date, "%Y-%m-%d")
    all_dates = [(start + pd.Timedelta(days=i)).strftime('%Y-%m-%d') for i in range((end - start).days + 1)]

    # Find missing dates
    existing_dates = set(df['date'])
    missing_dates = [d for d in all_dates if d not in existing_dates]

    # Create dummy rows with 0s
    dummy_rows = pd.DataFrame([{
        'date': d, **{f'H{i}': 0 for i in range(1, 25)}
    } for d in missing_dates])

    # Append to original df
    df = pd.concat([df, dummy_rows], ignore_index=True)


    # Group by date and calculate max per hour, then daily max
    grouped = df.groupby('date')[hour_cols].max()
    grouped['amount'] = grouped.max(axis=1)
    grouped = grouped.reset_index()

    # No need for Gregorian → Jalali conversion now (dates are already in Jalali)
    result = [
        {'date': row['date'], 'amount': float(row['amount'])}
        for _, row in grouped.iterrows()
    ]

    return ResultDataDailyPeak(
        region_code=data.region_code,
        fidder_code=data.fidder_code,
        company_id=data.company_id,
        status="success",
        result=result
    )
