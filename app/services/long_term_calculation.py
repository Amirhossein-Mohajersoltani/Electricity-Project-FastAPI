from app.datafetch import Database
import pandas as pd
import jdatetime
from app.models.schema import FilterDataLongTerm, ResultDataLongTerm

def long_term(data: FilterDataLongTerm) -> ResultDataLongTerm:
    """
    Compute weekly maximums where weeks end on Fridays in the Iranian calendar.
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

    result = {}

    # Process each year separately
    for year in sorted(df['year'].unique()):
        # Filter only data of this year
        df_year = df[df['year'] == year].copy()

        # Create a mapping from dates to rows
        date_to_rows = df_year.groupby('jalali_date')

        # Start from Farvardin 1
        current_date = jdatetime.date(int(year), 1, 1)  # Convert year to Python int
        last_date = jdatetime.date(int(year), 12, 29)  # Default to Esfand 29

        # # Check if the year is a leap year (Esfand 30)
        # if jdatetime.date(int(year), 12, 30).is_valid():
        #     last_date = jdatetime.date(int(year), 12, 30)

        week_num = 1
        weeks_data = []

        while current_date <= last_date:
            # Compute end of week (Friday)
            if current_date.weekday() == 6:  # If current_date is Friday, end the week on the same day
                week_end = current_date
            else:
                days_to_friday = (6 - current_date.weekday()) % 7  # Friday is 4
                week_end = current_date + jdatetime.timedelta(days=days_to_friday)

            # Ensure we don’t go past year end
            if week_end > last_date:
                week_end = last_date

            # Extract rows between current_date and week_end
            dates_in_week = [d for d in date_to_rows.groups.keys() if current_date <= d <= week_end]
            
            if dates_in_week:
                week_rows = df_year[df_year['jalali_date'].isin(dates_in_week)]

                week_rows['max_in_day'] = week_rows[hour_cols].max(axis=1)
                max_value = week_rows['max_in_day'].max()

                weeks_data.append({
                    'start date': current_date.strftime('%Y-%m-%d'),
                    'end date': week_end.strftime('%Y-%m-%d'),
                    'week': week_num,
                    'amount': max_value if not pd.isna(max_value) else None
                })

            # Move to the next week (Saturday after this Friday)
            current_date = week_end + jdatetime.timedelta(days=1)
            week_num += 1

        result[year] = weeks_data

    output = [{str(year): weeks} for year, weeks in result.items()]
    return ResultDataLongTerm(
        region_code=data.region_code,
        fidder_code=data.fidder_code,
        company_id=data.company_id,
        status="success",
        result=output
    )