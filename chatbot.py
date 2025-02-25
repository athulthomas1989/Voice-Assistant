
import uuid
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.message import add_messages
from typing import TypedDict, Annotated


from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate

load_dotenv()

api_key = os.getenv("GOOGLE_GENAI_API_KEY")

llm = ChatGoogleGenerativeAI(model="gemini-2.0-flash", temperature=0, api_key=api_key)    

class State(TypedDict):
    messages: Annotated[list, add_messages]
    input: str
    output: str

def chatbot_node(state: State):
    messages = state["messages"]
    user_input = state["input"]

    # Append user input
    messages.append(HumanMessage(content=user_input))

    # Generate AI response
    response = llm.invoke(messages)

    # Append AI message
    messages.append(AIMessage(content=response.content))

    return {"messages": messages, "output": response.content}


graph = StateGraph(State)
graph.add_node("chatbot", chatbot_node)
graph.set_entry_point("chatbot")
graph.add_edge("chatbot", END)

checkpointer = MemorySaver()
app_graph = graph.compile(checkpointer=checkpointer)

def get_bot_reply(user_input: str, session_id: str):
    state = {"input": user_input}
    result = app_graph.invoke(state, config={"configurable": {"thread_id": session_id}})
    return result