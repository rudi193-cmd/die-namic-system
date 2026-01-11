export function Phi(R) {
  const alpha = 1.1;
  const beta = 0.6;
  return alpha * Math.log(1 + R) + beta * Res(R);
}

function Res(R) {
  const fragments = getFragments();
  return fragments.reduce((sum, f) => {
    return sum + f.mu * Math.cos(f.theta + f.delta);
  }, 0) / fragments.length;
}

function getFragments() {
  return [
    { mu: 0.42, theta: 0, delta: 0 },
    { mu: -0.17, theta: Math.PI/2, delta: 0.1 },
    { mu: 0.88, theta: Math.PI, delta: 0.2 }
  ];
}
