import numpy as np
from typing import List, Callable

class ReinforcementLearner:
    """Simple Q‑learning for agent improvement."""
    def __init__(self, state_size, action_size):
        self.q_table = np.zeros((state_size, action_size))

    def update(self, state, action, reward, next_state, alpha=0.1, gamma=0.95):
        best_next = np.max(self.q_table[next_state])
        self.q_table[state, action] += alpha * (reward + gamma * best_next - self.q_table[state, action])

class EvolutionaryOptimizer:
    """Genetic algorithm for optimizing agent parameters."""
    def optimize(self, fitness_fn: Callable, population_size=10, generations=5):
        population = [np.random.random(10) for _ in range(population_size)]
        for _ in range(generations):
            fitnesses = [fitness_fn(ind) for ind in population]
            # Selection, crossover, mutation (simplified)
            population = self._select(population, fitnesses)
        return max(population, key=fitness_fn)

    def _select(self, pop, fit):
        # Truncation selection
        idx = np.argsort(fit)[-len(pop)//2:]
        return [pop[i] for i in idx] * 2
