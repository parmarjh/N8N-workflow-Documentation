import logging
import requests
import os
from typing import Dict

logger = logging.getLogger(__name__)

class n8nRunner:
    """
    Runs n8n workflows directly.
    """
    def __init__(self):
        self.webhook_url = os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/test")

    def run_workflow(self, workflow_id: str, data: Dict = {}) -> str:
        """
        Triggers an n8n workflow.
        If workflow_id is a webhook path, it uses that.
        """
        logger.info(f"Running n8n workflow {workflow_id} with data {data}")
        # In a real scenario, we might use the n8n public API to execute a specific workflow ID.
        # For now, we simulate or use a generic webhook.
        try:
            # response = requests.post(self.webhook_url, json=data)
            # return f"Workflow triggered. Status: {response.status_code}"
            return f"Workflow {workflow_id} triggered successfully (Simulated)."
        except Exception as e:
            return f"Failed to trigger workflow: {str(e)}"

# Tool definitions
def run_n8n_workflow(workflow_id: str, input_data: str) -> str:
    runner = n8nRunner()
    return runner.run_workflow(workflow_id, {"input": input_data})
