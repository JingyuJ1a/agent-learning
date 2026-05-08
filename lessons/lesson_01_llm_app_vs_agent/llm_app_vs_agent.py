"""Lesson 01: compare a simple LLM app with a minimal Agent loop.

This file intentionally uses a fake LLM so the lesson can run without API keys.
The point is to observe control flow, not model quality.
"""

from __future__ import annotations

from dataclasses import dataclass


class FakeLLM:
    """A tiny deterministic stand-in for a real LLM."""

    def complete(self, prompt: str) -> str:
        if "NEXT_ACTION" in prompt and "weather" in prompt.lower():
            return "USE_TOOL:get_weather:Shanghai"
        if "FINAL_ANSWER" in prompt:
            return "Shanghai is sunny today, based on the tool observation."
        return "I can answer from the prompt, but I cannot check the outside world."


def simple_llm_app(question: str, llm: FakeLLM) -> str:
    """One prompt in, one model answer out."""

    prompt = f"Answer the user's question directly.\nQuestion: {question}"
    return llm.complete(prompt)


def get_weather(city: str) -> str:
    """A fake external tool."""

    weather_by_city = {
        "Shanghai": "sunny",
        "Beijing": "cloudy",
        "Shenzhen": "rainy",
    }
    return weather_by_city.get(city, "unknown")


@dataclass
class AgentStep:
    thought: str
    action: str
    observation: str


def minimal_agent(question: str, llm: FakeLLM) -> tuple[str, list[AgentStep]]:
    """A minimal Agent loop: decide, act, observe, answer."""

    decision_prompt = (
        "You are an Agent. Decide the NEXT_ACTION.\n"
        "If weather is needed, reply USE_TOOL:get_weather:<city>.\n"
        f"User question: {question}"
    )
    action = llm.complete(decision_prompt)
    steps: list[AgentStep] = []

    if action.startswith("USE_TOOL:get_weather:"):
        city = action.split(":", maxsplit=2)[2]
        observation = get_weather(city)
        steps.append(
            AgentStep(
                thought="The question needs information outside the prompt.",
                action=action,
                observation=f"{city}: {observation}",
            )
        )
    else:
        observation = "no tool used"
        steps.append(
            AgentStep(
                thought="The question can be answered directly.",
                action="ANSWER_DIRECTLY",
                observation=observation,
            )
        )

    final_prompt = (
        "FINAL_ANSWER\n"
        f"Question: {question}\n"
        f"Observation: {observation}"
    )
    return llm.complete(final_prompt), steps


def main() -> None:
    llm = FakeLLM()
    question = "What is the weather in Shanghai?"

    print("=== Simple LLM App ===")
    print(simple_llm_app(question, llm))

    print("\n=== Minimal Agent ===")
    answer, steps = minimal_agent(question, llm)
    for index, step in enumerate(steps, start=1):
        print(f"Step {index}")
        print(f"Thought: {step.thought}")
        print(f"Action: {step.action}")
        print(f"Observation: {step.observation}")
    print(f"Answer: {answer}")


if __name__ == "__main__":
    main()
