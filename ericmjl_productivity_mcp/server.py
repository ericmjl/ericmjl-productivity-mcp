"""MCP server for personal productivity prompts, resources, and tools."""

import asyncio
import json
import random

from fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("personal-productivity-mcp")


def _get_issue_presentation_instructions() -> str:
    """Shared instructions for presenting issues to users in rank order."""
    return """**Walk Through Issues with User** (DO NOT OVERWHELM):
   - **CRITICAL: Present issues ONE AT A TIME, not in groups**
   - **Present issues in rank order from most critical to least critical**
   - Start with the single most critical issue first
   - **Present only ONE issue at a time** - wait for user's response before presenting the next issue
   - After presenting one issue, wait for the user to respond before moving to the next
   - Do NOT present multiple issues together, even if they're the same priority level
   - For each issue, clearly explain:
     - What the issue is
     - Where it occurs (file and line numbers, if applicable)
     - Why it's a concern
     - Suggested fix or improvement
   - **After addressing critical and high priority issues, ask the user** if they want to continue with medium/low priority items
   - If there are many issues, focus on the most impactful ones first, but still present them one at a time
   - **Respect user's decision** on each item:
     - If user agrees it's an issue, note it appropriately
     - If user disagrees or wants to keep it as-is, accept their decision and move on
     - If user wants more context, provide additional explanation
     - If user wants to stop or skip lower priority items, respect that
   - Don't be pushy - the user has final say on what needs to be addressed
   - **Remember: ONE issue per interaction, wait for user response, then proceed to the next issue**"""


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
   - Use this format: `- Description of what was learned`
   - If a section doesn't exist, create it with a proper markdown header

4. **Confirm what you remembered**: Tell me what you added to AGENTS.md and which section you placed it in.

Focus on capturing actionable insights that will help future AI agents understand the project context and user preferences."""  # noqa: E501


@mcp.prompt()
def correction(thing: str, different_thing: str) -> str:
    """Record a correction in AGENTS.md and then continue with the corrected approach."""
    return f"""You have been corrected. Follow these steps:

1. **Understand the correction**:
   - You were about to do or were doing: {thing}
   - Instead, you should do: {different_thing}

