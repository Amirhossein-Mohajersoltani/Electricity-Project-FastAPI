import pandas as pd
from api.app.datafetch import Database
from api.app.models.schema import FilterDataWeeklyPeak, ResultDataWeeklyPeak
import jdatetime


def get_next_friday(date: jdatetime.date) -> jdatetime.date:
    """Get the next Friday from a given Jalali date."""
    days_until_friday = (6 - date.weekday()) % 7  # 4 = Friday in jdatetime
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

    # Check if DataFrame is empty or missing 'date' column
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
    filtered_df = df.sort_values('date')
    filtered_df.set_index('date', inplace=True)

    # Parse start and end dates as Jalali
    start_date = jdatetime.date.fromisoformat(data.start_date)
    end_date = jdatetime.date.fromisoformat(data.end_date)

    def generate_week_ranges(start_date: jdatetime.date, end_date: jdatetime.date):
        week_ranges = []
        current_start = start_date

        # Determine first week end (Friday)
        if current_start.weekday() == 6:  # If Friday
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
                # Filter data for the week (dates are in Jalali format as strings)
                window_data = fider_df[(fider_df.index >= w_start.strftime('%Y-%m-%d')) & 
                                     (fider_df.index < w_end.strftime('%Y-%m-%d'))]

                if not window_data.empty:
                    day_max = []
                    hour_columns = [f"H{i}" for i in range(1, 25)]
                    for i in range(len(window_data)):
                        row = window_data.iloc[i]
                        day_max.append(float(row[hour_columns].max()))

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

        return ResultDataWeeklyPeak(
            region_code=data.region_code,
            fidder_code=data.fidder_code,
            status="success",
            company_id=data.company_id,
            result=results
        )

    else:
        for week_num, (w_start, w_end) in enumerate(week_ranges, start=1):
            window_data = filtered_df[(filtered_df.index >= w_start.strftime('%Y-%m-%d')) & 
                                    (filtered_df.index < w_end.strftime('%Y-%m-%d'))]

            if not window_data.empty:
                day_max = []
                hour_columns = [f"H{i}" for i in range(1, 25)]
                for i in range(len(window_data)):
                    row = window_data.iloc[i]
                    day_max.append(float(row[hour_columns].max()))

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

        return ResultDataWeeklyPeak(
            region_code=data.region_code,
            fidder_code=data.fidder_code,
            status="success",
            company_id=data.company_id,
            result=results
        )