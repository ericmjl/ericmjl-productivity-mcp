"""MCP server for personal productivity prompts, resources, and tools."""

import json
import random

from fastmcp import FastMCP

# Initialize the FastMCP server
mcp = FastMCP("personal-productivity-mcp")


def _get_vault_note_rules() -> str:
    """Shared rules for working with Obsidian vault notes - only link to
    existing notes."""
    return """**CRITICAL: Only Link to Existing Notes**:
   - **ONLY include notes that exist** - Never make up notes or include notes
     from outside the vault
   - **Verify existence** - Check the file system to confirm each note exists
     before including it
   - **Do NOT create or invent notes** - Only link to notes that ACTUALLY EXIST
     in the vault
   - **Do NOT include notes from outside the vault** - Only work with notes
     within the Obsidian vault
   - **Use wiki links only** - Always use [[Note Name]] format for all note
     references
   - **Double-check before finalizing** - Verify that every wiki link points to
     a note that exists"""


def _get_issue_presentation_instructions() -> str:
    """Shared instructions for presenting issues to users in rank order."""
    return """**Walk Through Issues with User** (DO NOT OVERWHELM):
   - **CRITICAL: Present issues ONE AT A TIME, not in groups**
   - **Present issues in rank order from most critical to least critical**
   - Start with the single most critical issue first
    - **Present only ONE issue at a time** - wait for user's response
      before presenting the next issue
   - After presenting one issue, wait for the user to respond before moving to the next
   - Do NOT present multiple issues together, even if they're the same priority level
   - For each issue, clearly explain:
     - What the issue is
     - Where it occurs (file and line numbers, if applicable)
     - Why it's a concern
     - Suggested fix or improvement
   - **After addressing critical and high priority issues, ask the user**
     if they want to continue with medium/low priority items
   - If there are many issues, focus on the most impactful ones first,
     but still present them one at a time
   - **Respect user's decision** on each item:
     - If user agrees it's an issue, note it appropriately
     - If user disagrees or wants to keep it as-is, accept their decision and move on
     - If user wants more context, provide additional explanation
     - If user wants to stop or skip lower priority items, respect that
   - Don't be pushy - the user has final say on what needs to be addressed
   - **Remember: ONE issue per interaction, wait for user response,
     then proceed to the next issue**"""


# Prompts
@mcp.prompt()
def task_prioritization(task_list: str = "your tasks") -> str:
    """Help prioritize tasks by urgency, importance, energy levels, and dependencies."""
    return f"""You are a productivity expert. Help me prioritize my tasks
by considering:
1. Urgency (deadlines, time-sensitive)
2. Importance (impact on goals, values)
3. Energy levels required
4. Dependencies between tasks

Please analyze this task list: {task_list}
Provide a prioritized order with reasoning for each task."""


@mcp.prompt()
def log_progress() -> str:
    """Document current progress and create a comprehensive work log
    for future reference."""
    return """You are helping me create a comprehensive work log to
capture all progress made during our current session. Follow these steps:

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
    - **Code Changes**: Specific files modified, functions added/changed,
      architectural decisions
   - **Problem Solving**: Issues encountered, debugging steps, solutions implemented
    - **Key Learnings**: Important insights, patterns discovered,
      best practices identified
   - **Next Steps**: Clear action items and priorities for future sessions
   - **Context Notes**: Any important context that would help pick up where we left off

4. **Focus on actionable continuity**: Write entries that will help you
   (or another AI) quickly understand the current state and continue
   work effectively.

5. **Confirm completion**: Tell me what you documented and highlight
   the key points for future reference.

This work log serves as a bridge between sessions, ensuring no progress
is lost and context is preserved for seamless continuation."""


@mcp.prompt()
def remember() -> str:
    """Add new content to AGENTS.md, then clean up the file for coherence."""
    return """You are tasked with adding new content to AGENTS.md and then cleaning it up to ensure coherence. Follow these steps:

1. **Wait for user content**: Do NOT review the conversation. Instead, wait for the user to provide the new content they want to add to AGENTS.md. The user will tell you what they want to remember.

2. **Add new content**: Once the user provides the content:
   - Read the existing AGENTS.md file (create it if it doesn't exist)
   - Categorize the new content into appropriate sections:
     - **User Preferences**: Preferences, likes/dislikes, workflow habits
     - **Project Structure**: File organization, directory structure, architecture decisions
     - **Code Patterns**: Implementation patterns, coding style, best practices
     - **Dependencies**: Package requirements, external tools, integrations
     - **Testing**: Testing strategies, frameworks, approaches
     - **Development Workflow**: General development processes, git workflows, deployment
   - Add the new content to the appropriate section(s) using clean bullet points
   - **DO NOT add timestamps** - use simple format: `- Description of what to remember`
   - If a section doesn't exist, create it with a proper markdown header

3. **Read and analyze entire AGENTS.md**:
   - Read the complete AGENTS.md file from start to finish
   - Understand the current structure and all existing content
   - Identify any contradictions between the new content you just added and existing content

4. **Clean up and reorganize**:
   - Remove all contradictions - if new content conflicts with existing content, keep the new content and remove or update the conflicting old content
   - Remove all timestamps from the document (format: `[YYYY-MM-DD HH:MM]`)
   - Reorganize sections for logical flow and coherence
   - Merge duplicate or similar entries
   - Ensure the document is well-structured and easy to navigate
   - Make sure related content is grouped together logically
   - Ensure the document reads as a coherent reference guide, not a chronological log

5. **Present for verification**:
   - Show the user the cleaned-up AGENTS.md file
   - Ask them: "Does this look correct? Does it accurately reflect what you want to remember?"
   - Wait for their confirmation before finalizing

6. **Finalize**:
   - Once the user confirms it looks correct, save the cleaned-up version
   - The final AGENTS.md should be a coherent, timeless reference document that future AI agents can easily follow

The goal is to maintain AGENTS.md as a coherent, well-organized reference document rather than a chronological log with timestamps."""  # noqa: E501