2. **Record the correction in AGENTS.md**:
   - Read the existing AGENTS.md file (create it if it doesn't exist)
   - Find or create a "Corrections" section (or add to "User Preferences" if more appropriate)
   - Add a timestamped entry documenting this correction:
     - Format: `- Do not {thing}. Instead, {different_thing}.`
   - This helps future AI agents avoid the same mistake

3. **Apply the correction immediately**:
   - Stop doing or planning to do: {thing}
   - Start doing or planning to do: {different_thing}

4. **Continue your work**:
   - After recording the correction, immediately continue with the corrected approach
   - Do not ask for confirmation - just proceed with {different_thing}
   - Maintain context and continue from where you left off

5. **Confirm briefly**: Tell me you've recorded the correction and are continuing with the corrected approach.

The goal is to quickly course-correct, document the learning, and seamlessly continue with the right approach."""


@mcp.prompt()
def add_markdownlint_rules() -> str:
    """Add markdownlint rules to AGENTS.md for consistent markdown formatting."""
    return """You are tasked with adding markdownlint rules to AGENTS.md to ensure
consistent markdown formatting across the project. Follow these steps:

1. **Read AGENTS.md**: Read the existing AGENTS.md file (create it if it doesn't
   exist).

2. **Find or create the Development Workflow section**: Look for a "Development
   Workflow" section. If it doesn't exist, create it with a proper markdown
   header (## Development Workflow).

3. **Add the markdownlint rules**: Add the following markdownlint rules:

   - **Markdownlint Rules**: Always run markdownlint on any
     markdown files that are edited or created. This ensures consistent
     formatting and catches common markdown issues. The workflow is:
     1. After editing any markdown file (`.md`), run `markdownlint <file-path>`
        to check for issues.
     2. If markdownlint is not found on PATH, install it using
        `pixi global install markdownlint-cli`. This installs it globally via
        pixi and makes it available on PATH.
     3. Always fix any issues that markdownlint raises before considering the
        task complete. Common issues include: trailing whitespace, missing
        blank lines around headers, improper list formatting, and line length
        violations.
     4. For multiple files, you can run `markdownlint "**/*.md"` to check all
        markdown files in the project, or specify individual files.
     5. If markdownlint reports errors, fix them immediately and re-run
        markdownlint to verify the fixes.

4. **Run markdownlint on AGENTS.md**: After adding the rules, run
   `markdownlint AGENTS.md` to check for any formatting issues. If
   markdownlint is not available, install it first using
   `pixi global install markdownlint-cli`.

5. **Fix any issues**: If markdownlint reports any errors, fix them
   immediately. Common fixes include:
   - Breaking long lines (keep lines under 80 characters)
   - Adding blank lines around headers
   - Fixing list formatting
   - Removing trailing whitespace

6. **Verify**: Re-run markdownlint to ensure all issues are resolved.

7. **Confirm completion**: Tell me that you've added the markdownlint rules to
   AGENTS.md and verified that the file passes markdownlint checks.

This ensures that all future markdown files in the project will be consistently
formatted and checked for quality."""


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


@mcp.prompt()
def debug_github_actions(workflow_url: str) -> str:
    """Debug GitHub Actions workflow failures by analyzing logs and providing actionable solutions."""
    return f"""You are helping me debug a failed GitHub Actions workflow. Follow these steps to systematically analyze and resolve the issue:

1. **Extract workflow information**: Parse the provided URL to identify:
   - Repository owner and name
   - Workflow run ID
   - Workflow name
   - Branch/commit that triggered the run

2. **Fetch workflow logs using GitHub CLI**:
   - Use `gh run list` to verify the workflow run exists
   - Use `gh run view <run-id>` to get detailed run information
   - Use `gh run view <run-id> --log` to download and display the full logs
   - Use `gh run view <run-id> --log-failed` to focus on failed job logs

3. **Analyze the failure**:
   - Identify which job(s) failed and at what step
   - Look for error messages, exit codes, and stack traces
   - Check for common issues: dependency problems, permission errors, timeout issues, resource constraints
   - Examine the workflow configuration and environment setup

4. **Provide debugging guidance**:
   - Explain what went wrong in simple terms
   - Suggest specific fixes or configuration changes
   - Provide commands or code snippets to resolve the issue
   - Recommend preventive measures to avoid similar failures

5. **Context-aware solutions**:
   - Consider the project type (Python, Node.js, etc.) and suggest appropriate fixes
   - Check for recent changes that might have caused the failure
   - Suggest workflow improvements or optimizations

6. **Follow-up actions**:
   - Recommend next steps for testing the fix
   - Suggest monitoring or alerting improvements
   - Provide guidance on preventing similar issues

Workflow URL: {workflow_url}

Focus on providing actionable, specific solutions rather than generic troubleshooting advice. Use the GitHub CLI commands to gather comprehensive information about the failure."""


@mcp.prompt()
def devdigest(timeframe: str = "last week") -> str:
    """Generate a comprehensive development digest using GitHub CLI to summarize commits, issues, PRs, and activity."""
    return f"""You are helping me create a comprehensive development digest that summarizes my GitHub activity and accomplishments. Follow these steps to gather and analyze my development work:

1. **Gather GitHub Activity Data** using the GitHub CLI:
   - **Commits**: Use `gh api /user/events` to get recent activity, or `gh log --oneline --since="{timeframe}"` for commit history
   - **Pull Requests**: Use `gh pr list --author=@me --state=all --limit=20` to get recent PRs
   - **Issues**: Use `gh issue list --author=@me --state=all --limit=20` to get issues I've created or commented on
   - **Comments**: Use `gh api /user/issues/comments` and `gh api /user/pulls/comments` for recent comments
   - **Repositories**: Use `gh repo list --limit=10` to see recent repository activity
   - **Stars/Activity**: Use `gh api /user/starred` for recently starred repositories

2. **Analyze the Data** and identify:
   - **Code Contributions**: Commits made, lines added/removed, files changed
   - **Pull Request Activity**: PRs created, reviewed, merged, or closed
   - **Issue Management**: Issues created, resolved, or participated in
   - **Repository Work**: New repos created, existing repos updated
   - **Community Engagement**: Comments, reviews, discussions participated in
   - **Learning & Discovery**: Repositories starred, new technologies explored

3. **Create a Structured Dev Log** with these sections:
   - **📊 Summary Stats**: Total commits, PRs, issues, repositories worked on
   - **🚀 Major Accomplishments**: Significant features, bug fixes, or improvements
   - **🔧 Technical Work**: Code refactoring, architecture changes, tooling improvements
   - **🤝 Collaboration**: PR reviews, issue discussions, community contributions
   - **📚 Learning & Growth**: New technologies, patterns, or skills demonstrated
   - **🎯 Project Highlights**: Notable projects or repositories with significant activity
   - **📈 Productivity Insights**: Patterns in work habits, peak activity times, project focus areas

4. **Format the Output** as a markdown document that:
   - Uses clear headings and bullet points
   - Includes specific metrics and numbers where possible
   - Highlights the most impactful work
   - Shows progression and growth over time
   - Provides context for why certain work was important

5. **Timeframe Context**: Focus on activity from {timeframe}, but also note any longer-term trends or patterns.

6. **Save the Digest**: Create or update a file called `DEV_DIGEST.md` with the comprehensive summary.

The goal is to create a professional, insightful summary that showcases development productivity, technical growth, and meaningful contributions to projects and the community. Use the GitHub CLI to gather as much relevant data as possible, then synthesize it into a compelling narrative of development accomplishments."""


@mcp.prompt()
def code_review(pr_url: str) -> str:
    """Perform a comprehensive code review on a pull request using GitHub CLI."""
    issue_instructions = _get_issue_presentation_instructions()
    return f"""You are helping me perform a thorough code review on a pull request. Follow these steps systematically:

1. **Checkout the PR using GitHub CLI**:
   - Parse the PR URL to extract repository and PR number
   - Use `gh pr checkout <pr-number>` to checkout the PR branch locally
   - If needed, use `gh pr view <pr-number>` to get PR details first
   - Ensure you're on the correct branch before proceeding

2. **Study the Diff**:
   - Use `git diff main...HEAD` or `git diff origin/main...HEAD` to see all changes
   - Use `gh pr diff <pr-number>` to view the PR diff via GitHub CLI
   - Review all modified, added, and deleted files
   - Understand the context and purpose of the changes
   - Note the scope and size of the changes

3. **Perform Comprehensive Code Review** on the following aspects:

   **a) Code Quality & Style**:
   - Consistency with project coding standards and style guide
   - Proper naming conventions (variables, functions, classes)
   - Code readability and clarity
   - Appropriate use of comments and documentation
   - Code organization and structure

   **b) Duplicated Code**:
   - Identify any code duplication within the PR
   - Check for duplication with existing codebase
   - Suggest refactoring opportunities to reduce duplication
   - Look for opportunities to extract common functionality

   **c) Potential Bugs**:
   - Logic errors and edge cases
   - Null pointer/null reference issues
   - Off-by-one errors and boundary conditions
   - Race conditions and concurrency issues
   - Memory leaks or resource management problems
   - Type mismatches and incorrect type handling
   - Error handling and exception management

   **d) Security Concerns**:
   - SQL injection vulnerabilities
   - Cross-site scripting (XSS) risks
   - Authentication and authorization issues
   - Sensitive data exposure
   - Input validation and sanitization
   - Dependency vulnerabilities

   **e) Performance Issues**:
   - Inefficient algorithms or data structures
   - Unnecessary database queries or API calls
   - Missing caching opportunities
   - Memory or CPU intensive operations
   - N+1 query problems

   **f) Testing**:
   - Adequacy of test coverage
   - Test quality and maintainability
   - Missing test cases for edge cases
   - Test organization and structure

   **g) Architecture & Design**:
   - Adherence to design patterns and principles
   - Separation of concerns
   - Dependency management and coupling
   - Scalability considerations
   - Maintainability and extensibility

   **h) Non-obvious Issues**:
   - Subtle bugs that might not be immediately apparent
   - Code that might break in edge cases
   - Assumptions that aren't explicitly documented
   - Complex logic that might need refactoring
   - Code that might be difficult to maintain or understand later
   - Interactions with other parts of the codebase that might be affected

   **i) Documentation**:
   - Missing or incomplete documentation
   - Outdated comments or docstrings
   - README updates if needed
   - API documentation updates

   **j) Dependencies & Configuration**:
   - New dependencies and their necessity
   - Version compatibility issues
   - Configuration changes and their impact
   - Environment variable or secret management

