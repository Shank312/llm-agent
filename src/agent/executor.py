

class ToolExecutor:
    def __init__(self, tools):
        self.tools = {tool.name: tool for tool in tools}

    def execute(self, action):
        tool_name = action["type"]
        tool_input = action.get("input", "")

        if tool_name not in self.tools:
            return "Unknown tool"

        return self.tools[tool_name].run(tool_input)