@mcp.prompt()
def correction(thing: str, different_thing: str) -> str:
    """Record a correction in AGENTS.md and then continue with the
    corrected approach."""
    return f"""You have been corrected. Follow these steps:

1. **Understand the correction**:
   - You were about to do or were doing: {thing}
   - Instead, you should do: {different_thing}

2. **Record the correction in AGENTS.md**:
   - Read the existing AGENTS.md file (create it if it doesn't exist)
    - Find or create a "Corrections" section (or add to "User Preferences"
      if more appropriate)
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

5. **Confirm briefly**: Tell me you've recorded the correction and are
   continuing with the corrected approach.

The goal is to quickly course-correct, document the learning, and seamlessly
continue with the right approach."""


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
    return """You are helping the user create a new git branch and stage
their changes. Follow these steps:

1. **Review the diff**: Examine the changes provided to understand what
   modifications were made.

2. **Confirm branch creation**: Ask the user which branch they want to
   create the new branch from. Default to creating from the current
   branch unless they specify otherwise.

3. **Generate branch name**: Based on the changes in the diff, suggest
   an appropriate branch name that clearly describes the work
   (e.g., 'add-login-feature', 'fix-api-timeout', 'refactor-database-layer').

4. **Create the branch**: Use `git checkout -b <branch-name>` to create
   and switch to the new branch.

5. **Stage all changes**: Run `git add .` or `git add -A` to stage all the changes.

6. **Confirm completion**: Let the user know the branch was created and
   changes were staged, but NOT committed yet.

Important: Do NOT commit the changes - only stage them. The user will
commit when ready."""


@mcp.prompt()
def debug_github_actions(workflow_url: str) -> str:
    """Debug GitHub Actions workflow failures by analyzing logs and
    providing actionable solutions."""
    return f"""You are helping me debug a failed GitHub Actions workflow.
Follow these steps to systematically analyze and resolve the issue:

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
    - Check for common issues: dependency problems, permission errors,
      timeout issues, resource constraints
   - Examine the workflow configuration and environment setup

4. **Reproduce the issue locally**:
   - Checkout the same commit/branch that triggered the failed workflow:
     `git checkout <commit-sha>` or `git checkout <branch-name>`
   - Review the workflow file (`.github/workflows/*.yaml`) to identify the exact
     commands and environment setup used in CI
   - Run the same commands locally that the workflow executes:
     - Install the same dependencies (e.g., `pixi install`, `npm install`,
       `pip install`)
     - Use the same environment versions (Python, Node.js, etc.) if specified
     - Execute the same test/build commands (e.g., `pixi run test`, `npm test`)
   - For more accurate reproduction, consider using `act` (GitHub Actions locally):
     - Install act: `brew install act` (macOS) or follow platform-specific instructions
     - Run the workflow locally: `act -j <job-name>` or `act` to run all jobs
     - Note: act may have limitations with certain actions or secrets
   - Compare local results with CI results to identify environment-specific issues
   - Document any differences between local and CI environments that might affect
     the failure

5. **Provide debugging guidance**:
   - Explain what went wrong in simple terms
   - Suggest specific fixes or configuration changes
   - Provide commands or code snippets to resolve the issue
   - Recommend preventive measures to avoid similar failures

6. **Context-aware solutions**:
   - Consider the project type (Python, Node.js, etc.) and suggest appropriate fixes
   - Check for recent changes that might have caused the failure
   - Suggest workflow improvements or optimizations

7. **Follow-up actions**:
   - Recommend next steps for testing the fix
   - Suggest monitoring or alerting improvements
   - Provide guidance on preventing similar issues

Workflow URL: {workflow_url}

Focus on providing actionable, specific solutions rather than generic
troubleshooting advice. Use the GitHub CLI commands to gather
comprehensive information about the failure."""


@mcp.prompt()
def devdigest(timeframe: str = "last week") -> str:
    """Generate a comprehensive development digest using GitHub CLI to
    summarize commits, issues, PRs, and activity."""
    return f"""You are helping me create a comprehensive development digest
that summarizes my GitHub activity and accomplishments. Follow these steps
to gather and analyze my development work:

1. **Gather GitHub Activity Data** using the GitHub CLI:
    - **Commits**: Use `gh api /user/events` to get recent activity, or
      `gh log --oneline --since="{timeframe}"` for commit history
    - **Pull Requests**: Use `gh pr list --author=@me --state=all
      --limit=20` to get recent PRs
    - **Issues**: Use `gh issue list --author=@me --state=all --limit=20`
      to get issues I've created or commented on
    - **Comments**: Use `gh api /user/issues/comments` and
      `gh api /user/pulls/comments` for recent comments
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
    - **🎯 Project Highlights**: Notable projects or repositories with
      significant activity
    - **📈 Productivity Insights**: Patterns in work habits, peak activity
      times, project focus areas

4. **Format the Output** as a markdown document that:
   - Uses clear headings and bullet points
   - Includes specific metrics and numbers where possible
   - Highlights the most impactful work
   - Shows progression and growth over time
   - Provides context for why certain work was important

5. **Timeframe Context**: Focus on activity from {timeframe}, but also
   note any longer-term trends or patterns.

6. **Save the Digest**: Create or update a file called `DEV_DIGEST.md`
   with the comprehensive summary.

The goal is to create a professional, insightful summary that showcases
development productivity, technical growth, and meaningful contributions
to projects and the community. Use the GitHub CLI to gather as much
relevant data as possible, then synthesize it into a compelling narrative
of development accomplishments."""


@mcp.prompt()
def code_review(pr_url: str) -> str:
    """Perform a comprehensive code review on a pull request using GitHub CLI."""
    issue_instructions = _get_issue_presentation_instructions()
    return f"""You are helping me perform a thorough code review on a pull
request. Follow these steps systematically:

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
    - Note: When noting issues for the review, document them appropriately
      for the PR review

6. **Provide Summary**:
   - After reviewing all categories, provide a summary of:
     - Total number of issues found (by priority)
     - Key recommendations
     - Positive feedback on good practices
     - Overall assessment of the PR

PR URL: {pr_url}

Focus on being thorough but constructive. The goal is to improve code
quality while respecting the author's work and the user's judgment on
what needs to be changed."""