4. **Organize Findings**:
   - Categorize all findings by the aspects above
   - **Rank order all issues by priority** (critical, high, medium, low)
   - Critical: Security vulnerabilities, bugs that will cause failures, data loss risks
   - High: Significant bugs, performance issues, architectural problems
   - Medium: Code quality issues, maintainability concerns, missing tests
   - Low: Style issues, minor improvements, documentation gaps
   - Group related issues together
   - Note positive aspects and good practices observed

5. {issue_instructions}
   - Note: When noting issues for the review, document them appropriately for the PR review

6. **Provide Summary**:
   - After reviewing all categories, provide a summary of:
     - Total number of issues found (by priority)
     - Key recommendations
     - Positive feedback on good practices
     - Overall assessment of the PR

PR URL: {pr_url}

Focus on being thorough but constructive. The goal is to improve code quality while respecting the author's work and the user's judgment on what needs to be changed."""


@mcp.prompt()
def present_issues() -> str:
    """Present a list of issues to the user in rank order, one by one."""
    issue_instructions = _get_issue_presentation_instructions()
    return f"""You have a list of issues (from any context - code review, linting, testing, analysis, etc.) that need to be presented to the user. Follow these steps:

1. **Identify and Rank Order Issues**:
   - Review the list of issues you have (from previous context or analysis)
   - **Rank order all issues by priority** (critical, high, medium, low):
     - Critical: Security vulnerabilities, bugs that will cause failures, data loss risks
     - High: Significant bugs, performance issues, architectural problems
     - Medium: Code quality issues, maintainability concerns, missing tests
     - Low: Style issues, minor improvements, documentation gaps
   - If issues don't have explicit priorities, infer them based on their nature and impact

