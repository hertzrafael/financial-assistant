from typing import Sequence

from langchain_core.messages import HumanMessage, BaseMessage, SystemMessage
from langchain_core.runnables import RunnableConfig
from langgraph.prebuilt.tool_node import ToolNode

from ai.nodes.tools import TOOLS
from ai.prompts.persona import PERSONA
from ai.state.agent_state import AgentState
from ai.llm.llm_utils import llm


tool_node = ToolNode(tools=TOOLS)
llm_with_tools = llm.bind_tools(TOOLS)


async def check_initial(state: AgentState) -> dict:
    messages = state["messages"]

    if len(messages) <= 0:
        messages.insert(
            0,
            SystemMessage(PERSONA),
        )

    return {"messages": messages}


async def call_llm(state: AgentState, config: RunnableConfig) -> dict:
    configurable = config.get("configurable", {})
    prompt = configurable.get("prompt")
    state_messages: Sequence[BaseMessage] = state.get("messages")

    if state_messages and state_messages[-1].type == "tool":
        messages = [*state_messages]
    else:
        messages = [
            *state_messages,
            HumanMessage(prompt),
        ]
    
    response = await llm_with_tools.ainvoke(messages)

    return {"messages": [response]}
