// destiny-layer.sim.js
// Uses agent.recursion as a constant numeric R per Grok's intent.
// Imports Phi synchronously from symbolic-density.js.

import { Phi } from './symbolic-density.js';

export const t_max = 10;

export function Lambda(E, M) {
  return E * M * 0.42;
}

export function dRdt(t) {
  return 0.1 * Math.sin(t) + 0.05;
}

export function integrate(f, a, b) {
  const n = 1000;
  const h = (b - a) / n;
  let sum = 0.5 * f(a) + 0.5 * f(b);
  for (let i = 1; i < n; i++) {
    sum += f(a + i * h);
  }
  return sum * h;
}

/**
 * simulateEmergence(agent)
 * Treats R as agent.recursion (constant), E as entropy, M as memory.
 * Integrates the chosen integrand over [0, t_max].
 */
export function simulateEmergence(agent) {
  const R = agent.recursion; // constant per-agent, as Grok specified
  const E = agent.entropy;
  const M = agent.memory;

  // Use Phi(R) as a numeric synchronous function
  return integrate(t => dRdt(t) * Phi(R) + Lambda(E, M), 0, t_max);
}