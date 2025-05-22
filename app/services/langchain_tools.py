from langchain.tools import Tool
from app.services.schema_explorer import list_columns

def describe_table_tool(table_name: str) -> str:
    try:
        columns = list_columns(table_name)
        col_names = [col["name"] for col in columns]
        return f"Table '{table_name}' has columns: {col_names}"
    except Exception as e:
        return f"Error retrieving table '{table_name}': {e}"

describe_table = Tool.from_function(
    func=describe_table_tool,
    name="DescribeTable",
    description="Use this to describe the structure of a table by its name.",
)
