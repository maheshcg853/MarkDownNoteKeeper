# Markdown Note Keeper

A simple CLI application to create, list, view, and delete markdown notes — organized into notebooks. No dependencies — just Python 3.

## Usage

### Basic Note Commands

```bash
python notes.py create "My First Note" "This is the content"
python notes.py list
python notes.py view 1
python notes.py delete 1
python notes.py search "keyword"
python notes.py help
```

### Notebooks

Organize your notes into notebooks (folders). Notes without a notebook live in the root `my_notes/` directory.

#### Manage Notebooks

```bash
python notes.py notebook create work
python notes.py notebook create personal
python notes.py notebook list
python notes.py notebook delete old_stuff
```

#### Create Notes in a Notebook

```bash
python notes.py create "Meeting Notes" "Discussed Q3 goals" -n work
python notes.py create "Grocery List" "Milk, eggs, bread" -n personal
```

#### List Notes in a Notebook

```bash
python notes.py list -n work
python notes.py list -n personal
```

#### View and Delete Notes in a Notebook

```bash
python notes.py view 1 -n work
python notes.py delete 2 -n personal
```

#### Search Notes

Search across all notebooks:

```bash
python notes.py search "meeting"
```

Search within a specific notebook:

```bash
python notes.py search "goals" -n work
```

#### Move Notes Between Notebooks

Move a note from root to a notebook:

```bash
python notes.py move 1 work
```

Move a note from one notebook to another:

```bash
python notes.py move 1 personal -n work
```

## Command Reference

| Command | Description |
|---------|-------------|
| `create <title> [content] [-n notebook]` | Create a new note |
| `list [-n notebook]` | List all notes |
| `search <keyword> [-n notebook]` | Search notes by keyword |
| `view <number\|filename> [-n notebook]` | View a note |
| `delete <number\|filename> [-n notebook]` | Delete a note |
| `move <number\|filename> <target> [-n source]` | Move a note to a notebook |
| `notebook create <name>` | Create a new notebook |
| `notebook list` | List all notebooks |
| `notebook delete <name>` | Delete a notebook and its notes |
| `help` | Show help |

## Options

| Flag | Description |
|------|-------------|
| `-n`, `--notebook` | Specify the notebook for the operation |

## How It Works

Notes are stored as `.md` files in the `my_notes/` folder. Notebooks are subdirectories within `my_notes/`. Each note has a timestamp-based filename and contains a markdown title, creation date, and your content.

```
my_notes/
├── 20250513_100000_My_First_Note.md
├── work/
│   ├── 20250513_101000_Meeting_Notes.md
│   └── 20250513_102000_Project_Plan.md
└── personal/
    └── 20250513_103000_Grocery_List.md
```

## Requirements

- Python 3.10+
- No external dependencies
