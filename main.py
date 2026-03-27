"""
AllTheBacteria (ATB) AI Agent System

The ATB agent is designed to assess the latest release of MLST data from ATB, while supplementing any data with PubMed literature.
For example by retrieving the top 10 sequence type and bacterial species, you can ask for 5 publications regarding outbreaks for
Staphylococcus aureus and sequence type 8. The agent will format the MLST report data to include full bacterial species names (acquired from
the MLST tool scheme) and then it will use the PubMed MCP to retrieve any papers.

For more details, see: https://docs.claude.com/en/api/agent-sdk/subagents
"""

from claude_agent_sdk import ClaudeSDKClient, ClaudeAgentOptions, AgentDefinition, tool, create_sdk_mcp_server
import os
from rich import print
from rich.console import Console
from cli_tools import parser, print_rich_message, parse_and_print_message, get_user_input
from tools import run_mlst
from dotenv import load_dotenv
load_dotenv()

async def main():
    console = Console()
    args = parser.parse_args()
    
    # create MCP server for MLST_agent tools 
    mlst_tools_server = create_sdk_mcp_server(
        name="mlst_tools",
        version="1.0.0",
        tools=[run_mlst]
    )
    
    options = ClaudeAgentOptions(
        model=args.model,
        permission_mode="acceptEdits",
        setting_sources=["project"],
        allowed_tools=[
            # standard Claude tools
            'Read',
            'Write',
            'Edit',
            'MultiEdit',
            'Grep',
            'Bash',
            'Task',
            'WebSearch',
            'WebFetch',
            # add all PubMed tools
            'mcp__pubmed__*',
            # custom tools
            'mcp__mlst_tools__run_mlst',
            'mcp__atb__*'
        ],
        # MCP servers include: All custom tools and GitLab
        mcp_servers={ 
            "pubmed": {
                "type": "stdio",
                "command": "npx",
                "args": ["-y", "@cyanheads/pubmed-mcp-server@latest"],
                "env": {
                    "MCP_TRANSPORT_TYPE": "stdio",
                    "MCP_LOG_LEVEL": "info",
                    "NCBI_API_KEY": os.getenv("NCBI_API_KEY")
                    }
                },

            "mlst_tools": mlst_tools_server,
            
            "atb": {
                "type": "stdio",
                "command": "atb",
                "args": ["mcp"]
                }
            },
        
        agents={
            "mlst-agent": AgentDefinition(
                description = f""" This agent has access to a tool that will put together the MLST file with all of the species name. Always format
                the data first.""",
                prompt = f"""
                When asked to format the data, normalize the schema so that it has the genus and species name.
                """,
                model = "haiku",
                tools=[
                    'mcp__mlst_tools__run_mlst'
                ]
            )
        }
    )
    
    ######## WELCOME MESSAGE ########
    print_rich_message(
        "system",
        f"Welcome to the AllTheBacteria AI agent system!\n\nSelected model: {args.model}",
        console
        )

    async with ClaudeSDKClient(options=options) as client:

        # while loop for an ongoing conversation
        while True:
            input_prompt = get_user_input(console)
            if input_prompt == "exit":
                break

            await client.query(input_prompt)

            async for message in client.receive_response():
                # Uncomment to print raw messages for debugging
                # print(message)
                parse_and_print_message(message, console)


if __name__ == "__main__":
    import asyncio
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())