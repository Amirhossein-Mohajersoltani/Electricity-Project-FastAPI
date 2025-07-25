# Electricity-Project-FastAPI

# 📘 API Documentation for Load Management System

**Base URL:** `http://178.236.33.157:8000`
**Date Format:** Shamsi (e.g., `1401-01-01` or `1401/01/01`)
**Request Method:** `POST`
**Company IDs:**

* `3`: Distribution Company
* `101`: Flour Company

---

## 1. 📈 Daily Peak

**Endpoint:** `/daily-peak`
**Description:** Returns the maximum load value for each day within the specified period.

**Request Parameters:**

| Parameter     | Type     | Required | Description                |
| ------------- | -------- | -------- | -------------------------- |
| `start_date`  | `string` | Yes      | Start date (Shamsi format) |
| `end_date`    | `string` | Yes      | End date (Shamsi format)   |
| `region_code` | `list`   | Yes      | List of region codes       |
| `fidder_code` | `list`   | No       | List of feeder codes       |
| `company_id`  | `list`   | Yes      | List with company ID       |

**Sample Response:**

```json
{
  "region_code": [10],
  "fidder_code": [20, 30],
  "company_id": [3],
  "status": "success",
  "result": [
    {"date": "1401-01-01", "amount": 2.72},
    {"date": "1401-01-02", "amount": 2.72},
    {"date": "1401-01-03", "amount": 2.778}
  ]
}
```

---

## 2. 📊 Daily Profile

**Endpoint:** `/daily-profile`
**Description:** Returns hourly load profile (mean or max) for the specified period.

**Request Parameters:**

| Parameter     | Type     | Required | Description                |
| ------------- | -------- | -------- | -------------------------- |
| `start_date`  | `string` | Yes      | Start date (Shamsi format) |
| `end_date`    | `string` | Yes      | End date (Shamsi format)   |
| `region_code` | `list`   | Yes      | List of region codes       |
| `fidder_code` | `list`   | No       | List of feeder codes       |
| `method`      | `string` | Yes      | `"mean"` or `"max"`        |
| `company_id`  | `list`   | Yes      | List with company ID       |

**Sample Response:**

```json
{
  "region_code": [10],
  "fidder_code": [20, 30],
  "status": "success",
  "method": "mean",
  "company_id": [3],
  "result": [
    {"hour": "H1", "amount": 1.325},
    {"hour": "H2", "amount": 1.197},
    {"hour": "H3", "amount": 1.046}
  ]
}
```

---

## 3. 📅 Weekly Peak

**Endpoint:** `/weekly-peak`
**Description:** Returns the maximum weekly load for each week in the specified period.

**Request Parameters:** Same as Daily Peak.

**Sample Response:**

```json
{
  "region_code": [10],
  "fidder_code": [20, 30],
  "company_id": [3],
  "status": "success",
  "result": [
    {
      "start_date": "1401/01/01",
      "end_date": "1401/01/07",
      "max_week": 2.778,
      "num_week": 1
    },
    {
      "start_date": "1401/01/08",
      "end_date": "1401/01/14",
      "max_week": 2.585,
      "num_week": 2
    }
  ]
}
```

---

## 4. 🗓️ Long-Term Analysis

**Endpoint:** `/long-term`
**Description:** Returns weekly load data for specified years.

**Request Parameters:**

| Parameter     | Type   | Required | Description            |
| ------------- | ------ | -------- | ---------------------- |
| `year`        | `list` | Yes      | List of years (Shamsi) |
| `region_code` | `list` | Yes      | List of region codes   |
| `fidder_code` | `list` | No       | List of feeder codes   |
| `company_id`  | `list` | Yes      | List with company ID   |

**Sample Response:**

```json
{
  "region_code": [10],
  "fidder_code": [20, 30],
  "status": "success",
  "company_id": [3],
  "result": [
      {"start date": "1401-01-01", "end date": "1401-01-07", "week": 1, "amount": 2},
      {"start date": "1401-01-08", "end date": "1401-01-14", "week": 2, "amount": 2}
  ]
}
```

---

## 5. 🔁 Load Continuity

**Endpoint:** `/Load-continuity`
**Description:** Analyzes load continuity over the specified period.

**Request Parameters:** Same as Daily Peak.

**Sample Response:**

```json
{
  "region_code": [10],
  "fidder_code": [20, 30],
  "status": "success",
  "company_id": [3],
  "result": [
    {
      "fidder": [20, 30],
      "region": [10],
      "start_date": "1401/01/01",
      "end_date": "1401/01/31",
      "sort_value": [
        {"value": 9.764, "hour": 13, "date": "1401-03-16"},
        {"value": 9.339, "hour": 12, "date": "1401-03-16"}
      ]
    }
  ]
}
```

---

## 6. ⚖️ Energetic Comparison

**Endpoint:** `/compare-energetic`
**Description:** Compares energy consumption across different years.

**Request Parameters:** Same as Long-Term Analysis.

**Sample Response:**

```json
{
  "region_code": [10],
  "fidder_code": [20, 30],
  "status": "success",
  "company_id": [3],
  "result": [
    {"num_fidder": 20, "year": 1401, "energetic": 6362.036},
    {"num_fidder": 30, "year": 1401, "energetic": 3763.703}
  ]
}
```

---

## 7. 🧾 Consumption Distribution by Tariff

**Endpoint:** `/consumption-distribution`
**Description:** Returns the percentage distribution of consumption across different tariffs for the specified period.

**Request Parameters:** Same as Daily Peak.

**Sample Response:**

```json
{
  "region_code": [10],
  "fidder_code": [20, 30],
  "status": "success",
  "result": [
    {
      "domestic": 40.0,
      "industrial": 25.0,
      "agriculture": 10.0,
      "commercial": 12.0,
      "lighting": 10.0,
      "administrative": 3.0
    }
  ]
}
```

---

## 8. ⛔ Consumption Limitation Analysis

**Endpoint:** `/consumption-limitation-analysis`
**Description:** Compares consumption during limited and unlimited periods.

**Request Parameters:**

| Parameter                  | Type     | Required | Description                                 |
| -------------------------- | -------- | -------- | ------------------------------------------- |
| `region_code`              | `list`   | Yes      | List of region codes                        |
| `fidder_code`              | `list`   | No       | List of feeder codes                        |
| `limitation_start_date`    | `string` | Yes      | Start date of limitation period (Shamsi)    |
| `limitation_end_date`      | `string` | Yes      | End date of limitation period (Shamsi)      |
| `No_limitation_start_date` | `string` | Yes      | Start date of no-limitation period (Shamsi) |
| `No_limitation_end_date`   | `string` | Yes      | End date of no-limitation period (Shamsi)   |
| `company_id`               | `list`   | Yes      | List with company ID                        |

**Sample Response:**

```json
{
  "region_code": [1, 2, 3],
  "fidder_code": [1, 137, 142, 149],
  "status": "success",
  "company_id": [3],
  "result": [
    {
      "fidder_code": 1,
      "consumption_reduction_factor": 1.1394,
      "start_date_limit": "1401-04-01",
      "end_date_limit": "1408-05-31",
      "start_date_no_limit": "1401-07-01",
      "end_date_no_limit": "1405-08-30"
    }
  ]
}
```

---

> **Note:** All endpoints require `Content-Type: application/json` header and accept only `POST` requests.
