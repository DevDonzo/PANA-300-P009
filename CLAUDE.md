# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a learning project for exploring Claude Code, skills, and subagents. It includes the **skill-maker** - a comprehensive skill lifecycle manager for creating and maintaining Claude Code skills.

## Key Features

- **skill-maker**: A comprehensive skill that manages the complete lifecycle of Claude Code skills
  - Create new skills from scratch
  - Enhance existing skills
  - Test and validate skills
  - Generate professional documentation
  - Prepare skills for publication

## Project Structure

```
.
├── CLAUDE.md                  # This file
├── skill-maker.md             # skill-maker documentation
├── skill-maker-config.json    # skill-maker configuration
├── skill-maker.js             # skill-maker implementation
└── skills/                    # Directory for created skills
```

## Using skill-maker

The `/skill-maker` command provides a complete workflow:

```bash
/skill-maker create              # Create a new skill
/skill-maker enhance <name>      # Improve an existing skill
/skill-maker test <name>         # Test and validate a skill
/skill-maker document <name>     # Generate documentation
/skill-maker publish <name>      # Prepare for release
```

See **skill-maker.md** for detailed usage and examples.

## Key Concepts

- **Skills**: Custom slash commands for Claude Code. See skill-maker.md for how to create them
- **Subagents**: Specialized agents for specific tasks (general-purpose, Explore, Plan, etc.)
- **MCP Servers**: Integration points for extended functionality

## Architecture Notes

The skill-maker skill demonstrates:
- Modular design with clear separation of concerns
- Each lifecycle action (create, enhance, test, document, publish) is independent
- Extensible template system for different skill types
- Comprehensive error handling and validation

## Best Practices

When creating skills (using skill-maker):
1. Keep skills focused on a single purpose
2. Include comprehensive input validation
3. Handle errors gracefully with meaningful messages
4. Document with examples and use cases
5. Write tests covering edge cases
6. Keep parameters minimal and intuitive
7. Return data in consistent, predictable formats
