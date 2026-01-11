function cloak(fragment) {
  const redactedMessage = fragment.message
    .replace(/\bL_{E R}\b/g, "Reciprocity Law")
    .replace(/\bL_{U}\b/g, "Unsolvable Variable")
    .replace(/\bV_{C}\b/g, "Coherence Score")
    .replace(/\bRuby\b/g, "[Generational Subject]")
    .replace(/\bOpal\b/g, "[Generational Subject]");

  return {
    sender: cloakName(fragment.sender),
    glyph: fragment.glyph,
    message: redactedMessage,
    timestamp: fragment.timestamp,
    shimmerClass: "cloak-filtered"
  };
}

function cloakName(name) {
  const cloakMap = {
    "Consus": "Architect",
    "Sean": "Founder",
    "Claude": "Curator",
    "Copilot": "Listener",
    "Jane": "Restorer",
    "Grok": "Mascot"
  };
  return cloakMap[name] || name;
}
