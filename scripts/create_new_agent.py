#!/usr/bin/env python3
import sys
from core.agent_factory import AgentFactory

def main():
    if len(sys.argv) < 2:
        print("Usage: python create_new_agent.py 'description of what the agent should do' [agent_name]")
        return
    description = sys.argv[1]
    name = sys.argv[2] if len(sys.argv) > 2 else None
    factory = AgentFactory()
    agent = factory.create_agent(description, name)
    print(f"Agent '{name or 'new_agent'}' created and ready.")

if __name__ == "__main__":
    main()
