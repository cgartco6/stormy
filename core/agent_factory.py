import inspect
import textwrap
from pathlib import Path
from typing import Type
from .brain import Brain
from .personality import Personality

class AgentFactory:
    def __init__(self):
        self.brain = Brain(Personality())
        self.agents_dir = Path(__file__).parent.parent / "modules" / "generated_agents"
        self.agents_dir.mkdir(parents=True, exist_ok=True)

    def create_agent(self, description: str, name: str = None) -> object:
        """Generate a new agent class code and instantiate it."""
        prompt = f"""
        You are an AI that creates new AI agents. Generate a Python class for an agent that can perform the following task:
        {description}

        The class must be named '{name or 'NewAgent'}' and must have:
        - A __init__ method that accepts optional config.
        - A process(self, instruction: str, context: dict) -> str method that returns the result.

        Return only the code, no explanation.
        """
        code = self.brain.generate(prompt)
        # Clean and write to file
        agent_file = self.agents_dir / f"{name or 'new_agent'}.py"
        with open(agent_file, "w") as f:
            f.write(code)
        # Dynamically import
        import importlib.util
        spec = importlib.util.spec_from_file_location(name or "new_agent", agent_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        agent_class = getattr(module, name or "NewAgent")
        return agent_class()
