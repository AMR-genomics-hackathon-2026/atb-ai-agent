# An Agentic System for AllTheBacteria
This is a simple AI agent to analyze MLST data produced from AllTheBacteria. 

To run: 
## 1. Clone the repository.

```
git clone https://github.com/AMR-genomics-hackathon-2026/atb-ai-agent.git
cd atb-ai-agent
```

## 2. Setup the environment.  
Create a virtual environment and install dependencies:  
```
uv sync
```
## 3. Configure API keys.  
[Anthropic API Key](console.anthropic.com)  
[NCBI API Key](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/api/api-keys/)  
Create a ```.env``` in the project root:
```
ANTHROPIC_API_KEY=your_api_key_here
NCBI_API_KEY=your_api_key_here
```
## 4. Run the ATB AI Agent!  
```uv run main.py```  
Simply add the MLST processed data from ATB and ask the agent to format it for you (e.g., "In the data folder, format the ATB MLST data". As a result, the agent should reformat the data (making it easier for it to understand sequence type and the bacteria species names)). This is important to give the agent more context; as the way the MLST data's original format says "mlst_st" and "mlst_scheme". To be clear with the agent, I have developed a tool to format it such that it is clear that "st" refers to sequence_type and scheme refers to the full bacteria name.  

You can follow up and ask other questions regarding MLST data (e.g., what are the top 10 most reported genome sequences from which bacteria?). And also make connections to the literature (hence the addition of PubMed MCP)!

For example, you could ask: "Format the ATB MLST data in the data folder. Using the formatted data, can you extract the most relevant publications to a recent outbreak for "Staphylococcus aureus" with "ST8"? Search PubMed."