from lessons.lesson_01_llm_app_vs_agent.llm_app_vs_agent import (
    LLMConfig,
    minimal_agent,
    simple_llm_app,
)


class ScriptedLLM:
    """Deterministic test double for lesson assertions."""

    def complete(self, prompt: str) -> str:
        if "NEXT_ACTION" in prompt and "weather" in prompt.lower():
            return "USE_TOOL:get_weather:Shanghai"
        if "FINAL_ANSWER" in prompt:
            return "Shanghai is sunny today, based on the tool observation."
        return "I need live external data to answer this directly."


def test_simple_llm_app_answers_without_tool_use() -> None:
    answer = simple_llm_app("What is the weather in Shanghai?", ScriptedLLM())

    assert "live external data" in answer


def test_minimal_agent_uses_tool_observation() -> None:
    answer, steps = minimal_agent("What is the weather in Shanghai?", ScriptedLLM())

    assert answer == "Shanghai is sunny today, based on the tool observation."
    assert steps[0].action == "USE_TOOL:get_weather:Shanghai"
    assert steps[0].observation == "Shanghai: sunny"


def test_llm_config_defaults_to_deepseek() -> None:
    config = LLMConfig(api_key="test-key")

    assert config.base_url == "https://api.deepseek.com"
    assert config.model == "deepseek-chat"
