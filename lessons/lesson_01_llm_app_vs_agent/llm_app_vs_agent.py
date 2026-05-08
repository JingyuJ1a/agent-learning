"""Lesson 01: compare a simple LLM app with a minimal Agent loop."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from typing import Protocol
from urllib import request


class LLM(Protocol):
    """The smallest interface this lesson needs from an LLM."""

    def complete(self, prompt: str) -> str:
        """Return a text completion for one prompt."""


class OpenAICompatibleLLM:
    """A minimal OpenAI-compatible chat completions client.

    Required environment variables:
    - OPENAI_API_KEY
    - OPENAI_MODEL

    Optional environment variable:
    - OPENAI_BASE_URL, defaults to https://api.openai.com/v1
    """

    def __init__(self) -> None:
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.model = os.environ.get("OPENAI_MODEL")
        self.base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")

        if not self.api_key:
            raise RuntimeError("Missing OPENAI_API_KEY environment variable.")
        if not self.model:
            raise RuntimeError("Missing OPENAI_MODEL environment variable.")

    def complete(self, prompt: str) -> str:
        body = {
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        }
        payload = json.dumps(body).encode("utf-8")
        url = f"{self.base_url.rstrip('/')}/chat/completions"
        http_request = request.Request(
            url,
            data=payload,
            headers={
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        with request.urlopen(http_request, timeout=30) as response:
            response_body = json.loads(response.read().decode("utf-8"))

        return response_body["choices"][0]["message"]["content"].strip()


def simple_llm_app(question: str, llm: LLM) -> str:
    """One prompt in, one model answer out."""

    prompt = (
        "Answer the user's question directly.\n"
        "Do not call tools. If the answer needs live external data, say what "
        "information is missing.\n"
        f"Question: {question}"
    )
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


def minimal_agent(question: str, llm: LLM) -> tuple[str, list[AgentStep]]:
    """A minimal Agent loop: decide, act, observe, answer."""

    decision_prompt = (
        "You are an Agent. Decide the NEXT_ACTION.\n"
        "Reply with exactly one line.\n"
        "If weather is needed, reply: USE_TOOL:get_weather:<city>\n"
        "If no tool is needed, reply: ANSWER_DIRECTLY\n"
        f"User question: {question}"
    )
    action = _first_action_line(llm.complete(decision_prompt))
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
        "Write the FINAL_ANSWER for the user.\n"
        f"Question: {question}\n"
        f"Observation: {observation}"
    )
    return llm.complete(final_prompt), steps


def _first_action_line(text: str) -> str:
    """Extract the first machine-readable action from a model response."""

    for line in text.splitlines():
        cleaned = line.strip()
        if cleaned.startswith("USE_TOOL:") or cleaned == "ANSWER_DIRECTLY":
            return cleaned
    return text.strip()


def main() -> None:
    llm = OpenAICompatibleLLM()
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
