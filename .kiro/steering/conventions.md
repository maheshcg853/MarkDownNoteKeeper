# Project Conventions

## Language & Runtime
- Python 3.6+ with standard library only
- No external dependencies allowed
- Single-file application (`notes.py`)

## Code Style
- Use snake_case for functions and variables
- Include docstrings for all functions
- Keep functions short and focused (under 30 lines)
- Use type hints where they improve clarity

## File Storage
- Notes are stored as markdown files in `my_notes/`
- Filenames use the pattern: `YYYYMMDD_HHMMSS_title.md`
- Never overwrite existing notes

## Testing
- Tests go in `test_notes.py`
- Use Python's built-in `unittest` module
- Each public function should have at least one test

## Error Handling
- Print user-friendly error messages to stdout
- Never crash on bad input — handle gracefully
- Return early on errors rather than nesting
