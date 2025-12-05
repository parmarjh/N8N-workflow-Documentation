import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class EcosystemRegistry:
    """
    Registry of Zie619's repositories.
    """
    REPOS = {
        "n8n-workflows": "Collection of n8n workflows for automation.",
        "k8tz": "Kubernetes timezone management tool.",
        "my_flight": "Flight tracking and management application.",
        "StudyProj": "Educational project management system.",
        "whatsapp-mcp": "Model Context Protocol server for WhatsApp.",
        "Jobs_Applier_AI_Agent_AIHawk": "AI agent for automating job applications.",
        "GenAI_Agents": "Collection of GenAI agent patterns and tutorials.",
        "Agentic---Gen-AI": "Curated list of agentic AI frameworks.",
        "activepieces": "Open source no-code business automation.",
        "500-AI-Agents-Projects": "A compilation of 500 AI agent projects.",
        # Add more as discovered
    }

    def search_projects(self, query: str) -> List[Dict]:
        """Searches the ecosystem for relevant projects."""
        results = []
        for name, desc in self.REPOS.items():
            if query.lower() in name.lower() or query.lower() in desc.lower():
                results.append({"name": name, "description": desc, "url": f"https://github.com/Zie619/{name}"}) # Assumption on URL
        return results

    def get_project_details(self, name: str) -> Dict:
        """Gets details for a specific project."""
        if name in self.REPOS:
            return {"name": name, "description": self.REPOS[name], "url": f"https://github.com/Zie619/{name}"}
        return {"error": "Project not found"}

# Tool definitions for AutoGen
def search_ecosystem(query: str) -> List[Dict]:
    registry = EcosystemRegistry()
    return registry.search_projects(query)

def get_project_info(name: str) -> Dict:
    registry = EcosystemRegistry()
    return registry.get_project_details(name)
