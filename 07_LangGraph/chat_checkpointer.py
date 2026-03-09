from dotenv import load_dotenv
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from openai import OpenAI
import os
from langgraph.checkpoint.mongodb import MongoDBSaver
from pymongo.errors import OperationFailure, ServerSelectionTimeoutError

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

class State(TypedDict):
    messages :Annotated[list, add_messages]
     

def chatbot(state: State):
    print("ChatBot Node", state)
    messages = [
        {
            "role": "user" if m.type == "human" else "assistant",
            "content": m.content
        }
        for m in state["messages"]
    ]
    response = client.chat.completions.create(
        model="gemini-2.5-flash",
        messages=messages
    )
    return {"messages": [response.choices[0].message.content]}

graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_edge(START, "chatbot")
graph_builder.add_edge("chatbot", END)


def compile_graph_with_checkpointer(checkpointer):
    return graph_builder.compile(checkpointer=checkpointer)

DB_URI = os.getenv("MONGODB_URI", "mongodb://admin:admin@localhost:27018/?authSource=admin")

try:
    with MongoDBSaver.from_conn_string(DB_URI) as checkpointer:
        graph_with_checkpointer = compile_graph_with_checkpointer(checkpointer=checkpointer)

        config = {
                "configurable": {
                    "thread_id": "jeevan" # user_id
                }
        }

        for chunk in graph_with_checkpointer.stream(
            State({"messages": ["what is my name and who am I?"]}),
            config,
            stream_mode="values"
            ):
                chunk["messages"][-1].pretty_print()
except OperationFailure as exc:
    if getattr(exc, "code", None) == 18:
        raise RuntimeError(
            "MongoDB authentication failed. Check MONGODB_URI username/password. "
            "If using docker-compose and credentials changed, recreate DB volume: "
            "docker compose down -v ; docker compose up -d"
        ) from exc
    raise
except ServerSelectionTimeoutError as exc:
    raise RuntimeError(
        "Cannot connect to MongoDB on localhost:27018. Start MongoDB first (for example: docker compose up -d)."
    ) from exc

