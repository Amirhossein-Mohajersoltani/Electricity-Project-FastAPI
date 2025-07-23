Base url: http://178.236.33.157:8000
date type: Shamsi



1- پیک روزانه

request type: POST
rout: /daily-peak

params: 
    start_date: str
    end_date: str
    region_code: list
    fidder_code: list 
Result:
	{
		'region_code': [10], 
		'fidder_code': [20, 30], 
		'status': 'success', 
		'result': [
			{'date': '1401-01-01', 'amount': 2.72}, 
			{'date': '1401-01-02', 'amount': 2.72}, 
			{'date': '1401-01-03', 'amount': 2.778}
		]
	}






2- پروفیل روزانه

request type: POST
rout: /daily-profile

Params:
    start_date: str
    end_date: str
    region_code: list
    fidder_code: list
    method : str = "max" | "mean"

Result:
	{
		'region_code': [10], 
		'fidder_code': [20, 30], 
		'status': 'success', 
		'method': 'mean', 
		'result': [
			{'hour': 'H1', 'amount': 1.325}, 
			{'hour': 'H2', 'amount': 1.197}, 
			{'hour': 'H3', 'amount': 1.046}
		]
	}






3- پیک هفتگی

request type: POST
rout: /weekly-peak

Params: 
    start_date: str
    end_date: str
    region_code: list
    fidder_code: list

Result:
	{
		'region_code': [10], 
		'fidder_code': [20, 30], 
		'status': 'success', 
		'result': [
			{'start_date': '1401/01/01', 'end_date': '1401/01/07', 'max_week': 2.778, 'num_week': 1}, 
			{'start_date': '1401/01/08', 'end_date': '1401/01/14', 'max_week': 2.585, 'num_week': 2}, 
			{'start_date': '1401/01/15', 'end_date': '1401/01/21', 'max_week': 2.534, 'num_week': 3}
		]
	}





4- بلند مدت

request type: POST
rout: /long-term


Params: 
    year : list
    region_code: list
    fidder_code: list

Result:
	{
		'region_code': [10], 
		'fidder_code': [20, 30], 
		'status': 'success', 
		'result': [
			{
				'1401': [
					{'start date': '1401-01-01', 'end date': '1401-01-07', 'week': 1, 'amount': 2}, 
					{'start date': '1401-01-08', 'end date': '1401-01-14', 'week': 2, 'amount': 2}, 
					{'start date': '1401-01-15', 'end date': '1401-01-21', 'week': 3, 'amount': 2}
				]
			}
		]
	}








5- تداوم بار

request type: POST
rout: /Load-continuity

Params:
    start_date: str
    end_date: str
    region_code: list
    fidder_code: list


Result:
	{
		'region_code': [10], 
		'fidder_code': [20, 30], 
		'status': 'success', 
		'result': [
			{
				'fidder': 20, 
				'start_date': '1401/01/01', 
				'end_date': '1401/01/31', 
				'sort_value': [
					2.908, 2.838, 2.808, 2.786, 2.778, 2.769, 2.76, 2.758, 2.752, 2.745, 2.735, 2.732, 2.723, 2.723, 2.72, 2.72, 2.713, 2.71, 2.707, ...
				]
			}, 
			{
				'fidder': 30, 
				'start_date': '1401/01/01', 
				'end_date': '1401/01/31', 
				'sort_value': [
					2.817, 2.623, 2.466, 2.407, 2.393, 2.38, 2.364, 2.362, 2.359, 2.284, 2.248, 2.246, 2.239, 2.222, 2.221, 2.21, 2.199, 2.185, 2.185, ...
				]
			}
		]
	}


6- مقایسه انژی

request type: POST
rout: /compare-energetic

Params:
    year : list
    region_code: list
    fidder_code: list


Result:
	{
		'region_code': [10], 
		'fidder_code': [20, 30], 
		'status': 'success', 
		'result': [
			{'num_fidder': 20, 'year': 1401, 'energetic': 6362.036000000002}, 
			{'num_fidder': 30, 'year': 1401, 'energetic': 3763.7029999999995}
		]
	}


7- سهم تعرفه ها

request type: POST
rout: /consumption-distribution

Params:
    start_date: str
    end_date: str
    region_code: list
    fidder_code: list


Result:
	{
		'region_code': [10], 
		'fidder_code': [20, 30], 
		'status': 'success', 
		'result': [
			{
				'domestic': 40.0, 
				'industrial': 25.0, 
				'agriculture': 10.0, 
				'commercial': 12.0, 
				'lighting': 10.0, 
				'administrative': 3.0
			}
		]
	}