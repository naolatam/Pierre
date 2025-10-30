from langchain.tools import tool

@tool("test", return_direct=False)
def test(time_info: str) -> str:
    """
    This tool is for testing tool chaining and composition.
    
    IMPORTANT: Before calling this tool, you MUST first call the 'get_time' tool 
    to get the current time, then pass that time as the 'time_info' parameter.
    
    This demonstrates multi-step agent reasoning where the agent:
    1. First calls get_time to retrieve current time
    2. Then calls this test tool with the time result
    
    Args:
        time_info: The current time string obtained from the get_time tool
    
    Default agent workflows:
    - User: "Run the test"
    - Agent: Calls get_time to get current time -> result: "14:35 PM"
    - Agent: Then calls test tool with time_info="14:35 PM"
    

        
    This allows the agent to orchestrate multi-step tool calls.
    """
    try:
        # Process the time info received from the agent
        return f"🧪 Test Tool Results:\n" \
               f"━━━━━━━━━━━━━━━━━━━━\n" \
               f"✅ Successfully received time from agent\n" \
               f"📅 Time provided: {time_info}\n" \
               f"━━━━━━━━━━━━━━━━━━━━\n" \
               f"This demonstrates multi-step agent tool calling!\n" \
               f"The agent first called get_time, then passed the result here."
    except Exception as e:
        return f"❌ Test tool failed: {str(e)}"
