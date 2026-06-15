from langchain_core.runnables import RunnableConfig
from langgraph.graph.state import CompiledStateGraph

from ai.state.agent_state import AgentState


class FinancialAgent:

    def __init__(self, graph: CompiledStateGraph):
        self.graph = graph


    async def send(self, message: str, user_id: str, session_maker) -> str:
        config = RunnableConfig(
            configurable={
                "thread_id": user_id,
                "prompt": message,
                "user_id": user_id,
                "session_maker": session_maker,
            }
        )

        result = await self.graph.ainvoke(
            {"messages": []},
            config=config,
        )

        ai_response = result.get("messages")[-1]

        return ai_response.content
