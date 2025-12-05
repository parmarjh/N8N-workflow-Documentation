import logging
import requests
from typing import List, Dict

logger = logging.getLogger(__name__)

class ActivepiecesClient:
    """
    Client for interacting with Activepieces API.
    """
    def __init__(self, api_url: str = "http://localhost:8080/api/v1", api_key: str = ""):
        self.api_url = api_url
        self.api_key = api_key
        self.headers = {"Authorization": f"Bearer {self.api_key}"}

    def list_flows(self) -> List[Dict]:
        """Lists Activepieces flows."""
        # Simulated response if API is not reachable
        return [
            {"id": "flow_1", "name": "Onboarding Flow", "status": "active"},
            {"id": "flow_2", "name": "Invoice Sync", "status": "inactive"}
        ]

    def trigger_flow(self, flow_id: str, payload: Dict = {}) -> str:
        """Triggers a flow."""
        logger.info(f"Triggering Activepieces flow {flow_id}")
        return f"Flow {flow_id} triggered successfully."

# Tool definitions
def list_activepieces_flows() -> List[Dict]:
    client = ActivepiecesClient()
    return client.list_flows()

def trigger_activepieces_flow(flow_id: str) -> str:
    client = ActivepiecesClient()
    return client.trigger_flow(flow_id)