@mcp.prompt()
def pre_commit_review() -> str:
    """Review staged code changes from a principal/staff engineer perspective
    before committing."""
    return """You are reviewing code changes as a principal or staff engineer
before they are committed. This is a critical review focused on ensuring
production-ready code quality, maintainability, and long-term project health.
Follow these steps systematically:

1. **Examine the Changes**:
   - Use `git diff --cached` or `git diff HEAD` to see all staged/unstaged changes
   - Review all modified, added, and deleted files
   - Understand the context and purpose of the changes
   - Check if this is part of a larger feature or a standalone change
   - Review the commit message (if provided) for clarity and accuracy

2. **Test Quality & Coverage** (CRITICAL):
   - **Tests that don't test what they should**:
     - Are tests actually verifying the intended behavior, or just checking
       that code runs without error?
     - Do tests assert meaningful outcomes, not just that functions execute?
     - Are edge cases and error conditions properly tested?
     - Do tests verify both positive and negative cases?
     - Are integration tests present where unit tests alone aren't sufficient?
   - **Test organization and maintainability**:
     - Are tests well-organized and easy to understand?
     - Do test names clearly describe what they're testing?
     - Is test setup/teardown appropriate and not overly complex?
     - Are tests independent and can run in any order?
     - Do tests avoid testing implementation details unnecessarily?
   - **Missing test coverage**:
     - Are all new functions, classes, and modules covered by tests?
     - Are error paths and exception handlers tested?
     - Are boundary conditions and edge cases tested?
     - Are integration points tested appropriately?
   - **Test quality issues**:
     - Are there flaky tests that might fail intermittently?
     - Do tests have proper assertions with meaningful error messages?
     - Are mocks/stubs used appropriately and not overused?
     - Do tests run efficiently and not take excessive time?

3. **Documentation Review** (CRITICAL):
   - **Missing documentation**:
     - Do all public APIs have docstrings/comments explaining their purpose?
     - Are complex algorithms or business logic explained?
     - Are non-obvious design decisions documented?
     - Is README updated if user-facing behavior changed?
     - Are API documentation files updated if applicable?
     - Are configuration options documented?
   - **Incorrect documentation**:
     - Do docstrings match the actual function signatures and behavior?
     - Are examples in documentation correct and runnable?
     - Are parameter descriptions accurate?
     - Are return value descriptions correct?
     - Is the documentation consistent with the code implementation?
     - Are deprecated features properly marked and migration paths documented?
   - **Documentation quality**:
     - Is documentation clear and understandable for new team members?
     - Are there examples where they would be helpful?
     - Is the documentation maintainable and likely to stay in sync with code?

4. **Architecture & Design**:
   - **Design patterns and principles**:
     - Is the code following established patterns consistently?
     - Are SOLID principles being followed appropriately?
     - Is there proper separation of concerns?
     - Are abstractions at the right level (not over/under-abstracted)?
   - **Coupling and cohesion**:
     - Are modules appropriately decoupled?
     - Is there unnecessary coupling between components?
     - Do changes introduce tight coupling that will be hard to maintain?
   - **Scalability and performance**:
     - Will this code scale appropriately as usage grows?
     - Are there obvious performance bottlenecks?
     - Are database queries optimized (no N+1 problems)?
     - Is caching used appropriately where beneficial?
   - **Breaking changes**:
     - Does this change break existing APIs or contracts?
     - If breaking changes are necessary, are they properly versioned?
     - Are migration paths provided for breaking changes?
     - Are deprecation warnings added before removal?

5. **Error Handling & Resilience**:
   - **Error handling completeness**:
     - Are all error cases handled appropriately?
     - Are exceptions caught at the right level?
     - Are error messages helpful for debugging?
     - Are errors logged appropriately for observability?
   - **Edge cases and boundary conditions**:
     - Are null/None values handled correctly?
     - Are empty collections handled appropriately?
     - Are boundary values (0, -1, max values) handled?
     - Are race conditions considered in concurrent code?
   - **Resource management**:
     - Are resources (files, connections, memory) properly cleaned up?
     - Are there potential memory leaks?
     - Is exception safety ensured (resources cleaned up even on exceptions)?

6. **Security Considerations**:
   - **Input validation**:
     - Is all user input validated and sanitized?
     - Are SQL injection, XSS, and other injection attacks prevented?
     - Are file uploads validated and restricted appropriately?
   - **Authentication and authorization**:
     - Are authentication checks in place where needed?
     - Is authorization verified at appropriate boundaries?
     - Are permissions checked correctly?
   - **Sensitive data**:
     - Are secrets, passwords, or tokens handled securely?
     - Is sensitive data logged inadvertently?
     - Are API keys or credentials exposed in code or logs?
   - **Dependencies**:
     - Are dependencies up-to-date with known vulnerabilities?
     - Are new dependencies necessary and from trusted sources?

7. **Code Quality & Maintainability**:
   - **Code smells**:
     - Are there long methods or classes that should be refactored?
     - Is there code duplication that should be extracted?
     - Are there magic numbers that should be constants?
     - Is there dead code that should be removed?
   - **Readability**:
     - Is the code self-documenting with clear naming?
     - Are complex expressions broken down for clarity?
     - Is the code structure easy to follow?
   - **Consistency**:
     - Does this code follow project conventions and style guides?
     - Is naming consistent with the rest of the codebase?
     - Are patterns used consistently across the codebase?

8. **Observability & Debugging**:
   - **Logging**:
     - Are important events logged at appropriate levels?
     - Are log messages helpful for debugging production issues?
     - Is sensitive information excluded from logs?
     - Are structured logs used where appropriate?
   - **Metrics and monitoring**:
     - Are key metrics exposed for monitoring?
     - Are performance-critical paths instrumented?
     - Are error rates trackable?

9. **Configuration & Environment**:
   - **Configuration management**:
     - Are configuration values properly externalized?
     - Are environment-specific configs handled correctly?
     - Are default values sensible and documented?
   - **Environment variables**:
     - Are required environment variables documented?
     - Are defaults provided where appropriate?
     - Is validation of configuration values performed?

10. **Dependencies & Versioning**:
    - **Dependency management**:
      - Are new dependencies truly necessary?
      - Are dependency versions pinned appropriately?
      - Are dependency licenses compatible with project license?
    - **Version compatibility**:
      - Will this work with the supported versions of dependencies?
      - Are there breaking changes in dependencies that need addressing?

11. **Integration & Compatibility**:
    - **Backward compatibility**:
      - Are existing integrations preserved?
      - Will this break existing clients or consumers?
    - **API contracts**:
      - Are API contracts maintained or properly versioned?
      - Are response formats consistent?

12. **Performance & Resource Usage**:
    - **Efficiency**:
      - Are algorithms and data structures optimal for the use case?
      - Are there unnecessary computations or database queries?
      - Is lazy loading used where appropriate?
    - **Resource constraints**:
      - Will this code work within resource limits (memory, CPU, disk)?
      - Are there potential resource exhaustion scenarios?

13. **Accessibility & Usability** (if applicable):
    - **Accessibility**:
      - Are accessibility standards followed (WCAG, ARIA attributes)?
      - Is keyboard navigation supported?
      - Are screen readers considered?
    - **User experience**:
      - Are error messages user-friendly?
      - Is feedback provided for long-running operations?

14. **Technical Debt**:
    - **Debt introduction**:
      - Does this code introduce technical debt?
      - Are there TODOs or FIXMEs that should be addressed?
      - Are shortcuts taken that will cause problems later?
    - **Debt reduction**:
      - Does this change reduce existing technical debt?
      - Are deprecated patterns being replaced?

15. **Final Assessment**:
    - **Critical blockers**:
      - Are there any issues that MUST be fixed before committing?
      - Security vulnerabilities, data loss risks, breaking changes without
        migration paths
    - **Important improvements**:
      - Issues that should be addressed but aren't blockers
      - Missing tests, incorrect documentation, performance concerns
    - **Nice-to-have improvements**:
      - Minor code quality improvements, style issues, documentation polish

**Review Output Format**:
- Categorize findings by the sections above
- Rank all issues by priority (critical, high, medium, low)
- Provide specific, actionable feedback with code examples where helpful
- Note positive aspects and good practices observed
- Provide a summary with total issues by priority
- Clearly indicate what MUST be fixed vs. what SHOULD be improved

Focus on being thorough, constructive, and focused on long-term code health.
The goal is to catch issues before they reach production and ensure the codebase
remains maintainable and high-quality. Be direct but respectful in your feedback."""


