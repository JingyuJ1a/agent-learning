from lessons.lesson_01_llm_app_vs_agent.llm_app_vs_agent import (
    FakeLLM,
    minimal_agent,
    simple_llm_app,
)


def test_simple_llm_app_answers_without_tool_use() -> None:
    answer = simple_llm_app("What is the weather in Shanghai?", FakeLLM())

    assert "cannot check the outside world" in answer


def test_minimal_agent_uses_tool_observation() -> None:
    answer, steps = minimal_agent("What is the weather in Shanghai?", FakeLLM())

    assert answer == "Shanghai is sunny today, based on the tool observation."
    assert steps[0].action == "USE_TOOL:get_weather:Shanghai"
    assert steps[0].observation == "Shanghai: sunny"
