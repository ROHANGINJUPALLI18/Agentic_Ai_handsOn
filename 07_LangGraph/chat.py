from typing import Annotated, TypedDict
import os
from langgraph.graph.message import add_messages
from langgraph.graph import StateGraph, START, END
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv

load_dotenv();

llm = init_chat_model(
    model=os.getenv("GEMINI_MODEL", "gemini-2.5-flash"),
    model_provider="google_genai",
)

class State(TypedDict):
    messages: Annotated[list, add_messages]
    
# this is a simple node that just returns a greeting message. 
def chatbot(state:State):
    print(f"\n\ninside chatbot node, current state: {state}")
    # here we are invoking the llm with the messages from the state. The llm will generate a response based on the messages and return it. We are then returning the response as a new state with the messages key.
    response = llm.invoke(state.get("messages", []))
    return {"messages": [response]}

# this is the sample node
def sampleNode(state:State):
    print(f"\n\ninside sampleNode, current state: {state}")
    return {"messages":["Hello! i am an sample node."]}
    
# in this part we are building the nodes 
graph_builder = StateGraph(State)
graph_builder.add_node("chatbot", chatbot)
graph_builder.add_node("sampleNode", sampleNode)

# now we are defining the edges of the graph. The edges define the flow of the conversation.

# 1.initallt call the edge from the start node to the chatbot node. This means that when the conversation starts, it will first call the chatbot function.
graph_builder.add_edge(START, "chatbot")
# 2. then we are defining an edge from the chatbot node to the sampleNode. This means that after the chatbot function is called, it will call the sampleNode function.
graph_builder.add_edge("chatbot", "sampleNode")
# 3. finally we are defining an edge from the sampleNode to the end node. This means that after the sampleNode function is called, it will end the conversation.
graph_builder.add_edge("sampleNode", END)


# compile the graph
graph = graph_builder.compile()

# invoking the graph
updated_state = graph.invoke({"messages": ["hi my name is rohan Ginjupalli"]})

print(f"\n\nfinal state: {updated_state}")
