def validate_tool_call(tool_name: str, arguments: dict) -> bool:
    """Security check for agentic tool usage."""
    banned_commands = ["rm -rf", "drop table", "format", "shutdown"]
    
    arg_str = str(arguments).lower()
    for command in banned_commands:
        if command in arg_str:
            return False
    return True