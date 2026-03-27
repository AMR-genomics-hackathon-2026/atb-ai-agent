import pandas as pd
from claude_agent_sdk import tool
from typing import Any
import subprocess

'''
Add the full name of the genus and species so that it's not just the scheme name. This data is formatted specific way
so that the agent can fully interpret the bacterial name and the sequence type.
'''

@tool("run_mlst", "Given a genome, run the MLST tool.", {"content": str, "filename": str})
async def run_mlst(args: dict[str, Any]) -> dict[str, Any]:
    filename = args["filename"]  
    # running mlst on command line  
    result = subprocess.run(
        ["mlst", filename],
        capture_output=True,
        text=True
    )
    
    return {
        "stdout": result.stdout,
        "stderr": result.stderr,
        "returncode": result.returncode
    }
    