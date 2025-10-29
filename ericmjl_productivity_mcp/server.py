"""MCP server for personal productivity prompts, resources, and tools."""

import asyncio
import json
import random

from fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("personal-productivity-mcp")


# Prompts
@mcp.prompt()
def task_prioritization(task_list: str = "your tasks") -> str:
    """Help prioritize tasks by urgency, importance, energy levels, and dependencies."""
    return f"""You are a productivity expert. Help me prioritize my tasks by considering:
1. Urgency (deadlines, time-sensitive)
2. Importance (impact on goals, values)
3. Energy levels required
4. Dependencies between tasks

Please analyze this task list: {task_list}
Provide a prioritized order with reasoning for each task."""


@mcp.prompt()
def log_progress() -> str:
    """Document current progress and create a comprehensive work log for future reference."""
    return """You are helping me create a comprehensive work log to capture all progress made during our current session. Follow these steps:

1. **Review our conversation**: Analyze everything we've accomplished, including:
   - Code changes and implementations
   - Problem-solving approaches taken
   - Decisions made and their rationale
   - Challenges encountered and how they were resolved
   - Key learnings and insights gained

2. **Create or update WORKLOG.md**:
   - Read the existing WORKLOG.md file (create it if it doesn't exist)
   - Add a new timestamped entry with today's date
   - Structure the entry with clear sections for easy future reference

3. **Document structure should include**:
   - **Date & Session Summary**: Brief overview of what was accomplished
   - **Code Changes**: Specific files modified, functions added/changed, architectural decisions
   - **Problem Solving**: Issues encountered, debugging steps, solutions implemented
   - **Key Learnings**: Important insights, patterns discovered, best practices identified
   - **Next Steps**: Clear action items and priorities for future sessions
   - **Context Notes**: Any important context that would help pick up where we left off

4. **Focus on actionable continuity**: Write entries that will help you (or another AI) quickly understand the current state and continue work effectively.

5. **Confirm completion**: Tell me what you documented and highlight the key points for future reference.

This work log serves as a bridge between sessions, ensuring no progress is lost and context is preserved for seamless continuation."""


@mcp.prompt()
def remember() -> str:
    """Capture learnings and instructions from conversation to AGENTS.md."""
    return """You are tasked with capturing important learnings and instructions from our conversation and adding them to AGENTS.md. Follow these steps:

1. **Review the conversation**: Look through our recent conversation for:
   - User preferences and workflow patterns
   - Important decisions or configurations
   - Code patterns or implementation details
   - Project structure insights
   - Testing approaches or dependencies

2. **Categorize the content** using these sections:
   - **User Preferences**: Preferences, likes/dislikes, workflow habits
   - **Project Structure**: File organization, directory structure, architecture decisions
   - **Code Patterns**: Implementation patterns, coding style, best practices
   - **Dependencies**: Package requirements, external tools, integrations
   - **Testing**: Testing strategies, frameworks, approaches
   - **Development Workflow**: General development processes, git workflows, deployment

3. **Update AGENTS.md**:
   - Read the existing AGENTS.md file (create it if it doesn't exist)
   - Add a timestamped entry to the appropriate section
   - Use this format: `- [YYYY-MM-DD HH:MM] Description of what was learned`
   - If a section doesn't exist, create it with a proper markdown header

4. **Confirm what you remembered**: Tell me what you added to AGENTS.md and which section you placed it in.

Focus on capturing actionable insights that will help future AI agents understand the project context and user preferences."""  # noqa: E501


@mcp.prompt()
def git_branch_and_stage() -> str:
    """Create a new branch and stage all changes based on a diff."""
    return """You are helping the user create a new git branch and stage their changes. Follow these steps:

1. **Review the diff**: Examine the changes provided to understand what modifications were made.

2. **Confirm branch creation**: Ask the user which branch they want to create the new branch from. Default to creating from the current branch unless they specify otherwise.

3. **Generate branch name**: Based on the changes in the diff, suggest an appropriate branch name that clearly describes the work (e.g., 'add-login-feature', 'fix-api-timeout', 'refactor-database-layer').

4. **Create the branch**: Use `git checkout -b <branch-name>` to create and switch to the new branch.

5. **Stage all changes**: Run `git add .` or `git add -A` to stage all the changes.

6. **Confirm completion**: Let the user know the branch was created and changes were staged, but NOT committed yet.

Important: Do NOT commit the changes - only stage them. The user will commit when ready."""


# Resources
@mcp.resource("resource://productivity_methods")
def productivity_methods() -> str:
    """Collection of proven productivity methodologies."""
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
    return json.dumps(content, indent=2)


@mcp.resource("resource://focus_tips")
def focus_tips() -> str:
    """Actionable tips for improving focus and concentration."""
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
    return json.dumps(content, indent=2)


@mcp.resource("resource://energy_management")
def energy_management() -> str:
    """Guidance on managing personal energy throughout the day."""
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
    return json.dumps(content, indent=2)


# Tools
@mcp.tool()
def create_task(task: str, priority: str = "medium", category: str = "general") -> str:
    """Creates a new task with specified priority and category."""
    task_id = f"task_{random.randint(1000, 9999)}"
    return f"Created task '{task}' with ID {task_id}, priority: {priority}, category: {category}"


@mcp.tool()
def time_block(start_time: str, duration_minutes: int, activity: str) -> str:
    """Creates a time block for focused work on a specific activity."""
    return (
        f"Time block created: {start_time} for {duration_minutes} minutes - {activity}"
    )


@mcp.tool()
def productivity_score(
    completed_tasks: int, planned_tasks: int, focus_time_minutes: int
) -> str:
    """Calculates a productivity score based on task completion and focus time."""
    completion_rate = (
        (completed_tasks / planned_tasks * 100) if planned_tasks > 0 else 0
    )
    focus_hours = focus_time_minutes / 60
    score = min(100, (completion_rate * 0.7) + (focus_hours * 2))

    return f"Productivity Score: {score:.1f}/100\nCompletion Rate: {completion_rate:.1f}%\nFocus Time: {focus_hours:.1f} hours"


async def run_server_stdio() -> None:
    """Run the MCP server using stdio transport."""
    await mcp.run()


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
        print(f"HTTP transport not yet implemented. Use stdio transport instead.")

    # FastMCP handles the event loop internally
    mcp.run()


if __name__ == "__main__":
    run_server()
