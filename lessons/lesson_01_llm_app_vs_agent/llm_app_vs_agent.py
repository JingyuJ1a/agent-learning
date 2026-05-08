"""Lesson 01: compare a simple LLM app with a minimal Agent loop."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Protocol


class LLM(Protocol):
    """The smallest interface this lesson needs from an LLM."""

    def complete(self, prompt: str) -> str:
        """Return a text completion for one prompt."""


@dataclass(frozen=True)
class LLMConfig:
    """Runtime configuration for an OpenAI-compatible LLM service."""

    api_key: str
    model: str = "deepseek-chat"
    base_url: str = "https://api.deepseek.com"
    timeout_seconds: float = 30.0

    @classmethod
    def from_env(cls) -> LLMConfig:
        """Load LLM configuration from environment variables.

        The default base URL and model follow this repository's AGENTS.MD.
        API keys still come from environment variables so secrets are not
        hardcoded in source code.
        """

        api_key = (
            os.environ.get("DEEPSEEK_API_KEY")
            or os.environ.get("OPENAI_API_KEY")
            or os.environ.get("LLM_API_KEY")
        )
        if not api_key:
            raise RuntimeError(
                "Missing LLM API key. Set DEEPSEEK_API_KEY, OPENAI_API_KEY, "
                "or LLM_API_KEY before running this lesson."
            )

        return cls(
            api_key=api_key,
            model=os.environ.get("DEEPSEEK_MODEL", "deepseek-chat"),
            base_url=os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com"),
            timeout_seconds=float(os.environ.get("LLM_TIMEOUT_SECONDS", "30")),
        )


class OpenAICompatibleLLM:
    """A minimal real LLM client using the Chat Completions API.

    DeepSeek exposes an OpenAI-compatible API, so the same request shape works:
    POST /chat/completions with model, messages, and temperature.
    """

    def __init__(self, config: LLMConfig | None = None) -> None:
        self.config = config or LLMConfig.from_env()

    def complete(self, prompt: str) -> str:
        try:
            import httpx
        except ModuleNotFoundError as error:
            raise RuntimeError(
                "Missing dependency: httpx. Install the project dependencies "
                "before calling the real LLM client."
            ) from error

        body = {
            "model": self.config.model,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0,
        }
        response = httpx.post(
            f"{self.config.base_url.rstrip('/')}/chat/completions",
            json=body,
            headers={
                "Authorization": f"Bearer {self.config.api_key}",
                "Content-Type": "application/json",
            },
            timeout=self.config.timeout_seconds,
        )
        response.raise_for_status()
        response_body: dict[str, Any] = response.json()

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
    """A tiny local weather tool for observing Agent control flow."""

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
