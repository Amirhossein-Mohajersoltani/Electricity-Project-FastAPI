from app.datafetch import Database
import pandas as pd
import numpy as np
import jdatetime
from app.models.schema import FilterDataLongTerm, ResultDataLongTerm

def long_term(data: FilterDataLongTerm) -> ResultDataLongTerm:
    """
    Compute weekly maximums where weeks end on Fridays in the Iranian calendar.
    Fills missing dates with dummy rows (H1–H24 = 0).
    """
    extractor = Database(
        host="178.236.33.157",
        port=3306,
        user="team_data",
        password="StrongPassword123!",
        database="electrodata"
    )

    df = extractor.extract_by_solar_years(
        years=data.year,
        fidder_ids=data.fidder_code,
        areas=data.region_code,
        company_ids=data.company_id
    )

    if df.empty:
        return ResultDataLongTerm(
            region_code=data.region_code,
            fidder_code=data.fidder_code,
            status="failed",
            result=[]
        )

    df['jalali_date'] = df['date'].apply(
        lambda x: jdatetime.date(*map(int, x.split('-')))
    )
    df['year'] = df['jalali_date'].apply(lambda d: d.year)

    hour_cols = [f'H{i}' for i in range(1, 25)]

    output = []

    for year in sorted(df['year'].unique()):
        df_year = df[df['year'] == year].copy()

        # Generate full Jalali date range for the year
        start_date = jdatetime.date(int(year), 1, 1)
        end_date = jdatetime.date(int(year), 12, 29)
        try:
            # Check for leap year
            _ = jdatetime.date(int(year), 12, 30)
            end_date = jdatetime.date(int(year), 12, 30)
        except ValueError:
            pass

        full_dates = [start_date + jdatetime.timedelta(days=i)
                      for i in range((end_date - start_date).days + 1)]
        full_df = pd.DataFrame({'jalali_date': full_dates})

        # Merge with existing data
        df_merged = pd.merge(full_df, df_year, on='jalali_date', how='left')

        # Fill missing H1–H24 with zeros
        for h in hour_cols:
            df_merged[h] = df_merged[h].fillna(0)

        # Add missing metadata if needed
        for col in ['fidder_code', 'region_code', 'company_id']:
            if col in df_merged.columns:
                df_merged[col] = df_merged[col].fillna(method='ffill').fillna(method='bfill')

        df_merged['year'] = year

        # Group by weeks (ending on Fridays)
        week_num = 1
        current_date = start_date

        while current_date <= end_date:
            # Find end of current week (Friday)
            days_to_friday = (6 - current_date.weekday()) % 7
            week_end = current_date + jdatetime.timedelta(days=days_to_friday)
            if week_end > end_date:
                week_end = end_date

            mask = (df_merged['jalali_date'] >= current_date) & (df_merged['jalali_date'] <= week_end)
            week_rows = df_merged[mask].copy()

            week_rows['max_in_day'] = week_rows[hour_cols].max(axis=1)
            max_value = week_rows['max_in_day'].max()

            # Convert amount to float if it's a NumPy type
            amount = float(max_value) if not pd.isna(max_value) else None

            output.append({
                'start date': current_date.strftime('%Y-%m-%d'),
                'end date': week_end.strftime('%Y-%m-%d'),
                'week': week_num,
                'amount': amount
            })

            current_date = week_end + jdatetime.timedelta(days=1)
            week_num += 1

    return ResultDataLongTerm(
        region_code=data.region_code,
        fidder_code=data.fidder_code,
        company_id=data.company_id,
        status="success",
        result=output
    )
