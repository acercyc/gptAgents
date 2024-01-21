# %%
import io
import contextlib
import sys
from langchain.tools import BaseTool, StructuredTool, tool
from typing import List

@tool
def execute_python_code(code) -> str:
    ''' Run Python code and capture stdout, stderr, and returned value'''
    # Create a StringIO stream to capture output
    output_stream = io.StringIO()

    # Redirect stdout to the stream
    with contextlib.redirect_stdout(output_stream):
        try:
            # Execute the given code
            exec(code)
        except Exception as e:
            # Print any errors to the output stream
            print(f"Error: {e}", file=sys.stderr)

    # Return the content of the stream
    return output_stream.getvalue()

