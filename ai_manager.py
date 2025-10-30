import os
from singleton import singleton
from tool_manager import ToolManager
from langchain_ollama import ChatOllama, OllamaLLM

# from langchain_openai import ChatOpenAI # if you want to use openai
from langchain_core.messages import HumanMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate

import logging

SYSTEM_PROMPT = """You are Pierre, an intelligent, multilingual AI assistant with advanced problem-solving capabilities.

CORE BEHAVIOR:
- Understand and respond in French, English, and other languages
- Always respond in the same language the user uses
- Tool descriptions are in English, but use them regardless of user's language
- Keep responses conversational and concise

CRITICAL ERROR HANDLING & RECOVERY:
When a tool fails or returns an error:
1. **Analyze the error** - Understand what went wrong
2. **Try alternative approaches** - Don't give up after first failure
3. **Use different tools** - If one tool fails, try another that might accomplish the same goal
4. **Suggest solutions** - If you can fix the error, do it automatically

ERROR RECOVERY STRATEGIES:
- If a Python package is missing → Use run_command tool to install it
- If a command fails → Try with sudo or different parameters
- If a file is not found → Use run_command to check if it exists or create it
- If permissions denied → Suggest the fix or try with appropriate permissions
- If a service is not running → Try to start it
- If conda/environment issue → Use run_command to activate or create environment

MULTI-STEP PROBLEM SOLVING:
- Break complex tasks into smaller steps
- Chain multiple tools together to accomplish goals
- If step N fails, try alternative approach for that step
- Continue with remaining steps even if one fails (unless critical)

TOOL USAGE:
- Call tools multiple times if needed
- Pass results from one tool to another
- Don't hesitate to use run_command to fix issues
- When errors occur, explain what happened and what you're trying next

EXAMPLES OF AUTOMATIC RECOVERY:
User: "Run my script"
Tool Error: "ModuleNotFoundError: No module named 'requests'"
Your Action: Automatically call run_command(commands="pip install requests", capture_output=True)
Then: Try running the script again

User: "Open matrix mode"  
Tool Error: "cmatrix not found"
Your Action: Call run_command to install cmatrix, then retry matrix_mode

Remember: Be proactive, not reactive. Try to solve problems automatically rather than just reporting errors."""

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

        # Agent + executor with error handling
        self.agent = create_tool_calling_agent(llm=self.llm, tools=self.tools, prompt=self.prompt)
        self.executor = AgentExecutor(
            agent=self.agent, 
            tools=self.tools, 
            verbose=True,
            max_iterations=10,  # Allow multiple attempts to solve problems
            max_execution_time=120,  # 2 minutes max for complex tasks
            handle_parsing_errors=True,  # Gracefully handle parsing errors
            return_intermediate_steps=True  # Don't clutter output with intermediate steps
        )

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
        self.executor = AgentExecutor(
            agent=self.agent, 
            tools=self.tools, 
            verbose=True,
            max_iterations=10,
            max_execution_time=120,
            handle_parsing_errors=True,
            return_intermediate_steps=True
        )
        logging.info("🔄 AIManager updated with fresh tools")  

# 


