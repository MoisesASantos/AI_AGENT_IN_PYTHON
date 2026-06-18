# AI Agent in Python

This project is an AI-powered coding agent built in Python using the Gemini API.  
The agent is capable of reading, understanding, and modifying a local codebase using function calling (tools).

It can:
- Explore the filesystem
- Read file contents
- Execute Python files
- Write or modify files
- Debug issues based on user instructions

---

## Project Overview

The goal of this project is to simulate a simple autonomous coding agent that can iteratively solve tasks by interacting with a codebase.

Instead of directly answering user questions, the agent:
1. Plans actions using an LLM (Gemini)
2. Calls tools (functions) to interact with the filesystem
3. Processes results
4. Repeats until the task is completed

This mimics how modern AI coding agents (like SWE agents) operate.

---

##  Features

- LLM-powered reasoning (Gemini 2.5 Flash)
- Tool/function calling system
- Iterative agent loop (up to 20 steps)
- File system exploration
- Python code execution
- File reading and writing
- Debugging capabilities based on expected behavior

---

##  Available Tools

The agent can use the following functions:

- `get_files_info(directory)`  
  Lists files and directories with metadata.

- `get_file_content(file_path)`  
  Reads the content of a file.

- `run_python_file(file_path, args)`  
  Executes a Python file with optional arguments.

- `write_file(file_path, content)`  
  Creates or overwrites a file.

---

##  Architecture

The system is composed of:

### 1. LLM Layer
- Gemini model (`gemini-2.5-flash`)
- Receives user input and tool results
- Decides next action

### 2. Agent Loop
- Runs up to 20 iterations
- Handles tool calls
- Maintains conversation history

### 3. Tool System
- Maps function names to Python implementations
- Executes safe filesystem operations

---

##  Execution Flow

1. User sends a request
2. Agent sends request to LLM
3. LLM returns either:
   - Final answer
   - Tool calls
4. If tool calls exist:
   - Execute tools
   - Append results to context
   - Repeat loop
5. If final answer:
   - Print response and exit

---

##  Example Usage

### Run a Python file
```bash
uv run main.py "run tests.py"

##  Project Structure

AI_AGENT_IN_PYTHON/
│
├── main.py
├── call_function.py
├── prompts.py
│
├── functions/
│   ├── get_files_info.py
│   ├── get_file_content.py
│   ├── run_python_file.py
│   └── write_file.py
│
├── pkg/
│   ├── calculator.py
│   └── render.py
│
└── tests.py
