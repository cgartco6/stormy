from .ecosystem import Ecosystem

class Brain:
    def __init__(self, personality):
        self.personality = personality
        self.ecosystem = Ecosystem()
        self.mode = LLM_MODE  # local or cloud

    def generate(self, prompt: str, context: Optional[str] = None) -> str:
        # Check if the prompt is a command that might require multiple agents
        if self._is_complex_task(prompt):
            return self.ecosystem.route_task(prompt, {"user_input": prompt, "context": context})
        else:
            return self._llm_generate(prompt, context)

    def _is_complex_task(self, prompt):
        # Simple heuristic – can be improved with LLM
        keywords = ["and then", "also", "after that", "plan", "schedule", "route"]
        return any(k in prompt.lower() for k in keywords)
