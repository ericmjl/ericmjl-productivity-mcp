"""MCP server for personal productivity prompts, resources, and tools."""

import asyncio
import json
import random
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListPromptsRequest,
    ListPromptsResult,
    ListResourcesRequest,
    ListResourcesResult,
    ListToolsRequest,
    ListToolsResult,
    Prompt,
    PromptArgument,
    ReadResourceRequest,
    ReadResourceResult,
    Resource,
    TextContent,
    Tool,
)

# Initialize the MCP server
server = Server("personal-productivity-mcp")


# Prompts
@server.list_prompts()
async def list_prompts() -> ListPromptsResult:
    """List available productivity prompts."""
    return ListPromptsResult(
        prompts=[
            Prompt(
                name="task_prioritization",
                description="Help prioritize tasks by urgency, importance, energy levels, and dependencies",
                arguments=[
                    PromptArgument(
                        name="task_list",
                        description="List of tasks to prioritize",
                        required=True,
                    )
                ],
            ),
            Prompt(
                name="focus_session",
                description="Create an optimal focus session with environmental optimizations and break timing",
                arguments=[
                    PromptArgument(
                        name="duration_minutes",
                        description="Desired focus session duration in minutes",
                        required=False,
                    )
                ],
            ),
            Prompt(
                name="daily_reflection",
                description="Guide through end-of-day productivity reflection and planning",
                arguments=[
                    PromptArgument(
                        name="completed_tasks",
                        description="List of tasks completed today",
                        required=False,
                    )
                ],
            ),
        ]
    )


@server.get_prompt()
async def get_prompt(name: str, arguments: Dict[str, str]) -> str:
    """Get a specific productivity prompt."""
    if name == "task_prioritization":
        task_list = arguments.get("task_list", "your tasks")
        return f"""You are a productivity expert. Help me prioritize my tasks by considering:
1. Urgency (deadlines, time-sensitive)
2. Importance (impact on goals, values)
3. Energy levels required
4. Dependencies between tasks

Please analyze this task list: {task_list}
Provide a prioritized order with reasoning for each task."""

    elif name == "focus_session":
        duration = arguments.get("duration_minutes", "90")
        return f"""Help me create an optimal focus session by:
1. Identifying my most important task for the next {duration} minutes
2. Suggesting environmental optimizations (noise, lighting, tools)
3. Recommending break timing and activities
4. Providing motivation and accountability check-ins

Focus on deep work principles and minimizing distractions."""

    elif name == "daily_reflection":
        completed = arguments.get("completed_tasks", "my completed tasks")
        return f"""Guide me through a productive daily reflection by asking about:
1. What went well today and why
2. What challenges I faced and how I handled them
3. What I learned about my productivity patterns
4. What I want to improve tomorrow
5. Gratitude and wins to celebrate

Help me extract insights and plan for better tomorrow based on: {completed}"""

    else:
        raise ValueError(f"Unknown prompt: {name}")


# Resources
@server.list_resources()
async def list_resources() -> ListResourcesResult:
    """List available productivity resources."""
    return ListResourcesResult(
        resources=[
            Resource(
                uri="resource://productivity_methods",
                name="Productivity Methods",
                description="Collection of proven productivity methodologies",
                mimeType="application/json",
            ),
            Resource(
                uri="resource://focus_tips",
                name="Focus Tips",
                description="Actionable tips for improving focus and concentration",
                mimeType="application/json",
            ),
            Resource(
                uri="resource://energy_management",
                name="Energy Management",
                description="Guidance on managing personal energy throughout the day",
                mimeType="application/json",
            ),
        ]
    )


@server.read_resource()
async def read_resource(uri: str) -> ReadResourceResult:
    """Read a specific productivity resource."""
    if uri == "resource://productivity_methods":
        content = {
            "methods": [
                {
                    "name": "Getting Things Done (GTD)",
                    "description": "A workflow methodology for organizing tasks and projects",
                    "key_principles": [
                        "Capture",
                        "Clarify",
                        "Organize",
                        "Reflect",
                        "Engage",
                    ],
                },
                {
                    "name": "Pomodoro Technique",
                    "description": "Time management method using 25-minute focused work sessions",
                    "key_principles": [
                        "Work in sprints",
                        "Take breaks",
                        "Track progress",
                    ],
                },
                {
                    "name": "Eisenhower Matrix",
                    "description": "Prioritization framework based on urgency and importance",
                    "key_principles": [
                        "Urgent & Important",
                        "Not Urgent & Important",
                        "Urgent & Not Important",
                        "Not Urgent & Not Important",
                    ],
                },
            ]
        }
    elif uri == "resource://focus_tips":
        content = {
            "tips": [
                "Use noise-canceling headphones or ambient sounds to block distractions",
                "Put your phone in another room or use focus mode",
                "Set up a dedicated workspace with good lighting",
                "Take regular breaks every 25-45 minutes",
                "Use the 'two-minute rule' for quick tasks",
                "Batch similar activities together",
                "Practice mindfulness meditation to improve attention span",
            ]
        }
    elif uri == "resource://energy_management":
        content = {
            "peak_hours": "Identify your natural energy peaks (usually morning or afternoon)",
            "energy_types": {
                "physical": "Exercise, nutrition, sleep quality",
                "emotional": "Stress management, relationships, mood",
                "mental": "Learning, problem-solving, creativity",
                "spiritual": "Purpose, values, meaning",
            },
            "recovery_strategies": [
                "Power naps (10-20 minutes)",
                "Short walks in nature",
                "Deep breathing exercises",
                "Hydration and healthy snacks",
            ],
        }
    else:
        raise ValueError(f"Unknown resource: {uri}")

    return ReadResourceResult(
        contents=[TextContent(type="text", text=json.dumps(content, indent=2))]
    )


