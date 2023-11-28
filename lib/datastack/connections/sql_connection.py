import pandas as pd


class SQLConnection:
    def __init__(self, params):
        import sqlalchemy

        self.params = params
        self.url = sqlalchemy.engine.URL.create(
            "mssql+pyodbc",
            host=params.get("server"),
            database=params.get("database"),
            query=dict(
                driver="ODBC Driver 17 for SQL Server", trusted_connection="Yes"
            ),
        )

        self.engine = sqlalchemy.create_engine(self.url)
        # self.engine = sqlalchemy.create_engine('mssql+pyodbc://@' + params['server'] + '/' + params['database'] + '?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server')

    def query(self, sql_query):
        return pd.read_sql(sql_query, self.engine)
