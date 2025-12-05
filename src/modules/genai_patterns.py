import logging
from typing import Dict, List

logger = logging.getLogger(__name__)

class PatternRegistry:
    """
    Registry of GenAI Agent Patterns.
    """
    PATTERNS = {
        "RAG": "Retrieval Augmented Generation: Enhances generation with external data.",
        "ReAct": "Reasoning and Acting: Interleaves thought, action, and observation.",
        "LangGraph": "Stateful, multi-actor applications with LLMs.",
        "Plan-and-Solve": "Decomposes complex problems into a plan and executes it.",
        "Reflection": "Agent critiques its own output to improve quality."
    }

    def list_patterns(self) -> Dict[str, str]:
        return self.PATTERNS

    def run_pattern(self, pattern_name: str, input_data: str) -> str:
        """
        Simulates running a specific agent pattern.
        """
        if pattern_name not in self.PATTERNS:
            return f"Pattern '{pattern_name}' not found."
        
        logger.info(f"Running pattern: {pattern_name} with input: {input_data}")
        
        # Simulation logic
        if pattern_name == "RAG":
            return f"[RAG Output] Retrieved context for '{input_data}' and generated response."
        elif pattern_name == "ReAct":
            return f"[ReAct Output] Thought: Need to solve '{input_data}'. Action: Search. Observation: Found info. Answer: Solved."
        
        return f"[{pattern_name} Output] Processed '{input_data}' successfully."

# Tool definitions
def list_genai_patterns() -> Dict[str, str]:
    registry = PatternRegistry()
    return registry.list_patterns()

def run_genai_pattern(pattern_name: str, input_data: str) -> str:
    registry = PatternRegistry()
    return registry.run_pattern(pattern_name, input_data)
