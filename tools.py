import pandas as pd
from claude_agent_sdk import tool
from typing import Any

'''
Add the full name of the genus and species so that it's not just the scheme name. This data is formatted specific way
so that the agent can fully interpret the bacterial name and the sequence type.
'''
@tool("mlst_scheme", "Assess the MLST results and map the name of scheme to make the ultimate file containing the GENUS_SPECIES column.", {"content": str})
async def mlst_scheme(args: dict[str, Any]) -> dict[str, Any]:
    mlst_data = pd.read_csv("data/mlst_processed_all_samples.tsv", sep="\t")
    scheme_species_map = pd.read_csv("data/scheme_species_map_combined.csv")
    scheme_species_map = scheme_species_map.rename(columns={"SCHEME": "mlst_scheme", "SPECIES": "species"})

    # merge scheme_species_map with MLST data from ATB
    new_mlst_data = (mlst_data
                     .merge(scheme_species_map, on="mlst_scheme")
                     .rename(columns={"mlst_st": "mlst_sequence_type"})
                     )
    
    # written out MLST sequence type name 
    file_path = "outputs/mlst_data.csv"
    new_mlst_data.to_csv(file_path, index=None)
                
    return {
        "content": [{
            "type": "text",
            "text": f"Data successfully saved to {file_path}."
        }]
    }

