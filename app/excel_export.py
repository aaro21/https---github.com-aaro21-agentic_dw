import pyodbc
import pandas as pd

# Configuration
server = 'YOUR_SERVER_NAME'
database = 'YOUR_DATABASE_NAME'
schema = 'YOUR_SCHEMA_NAME'
excel_output = 'views_top5_export.xlsx'

# Connect to SQL Server using ODBC 18, trusted connection, and trust server certificate
conn_str = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"Trusted_Connection=yes;"
    f"TrustServerCertificate=yes;"
)
conn = pyodbc.connect(conn_str)

# Get list of views in the specified schema
views_query = f"""
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.VIEWS
WHERE TABLE_SCHEMA = '{schema}'
"""
views_df = pd.read_sql(views_query, conn)
views = views_df['TABLE_NAME'].tolist()

# Create a Pandas Excel writer
with pd.ExcelWriter(excel_output, engine='openpyxl', datetime_format='yyyy-mm-dd hh:mm:ss') as writer:
    for view in views:
        query = f"SELECT TOP 5 * FROM [{schema}].[{view}]"
        try:
            df = pd.read_sql(query, conn)
            df.to_excel(writer, sheet_name=view[:31], index=False)  # Sheet name limit
            print(f"✅ Exported top 5 from {schema}.{view}")
        except Exception as e:
            print(f"⚠️ Skipping {schema}.{view} due to error: {e}")

conn.close()
print(f"\n✅ Export complete. File saved as '{excel_output}'")
