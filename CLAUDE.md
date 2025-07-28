# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Development Commands

### Essential Commands
- **Run the application**: `uv run phantommail`
- **Install/sync dependencies**: `uv sync`
- **Add dependencies**: `uv add package_name` (never manually edit pyproject.toml)
- **Remove dependencies**: `uv remove package_name`
- **Add dev dependencies**: `uv add --dev package_name`

### Code Quality & Testing
- **Run linter**: `uv run ruff check --fix`
- **Format code**: `uv run ruff format`
- **Run tests**: `uv run pytest`
- **Run specific test**: `uv run pytest tests/phantommail/test_transport.py::test_name`
- **Install pre-commit hooks**: `pre-commit install`
- **Run pre-commit on all files**: `pre-commit run --all-files`

### LangGraph Development
- **Launch local LangGraph server**: `uvx --refresh --from "langgraph-cli[inmem]" --with-editable . --python 3.13 langgraph dev`

## Architecture Overview

PhantomMail is a LangGraph-based application that generates and sends realistic transport-related emails using AI. The system follows a graph-based state machine pattern:

### Core Flow
1. **Entry Point** (`src/phantommail/main.py`): CLI interface that prompts for recipient email
2. **State Graph** (`src/phantommail/graphs/graph.py`): Defines the workflow with conditional routing based on email type
3. **State Management** (`src/phantommail/graphs/state.py`): FakeEmailState TypedDict maintains data flow between nodes
4. **Graph Nodes** (`src/phantommail/graphs/nodes.py`): Contains async node implementations for each email type

### Email Generation Pipeline
The system supports four email types, each with its own generation flow:
- **Transport Orders**: Fake shipping orders with pickup/delivery details
- **Customs Declarations**: Documents with PDF attachments generated from HTML templates
- **Customer Questions**: Natural language inquiries about shipments
- **Complaints**: Customer complaint emails

### Key Components
- **Fakers** (`src/phantommail/fakers/`): Generate realistic fake data using Faker library
- **Models** (`src/phantommail/models/`): Pydantic models for type safety
- **Email Sending** (`src/phantommail/send_email.py`): Resend integration for delivery
- **PDF Generation** (`src/phantommail/helpers/html_to_pdf.py`): Creates PDF attachments from HTML

### AI Integration
- Uses Google Gemini 2.5 Flash for content generation
- Structured output via Pydantic models
- System/Human message pattern for consistent generation

### Configuration
The app requires environment variables in `.env.local`:
- `RESEND_API_KEY`: Email delivery service
- `GOOGLE_API_KEY`: Gemini AI access
- `SENDER_EMAIL`: From address
- `LANGCHAIN_*`: Optional debugging/tracing