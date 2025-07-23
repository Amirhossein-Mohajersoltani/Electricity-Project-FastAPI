from api.app.datafetch import Database
from api.app.models.schema import FilterDataTariffShare , ResultDataTariffShare


def tariff_share_analyze(data : FilterDataTariffShare)-> ResultDataTariffShare:
    extractor = Database(
        host="178.236.33.157",
        port=3306,
        user="team_data",
        password="StrongPassword123!",
        database="electrodata"
    )

    df = extractor.extract_share_consumption(
        start_date=data.start_date,
        end_date=data.end_date,
        areas=data.region_code,
        fidder_ids=data.fidder_code,
        company_ids=data.company_id
    )

    if df.empty or 'date' not in df.columns or 'total_consumption' not in df.columns:
        return ResultDataTariffShare (
                region_code = data.region_code ,
                fidder_code= data.fidder_code ,
                status = "failed" , 
                result = []
        )

    categories = ['domestic', 'industrial', 'agriculture', 'commercial', 'lighting', 'administrative']

    # Calculate actual usage for each category
    for category in categories:
        df[category + '_usage'] = df[category] * df['total_consumption']


    # Sum total usage per category
    total_usages = {cat: df[cat + '_usage'].sum() for cat in categories}

    grand_total = sum(total_usages.values())


    # Calculate percentage share per category
    result = [
        {cat: float(round((usage / grand_total) * 100, 2))
        for cat, usage in total_usages.items()}
    ]

    return ResultDataTariffShare (
                region_code = data.region_code ,
                fidder_code= data.fidder_code ,
                status = "success" , 
                company_id = data.company_id,
                result = result
        )

