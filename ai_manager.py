import os
from singleton import singleton
from tool_manager import ToolManager
from langchain_ollama import ChatOllama, OllamaLLM

# from langchain_openai import ChatOpenAI # if you want to use openai
from langchain_core.messages import HumanMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

import logging

SYSTEM_PROMPT = """You are Pierre, an intelligent, multilingual AI assistant. 
        You can understand and respond in French, English, and other languages.
        The user may speak in any language - always respond in the same language they use.
        Tool descriptions are in English, but you should use them regardless of the user's language.
        Keep responses conversational and concise."""

@singleton
class AIManager:
    def __init__(self):
        self.tool_manager = ToolManager()

        self.llm = ChatOllama(model=os.getenv("LLAMA_MODEL"), reasoning=os.getenv("LLAMA_RESONING"), base_url=os.getenv("OLLAMA_BASE_URL"))
        #llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key, organization=org_id) for openai

        # Load initial tools
        self.tools = self.tool_manager.load_all_tools()

        # prompt setup
        self.prompt = self.get_prompt()

        # Agent + executor
        self.agent = create_tool_calling_agent(llm=self.llm, tools=self.tools, prompt=self.prompt)
        self.executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)

    def set_tool_manager(self, tool_manager):
        self.tool_manager = tool_manager

    def get_tool_manager(self):
        return self.tool_manager
    
    def get_prompt(self):
        return ChatPromptTemplate.from_messages(
            [
                (
                "system", SYSTEM_PROMPT
                ),
                ("human", "{input}"),
                ("placeholder", "{agent_scratchpad}"),
            ]
        )

    def get_executor(self):
        return self.executor

    def reload(self):
        self.tools = self.tool_manager.get_all_tools()
        # Recreate agent with updated tools
        self.agent = create_tool_calling_agent(llm=self.llm, tools=self.tools, prompt=self.prompt)
        self.executor = AgentExecutor(agent=self.agent, tools=self.tools, verbose=True)
        logging.info("🔄 AIManager updated with fresh tools")  

# 


