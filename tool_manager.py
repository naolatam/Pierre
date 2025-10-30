"""
Tool Manager for Hot-Reloading Tools
Dynamically loads and reloads tools from the tools directory at runtime.
"""

import importlib
import sys
import logging
from pathlib import Path
from typing import List, Dict, Any
from singleton import singleton
from langchain_ollama import ChatOllama, OllamaLLM

# from langchain_openai import ChatOpenAI # if you want to use openai
from langchain_core.messages import HumanMessage
from langchain.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate


@singleton
class ToolManager:
    """Singleton class to manage dynamic loading and reloading of tools."""
    
    def __init__(self):
        
        self.tools_directory = "tools"
        self.loaded_modules = {}
        self.tools = {}
        self.tool_to_module = {}  # Maps tool name to module name
        self.module_to_tools = {}  # Maps module name to list of tool names
        logging.info("🔧 ToolManager initialized")
    
    def discover_tool_files(self) -> List[str]:
        """Discover all Python files in the tools directory."""
        tools_path = Path(self.tools_directory)
        
        if not tools_path.exists():
            logging.warning(f"Tools directory not found: {self.tools_directory}")
            return []
        
        tool_files = []
        for file in tools_path.glob("*.py"):
            # Skip __init__, __pycache__, and private files
            if file.stem not in ["__init__"] and not file.stem.startswith("_"):
                tool_files.append(file.stem)
        
        logging.debug(f"Discovered {len(tool_files)} tool files: {tool_files}")
        return tool_files
    
    def load_module(self, module_name: str, reload: bool = False):
        """Load or reload a specific module."""
        full_module_name = f"{self.tools_directory}.{module_name}"
        
        try:
            if reload and full_module_name in sys.modules:
                logging.info(f"♻️  Reloading module: {module_name}")
                module = importlib.reload(sys.modules[full_module_name])
            else:
                logging.info(f"📦 Loading module: {module_name}")
                module = importlib.import_module(full_module_name)
            
            self.loaded_modules[module_name] = module
            return module
            
        except Exception as e:
            logging.error(f"❌ Failed to load module {module_name}: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    def extract_tools_from_module(self, module, module_name: str) -> Dict[str, Any]:
        """Extract all LangChain tools from a module."""
        tools = {}
        
        for attr_name in dir(module):
            # Skip private attributes
            if attr_name.startswith('_'):
                continue
            
            try:
                attr = getattr(module, attr_name)
                
                # Check if it's a LangChain tool
                # LangChain tools have 'name', 'description', and are callable
                if (hasattr(attr, 'name') and 
                    hasattr(attr, 'description') and 
                    callable(attr) and
                    hasattr(attr, 'invoke')):  # LangChain tools have invoke method
                    
                    tools[attr.name] = attr
                    # Track which module this tool came from
                    self.tool_to_module[attr.name] = module_name
                    logging.debug(f"  ✓ Found tool: {attr.name} from module {module_name}")
                    
            except Exception as e:
                logging.debug(f"  ⚠️  Skipping {attr_name}: {e}")
                continue
        
        # Update module to tools mapping
        if tools:
            self.module_to_tools[module_name] = list(tools.keys())
        
        return tools
    
    def load_all_tools(self, reload: bool = False) -> List[Any]:
        """
        Load or reload all tools from the tools directory.
        
        Args:
            reload: If True, reload existing modules
            
        Returns:
            List of all loaded tool objects
        """
        logging.info(f"{'🔄 Reloading' if reload else '📚 Loading'} all tools...")
        
        if reload:
            self.tools.clear()
            self.tool_to_module.clear()
            self.module_to_tools.clear()
        
        tool_files = self.discover_tool_files()
        logging.info(f"Found {len(tool_files)} tool modules")
        
        for module_name in tool_files:
            module = self.load_module(module_name, reload=reload)
            
            if module:
                module_tools = self.extract_tools_from_module(module, module_name)
                self.tools.update(module_tools)
        
        logging.info(f"✅ Loaded {len(self.tools)} tools total: {list(self.tools.keys())}")
        return list(self.tools.values())
    
    def reload_all_tools(self) -> List[Any]:
        """Reload all tools."""
        return self.load_all_tools(reload=True)
    
    def reload_specific_tool(self, identifier: str) -> List[Any]:
        """
        Reload a specific tool module by module name or tool name.
        
        Args:
            identifier: Module name (e.g., "time") or tool name (e.g., "get_time")
            
        Returns:
            List of all tools (after reloading the specific one)
        """
        # Check if identifier is a tool name and get the module name
        if identifier in self.tool_to_module:
            module_name = self.tool_to_module[identifier]
            logging.info(f"� Tool '{identifier}' found in module '{module_name}'")
        else:
            # Assume it's a module name
            module_name = identifier
        
        logging.info(f"🔄 Reloading module: {module_name}")
        
        module = self.load_module(module_name, reload=True)
        
        if module:
            # Remove old tools from this module
            if module_name in self.module_to_tools:
                old_tool_names = self.module_to_tools[module_name]
                for tool_name in old_tool_names:
                    if tool_name in self.tools:
                        del self.tools[tool_name]
                        logging.debug(f"  Removed old tool: {tool_name}")
                    if tool_name in self.tool_to_module:
                        del self.tool_to_module[tool_name]
            
            # Add new tools from reloaded module
            module_tools = self.extract_tools_from_module(module, module_name)
            self.tools.update(module_tools)

            logging.info(f"✅ Reloaded {module_name}. Total tools: {len(self.tools)}")
        else:
            logging.error(f"❌ Failed to reload module: {module_name}")

        return list(self.tools.values())
    
    def get_all_tools(self) -> List[Any]:
        """
        Get all currently loaded tools.
        
        Returns:
            List of all tool objects
        """
        return list(self.tools.values())
    
    def get_tool_names(self) -> List[str]:
        """
        Get names of all currently loaded tools.
        
        Returns:
            List of tool names
        """
        return list(self.tools.keys())
    
    def get_tool_by_name(self, name: str) -> Any:
        """
        Get a specific tool by name.
        
        Args:
            name: The tool name
            
        Returns:
            Tool object or None if not found
        """
        return self.tools.get(name)
    
    def get_tool_count(self) -> int:
        """Get the number of loaded tools."""
        return len(self.tools)
    
    def get_tools_info(self) -> str:
        """Get formatted information about all loaded tools."""
        if not self.tools:
            return "No tools loaded."
        
        info = f"📋 {len(self.tools)} tools loaded:\n"
        for name, tool in self.tools.items():
            module_name = self.tool_to_module.get(name, "unknown")
            desc = tool.description[:60] + "..." if len(tool.description) > 60 else tool.description
            info += f"  • {name} (from {module_name}.py): {desc}\n"
        
        return info
    
    def get_module_for_tool(self, tool_name: str) -> str:
        """Get the module name for a specific tool."""
        return self.tool_to_module.get(tool_name, None)
    
    def get_tools_in_module(self, module_name: str) -> List[str]:
        """Get all tool names in a specific module."""
        return self.module_to_tools.get(module_name, [])

