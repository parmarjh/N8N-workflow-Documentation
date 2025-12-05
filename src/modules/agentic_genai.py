import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class FrameworkRegistry:
    """
    Registry of Agentic GenAI Frameworks.
    """
    FRAMEWORKS = {
        "CrewAI": "Orchestrate role-playing autonomous AI agents.",
        "LangChain": "Building applications with LLMs through composability.",
        "AutoGen": "Enabling next-gen LLM applications with multi-agent conversations.",
        "ChatDev": "Communicative agents for software development.",
        "BabyAGI": "Task-driven autonomous agent."
    }

    def list_frameworks(self) -> Dict[str, str]:
        return self.FRAMEWORKS

    def generate_integration_workflow(self, framework: str) -> str:
        """
        Generates an n8n workflow JSON to integrate the chosen framework.
        """
        if framework not in self.FRAMEWORKS:
            return "Framework not found."
        
        logger.info(f"Generating n8n workflow for {framework}")
        # Return a mock JSON structure for n8n
        return f"""
        {{
            "name": "Auto-Integration: {framework}",
            "nodes": [
                {{
                    "parameters": {{}},
                    "name": "Start",
                    "type": "n8n-nodes-base.start",
                    "typeVersion": 1,
                    "position": [250, 300]
                }},
                {{
                    "parameters": {{
                        "content": "Running {framework} agent..."
                    }},
                    "name": "{framework} Node",
                    "type": "n8n-nodes-base.httpRequest",
                    "typeVersion": 1,
                    "position": [450, 300]
                }}
            ],
            "connections": {{
                "Start": {{
                    "main": [[{{ "node": "{framework} Node", "type": "main", "index": 0 }}]]
                }}
            }}
        }}
        """

# Tool definitions
def list_agent_frameworks() -> Dict[str, str]:
    registry = FrameworkRegistry()
    return registry.list_frameworks()

def generate_n8n_integration(framework_name: str) -> str:
    registry = FrameworkRegistry()
    return registry.generate_integration_workflow(framework_name)
