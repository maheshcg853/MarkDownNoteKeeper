# Markdown Note Keeper

A simple CLI application to create, list, view, and delete markdown notes. No dependencies — just Python 3.

## Usage

```bash
python notes.py create "My First Note" "This is the content"
python notes.py create --template meeting "Standup 2025-01-15"
python notes.py templates
python notes.py list
python notes.py search "keyword"
python notes.py view 1
python notes.py delete 1
python notes.py help
```

## Templates

Pre-defined templates scaffold the note structure for common use cases:

| Template | Description |
|----------|-------------|
| meeting  | Meeting notes with attendees, agenda, and action items |
| todo     | Todo list with priority sections |
| journal  | Daily journal entry with prompts |

Use `python notes.py templates` to see all available templates.

### Example

```bash
python notes.py create --template meeting "Standup 2025-01-15"
```

This creates a note pre-filled with sections for attendees, agenda, discussion notes, and action items.

## How it works

Notes are stored as `.md` files in the `my_notes/` folder. Each note has a timestamp-based filename and contains a markdown title, creation date, and your content.

## Requirements

- Python 3.6+
- No external dependencies
