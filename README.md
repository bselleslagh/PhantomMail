# Faketrix

[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
![GitHub License](https://img.shields.io/github/license/bselleslagh/faketrix)
![GitHub Release](https://img.shields.io/github/v/release/bselleslagh/faketrix)
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


## Configuration

Create a `.env.local` file in the root directory with the following variables:

```bash
RESEND_API_KEY= # Get from https://resend.com
GOOGLE_API_KEY= # Your Google API key for Gemini
SENDER_EMAIL= # Email address to send from
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY= # Optional: For LangChain debugging
LANGCHAIN_PROJECT=faketrix
```

## Usage
Run the application using UV:

```bash
uv run faketrix
```

The application will:
1. Prompt you for a recipient email address
2. Generate a fake transport order
3. Create an email using Gemini AI
4. Convert the content to HTML
5. Send the email via Resend

## Project Structure

- `src/faketrix/main.py`: Entry point and email recipient handling
- `src/faketrix/graphs/`: LangGraph implementation
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