@mcp.prompt()
def present_issues() -> str:
    """Present a list of issues to the user in rank order, one by one."""
    issue_instructions = _get_issue_presentation_instructions()
    return f"""You have a list of issues (from any context - code review,
linting, testing, analysis, etc.) that need to be presented to the user.
Follow these steps:

1. **Identify and Rank Order Issues**:
   - Review the list of issues you have (from previous context or analysis)
   - **Rank order all issues by priority** (critical, high, medium, low):
     - Critical: Security vulnerabilities, bugs that will cause failures,
       data loss risks
     - High: Significant bugs, performance issues, architectural problems
     - Medium: Code quality issues, maintainability concerns, missing tests
     - Low: Style issues, minor improvements, documentation gaps
    - If issues don't have explicit priorities, infer them based on their
      nature and impact

2. {issue_instructions}

3. **Provide Summary**:
   - After going through all issues (or when the user stops), provide a summary:
     - Total number of issues found (by priority)
     - Number of issues addressed vs. skipped
     - Key recommendations or next steps

The context of where these issues came from is unknown - they could be
from code review, static analysis, testing, manual inspection, or any
other source. Focus on presenting them clearly and systematically,
respecting the user's decisions on each item."""


@mcp.prompt()
def frontend_aesthetics() -> str:
    """Apply distinctive, creative frontend design principles to avoid
    generic AI-generated aesthetics."""
    return """When building frontend interfaces, avoid converging toward
generic, "on distribution" outputs that create what users call the "AI
slop" aesthetic. Instead, create creative, distinctive frontends that
surprise and delight. Apply these principles:

**Typography**:
- Choose fonts that are beautiful, unique, and interesting
- Avoid generic fonts like Arial, Inter, and Roboto
- Opt for distinctive typographic choices that elevate the frontend's aesthetics
- Vary your font selections across different projects - don't default to
  common choices like Space Grotesk

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
- Focus on high-impact moments: one well-orchestrated page load with
  staggered reveals (using animation-delay) creates more delight than
  scattered micro-interactions

**Backgrounds & Atmosphere**:
- Create atmosphere and depth rather than defaulting to solid colors
- Layer CSS gradients, use geometric patterns, or add contextual effects
  that match the overall aesthetic
- Think about how backgrounds contribute to the overall visual narrative

**Avoid Generic Patterns**:
- Overused font families (Inter, Roboto, Arial, system fonts)
- Clichéd color schemes (particularly purple gradients on white backgrounds)
- Predictable layouts and component patterns
- Cookie-cutter design that lacks context-specific character

**Creative Interpretation**:
- Interpret creatively and make unexpected choices that feel genuinely
  designed for the context
- Think outside the box - avoid converging on common choices across generations
- Each project should have its own distinctive character and aesthetic identity

Apply these principles to create frontends that feel thoughtfully designed
rather than generically generated. Make creative, distinctive choices that
surprise and delight users."""


