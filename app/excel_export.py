import pyodbc
import pandas as pd

# Configuration
server = 'YOUR_SERVER_NAME'
database = 'YOUR_DATABASE_NAME'
schema = 'YOUR_SCHEMA_NAME'
excel_output = 'views_top5_export.xlsx'

# Use trusted connection and certificate, ODBC 18
conn_str = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"Trusted_Connection=yes;"
    f"TrustServerCertificate=yes;"
)

# Connect with decoding workaround
conn = pyodbc.connect(conn_str)
conn.setencoding(encoding='utf-8')
conn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')

# Get list of views
views_query = f"""
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.VIEWS
WHERE TABLE_SCHEMA = '{schema}'
"""
views_df = pd.read_sql(views_query, conn)
views = views_df['TABLE_NAME'].tolist()

# Create Excel file
with pd.ExcelWriter(excel_output, engine='openpyxl', datetime_format='yyyy-mm-dd hh:mm:ss') as writer:
    for view in views:
        try:
            # Fetch column metadata
            cursor = conn.cursor()
            cursor.execute(f"SELECT TOP 0 * FROM [{schema}].[{view}]")
            columns = [column[0] for column in cursor.description]
            types = [column[1] for column in cursor.description]

            # Build SELECT query with CAST for datetimeoffset
            select_clauses = []
            for col, sqltype in zip(columns, types):
                if sqltype == -155:  # datetimeoffset
                    select_clauses.append(f"CAST([{col}] AS datetime) AS [{col}]")
                else:
                    select_clauses.append(f"[{col}]")

            select_clause = ", ".join(select_clauses)
            query = f"SELECT TOP 5 {select_clause} FROM [{schema}].[{view}]"

            # Execute and write to Excel
            df = pd.read_sql(query, conn)
            df.to_excel(writer, sheet_name=view[:31], index=False)
            print(f"✅ Exported top 5 from {schema}.{view}")
        except Exception as e:
            print(f"⚠️ Skipping {schema}.{view} due to error: {e}")

conn.close()
print(f"\n✅ Export complete. File saved as '{excel_output}'")
