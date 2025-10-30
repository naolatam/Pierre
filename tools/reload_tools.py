from langchain.tools import tool
import logging
import sys
import os

from tool_manager import ToolManager

# Add parent directory to path for import
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from ai_manager import AIManager
logger = logging.getLogger(__name__)


@tool("reload_tools", return_direct=False)
def reload_tools(identifier: str = "all") -> str:
    """
    Reloads tool modules without restarting the application.
    
    Args:
        identifier: Can be:
            - "all" to reload all tools
            - "list" to list all current tools without reloading
            - A module name (e.g., "time", "matrix") to reload that file
            - A tool name (e.g., "get_time") to reload the module containing that tool
    
    Use this when you've made changes to a tool and want to reload it without restarting Pierre.
    
    Example queries:
    - "Reload all tools"
    - "Reload the time tool" (will find and reload time.py)
    - "Reload get_time" (will find and reload the module containing get_time)
    - "Reload time module"
    - "Refresh tools"
    - "List all tools"
    """
    
    try:
        ai_manager = AIManager()
        tool_manager = ai_manager.get_tool_manager()
        
        if identifier.lower() == "all":
            logger.info("🔄 Reloading all tools...")
            tool_manager.reload_all_tools()
            ai_manager.reload()
            return "✅ Successfully reloaded all tools!" 
        elif identifier.lower() == "list":
            # List current tools without reloading
            return tool_manager.get_tools_info()
        else:
            logger.info(f"🔄 Reloading: {identifier}")
            
            # Check if it's a tool name first
            module_name = tool_manager.get_module_for_tool(identifier)
            if module_name:
                logger.info(f"🔍 Found tool '{identifier}' in module '{module_name}'")
                display_name = f"tool '{identifier}' (module {module_name}.py)"
            else:
                # Assume it's a module name
                module_name = identifier
                display_name = f"module '{module_name}.py'"
            
            tools = tool_manager.reload_specific_tool(identifier)
            ai_manager.reload()
            
            # Get the tools that were reloaded from this module
            reloaded_tools = tool_manager.get_tools_in_module(module_name)
            
            result = f"✅ Successfully reloaded {display_name}\n"
            result += f"📦 Reloaded {len(reloaded_tools)} tool(s): {', '.join(reloaded_tools)}\n"
            result += f"📊 Total tools loaded: {len(tools)}\n\n"
            
            return result
            
    except Exception as e:
        error_msg = f"❌ Failed to reload tools: {str(e)}"
        logger.error(error_msg)
        import traceback
        traceback.print_exc()
        return error_msg