# Tools
@server.list_tools()
async def list_tools() -> ListToolsResult:
    """List available productivity tools."""
    return ListToolsResult(
        tools=[
            Tool(
                name="create_task",
                description="Creates a new task with specified priority and category",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "task": {
                            "type": "string",
                            "description": "Description of the task",
                        },
                        "priority": {
                            "type": "string",
                            "enum": ["low", "medium", "high", "urgent"],
                            "description": "Priority level",
                            "default": "medium",
                        },
                        "category": {
                            "type": "string",
                            "description": "Task category (work, personal, health, learning, etc.)",
                            "default": "general",
                        },
                    },
                    "required": ["task"],
                },
            ),
            Tool(
                name="time_block",
                description="Creates a time block for focused work on a specific activity",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "start_time": {
                            "type": "string",
                            "description": "Start time in HH:MM format",
                        },
                        "duration_minutes": {
                            "type": "integer",
                            "description": "Duration in minutes",
                        },
                        "activity": {
                            "type": "string",
                            "description": "Description of the planned activity",
                        },
                    },
                    "required": ["start_time", "duration_minutes", "activity"],
                },
            ),
            Tool(
                name="productivity_score",
                description="Calculates a productivity score based on task completion and focus time",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "completed_tasks": {
                            "type": "integer",
                            "description": "Number of tasks completed",
                        },
                        "planned_tasks": {
                            "type": "integer",
                            "description": "Number of tasks planned",
                        },
                        "focus_time_minutes": {
                            "type": "integer",
                            "description": "Total focused work time in minutes",
                        },
                    },
                    "required": [
                        "completed_tasks",
                        "planned_tasks",
                        "focus_time_minutes",
                    ],
                },
            ),
        ]
    )


@server.call_tool()
async def call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Execute a productivity tool."""
    if name == "create_task":
        task = arguments["task"]
        priority = arguments.get("priority", "medium")
        category = arguments.get("category", "general")
        task_id = f"task_{random.randint(1000, 9999)}"

        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Created task '{task}' with ID {task_id}, priority: {priority}, category: {category}",
                )
            ]
        )

    elif name == "time_block":
        start_time = arguments["start_time"]
        duration_minutes = arguments["duration_minutes"]
        activity = arguments["activity"]

        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Time block created: {start_time} for {duration_minutes} minutes - {activity}",
                )
            ]
        )

    elif name == "productivity_score":
        completed_tasks = arguments["completed_tasks"]
        planned_tasks = arguments["planned_tasks"]
        focus_time_minutes = arguments["focus_time_minutes"]

        completion_rate = (
            (completed_tasks / planned_tasks * 100) if planned_tasks > 0 else 0
        )
        focus_hours = focus_time_minutes / 60
        score = min(100, (completion_rate * 0.7) + (focus_hours * 2))

        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Productivity Score: {score:.1f}/100\nCompletion Rate: {completion_rate:.1f}%\nFocus Time: {focus_hours:.1f} hours",
                )
            ]
        )

    else:
        raise ValueError(f"Unknown tool: {name}")


async def run_server_stdio() -> None:
    """Run the MCP server using stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )


async def run_server_http(port: int = 9247) -> None:
    """Run the MCP server using HTTP transport."""
    # Note: HTTP transport would require additional setup
    # For now, we'll use stdio as the primary transport
    print(f"HTTP transport not yet implemented. Use stdio transport instead.")
    await run_server_stdio()


def run_server(
    transport: str = "stdio", port: int = 9247, auto_reload: bool = True
) -> None:
    """Run the MCP server with specified transport and configuration.

    Args:
        transport: Transport method ("stdio" or "http")
        port: Port number for http transport
        auto_reload: Enable auto-reload for development (not implemented yet)
    """
    if transport == "http":
        asyncio.run(run_server_http(port))
    else:
        asyncio.run(run_server_stdio())


if __name__ == "__main__":
    run_server()
