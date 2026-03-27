# An Agentic System for AllTheBacteria
This is a simple AI agent to analyze data from ATB. The tasks that can be done include querying the ATB CLI, performing a PubMed search, and also performing MLST analysis.  

To run: 
## 1. Clone the repository

```
git clone https://github.com/AMR-genomics-hackathon-2026/atb-ai-agent.git
cd atb-ai-agent
```

## 2. Setup the environment   
Create a virtual environment and install dependencies:  
```
uv sync
```

## 3. Install CLIs
[AllTheBacteria Claude CLI](https://github.com/AMR-genomics-hackathon-2026/atb-cli-claude)  
[MLST CLI](https://github.com/tseemann/mlst)  

## 4. Configure API keys  
[Anthropic API Key](console.anthropic.com) -- for using the AI agent (Claude's Haiku model).  
[NCBI API Key](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/api/api-keys/) -- for performing PubMed searches.  

Create a ```.env``` in the project root:
```
ANTHROPIC_API_KEY=your_api_key_here
NCBI_API_KEY=your_api_key_here
```

## 5. Run the ATB AI Agent  
```uv run main.py```  

Example prompts:  
- Can you run MLST on the fasta sequence in the folder data?
- Can you extract the 5 relevant publications from the past year to a recent outbreak for "Staphylococcus aureus" with "ST8"? Search PubMed. And save the output of these papers to the outputs folder.