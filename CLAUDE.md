# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

sumMyMail is a Python Windows desktop application that processes email threads using OpenAI's GPT-4o model. It provides:
- Concise summaries of email threads
- Action items extraction for Eduardo Mangarelli
- Participant list extraction

The application is built with tkinter for the GUI and uses the OpenAI Python client for API integration.

## Key Commands

### Running the Application
```bash
python sumMyMail.py
```

### Installing Dependencies
```bash
pip install -r requirements.txt
```

### Testing the Application
- No automated test suite currently exists
- Manual testing: run the application and paste an email thread to verify processing

## Architecture

### Single-File Application
The entire application is contained in `sumMyMail.py` with a simple class-based architecture:

**EmailSummarizerApp Class** (sumMyMail.py:17-189)
- Main application class that handles both UI and business logic
- Key components:
  - `setup_ui()`: Creates tkinter GUI with input/output text areas and progress bar
  - `load_api_key()`: Loads OpenAI API key from `config.ini` or environment variable
  - `process_email()`: Orchestrates the email processing workflow
  - `analyze_email_thread()`: Sends email text to GPT-4o with structured system prompt
  - `display_results()`: Updates GUI with analysis results

### Configuration Management
- API key is loaded from `config.ini` (primary) or `OPENAI_API_KEY` environment variable (fallback)
- `config.ini` is git-ignored for security
- `config.ini.example` provides the configuration template

### GPT-4o Integration
- Model: `gpt-4o` (configurable via `MODEL_NAME` constant)
- Temperature: `0.3` (for consistency)
- Max tokens: `1000`
- System prompt (sumMyMail.py:153-170) defines structured output format with three sections: SUMMARY, ACTION ITEMS, and PARTICIPANTS

## Development Notes

### Modifying the AI Prompt
The system prompt that instructs GPT-4o is in the `analyze_email_thread()` method (sumMyMail.py:153-170). Changes to the analysis format or focus should be made here.

### Changing Model Parameters
Model configuration constants are defined at the class level (sumMyMail.py:19-21):
- `MODEL_NAME`: The OpenAI model to use
- `TEMPERATURE`: Controls randomness (0-1)
- `MAX_TOKENS`: Maximum response length

### Adding New Features
Since this is a single-file application with coupled UI and logic:
1. UI changes go in `setup_ui()` method
2. Processing logic changes go in `process_email()` or `analyze_email_thread()`
3. Consider refactoring into separate modules if adding significant functionality

### Error Handling
- API key validation occurs on startup (sumMyMail.py:29-37)
- OpenAI API errors are caught in the `process_email()` try/except block (sumMyMail.py:136-149)
- User-facing errors are displayed via tkinter messageboxes