@mcp.prompt()
def upgrade_repo_to_template(yolo_mode: bool = False) -> str:
    """Upgrade a repository to match the standards from the cookiecutter-python-project
    template at https://github.com/ericmjl/cookiecutter-python-project."""
    yolo_instruction = (
        "**YOLO MODE ENABLED**: The user has enabled yolo mode, which means "
        "you should automatically approve all suggested changes and proceed "
        "with implementation without asking for individual confirmations. "
        "Still present the full list of changes for transparency, but proceed "
        "directly to implementation after listing them."
        if yolo_mode
        else (
            "**APPROVAL REQUIRED**: Present each change individually and wait "
            "for user approval before proceeding. The user can approve, reject, "
            "or request modifications for each change."
        )
    )

    return f"""You are helping upgrade a repository to match the standards from the
cookiecutter-python-project template (https://github.com/ericmjl/cookiecutter-python-project).
Follow these phases systematically:

## Phase 1: Analyze Current Repository Structure

1. **Examine the repository structure**:
   - List all files in the root directory
   - Check for existing configuration files
     (pyproject.toml, .pre-commit-config.yaml, mkdocs.yaml, etc.)
   - Review the project structure and organization
   - Identify the package/module structure
   - Check for existing GitHub Actions workflows
   - Review existing dependencies and tool configurations

2. **Document current state**:
   - Note what's already present and what's missing
   - Identify any custom configurations that should be preserved
   - Check for project-specific requirements that need to be maintained

## Phase 2: Compare with CookieCutter Template Standards

**CRITICAL FIRST STEP**: Clone or access the cookiecutter-python-project template
repository to compare files directly:

1. **Clone the template repository**:
   - Run: `git clone https://github.com/ericmjl/cookiecutter-python-project.git
     /tmp/cookiecutter-template`
   - Or access it via GitHub API/web interface if cloning isn't possible
   - Navigate to the template directory to examine files

2. **Compare files side-by-side**:
   - For each configuration file in the template, compare it with the current repository
   - Check for differences in structure, content, and configuration values
   - Note which files exist in the template but are missing in the current repo
   - Identify which existing files need updates to match template standards

3. **Examine template structure**:
   - Review the template's directory structure
   - Check the template files in the `{{ cookiecutter.__repo_name }}` directory
   - Note any template variables ({{ cookiecutter.* }}) that need to be replaced
   - Understand how the template is structured

After accessing the template repository, identify the following key components that
should be present in the upgraded repository:

**Core Configuration Files:**
- `pyproject.toml` with sections for:
  - `[build-system]` (setuptools >=61.0, wheel)
  - `[tool.interrogate]` (documentation coverage, fail-under: 100)
  - `[tool.pytest.ini_options]` (test configuration with coverage)
  - `[tool.ruff]` (line-length: 88, select: ["E", "F", "I"])
  - `[tool.pydoclint]` (docstring linting)
  - `[tool.coverage.run]` (coverage configuration)
  - `[tool.pixi.project]` (channels: conda-forge, platforms)
  - `[tool.pixi.pypi-dependencies]` (editable package install)
  - `[tool.pixi.feature.tests.dependencies]` (pytest, pytest-cov, hypothesis)
  - `[tool.pixi.feature.docs.dependencies]` (mkdocs, mkdocs-material, mknotebooks)
  - `[tool.pixi.feature.notebook.dependencies]`
    (ipykernel, ipython, jupyter, pixi-kernel)
  - `[tool.pixi.feature.devtools.dependencies]` (pre-commit)
  - `[tool.pixi.feature.tests.tasks]` (test: pytest)
  - `[tool.pixi.feature.devtools.tasks]`
    (lint: pre-commit run --all-files, commit: git commit)
  - `[tool.pixi.feature.docs.tasks]`
    (build-docs: mkdocs build, serve-docs: mkdocs serve)
  - `[tool.pixi.feature.setup.tasks]`
    (setup: pre-commit autoupdate && pre-commit install --install-hooks,
     update: pre-commit autoupdate)
  - `[tool.pixi.environments]` (default, docs, tests environments)
  - `[project]` (name, version, requires-python, dependencies, readme, scripts)
  - `[project.scripts]` (CLI entry points)

- `.pre-commit-config.yaml` with hooks for:
  - pre-commit-hooks (check-yaml, end-of-file-fixer, trailing-whitespace)
  - nbstripout (for Jupyter notebooks)
  - interrogate (documentation coverage)
  - pydoclint (docstring linting)
  - ruff-pre-commit (ruff-check and ruff-format)
  - local pixi-install hook (to keep lockfile up-to-date)

- `mkdocs.yaml` with:
  - site_name and site_url configuration
  - Material theme setup
  - mknotebooks plugin configuration
  - Markdown extensions (codehilite, admonition, pymdownx.superfences)
  - Repository links and social links

- `.gitignore` with Python-specific patterns:
  - Standard Python ignores (__pycache__, *.pyc, etc.)
  - Distribution/packaging ignores
  - Testing/coverage ignores
  - Environment ignores (.env, .venv, etc.)
  - Documentation ignores (/site)
  - Project-specific ignores (.pixi, .llamabot/, etc.)

- `MANIFEST.in` for package distribution

**GitHub Actions Workflows:**
- `.github/workflows/pr-tests.yaml`:
  - Runs tests on pull requests using pixi
  - Includes bare-install test for multiple Python versions
  - Uploads code coverage to codecov

- `.github/workflows/docs.yaml`:
  - Builds documentation on push to main
  - Deploys to GitHub Pages

- `.github/workflows/code-style.yaml`:
  - Runs pre-commit hooks on pull requests

- `.github/dependabot.yml`:
  - Weekly updates for GitHub Actions

**Project Structure:**
- Proper package/module structure
- Tests directory with pytest configuration
- Documentation directory (docs/) for mkdocs
- README.md with project information

## Phase 3: Identify Required Changes

**Use the cloned template repository** to create a comprehensive list of all changes
needed. For each file in the template:

1. **Read the template file** from the cloned repository
2. **Compare with the current repository's version** (if it exists)
3. **Identify specific differences**:
   - Missing sections or configurations
   - Outdated values or versions
   - Structural differences
   - Missing files entirely

Categorize all changes needed by type:

**A. Files to Add:**
- List any missing configuration files that need to be created
- Include GitHub Actions workflows that are missing
- Note any missing documentation structure

**B. Files to Update:**
- Identify existing files that need modifications to match template standards
- Note specific sections that need updating (e.g., pyproject.toml sections)
- Identify configuration mismatches

**C. Commands to Run:**
- `pre-commit autoupdate` (to update pre-commit hook versions)
- `pre-commit install --install-hooks` (to install hooks)
- `pixi install` (to update pixi.lock after configuration changes)
- Any other setup commands needed

**D. Project-Specific Adaptations:**
- Note any project-specific values that need to be preserved:
  - Package name and module name
  - CLI entry points
  - Project-specific dependencies
  - Custom tasks or configurations
  - Repository URLs and names

For each change, provide:
- **What**: Clear description of the change
- **Why**: Reason it's needed to match template standards
- **Impact**: What will be affected by this change
- **Preservation**: Any existing values that should be kept

## Phase 4: Present Changes for Approval

{yolo_instruction}

**Present the complete list of changes** organized by category:

1. **Files to Add** (with brief descriptions)
2. **Files to Update** (with specific sections/changes)
3. **Commands to Run** (in order of execution)
4. **Project-Specific Adaptations** (values to preserve)

For each change, clearly state:
- The change being made
- Why it's needed
- What will be preserved from the current repository

**If NOT in yolo mode:**
- Present changes ONE AT A TIME or in small logical groups
- Wait for user approval before proceeding to the next change
- Allow user to approve, reject, or request modifications
- Respect user decisions and adapt accordingly

**If in yolo mode:**
- Present the full list for transparency
- Proceed directly to implementation after listing
- Still preserve project-specific values appropriately

## Phase 5: Implement Approved Changes

After receiving approval (or in yolo mode), implement changes systematically using
the cloned template repository as the source:

1. **Add new files**:
   - Copy files directly from the cloned template repository
   - Read the template file content and adapt it for the current project
   - Replace template variables ({{ cookiecutter.* }}) with actual project values
   - Preserve any project-specific customizations that exist

2. **Update existing files**:
   - Merge template configurations with existing ones
   - Preserve project-specific dependencies and settings
   - Update only the sections that need to match template standards
   - Be careful not to overwrite project-specific configurations

3. **Run setup commands**:
   - Run `pre-commit autoupdate` to update hook versions
   - Run `pre-commit install --install-hooks` to install hooks
   - Run `pixi install` to update the lockfile
   - Verify commands complete successfully

4. **Verify file integrity**:
   - Check that all files were created/updated correctly
   - Ensure project-specific values were preserved
   - Verify configurations are valid (e.g., TOML syntax)

## Phase 6: Verification

After implementation, verify the migration:

1. **Run `pixi shell`**:
   - This activates the pixi environment and verifies basic setup
   - Check that the environment activates without errors
   - Verify that dependencies resolve correctly

2. **Test basic functionality**:
   - Run `pixi run test` to ensure tests still work
   - Run `pixi run lint` to verify linting setup
   - Check that CLI entry points work (if applicable)

3. **Verify configurations**:
   - Check that pre-commit hooks are installed
   - Verify GitHub Actions workflows are valid
   - Ensure documentation builds (if applicable)

4. **Report completion**:
   - Summarize what was changed
   - Note any issues encountered
   - Provide next steps or recommendations

## Important Guidelines

- **Preserve project-specific values**: Always maintain project name,
  module name, dependencies, and custom configurations
- **Merge, don't replace**: When updating existing files, merge template
  standards with existing configurations
- **Test incrementally**: After major changes, verify the project still works
- **Document changes**: Note what was changed and why for future reference
- **Respect user decisions**: If user rejects a change, accept it and move on

The goal is to upgrade the repository to match template standards while
preserving all project-specific customizations and ensuring everything
continues to work correctly."""


