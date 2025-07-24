import pandas as pd
from app.datafetch import Database
from app.models.schema import FilterDataWeeklyPeak, ResultDataWeeklyPeak
import jdatetime


def get_next_friday(date: jdatetime.date) -> jdatetime.date:
    """Get the next Friday from a given Jalali date."""
    days_until_friday = (6 - date.weekday()) % 7
    return date + jdatetime.timedelta(days=days_until_friday)


def analize_week(data: FilterDataWeeklyPeak) -> ResultDataWeeklyPeak:
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
        fidder_ids=data.fidder_code,
        areas=data.region_code,
        company_ids=data.company_id
    )

    if df.empty or 'date' not in df.columns:
        return ResultDataWeeklyPeak(
            region_code=data.region_code,
            fidder_code=data.fidder_code,
            status="error",
            company_id=data.company_id,
            result=[],
        )

    # Ensure dates are in Jalali format (YYYY-MM-DD)
    df['date'] = df['date'].astype(str)
    df = df.sort_values('date')

    # 🧠 Create full Jalali date range
    g_start = jdatetime.date.fromisoformat(data.start_date).togregorian()
    g_end = jdatetime.date.fromisoformat(data.end_date).togregorian()
    full_dates = pd.date_range(start=g_start, end=g_end, freq='D')
    full_jalali_dates = [jdatetime.date.fromgregorian(date=d).strftime('%Y-%m-%d') for d in full_dates]
    full_df = pd.DataFrame({'date': full_jalali_dates})

    # 🧩 Merge and fill missing dates
    merged_df = pd.merge(full_df, df, on='date', how='left')

    # Fill missing H1–H24 with zeros
    hour_columns = [f"H{i}" for i in range(1, 25)]
    for col in hour_columns:
        merged_df[col] = merged_df[col].fillna(0)

    # Fill 'feeder code' if needed
    if 'feeder code' in merged_df.columns:
        merged_df['feeder code'] = merged_df['feeder code'].fillna(method='ffill').fillna(method='bfill')

    # Use the merged and completed DataFrame
    filtered_df = merged_df.set_index('date')

    # Parse start and end dates
    start_date = jdatetime.date.fromisoformat(data.start_date)
    end_date = jdatetime.date.fromisoformat(data.end_date)

    def generate_week_ranges(start_date: jdatetime.date, end_date: jdatetime.date):
        week_ranges = []
        current_start = start_date

        if current_start.weekday() == 6:
            first_week_end = current_start
        else:
            first_week_end = get_next_friday(current_start)

        current_end = min(first_week_end + jdatetime.timedelta(days=1), end_date + jdatetime.timedelta(days=1))
        week_ranges.append((current_start, current_end))

        current_start = current_end
        while current_start < end_date:
            current_end = min(current_start + jdatetime.timedelta(days=7), end_date + jdatetime.timedelta(days=1))
            week_ranges.append((current_start, current_end))
            current_start = current_end

        return week_ranges

    fiders_week_max = []
    week_ranges = generate_week_ranges(start_date, end_date)

    if data.fidder_code is not None:
        for fider in data.fidder_code:
            fider_df = filtered_df[filtered_df['feeder code'] == fider]

            for week_num, (w_start, w_end) in enumerate(week_ranges, start=1):
                window_data = fider_df[(fider_df.index >= w_start.strftime('%Y-%m-%d')) & 
                                       (fider_df.index < w_end.strftime('%Y-%m-%d'))]

                if not window_data.empty:
                    day_max = [float(row[hour_columns].max()) for _, row in window_data.iterrows()]

                    start_jalali = w_start.strftime('%Y/%m/%d')
                    end_jalali = (w_end - jdatetime.timedelta(days=1)).strftime('%Y/%m/%d')
                    key = f"{start_jalali} - {end_jalali}"

                    week_max = {
                        'num_week': week_num,
                        'date': key,
                        'start_date': start_jalali,
                        'end_date': end_jalali,
                        'max_week': max(day_max) if day_max else None
                    }

                    fiders_week_max.append(week_max)

        results_df = pd.DataFrame(fiders_week_max)
        if not results_df.empty:
            idx = results_df.groupby('date')['max_week'].idxmax()
            max_per_date_df = results_df.loc[idx, ['start_date', 'end_date', 'max_week', 'num_week']].reset_index(drop=True)
            results = max_per_date_df.to_dict(orient='records')
        else:
            results = []

    else:
        for week_num, (w_start, w_end) in enumerate(week_ranges, start=1):
            window_data = filtered_df[(filtered_df.index >= w_start.strftime('%Y-%m-%d')) & 
                                      (filtered_df.index < w_end.strftime('%Y-%m-%d'))]

            if not window_data.empty:
                day_max = [float(row[hour_columns].max()) for _, row in window_data.iterrows()]

                start_jalali = w_start.strftime('%Y/%m/%d')
                end_jalali = (w_end - jdatetime.timedelta(days=1)).strftime('%Y/%m/%d')
                key = f"{start_jalali} - {end_jalali}"

                week_max = {
                    'num_week': week_num,
                    'date': key,
                    'start_date': start_jalali,
                    'end_date': end_jalali,
                    'max_week': float(max(day_max)) if day_max else None
                }

                fiders_week_max.append(week_max)

        results_df = pd.DataFrame(fiders_week_max)
        if not results_df.empty:
            idx = results_df.groupby('date')['max_week'].idxmax()
            max_per_date_df = results_df.loc[idx, ['start_date', 'end_date', 'max_week', 'num_week']].reset_index(drop=True)
            results = max_per_date_df.to_dict(orient='records')
        else:
            results = []

    return ResultDataWeeklyPeak(
        region_code=data.region_code,
        fidder_code=data.fidder_code,
        status="success",
        company_id=data.company_id,
        result=results
    )
