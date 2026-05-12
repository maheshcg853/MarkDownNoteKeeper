# Markdown Note Keeper

A simple CLI application to create, list, view, and delete markdown notes. No dependencies — just Python 3.

## Usage

```bash
python notes.py create "My First Note" "This is the content"
python notes.py list
python notes.py view 1
python notes.py delete 1
python notes.py help
```

## How it works

Notes are stored as `.md` files in the `my_notes/` folder. Each note has a timestamp-based filename and contains a markdown title, creation date, and your content.

## Requirements

- Python 3.6+
- No external dependencies