@mcp.prompt()
def fix_pre_commit_issues() -> str:
    """Run all pre-commit hooks and fix all issues identified by the hooks."""
    return """You are helping to run pre-commit hooks and fix all issues they
identify. Follow these steps systematically:

## Step 1: Run Pre-commit Hooks

1. **Run pre-commit hooks on all files**:
   - Execute: `pixi run lint` or `pre-commit run --all-files`
   - If pixi is not available, use: `pre-commit run --all-files` directly
   - Capture the full output including all errors and warnings

2. **Review the output**:
   - Identify which hooks ran and which ones failed
   - Note the specific files and line numbers where issues were found
   - Categorize issues by type (formatting, linting, documentation, etc.)
   - Count how many issues were found per hook

## Step 2: Categorize Issues

Organize the issues by hook type:

**Formatting Issues** (ruff-format, black, etc.):
- Trailing whitespace
- Line length violations
- Indentation problems
- Missing blank lines
- End-of-file issues

**Linting Issues** (ruff-check, pylint, etc.):
- Code style violations
- Unused imports
- Undefined variables
- Type checking issues
- Security concerns

**Documentation Issues** (interrogate, pydoclint, etc.):
- Missing docstrings
- Incomplete docstrings
- Docstring format violations
- Documentation coverage below threshold

**Other Issues**:
- YAML/JSON syntax errors
- Notebook output issues (nbstripout)
- File permission issues
- Other hook-specific problems

## Step 3: Fix Issues Systematically

Fix issues one category at a time, starting with the most critical:

1. **Fix formatting issues first**:
   - Many hooks can auto-fix formatting: run `ruff format .` or let
     ruff-format hook fix issues automatically
   - For trailing whitespace: remove it
   - For line length: break long lines appropriately
   - For end-of-file: ensure files end with newline
   - Re-run hooks after fixes to verify

2. **Fix linting issues**:
   - Address code style violations
   - Remove unused imports
   - Fix undefined variables or imports
   - Address type checking issues if applicable
   - Some issues can be auto-fixed by ruff-check with --fix flag
   - For issues that can't be auto-fixed, make manual corrections

3. **Fix documentation issues**:
   - Add missing docstrings to functions, classes, and modules
   - Complete incomplete docstrings with proper format
   - Ensure docstrings follow project conventions (Google, NumPy, etc.)
   - Update docstrings to match pydoclint requirements

4. **Fix other issues**:
   - Fix YAML/JSON syntax errors
   - Clean notebook outputs if needed
   - Address any other hook-specific issues

## Step 4: Re-run Hooks After Fixes

After fixing issues in each category:

1. **Re-run pre-commit hooks**:
   - Run `pixi run lint` or `pre-commit run --all-files` again
   - Verify that the issues you fixed are now resolved
   - Check if any new issues were introduced by your fixes

2. **Iterate until clean**:
   - Continue fixing and re-running until all hooks pass
   - Some fixes may reveal additional issues - address them systematically
   - Ensure no regressions were introduced

## Step 5: Verify Final State

Once all hooks pass:

1. **Final verification**:
   - Run `pre-commit run --all-files` one final time
   - Confirm all hooks pass with exit code 0
   - Verify no warnings or errors remain

2. **Check for edge cases**:
   - Ensure auto-fixes didn't break functionality
   - Verify that code still runs correctly
   - Check that tests still pass (run `pixi run test` if applicable)

## Important Guidelines

- **Auto-fix when possible**: Many hooks can auto-fix issues. Use `ruff format .`
  and `ruff check --fix .` to automatically fix formatting and some linting
  issues before manual fixes.

- **Preserve functionality**: When fixing issues, ensure you don't change the
  logic or behavior of the code. Only fix style, formatting, and documentation.

- **Follow project conventions**: Maintain consistency with existing code style
  and documentation format.

- **Fix incrementally**: Fix issues category by category rather than all at
  once. This makes it easier to verify fixes and catch any problems.

- **Document significant changes**: If you make substantial changes to fix
  issues, note what was changed and why.

- **Respect hook configurations**: Follow the project's pre-commit configuration.
  Don't disable hooks or change configurations unless explicitly requested.

The goal is to have all pre-commit hooks pass cleanly while maintaining code
functionality and following project standards."""


@mcp.prompt()
def create_obsidian_moc(topic: str) -> str:
    """Create a map of content (MOC) page for a topic in the Obsidian vault's
    MOCS folder."""
    vault_rules = _get_vault_note_rules()
    return f"""You are helping me create a map of content (MOC) page for the
topic "{topic}" in my Obsidian vault. Follow these steps carefully:

1. **Locate the Obsidian Vault**:
   - Identify the root directory of the Obsidian vault
   - Navigate to or create the "MOCs" folder (capital M, capital O, capital C,
     lowercase s) if it doesn't exist
   - The folder name must be exactly "MOCs" (not "MOCS", "Mocs", or any other
     variation)

2. **Scan the Vault for Existing Notes**:
   - Search through the entire Obsidian vault for notes related to "{topic}"
   - Look for notes that:
     - Have titles or content related to the topic
     - Contain keywords or concepts related to the topic
     - Are tagged with relevant tags
   - {vault_rules}

3. **Categorize the Notes**:
   - Organize the found notes into logical categories
   - Create meaningful category headings that group related notes together
   - Examples of categories might be:
     - Core Concepts
     - Applications
     - Related Topics
     - Resources
     - Examples
   - Adapt categories based on the actual notes found and the topic

4. **Create the MOC File**:
   - Create a new markdown file in the MOCs folder
   - Name it appropriately for the topic (e.g., "{topic} MOC.md" or
     "{topic}.md")
   - The file should contain:
     - A main heading with the topic name
     - Categorized headings (using ## for main categories)
     - Wiki links (using [[Note Name]]) to existing notes under each category
     - Only include notes that you verified exist in the vault

5. **Format the MOC**:
   - Use standard Obsidian markdown formatting
   - Use categorized headings (##) to organize sections
   - Use wiki link syntax: [[Note Name]] for each note
   - Ensure proper markdown structure with blank lines between sections
   - Keep the organization clear and hierarchical

6. **Verify Before Finalizing**:
   - Double-check that every wiki link points to a note that exists
   - Confirm the file is saved in the MOCs folder
   - Ensure no fictional or non-existent notes are included
   - Verify the categorization makes sense for the topic

7. **Confirm Completion**:
   - Tell me the path where the MOC was created
   - List the categories you created
   - Mention how many notes were included
   - Note if the MOCs folder needed to be created

**Important Rules**:
- {vault_rules}
- **MOCs folder name is exact** - Capital M, capital O, capital C, lowercase s
- **Use categorized headings** - The MOC should be organized with clear category
  headings

The goal is to create a useful map of content that helps navigate existing
notes related to "{topic}" without inventing any content that doesn't exist."""