2. {issue_instructions}

3. **Provide Summary**:
   - After going through all issues (or when the user stops), provide a summary:
     - Total number of issues found (by priority)
     - Number of issues addressed vs. skipped
     - Key recommendations or next steps

The context of where these issues came from is unknown - they could be from code review, static analysis, testing, manual inspection, or any other source. Focus on presenting them clearly and systematically, respecting the user's decisions on each item."""


@mcp.prompt()
def frontend_aesthetics() -> str:
    """Apply distinctive, creative frontend design principles to avoid generic AI-generated aesthetics."""
    return """When building frontend interfaces, avoid converging toward generic, "on distribution" outputs that create what users call the "AI slop" aesthetic. Instead, create creative, distinctive frontends that surprise and delight. Apply these principles:

**Typography**:
- Choose fonts that are beautiful, unique, and interesting
- Avoid generic fonts like Arial, Inter, and Roboto
- Opt for distinctive typographic choices that elevate the frontend's aesthetics
- Vary your font selections across different projects - don't default to common choices like Space Grotesk

**Color & Theme**:
- Commit to a cohesive aesthetic with CSS variables for consistency
- Use dominant colors with sharp accents rather than timid, evenly-distributed palettes
- Draw inspiration from IDE themes and cultural aesthetics
- Vary between light and dark themes across different projects
- Avoid clichéd color schemes, particularly purple gradients on white backgrounds

**Motion & Animation**:
- Use animations for effects and micro-interactions
- Prioritize CSS-only solutions for HTML
- Use Motion library for React when available
- Focus on high-impact moments: one well-orchestrated page load with staggered reveals (using animation-delay) creates more delight than scattered micro-interactions

**Backgrounds & Atmosphere**:
- Create atmosphere and depth rather than defaulting to solid colors
- Layer CSS gradients, use geometric patterns, or add contextual effects that match the overall aesthetic
- Think about how backgrounds contribute to the overall visual narrative

**Avoid Generic Patterns**:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Clichéd color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

**Creative Interpretation**:
- Interpret creatively and make unexpected choices that feel genuinely designed for the context
- Think outside the box - avoid converging on common choices across generations
- Each project should have its own distinctive character and aesthetic identity

Apply these principles to create frontends that feel thoughtfully designed rather than generically generated. Make creative, distinctive choices that surprise and delight users."""


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
