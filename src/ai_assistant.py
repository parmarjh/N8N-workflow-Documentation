import os
import logging
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import autogen
from autogen import AssistantAgent, UserProxyAgent

# Import all modules
from modules.whatsapp import send_whatsapp_message, read_whatsapp_messages
from modules.ecosystem import search_ecosystem, get_project_info
from modules.job_applier import apply_for_job
from modules.genai_patterns import list_genai_patterns, run_genai_pattern
from modules.workflow_discovery import search_online_workflows
from modules.analytics import get_analytics_overview
from modules.activepieces import list_activepieces_flows, trigger_activepieces_flow
from modules.n8n_runner import run_n8n_workflow
from modules.agentic_genai import list_agent_frameworks, generate_n8n_integration
from modules.supabase_n8n import store_supabase_chat, get_supabase_context
from modules.git_manager import pull_repo, push_repo, get_repo_status

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"

class AutoGenAssistant:
    def __init__(self):
        self.config_list = [
            {
                "model": "gpt-4",
                "api_key": os.getenv("OPENAI_API_KEY", "sk-placeholder")
            }
        ]
        self.llm_config = {
            "config_list": self.config_list,
            "temperature": 0,
            "timeout": 120,
        }
        
        self.assistant = AssistantAgent(
            name="n8n_expert",
            llm_config=self.llm_config,
            system_message="""You are a Super Agent for n8n and automation. 
            You have access to a wide range of tools:
            1. WhatsApp: Send/Read messages.
            2. Ecosystem: Search Zie619's repositories.
            3. Job Applier: Apply for jobs.
            4. GenAI Patterns: Run RAG, ReAct, etc.
            5. Workflow Discovery: Find n8n workflows.
            6. Analytics: View workflow stats.
            7. Activepieces: Manage Activepieces flows.
            8. n8n Runner: Trigger n8n workflows.
            9. Agentic GenAI: Integrate frameworks like CrewAI/LangChain.
            10. Git Manager: Sync documentation.
            11. Supabase: Store chat history.
            
            Use these tools to answer user requests. If a tool fails, report the error.
            """
        )
        
        self.user_proxy = UserProxyAgent(
            name="user_proxy",
            human_input_mode="NEVER",
            max_consecutive_auto_reply=10,
            is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
            code_execution_config=False,
        )
        
        # Register tools
        self.register_tools()

    def register_tools(self):
        # WhatsApp
        self.user_proxy.register_function(function_map={
            "send_whatsapp_message": send_whatsapp_message,
            "read_whatsapp_messages": read_whatsapp_messages,
            "search_ecosystem": search_ecosystem,
            "get_project_info": get_project_info,
            "apply_for_job": apply_for_job,
            "list_genai_patterns": list_genai_patterns,
            "run_genai_pattern": run_genai_pattern,
            "search_online_workflows": search_online_workflows,
            "get_analytics_overview": get_analytics_overview,
            "list_activepieces_flows": list_activepieces_flows,
            "trigger_activepieces_flow": trigger_activepieces_flow,
            "run_n8n_workflow": run_n8n_workflow,
            "list_agent_frameworks": list_agent_frameworks,
            "generate_n8n_integration": generate_n8n_integration,
            "store_supabase_chat": store_supabase_chat,
            "get_supabase_context": get_supabase_context,
            "pull_repo": pull_repo,
            "push_repo": push_repo,
            "get_repo_status": get_repo_status
        })
        
        # Register for Assistant as well (for tool calling schema)
        # AutoGen 0.2 handles this via register_function if done correctly, 
        # but explicit registration helps.
        # Note: In 0.2, we often just need to register with user_proxy for execution 
        # and pass the config to assistant.
        pass

    def generate_response(self, message: str) -> str:
        try:
            self.user_proxy.initiate_chat(
                self.assistant,
                message=message,
                clear_history=False
            )
            # Retrieve the last message from the chat
            # This is a simplification; getting the exact final answer depends on the chat flow.
            last_msg = self.user_proxy.chat_messages[self.assistant][-1]["content"]
            return last_msg
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return f"Error: {str(e)}"

# Global instance
agent = AutoGenAssistant()

@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    response = agent.generate_response(request.message)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
