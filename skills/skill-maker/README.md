# Skill-Maker: Comprehensive Skill Lifecycle Manager

A Claude Code skill that helps you create, enhance, test, and document skills efficiently.

## Description

The skill-maker skill provides an interactive workflow for managing the complete lifecycle of Claude Code skills. It guides you through best practices and generates high-quality skill code.

## Usage

```bash
/skill-maker [action]
```

## Available Actions

### 1. **create** - Generate a New Skill
Create a new skill from scratch with guided setup.

```bash
/skill-maker create
```

**What it does:**
- Asks you about your skill's purpose
- Determines input parameters and outputs
- Validates the skill design
- Generates skill scaffolding
- Creates documentation template

**Example:**
```bash
/skill-maker create
# Prompts:
# - What should this skill do?
# - What inputs does it need?
# - What should it output?
# - Who is the target user?
```

### 2. **enhance** - Improve an Existing Skill
Refactor and improve a skill that already exists.

```bash
/skill-maker enhance [skill-name]
```

**What it does:**
- Analyzes the current skill
- Identifies improvement opportunities
- Refactors for clarity and performance
- Adds missing error handling
- Updates documentation

### 3. **test** - Validate and Test a Skill
Create and run comprehensive tests for your skill.

```bash
/skill-maker test [skill-name]
```

**What it does:**
- Generates test cases
- Tests with various inputs
- Validates error handling
- Provides coverage report
- Suggests edge cases to test

### 4. **document** - Generate Skill Documentation
Create professional documentation for your skill.

```bash
/skill-maker document [skill-name]
```

**What it does:**
- Analyzes the skill code
- Generates README with examples
- Creates usage guide
- Documents parameters
- Adds troubleshooting section

### 5. **publish** - Prepare Skill for Release
Finalize and prepare a skill for publication.

```bash
/skill-maker publish [skill-name]
```

**What it does:**
- Runs full test suite
- Validates documentation
- Checks code quality
- Creates version info
- Prepares release notes

## Best Practices

When creating skills, follow these patterns:

### 1. **Clear Purpose**
Each skill should do one thing well.
```
✓ /format-json - Formats and validates JSON
✗ /do-everything - Does JSON, YAML, XML, CSV...
```

### 2. **Simple Input/Output**
Keep parameters minimal and return values clear.
```
Input: text, format
Output: formatted string, validation result
```

### 3. **Error Handling**
Always handle edge cases gracefully.
```
- Invalid input
- Empty/null values
- Format mismatches
- File access errors
```

### 4. **Documentation**
Include examples and use cases.
```
- Basic usage example
- Advanced options
- Common errors and solutions
- Performance notes
```

## Skill Template

When `/skill-maker create` generates a skill, it follows this structure:

```
skill-name/
├── index.js          # Main skill logic
├── README.md         # Documentation
├── tests/
│   └── index.test.js # Test cases
└── config.json       # Skill configuration
```

## Examples

### Example 1: Creating a Code Formatter Skill

```bash
/skill-maker create

Prompts:
Name: code-formatter
Purpose: Format and validate code in multiple languages
Inputs: code (string), language (enum), style (optional)
Outputs: formatted code, validation errors
Target Users: developers

Generated files:
- skill-maker/code-formatter/
- Automated tests
- Documentation with examples
```

### Example 2: Enhancing an Existing Skill

```bash
/skill-maker enhance json-converter

Analysis:
- Missing error handling for circular references
- Input validation could be stricter
- Performance issue with large files
- Documentation lacks examples

Improvements applied:
✓ Added try-catch blocks
✓ Implemented input schema validation
✓ Optimized for large files
✓ Added 5 usage examples
```

### Example 3: Testing a Skill

```bash
/skill-maker test markdown-converter

Test Results:
✓ Basic conversion (10ms)
✓ Complex nesting (25ms)
✓ Error handling (5ms)
✓ Edge cases (8ms)

Coverage: 94%
All tests passed!
```

## Advanced Features

### Custom Validators
Define what valid inputs look like:
```javascript
validators: {
  email: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  url: /^https?:\/\/.+/,
  port: (val) => val > 0 && val < 65536
}
```

### Async Operations
Skills can perform async tasks:
```javascript
async function processFile(filepath) {
  const content = await readFile(filepath);
  return await transform(content);
}
```

### Chaining Skills
Combine multiple skills:
```bash
/first-skill input | /second-skill | /third-skill
```

## Configuration Reference

Each skill has a `config.json`:

```json
{
  "name": "skill-name",
  "version": "1.0.0",
  "description": "What this skill does",
  "author": "Your Name",
  "inputs": [
    {
      "name": "param1",
      "type": "string",
      "required": true,
      "description": "What this param does"
    }
  ],
  "outputs": [
    {
      "name": "result",
      "type": "string",
      "description": "What is returned"
    }
  ],
  "timeout": 30000,
  "rateLimit": null
}
```

## Troubleshooting

**Skill not appearing in suggestions?**
- Verify `config.json` is valid
- Check file permissions
- Restart Claude Code

**Skill running slowly?**
- Use `/skill-maker test` to profile
- Check for sync operations that should be async
- Optimize loops and data structures

**Tests failing?**
- Run `/skill-maker test` for detailed output
- Review error messages
- Check input validation logic

## Quick Start

1. Run `/skill-maker create` to start a new skill
2. Answer the guided questions
3. Review generated files
4. Run `/skill-maker test [skill-name]` to validate
5. Run `/skill-maker document [skill-name]` to add docs
6. Run `/skill-maker publish [skill-name]` when ready

---

**Tips for learning:**
- Start with simple skills (single input, single output)
- Look at existing skill examples
- Test edge cases thoroughly
- Document as you code
- Get feedback from other users