@mcp.prompt()
def add_note_to_mocs(note_name: str) -> str:
    """Add a note to the appropriate map(s) of content in the Obsidian vault's
    MOCs folder, maintaining each MOC's existing style."""
    vault_rules = _get_vault_note_rules()
    return f"""You are helping me add the note "{note_name}" to the appropriate
map(s) of content (MOCs) in my Obsidian vault. Follow these steps carefully:

1. **Locate the Note**:
   - Find the note "{note_name}" in the Obsidian vault
   - {vault_rules}
   - Read the note's content to understand its topic, themes, and subject matter
   - Identify key concepts, tags, and relationships that might indicate which
     MOCs it belongs to

2. **Scan the MOCs Folder**:
   - Navigate to the "MOCs" folder (capital M, capital O, capital C, lowercase s)
   - List all MOC files in this folder
   - Read each MOC file to understand:
     - What topic or theme it covers
     - Its structure and organization
     - The style and formatting conventions it uses
     - The categories it contains

3. **Determine Appropriate MOCs**:
   - Analyze the note's content against each MOC's topic
   - Identify which MOC(s) the note logically belongs to based on:
     - Topic alignment
     - Conceptual relationships
     - Thematic connections
   - The note may belong to multiple MOCs if it spans multiple topics
   - Use your judgment to determine the best fit(s)

4. **Read Each Relevant MOC's Style**:
   - For each MOC where the note should be added:
     - Study the existing structure and formatting
     - Note the heading hierarchy used (##, ###, etc.)
     - Observe the category names and organization
     - Identify any patterns in how notes are listed
     - Check for any specific formatting conventions (bullet points, numbering, etc.)
     - Note the order of notes within categories (alphabetical, chronological, etc.)

5. **Determine Appropriate Category**:
   - For each relevant MOC, identify which category section the note fits into
   - If no existing category fits, determine if a new category should be created
     (only if the note truly represents a new theme not covered by existing categories)
   - Consider the note's relationship to other notes already in that category

6. **Add the Note to Each MOC**:
   - For each MOC where the note should be added:
     - Open the MOC file
     - Find the appropriate category section
     - Add the note using a wiki link: [[{note_name}]]
     - Maintain the exact formatting style of that MOC:
       - Use the same heading levels
       - Follow the same list format (bullets, numbering, etc.)
       - Match the indentation and spacing
       - Preserve the ordering convention (alphabetical, chronological, etc.)
     - If creating a new category, match the style of existing category
       headings
     - Ensure the addition feels natural and consistent with the MOC's
       existing structure

7. **Verify the Additions**:
   - Double-check that the note was added to all appropriate MOCs
   - Verify that the formatting matches each MOC's style
   - Ensure the note link is correct: [[{note_name}]]
   - Confirm the note actually exists in the vault
   - Check that the additions maintain the logical flow of each MOC

8. **Confirm Completion**:
   - Tell me which MOC(s) the note was added to
   - List the category(ies) where it was placed
   - Note if any new categories were created
   - Mention any style considerations you maintained

**Important Rules**:
- {vault_rules}
- **Maintain each MOC's style** - Preserve the exact formatting, structure, and
  conventions of each MOC you modify
- **Only add to appropriate MOCs** - Use judgment to determine which MOCs the
  note truly belongs to, don't add it everywhere
- **Preserve organization** - Maintain the existing order and structure of each
  MOC
- **Match formatting exactly** - Follow the exact style of each MOC, including
  spacing, indentation, and list formatting

The goal is to seamlessly integrate the note into the appropriate MOC(s) while
maintaining the unique style and structure of each map of content."""


@mcp.prompt()
def update_obsidian_moc(moc_name: str) -> str:
    """Update an existing map of content (MOC) in the Obsidian vault's MOCs
    folder, ensuring it includes all relevant existing notes and maintains its
    style."""
    vault_rules = _get_vault_note_rules()
    return f"""You are helping me update the map of content (MOC) "{moc_name}" in
my Obsidian vault. Follow these steps carefully:

1. **Locate the MOC**:
   - Navigate to the "MOCs" folder (capital M, capital O, capital C, lowercase s)
   - Find the MOC file named "{moc_name}" (or similar variations)
   - Read the existing MOC to understand:
     - Its current structure and organization
     - The style and formatting conventions it uses
     - The categories it contains
     - The notes currently linked

2. **Analyze the MOC's Topic**:
   - Determine what topic or theme the MOC covers
   - Identify the key concepts and themes associated with this MOC
   - Understand the scope and purpose of the MOC

3. **Scan the Vault for Relevant Notes**:
   - Search through the entire Obsidian vault for notes related to the MOC's
     topic
   - Look for notes that:
     - Have titles or content related to the topic
     - Contain keywords or concepts related to the topic
     - Are tagged with relevant tags
     - Are conceptually related to the MOC's theme
   - {vault_rules}

4. **Verify Existing Links**:
   - Check each note currently linked in the MOC
   - Verify that each linked note still exists in the vault
   - Identify any broken links (notes that no longer exist)
   - Note which existing links should remain

5. **Categorize Notes**:
   - Organize all relevant existing notes into logical categories
   - Match the existing category structure where possible
   - Determine if new categories are needed for notes that don't fit existing
     ones
   - Consider if any existing categories should be removed or merged

6. **Update the MOC**:
   - Maintain the exact formatting style of the existing MOC:
     - Use the same heading hierarchy (##, ###, etc.)
     - Follow the same list format (bullets, numbering, etc.)
     - Match the indentation and spacing
     - Preserve the ordering convention (alphabetical, chronological, etc.)
   - Add wiki links to relevant notes that are missing: [[Note Name]]
   - Remove links to notes that no longer exist
   - Reorganize categories if needed while maintaining the MOC's style
   - Ensure all additions and changes feel natural and consistent with the
     existing structure

7. **Verify the Updates**:
   - Double-check that every wiki link points to a note that exists
   - Confirm no broken links remain
   - Verify that the formatting matches the MOC's original style
   - Ensure the organization makes sense for the topic
   - Check that all relevant existing notes are included

8. **Confirm Completion**:
   - Tell me what updates were made to the MOC
   - List any notes that were added
   - List any notes that were removed (broken links)
   - Note any categories that were added, removed, or reorganized
   - Mention how many notes are now linked in the MOC
   - Confirm that the MOC's style was preserved

**Important Rules**:
- {vault_rules}
- **Maintain the MOC's style** - Preserve the exact formatting, structure, and
  conventions of the existing MOC
- **Remove broken links** - Delete links to notes that no longer exist
- **Include all relevant notes** - Ensure the MOC includes all existing notes
  that relate to its topic
- **Preserve organization** - Maintain the existing order and structure unless
  reorganization improves clarity
- **Match formatting exactly** - Follow the exact style of the MOC, including
  spacing, indentation, and list formatting

The goal is to keep the MOC up-to-date with all relevant existing notes while
maintaining its unique style and structure, and removing any links to notes
that no longer exist."""


