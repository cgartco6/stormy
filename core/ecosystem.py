import json
import importlib
from pathlib import Path
from typing import Dict, Any, Optional
from .agent_factory import AgentFactory
from .strategic_intelligence import StrategicPlanner
from .harness_engineering import HarnessEngineer

class Ecosystem:
    def __init__(self, config_path: str = None):
        self.config_path = Path(config_path or Path.home() / ".stormy" / "ecosystem.json")
        self.agents: Dict[str, Any] = {}
        self.factory = AgentFactory()
        self.planner = StrategicPlanner()
        self.engineer = HarnessEngineer()
        self.load_agents()

    def load_agents(self):
        if self.config_path.exists():
            with open(self.config_path) as f:
                config = json.load(f)
                for name, spec in config.get("agents", {}).items():
                    self._load_agent(name, spec)

    def save_agents(self):
        config = {"agents": {name: {"type": type(agent).__name__, "path": agent.__module__} for name, agent in self.agents.items()}}
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, "w") as f:
            json.dump(config, f, indent=2)

    def _load_agent(self, name: str, spec: dict):
        module = importlib.import_module(spec["path"])
        cls = getattr(module, spec["type"])
        self.agents[name] = cls()

    def register_agent(self, name: str, agent_instance):
        self.agents[name] = agent_instance
        self.save_agents()

    def route_task(self, task: str, context: Optional[Dict] = None) -> str:
        """Let the strategic planner decide which agent(s) to use."""
        plan = self.planner.plan(task, context, self.agents)
        return self._execute_plan(plan, context)

    def _execute_plan(self, plan: list, context: Dict) -> str:
        results = []
        for step in plan:
            agent_name = step["agent"]
            if agent_name not in self.agents:
                # Agent not found – maybe create it
                new_agent = self.factory.create_agent(step["description"])
                self.register_agent(agent_name, new_agent)
            agent = self.agents[agent_name]
            # Call the agent's method; each agent must have a `process` method
            result = agent.process(step["instruction"], context)
            results.append(result)
        return "\n".join(results)

    def evolve_agents(self):
        """Periodically improve agents using harness engineering."""
        for name, agent in self.agents.items():
            improved = self.engineer.improve_agent(agent)
            if improved:
                self.agents[name] = improved
        self.save_agents()
