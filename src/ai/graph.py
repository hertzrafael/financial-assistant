from langgraph.constants import START, END
from langgraph.graph import StateGraph
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt.tool_node import tools_condition

from ai.state.agent_state import AgentState
from ai.nodes.nodes import (
    tool_node,
    call_llm,
    check_initial,
)


async def build_graph(checkpointer) -> CompiledStateGraph:
    build = StateGraph(
        state_schema=AgentState,
        input_schema=AgentState,
        output_schema=AgentState
    )

    build.add_node("check_initial", check_initial)
    build.add_node("call_llm", call_llm)
    build.add_node("tools", tool_node)
    
    build.add_edge(START, "check_initial")
    build.add_edge("check_initial", "call_llm")
    build.add_conditional_edges("call_llm", tools_condition, ["tools", END])
    build.add_edge("tools", "call_llm")

    return build.compile(checkpointer=checkpointer)
