import pandas as pd
from app.datafetch import Database
import jdatetime
from app.models.schema import FilterDataToziBar , ResultDataToziBar

def tozi_bar(data: FilterDataToziBar) -> ResultDataToziBar:
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

    start_time = pd.Timestamp(jdatetime.date.fromisoformat(data.start_date).togregorian())
    end_time = pd.Timestamp(jdatetime.date.fromisoformat(data.end_date).togregorian())

    result = []

    def get_hourly_data_with_context(df_subset):
        hourly_data = []
        hour_columns = [f"H{i}" for i in range(1, 25)]
        for i in range(len(df_subset)):
            row = df_subset.iloc[i]
            date = row['date']
            for j, col in enumerate(hour_columns, start=1):
                try:
                    value = float(row[col])
                    hourly_data.append({
                        'value': value,
                        'hour': j,
                        'date': date
                    })
                except (ValueError, TypeError):
                    continue  # Skip invalid or missing values
        # Sort descending by value
        return sorted(hourly_data, key=lambda x: x['value'], reverse=True)

    try:
        start_jalali = jdatetime.date.fromgregorian(date=start_time.date()).strftime('%Y/%m/%d')
        end_jalali = jdatetime.date.fromgregorian(date=end_time.date()).strftime('%Y/%m/%d')
    except Exception:
        start_jalali = str(start_time.date())
        end_jalali = str((end_time - pd.Timedelta(days=1)).date())

    if data.fidder_code is not None:
        for fidder in data.fidder_code:
            fidder_filter = df[df['feeder code'] == fidder]
            sort_value_list = get_hourly_data_with_context(fidder_filter)

            tozi_bar_dict = {
                'fidder': fidder,
                'start_date': start_jalali,
                'end_date': end_jalali,
                'sort_value': sort_value_list
            }
            result.append(tozi_bar_dict)
    else:
        sort_value_list = get_hourly_data_with_context(df)

        tozi_bar_dict = {
            'area': data.region_code,
            'start_date': start_jalali,
            'end_date': end_jalali,
            'sort_value': sort_value_list
        }
        result.append(tozi_bar_dict)

    return ResultDataToziBar(
        fidder_code=data.fidder_code,
        region_code=data.region_code,
        status="success",
        company_id=data.company_id,
        result=result
    )