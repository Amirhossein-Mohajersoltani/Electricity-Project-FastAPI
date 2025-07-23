import pandas as pd
from api.app.datafetch import Database
import jdatetime
from datetime import datetime
from api.app.models.schema import FilterDataEnergyCompare , ResultDataEnergyCompare


def convert_to_gregorian(date_str):
    try:
        jalali_date = jdatetime.datetime.strptime(date_str, '%Y-%m-%d')
        gregorian_date = jalali_date.togregorian()
        return pd.Timestamp(gregorian_date)
    except Exception as e:
        print(f"خطا در تبدیل تاریخ: {date_str} - {e}")

def compare_energetic(data : FilterDataEnergyCompare)->ResultDataEnergyCompare:
    extractor = Database(
    host="178.236.33.157",
    port=3306,
    user="team_data",
    password="StrongPassword123!",
    database="electrodata"
    )

    df = extractor.extract_by_solar_years( years = data.year, fidder_ids=data.fidder_code  ,areas = data.region_code , company_ids=data.company_id)


    df['date'] = df['date'].astype(str)
    df['date'] = df['date'].apply(convert_to_gregorian)
    df['date'] = pd.to_datetime(df['date'])

    df['jalali_year'] = df['date'].apply(lambda d: jdatetime.date.fromgregorian(date=d).year)

    if data.fidder_code != None :
        energetic_compair = []
        for fidder in data.fidder_code:
            filtered_df = df[df['feeder code'] == fidder]
            for year in data.year:
                year = int(year)
                filtered_df_year = filtered_df[filtered_df['jalali_year'] == year]
                if not filtered_df_year.empty:
                    hour_columns = [f"H{i}" for i in range(1, 25)]
                    sum_year = []
                    for i in range(len(filtered_df_year)):
                        row = filtered_df_year.iloc[i]
                        sum_day = 0
                        for j in range(0 , len(hour_columns)):
                            sum_day = sum_day + float(row[hour_columns[j]])
                        sum_year.append(sum_day)
                    energetic_year = sum(sum_year)
                    energetic_fidder = {
                        'num_fidder' : fidder ,
                        'year' : year ,
                        'energetic' : energetic_year
                    }
                    energetic_compair.append(energetic_fidder)
                else:
                    energetic_fidder = {
                        'num_fidder' : fidder ,
                        'year' : year ,
                        'energetic' : 0
                    }
                    energetic_compair.append(energetic_fidder.copy())
        return ResultDataEnergyCompare (
                region_code = data.region_code ,
                fidder_code= data.fidder_code ,
                status = "success" , 
                result = energetic_compair
        )
    else :
        energetic_compair = []
        for year in data.year:
            year = int(year)
            filtered_df_year = df[df['jalali_year'] == year]
            hour_columns = [f"H{i}" for i in range(1, 25)]
            sum_year = []
            for i in range(len(filtered_df_year)):
                row = filtered_df_year.iloc[i]
                sum_day = 0
                for j in range(0 , len(hour_columns)):
                    sum_day = sum_day + float(row[hour_columns[j]])
                sum_year.append(sum_day)
            energetic_year = sum(sum_year)
            g_date = datetime(year, 6, 1)
            shamsi_year = jdatetime.date.fromgregorian(date=g_date)

            energetic_fidder = {
                'section' : data.region_code ,
                'year' : year ,
                'energetic' : energetic_year
            }
            energetic_compair.append(energetic_fidder.copy())
        return ResultDataEnergyCompare (
                region_code = data.region_code ,
                fidder_code= data.fidder_code ,
                status = "success" ,
                company_id = data.company_id,
                result = energetic_compair
        )

