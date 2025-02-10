# PhantomMail

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
![GitHub License](https://img.shields.io/github/license/bselleslagh/phantommail)
![GitHub Release](https://img.shields.io/github/v/release/bselleslagh/phantommail)
![X (formerly Twitter) Follow](https://img.shields.io/twitter/follow/BenSelleslagh)


A Python application that generates and sends fake transport order emails using Google's Gemini 2.0 Flash model and Resend for email delivery.

## Features

- Generates realistic transport order data
- Creates convincing email content using Gemini 2.0 Flash
- Converts email content to HTML format
- Sends emails via Resend
- Supports multiple writing styles and languages

## Installation

1. Clone the repository
2. Install dependencies using UV:

```bash
uv sync
```

### Install Pre-Commit Hooks

To ensure code quality, install pre-commit hooks by running the following commands:

1. **Set Up Git Hooks**:
   ```bash
   pre-commit install
   ```
   This will ensure the hooks run automatically before you commit any changes.

2. **Run Hooks on All Files** (Optional):
   ```bash
   pre-commit run --all-files
   ```
   Use this command to apply the hooks across the entire codebase if you're contributing 
   for the first time or after changes to the pre-commit config.

Notes

- Make sure to run these commands after cloning the repository.
- For more details, refer to pre-commit documentation.


## Configuration

Create a `.env.local` file in the root directory with the following variables:

```bash
RESEND_API_KEY= # Get from https://resend.com
GOOGLE_API_KEY= # Your Google API key for Gemini
SENDER_EMAIL= # Email address to send from
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY= # Optional: For LangChain debugging
LANGCHAIN_PROJECT=phantommail
```

## Usage
Run the application using UV:

```bash
uv run phantommail
```

The application will:
1. Prompt you for a recipient email address
2. Generate a fake transport order
3. Create an email using Gemini AI
4. Convert the content to HTML
5. Send the email via Resend

## Project Structure

- `src/phantommail/main.py`: Entry point and email recipient handling
- `src/phantommail/graphs/`: LangGraph implementation
  - `state.py`: State management for the email generation pipeline
  - `nodes.py`: Graph nodes for data generation, email creation, and sending

## Dependencies

- LangChain
- LangGraph
- Google Generative AI (Gemini Flash 2.0)
- Resend
- Python-dotenv

## Getting Started with Resend

1. Create an account at [https://resend.com](https://resend.com)
2. Get your API key from the dashboard
3. Add the API key to your `.env.local` file

## License
MIT