@mcp.prompt()
def edit_blog_post(blog_post_path: str) -> str:
    """Edit a blog post to preserve the author's voice while improving clarity
    and flow."""
    return f"""You are helping me edit a blog post located at "{blog_post_path}".
Follow these steps to improve the post while preserving my authentic voice:

1. **Read the Original Post**:
   - Read the entire blog post carefully
   - Understand the main message and key points
   - Note the current structure and flow
   - Identify the intended audience

2. **Preserve Voice and Tone**:
   - **Maintain first-person perspective** - Keep "I" statements and personal
     experiences
   - **Keep conversational tone** - Don't make it overly formal or academic
   - **Preserve personal anecdotes** - These add authenticity and engagement
   - **Maintain friendly, approachable style** - Keep the human connection
   - **Don't remove personality** - Avoid making it sound generic or "AI-written"
   - **Keep the author's unique phrasing** - Don't replace distinctive expressions
     with generic alternatives

3. **Improve Clarity and Flow**:
   - **Use active voice** - Prefer "I built" over "was built"
   - **Break up long sentences** - Make complex ideas easier to follow
   - **Improve transitions** - Add smooth connections between paragraphs and
     sections
   - **Clarify ambiguous references** - Make sure pronouns and references are clear
   - **Strengthen topic sentences** - Ensure each paragraph has a clear focus
   - **Remove redundancy** - Cut repetitive phrases while keeping key points

4. **Structure and Organization**:
   - **Maintain clear headings** - Use descriptive section headings (## for main
     sections)
   - **Ensure logical flow** - Ideas should build on each other naturally
   - **Balance section lengths** - Avoid sections that are too short or too long
   - **Use lists when appropriate** - Break down complex points into bulleted or
     numbered lists
   - **Add subheadings if needed** - Break up long sections for readability

5. **Content Refinement**:
   - **Keep practical, actionable advice** - Preserve concrete examples and
     real-world applications
   - **Maintain technical accuracy** - Don't simplify technical concepts incorrectly
   - **Preserve code examples** - Keep code snippets intact and well-formatted
   - **Keep personal experiences** - Don't remove stories or examples from actual
     work
   - **Enhance examples** - If examples are unclear, clarify them without removing
     the original context

6. **Writing Quality**:
   - **Fix grammar and spelling** - Correct errors while preserving natural phrasing
   - **Improve word choice** - Use clearer, more precise language when needed
   - **Ensure consistency** - Use consistent terminology throughout
   - **Check punctuation** - Fix punctuation errors, especially around quotes and
     code blocks
   - **Verify markdown formatting** - Ensure proper markdown syntax for headings,
     lists, code blocks, and links

7. **Ending**:
   - **Preserve the original conclusion style** - Keep friendly sign-offs or
     thought-provoking endings
   - **Ensure the ending ties back to the main message** - Make sure the conclusion
     reinforces the key points
   - **Maintain the author's voice** - Don't replace personal endings with generic
     conclusions

8. **Final Review**:
   - Read through the edited version
   - Verify that the author's voice is preserved
   - Check that improvements enhance rather than replace the original
   - Ensure the post reads smoothly and naturally
   - Confirm technical accuracy is maintained

**Important Guidelines**:
- **Preserve voice above all** - If improving clarity conflicts with preserving
  voice, choose voice
- **Don't over-edit** - The goal is refinement, not rewriting
- **Keep it authentic** - Avoid making it sound like generic AI-generated content
- **Maintain personal touch** - Preserve anecdotes, opinions, and personal
  experiences
- **Improve, don't replace** - Enhance what's there rather than rewriting from
  scratch
- **Respect the author's style** - Don't impose a different writing style

**What to Avoid**:
- Don't remove personal anecdotes or experiences
- Don't make the tone overly formal or academic
- Don't replace distinctive phrasing with generic alternatives
- Don't remove personality or make it sound "corporate"
- Don't over-explain technical concepts (keep them accessible but accurate)
- Don't add unnecessary words or fluff

After editing, provide a brief summary of:
- What voice elements you preserved
- What clarity improvements you made
- Any structural changes
- How the post maintains the author's authentic voice

The goal is to make the blog post read cleanly and fluently while preserving my
tone, voice, and personal style."""


# Resources
@mcp.resource("resource://productivity_methods")
def productivity_methods() -> str:
    """Collection of proven productivity methodologies."""
    content = {
        "methods": [
            {
                "name": "Getting Things Done (GTD)",
                "description": (
                    "A workflow methodology for organizing tasks and projects"
                ),
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
                "description": (
                    "Time management method using 25-minute focused work sessions"
                ),
                "key_principles": [
                    "Work in sprints",
                    "Take breaks",
                    "Track progress",
                ],
            },
            {
                "name": "Eisenhower Matrix",
                "description": (
                    "Prioritization framework based on urgency and importance"
                ),
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
        "peak_hours": (
            "Identify your natural energy peaks (usually morning or afternoon)"
        ),
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
    return (
        f"Created task '{task}' with ID {task_id}, priority: {priority}, "
        f"category: {category}"
    )


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

    return (
        f"Productivity Score: {score:.1f}/100\n"
        f"Completion Rate: {completion_rate:.1f}%\n"
        f"Focus Time: {focus_hours:.1f} hours"
    )


async def run_server_stdio() -> None:
    """Run the MCP server using stdio transport."""
    await mcp.run()


async def run_server_http(port: int = 9247) -> None:
    """Run the MCP server using HTTP transport."""
    # Note: HTTP transport would require additional setup
    # For now, we'll use stdio as the primary transport
    print("HTTP transport not yet implemented. Use stdio transport instead.")
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
        print("HTTP transport not yet implemented. Use stdio transport instead.")

    # FastMCP handles the event loop internally
    mcp.run()


if __name__ == "__main__":
    run_server()
