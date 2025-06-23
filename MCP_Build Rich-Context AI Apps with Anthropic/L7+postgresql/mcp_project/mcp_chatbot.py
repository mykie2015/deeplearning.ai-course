from dotenv import load_dotenv
import openai
import os
import json as json_module
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client
from typing import List, Dict, TypedDict
from contextlib import AsyncExitStack
import json
import asyncio
import nest_asyncio

nest_asyncio.apply()

load_dotenv()

class MCP_ChatBot:
    def __init__(self):
        self.openai_client = openai.OpenAI(
            api_key=os.environ.get("OPENAI_API_KEY"),
            base_url=os.environ.get("OPENAI_API_BASE")
        )
        self.exit_stack = AsyncExitStack()
        # Tools list required for OpenAI API
        self.available_tools = []
        # Prompts list for quick display 
        self.available_prompts = []
        # Sessions dict maps tool/prompt names or resource URIs to MCP client sessions
        self.sessions = {}

    async def connect_to_server(self, server_name, server_config):
        try:
            server_params = StdioServerParameters(**server_config)
            stdio_transport = await self.exit_stack.enter_async_context(
                stdio_client(server_params)
            )
            read, write = stdio_transport
            session = await self.exit_stack.enter_async_context(
                ClientSession(read, write)
            )
            await session.initialize()
            
            try:
                # List available tools
                response = await session.list_tools()
                for tool in response.tools:
                    self.sessions[tool.name] = session
                    self.available_tools.append({
                        "name": tool.name,
                        "description": tool.description,
                        "input_schema": tool.inputSchema
                    })
            
                # List available prompts
                prompts_response = await session.list_prompts()
                if prompts_response and prompts_response.prompts:
                    for prompt in prompts_response.prompts:
                        self.sessions[prompt.name] = session
                        self.available_prompts.append({
                            "name": prompt.name,
                            "description": prompt.description,
                            "arguments": prompt.arguments
                        })
                        
                # List available resources
                resources_response = await session.list_resources()
                if resources_response and resources_response.resources:
                    for resource in resources_response.resources:
                        resource_uri = str(resource.uri)
                        self.sessions[resource_uri] = session
                        # Also map the base URI pattern for dynamic resources
                        if "://{" in resource_uri:
                            base_uri = resource_uri.split("://")[0] + "://"
                            self.sessions[base_uri] = session
            
            except Exception as e:
                print(f"Error {e}")
                
        except Exception as e:
            print(f"Error connecting to {server_name}: {e}")

    async def connect_to_servers(self):
        try:
            with open("server_config.json", "r") as file:
                data = json.load(file)
            servers = data.get("mcpServers", {})
            for server_name, server_config in servers.items():
                await self.connect_to_server(server_name, server_config)
        except Exception as e:
            print(f"Error loading server config: {e}")
            raise

    async def process_query(self, query):
        messages = [{'role':'user', 'content':query}]
        
        # Convert tools to OpenAI format
        openai_tools = []
        for tool in self.available_tools:
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": tool["name"],
                    "description": tool["description"],
                    "parameters": tool["input_schema"]
                }
            })
        
        while True:
            response = self.openai_client.chat.completions.create(
                max_completion_tokens=2024,
                model=os.environ.get("DEFAULT_LLM_MODEL", "o4-mini"),
                tools=openai_tools if openai_tools else None,
                messages=messages
            )
            
            message = response.choices[0].message
            
            if message.content:
                print(message.content)
                
            if message.tool_calls:
                # Add assistant message with tool calls
                messages.append({
                    "role": "assistant", 
                    "content": message.content,
                    "tool_calls": message.tool_calls
                })
                
                # Process each tool call
                for tool_call in message.tool_calls:
                    tool_name = tool_call.function.name
                    tool_args = json_module.loads(tool_call.function.arguments)
                    
                    print(f"🛠️  Calling tool `{tool_name}` with arguments: {tool_args}")
                    
                    # Get session and call tool
                    session = self.sessions.get(tool_name)
                    if not session:
                        print(f"Tool '{tool_name}' not found.")
                        break
                        
                    result = await session.call_tool(tool_name, arguments=tool_args)
                    
                    print(f"✅ Tool `{tool_name}` finished.")
                    
                    # Prepare tool result content as string
                    if hasattr(result, 'content'):
                        tool_content = result.content
                    else:
                        try:
                            tool_content = json.dumps(result, ensure_ascii=False)
                        except Exception:
                            tool_content = str(result)
                    
                    # Add tool result message
                    messages.append({
                        "role": "tool",
                        "tool_call_id": tool_call.id,
                        "content": tool_content
                    })
                
                # Continue the loop to let AI process tool results
                continue
            else:
                # No more tool calls, conversation is complete
                print("\\n✍️  All tools have been run. Synthesizing the final answer...")
                if message.content:
                    print(message.content)
                break

    async def get_resource(self, resource_uri):
        print(f"📄 Accessing resource: {resource_uri}")
        session = self.sessions.get(resource_uri)
        
        # If exact URI not found, look for a matching dynamic resource session
        if not session:
            for uri, sess in self.sessions.items():
                if "://{" in uri and resource_uri.startswith(uri.split("://")[0] + "://"):
                    session = sess
                    break
        
        if not session:
            print(f"Resource '{resource_uri}' not found.")
            return
        
        try:
            result = await session.read_resource(resource_uri)
            for content in result.contents:
                if hasattr(content, 'text'):
                    print(content.text)
                else:
                    print(str(content))
        except Exception as e:
            print(f"Error reading resource: {e}")

    async def execute_prompt(self, prompt_name, prompt_args):
        session = self.sessions.get(prompt_name)
        if not session:
            print(f"Prompt '{prompt_name}' not found.")
            return
        
        try:
            print(f"🤖 Executing prompt: '{prompt_name}'...")
            result = await session.get_prompt(prompt_name, arguments=prompt_args)
            prompt_content = ""
            for message in result.messages:
                if hasattr(message.content, 'text'):
                    prompt_content += message.content.text
                else:
                    prompt_content += str(message.content)
            
            print(f"\n--- Generated Prompt ---\n{prompt_content}\n--- End Prompt ---\n")
            await self.process_query(prompt_content)
        except Exception as e:
            print(f"Error executing prompt: {e}")

    def list_prompts(self):
        if not self.available_prompts:
            print("No prompts available.")
            return
        
        print("\nAvailable prompts:")
        for prompt in self.available_prompts:
            print(f"- {prompt['name']}: {prompt['description']}")
            if prompt.get('arguments'):
                args = ", ".join([f"{arg.name}={arg.name}" for arg in prompt['arguments']])
                print(f"  Usage: /prompt {prompt['name']} {args}")
        print()

    async def chat_loop(self):
        print("\nMCP Chatbot Started!")
        print("Type your queries or 'quit' to exit.")
        print("Use @folders to see available topics")
        print("Use @<topic> to search papers in that topic")
        print("Use /prompts to list available prompts")
        print("Use /prompt <name> <arg1=value1> to execute a prompt")
        
        while True:
            try:
                query = input("\nQuery: ").strip()
                if not query:
                    continue
        
                if query.lower() == 'quit':
                    break
                
                # Handle resource requests
                if query.startswith('@'):
                    if query == '@folders':
                        await self.get_resource("papers://folders")
                    else:
                        topic = query[1:]  # Remove @ prefix
                        await self.get_resource(f"papers://{topic}")
                    continue
                
                # Handle prompt commands
                if query.startswith('/'):
                    parts = query[1:].split(' ', 1)
                    command = parts[0]
                    
                    if command == 'prompts':
                        self.list_prompts()
                    elif command == 'prompt' and len(parts) > 1:
                        prompt_parts = parts[1].split(' ', 1)
                        prompt_name = prompt_parts[0]
                        prompt_args = {}
                        
                        if len(prompt_parts) > 1:
                            # Parse arguments like 'topic="AI research" num_papers=3'
                            args_str = prompt_parts[1]
                            
                            # Handle quoted arguments properly
                            import re
                            # Pattern to match key=value pairs, including quoted values
                            pattern = r'(\w+)=(?:"([^"]*)"|\'([^\']*)\'|(\S+))'
                            matches = re.findall(pattern, args_str)
                            
                            for match in matches:
                                key = match[0]
                                # Get the value from whichever group matched (quoted or unquoted)
                                value = match[1] or match[2] or match[3]
                                prompt_args[key] = value
                        
                        await self.execute_prompt(prompt_name, prompt_args)
                    else:
                        print("Unknown command. Use /prompts to list available prompts.")
                    continue
                    
                await self.process_query(query)
                    
            except Exception as e:
                print(f"\nError: {str(e)}")

    async def cleanup(self):
        await self.exit_stack.aclose()

async def main():
    chatbot = MCP_ChatBot()
    try:
        await chatbot.connect_to_servers()
        await chatbot.chat_loop()
    finally:
        await chatbot.cleanup()

if __name__ == "__main__":
    asyncio.run(main())