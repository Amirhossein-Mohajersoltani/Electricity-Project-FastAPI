import mysql.connector
import pandas as pd
import jdatetime


class Database:
    def __init__(self, host, port, user, password, database):
        self.db_config = {
            "host": host,
            "port": port,
            "user": user,
            "passwd": password,
            "database": database
        }
        self.connection = None
        self.cursor = None

    def connect(self):
        self.connection = mysql.connector.connect(**self.db_config)
        self.cursor = self.connection.cursor(dictionary=True)

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

    @staticmethod
    def solar_to_gregorian(solar_str):
        """Convert Solar (Jalali) date string YYYY-MM-DD to Gregorian date object."""
        year, month, day = map(int, solar_str.split('-'))
        return jdatetime.date(year, month, day).togregorian()


    def extract(self, start_date, end_date, areas=None, fidder_ids=None, company_ids=None):
        """Extract power consumption data with optional filters for multiple areas, feeder_ids, and company_ids."""
        g_start = self.solar_to_gregorian(start_date)
        g_end = self.solar_to_gregorian(end_date)

        self.connect()

        # Base query
        select_clause = """
            SELECT DISTINCT
                p.feeder_id AS `feeder code`,
                p.date AS `date`,
                p.H1, p.H2, p.H3, p.H4, p.H5, p.H6,
                p.H7, p.H8, p.H9, p.H10, p.H11, p.H12,
                p.H13, p.H14, p.H15, p.H16, p.H17, p.H18,
                p.H19, p.H20, p.H21, p.H22, p.H23, p.H24
        """
        from_clause = " FROM power_consumption_data p"
        where_clause = " WHERE p.date BETWEEN %s AND %s"
        params = [g_start, g_end]


        if areas:
            select_clause += ", f.area AS `area`"
            from_clause += " JOIN feeders f ON p.feeder_id = f.feeder_name"
            placeholders = ', '.join(['%s'] * len(areas))
            where_clause += f" AND f.area IN ({placeholders})"
            params.extend(areas)

        if fidder_ids:
            placeholders = ', '.join(['%s'] * len(fidder_ids))
            where_clause += f" AND p.feeder_id IN ({placeholders})"
            params.extend(fidder_ids)

        if company_ids:
            placeholders = ', '.join(['%s'] * len(company_ids))
            where_clause += f" AND p.distribution_id IN ({placeholders})"
            params.extend(company_ids)

        query = select_clause + from_clause + where_clause

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        df = pd.DataFrame(rows)

        if not df.empty:
            df['date'] = pd.to_datetime(df['date']).apply(
                lambda x: jdatetime.date.fromgregorian(date=x).strftime('%Y-%m-%d')
            )


        self.close()
        print(df.head(5))
        return df

    def extract_by_solar_years(self, years, areas=None, fidder_ids=None, company_ids=None):
        """
        Extract power consumption data for given Jalali years (e.g., ["1401", "1402"]),
        optionally filtered by areas, feeder_ids, and company_ids.
        """
        self.connect()
        table = "power_consumption_data"

        select_clause = """
            SELECT DISTINCT
                p.feeder_id AS `feeder code`,
                p.date AS `date`,
                p.H1, p.H2, p.H3, p.H4, p.H5, p.H6,
                p.H7, p.H8, p.H9, p.H10, p.H11, p.H12,
                p.H13, p.H14, p.H15, p.H16, p.H17, p.H18,
                p.H19, p.H20, p.H21, p.H22, p.H23, p.H24
        """
        from_clause = f" FROM {table} p"
        where_clause = " WHERE YEAR(p.date) IN ("
        params = []

        # Convert Jalali years to Gregorian years
        gregorian_years = []
        for year in years:
            jalali_date = jdatetime.date(int(year), 1, 1)
            gregorian_date = jalali_date.togregorian()
            gregorian_years.append(gregorian_date.year)
        placeholders = ', '.join(['%s'] * len(gregorian_years))
        where_clause += placeholders + ")"
        params.extend(gregorian_years)

        if areas:
            select_clause += ", f.area AS `area`"
            from_clause += " JOIN feeders f ON p.feeder_id = f.feeder_name"
            placeholders = ', '.join(['%s'] * len(areas))
            where_clause += f" AND f.area IN ({placeholders})"
            params.extend(areas)

        if fidder_ids:
            placeholders = ', '.join(['%s'] * len(fidder_ids))
            where_clause += f" AND p.feeder_id IN ({placeholders})"
            params.extend(fidder_ids)

        if company_ids:
            placeholders = ', '.join(['%s'] * len(company_ids))
            where_clause += f" AND p.distribution_id IN ({placeholders})"
            params.extend(company_ids)

        query = select_clause + from_clause + where_clause

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        df = pd.DataFrame(rows)

        if not df.empty:
            df['date'] = pd.to_datetime(df['date']).apply(
                lambda x: jdatetime.date.fromgregorian(date=x).strftime('%Y-%m-%d')
            )
        print(df.head(5))

        self.close()
        return df

    def extract_share_consumption(self, start_date, end_date, areas=None, fidder_ids=None, company_ids=None):
        """Extract power consumption data of different share usage with optional filters for areas, feeder_ids, and company_ids."""

        g_start = self.solar_to_gregorian(start_date)
        g_end = self.solar_to_gregorian(end_date)

        self.connect()
        table = "power_consumption_data"

        select_clause = """
            SELECT DISTINCT
                p.feeder_id AS `feeder code`,
                p.date AS `date`,
                p.domestic, p.industrial, p.agriculture,
                p.commercial, p.lighting, p.administrative,
                p.total_consumption
        """
        from_clause = f" FROM {table} p"
        where_clause = " WHERE p.date BETWEEN %s AND %s"
        params = [g_start, g_end]

        if areas:
            select_clause += ", f.area AS `area`"
            from_clause += " JOIN feeders f ON p.feeder_id = f.feeder_name"
            placeholders = ', '.join(['%s'] * len(areas))
            where_clause += f" AND f.area IN ({placeholders})"
            params.extend(areas)

        if fidder_ids:
            placeholders = ', '.join(['%s'] * len(fidder_ids))
            where_clause += f" AND p.feeder_id IN ({placeholders})"
            params.extend(fidder_ids)

        if company_ids:
            placeholders = ', '.join(['%s'] * len(company_ids))
            where_clause += f" AND p.distribution_id IN ({placeholders})"
            params.extend(company_ids)

        query = select_clause + from_clause + where_clause

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        df = pd.DataFrame(rows)

        if not df.empty:
            df['date'] = pd.to_datetime(df['date']).apply(
                lambda x: jdatetime.date.fromgregorian(date=x).strftime('%Y-%m-%d')
            )

        self.close()
        return df

    def extract_total_consumption(self, start_date, end_date, areas=None, fidder_ids=None, company_ids=None):
        """Extract total power consumption with optional filters for areas, feeder_ids, and company_ids."""

        g_start = self.solar_to_gregorian(start_date)
        g_end = self.solar_to_gregorian(end_date)

        self.connect()
        table = "power_consumption_data"

        select_clause = """
            SELECT DISTINCT
                p.feeder_id AS `feeder code`,
                p.date AS `date`,
                p.total_consumption
        """
        from_clause = f" FROM {table} p"
        where_clause = " WHERE p.date BETWEEN %s AND %s"
        params = [g_start, g_end]

        if areas:
            select_clause += ", f.area AS `area`"
            from_clause += " JOIN feeders f ON p.feeder_id = f.feeder_name"
            placeholders = ', '.join(['%s'] * len(areas))
            where_clause += f" AND f.area IN ({placeholders})"
            params.extend(areas)

        if fidder_ids:
            placeholders = ', '.join(['%s'] * len(fidder_ids))
            where_clause += f" AND p.feeder_id IN ({placeholders})"
            params.extend(fidder_ids)

        if company_ids:
            placeholders = ', '.join(['%s'] * len(company_ids))
            where_clause += f" AND p.distribution_id IN ({placeholders})"
            params.extend(company_ids)

        query = select_clause + from_clause + where_clause

        self.cursor.execute(query, params)
        rows = self.cursor.fetchall()
        df = pd.DataFrame(rows)

        if not df.empty:
            df['date'] = pd.to_datetime(df['date']).apply(
                lambda x: jdatetime.date.fromgregorian(date=x).strftime('%Y-%m-%d')
            )

        self.close()
        
        return df
