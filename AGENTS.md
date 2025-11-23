# Agent Guidelines for sumMyMail

These instructions apply to all files in this repository.

## Development Practices
- Prefer clear, beginner-friendly Python code; avoid unnecessary abstractions.
- Keep the tkinter UI layout consistent with the existing structure and ensure widgets remain accessible with keyboard navigation.
- Treat `config.ini` as secret configuration; never hard-code real API keys or commit user-specific settings.
- When interacting with the OpenAI client, reuse the existing `EmailSummarizerApp` patterns and keep model settings as constants near the top of the class.
- Include docstrings for new functions or classes explaining their role in the GUI workflow.

## Testing & Validation
- If you modify application logic, sanity-check by running `python sumMyMail.py` when possible; otherwise, explain in your summary why runtime validation was skipped.
- Ensure new dependencies are added to `requirements.txt`.

## Documentation & Style
- Update `README.md` if behavior, setup, or configuration steps change.
- Follow Markdown best practices: use descriptive headings, ordered lists for sequences, and fenced code blocks for commands.
- Keep user-facing strings concise and free of jargon.

## Version Control
- Keep commits scoped and descriptive; avoid bundling unrelated changes.
- Do not remove existing instructions from this file without justification.
