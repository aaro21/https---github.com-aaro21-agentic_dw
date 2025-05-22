import pyodbc
import pandas as pd
from openpyxl.utils import get_column_letter  # ✅ This was missing!

# Configuration
server = 'YOUR_SERVER_NAME'
database = 'YOUR_DATABASE_NAME'
schema = 'YOUR_SCHEMA_NAME'
excel_output = 'views_top5_export.xlsx'

# Connection string for SQL Server with trusted settings
conn_str = (
    f"DRIVER={{ODBC Driver 18 for SQL Server}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    f"Trusted_Connection=yes;"
    f"TrustServerCertificate=yes;"
)

# Establish connection
conn = pyodbc.connect(conn_str)
conn.setencoding(encoding='utf-8')
conn.setdecoding(pyodbc.SQL_CHAR, encoding='utf-8')
conn.setdecoding(pyodbc.SQL_WCHAR, encoding='utf-8')

# Fetch list of views
views_query = f"""
SELECT TABLE_NAME
FROM INFORMATION_SCHEMA.VIEWS
WHERE TABLE_SCHEMA = '{schema}'
"""
views_df = pd.read_sql(views_query, conn)
views = views_df['TABLE_NAME'].tolist()

# Create Excel writer
with pd.ExcelWriter(excel_output, engine='openpyxl', datetime_format='yyyy-mm-dd hh:mm:ss') as writer:
    for view in views:
        try:
            # Get datetimeoffset columns from metadata
            col_type_query = f"""
            SELECT c.name
            FROM sys.columns c
            JOIN sys.views v ON c.object_id = v.object_id
            JOIN sys.types t ON c.user_type_id = t.user_type_id
            WHERE v.name = '{view}' AND SCHEMA_NAME(v.schema_id) = '{schema}' AND t.name = 'datetimeoffset'
            """
            dt_offset_cols = pd.read_sql(col_type_query, conn)['name'].tolist()

            # Get all columns
            col_query = f"SELECT TOP 0 * FROM [{schema}].[{view}]"
            cursor = conn.cursor()
            cursor.execute(col_query)
            columns = [col[0] for col in cursor.description]

            # Build SELECT with datetimeoffset CASTs
            select_clauses = [
                f"CAST([{col}] AS datetime) AS [{col}]" if col in dt_offset_cols else f"[{col}]"
                for col in columns
            ]
            query = f"SELECT TOP 5 {', '.join(select_clauses)} FROM [{schema}].[{view}]"

            # Fetch and fix data
            df = pd.read_sql(query, conn)

            for col in df.columns:
                if pd.api.types.is_integer_dtype(df[col]) and df[col].max() > 1e11:
                    df[col] = df[col].astype(str)

            # Write to Excel
            sheet_name = view[:31]  # Excel max sheet name length
            df.to_excel(writer, sheet_name=sheet_name, index=False)

            # Auto-size columns
            worksheet = writer.sheets[sheet_name]
            for i, col in enumerate(df.columns, 1):
                max_len = max(df[col].astype(str).map(len).max(), len(col))
                worksheet.column_dimensions[get_column_letter(i)].width = max_len + 2

            print(f"✅ Exported top 5 from {schema}.{view}")

        except Exception as e:
            print(f"⚠️ Skipping {schema}.{view} due to error: {e}")

conn.close()
print(f"\n✅ Export complete. File saved as '{excel_output}'")
