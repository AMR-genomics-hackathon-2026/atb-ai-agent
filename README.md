# An Agentic System for AllTheBacteria
This is a simple AI agent to analyze MLST data produced from AllTheBacteria. 

To run: 
1. Clone the repository.

```
git clone https://github.com/AMR-genomics-hackathon-2026/atb-ai-agent.git
cd atb-ai-agent
```

2. Setup the environment.  
Create a virtual environment and install dependencies:  
```
uv sync
```
3. Configure API keys.  
Anthropic: [Anthropic API Key](console.anthropic.com)  
NCBI: [NCBI API Key](https://www.ncbi.nlm.nih.gov/datasets/docs/v2/api/api-keys/)  
Create a ```.env``` in the project root:
```
ANTHROPIC_API_KEY=your_api_key_here
NCBI_API_KEY=your_api_key_here
```
4. Run the ATB AI Agent!
```uv run main.py```
