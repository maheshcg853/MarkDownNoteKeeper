#!/usr/bin/env python3
"""Markdown Note Keeper - A simple CLI app to manage markdown notes."""

import os
import shutil
import sys
from datetime import datetime

NOTES_DIR = "my_notes"


def ensure_notes_dir() -> None:
    """Create the notes directory if it doesn't exist."""
    os.makedirs(NOTES_DIR, exist_ok=True)


def get_notebook_path(notebook: str | None = None) -> str:
    """Return the path to the notebook directory, or the root notes directory.

    Args:
        notebook: Optional notebook name. If None, returns root notes dir.

    Returns:
        The resolved directory path for the notebook.
    """
    if notebook:
        return os.path.join(NOTES_DIR, sanitize_filename(notebook))
    return NOTES_DIR


def ensure_notebook_dir(notebook: str | None = None) -> str:
    """Ensure the target notebook directory exists and return its path.

    Args:
        notebook: Optional notebook name.

    Returns:
        The path to the notebook directory.
    """
    path = get_notebook_path(notebook)
    os.makedirs(path, exist_ok=True)
    return path


# --- Notebook management ---


def create_notebook(name: str) -> None:
    """Create a new notebook (subdirectory).

    Args:
        name: The name of the notebook to create.
    """
    if not name or not name.strip():
        print("Error: Notebook name cannot be empty.")
        return

    sanitized = sanitize_filename(name)
    if not sanitized:
        print("Error: Invalid notebook name.")
        return

    notebook_path = os.path.join(NOTES_DIR, sanitized)
    if os.path.exists(notebook_path):
        print(f"Notebook '{sanitized}' already exists.")
        return

    os.makedirs(notebook_path, exist_ok=True)
    print(f"Created notebook: {sanitized}")


def list_notebooks() -> None:
    """List all notebooks."""
    ensure_notes_dir()
    notebooks = sorted(
        entry
        for entry in os.listdir(NOTES_DIR)
        if os.path.isdir(os.path.join(NOTES_DIR, entry))
    )

    if not notebooks:
        print("No notebooks found.")
        return

    print(f"\n{'#':<4} {'Notebook':<30} {'Notes':<6}")
    print("-" * 40)
    for i, nb in enumerate(notebooks, 1):
        nb_path = os.path.join(NOTES_DIR, nb)
        note_count = len([f for f in os.listdir(nb_path) if f.endswith(".md")])
        print(f"{i:<4} {nb:<30} {note_count:<6}")


def delete_notebook(name: str) -> None:
    """Delete a notebook and all its notes.

    Args:
        name: The name of the notebook to delete.
    """
    if not name or not name.strip():
        print("Error: Notebook name cannot be empty.")
        return

    sanitized = sanitize_filename(name)
    notebook_path = os.path.join(NOTES_DIR, sanitized)

    if not os.path.isdir(notebook_path):
        print(f"Notebook '{sanitized}' not found.")
        return

    note_count = len([f for f in os.listdir(notebook_path) if f.endswith(".md")])
    shutil.rmtree(notebook_path)
    print(f"Deleted notebook '{sanitized}' ({note_count} note(s) removed).")


# --- Note operations (notebook-aware) ---


def create_note(title: str, content: str = "", notebook: str | None = None) -> str | None:
    """Create a new markdown note.

    Args:
        title: The title of the note.
        content: Optional body content for the note.
        notebook: Optional notebook name to place the note in.

    Returns:
        The filename of the created note, or None on failure.
    """
    if not title or not title.strip() or not sanitize_filename(title):
        print("Error: Title cannot be empty.")
        return None

    notes_path = ensure_notebook_dir(notebook)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{sanitize_filename(title)}.md"
    filepath = os.path.join(notes_path, filename)

    with open(filepath, "w") as f:
        f.write(f"# {title}\n\n")
        f.write(f"*Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")
        if content:
            f.write(content + "\n")

    location = f" in notebook '{sanitize_filename(notebook)}'" if notebook else ""
    print(f"Created: {filename}{location}")
    return filename


def list_notes(notebook: str | None = None) -> None:
    """List all notes, optionally filtered by notebook.

    Args:
        notebook: Optional notebook name to list notes from.
    """
    notes_path = ensure_notebook_dir(notebook)
    notes = sorted(
        [f for f in os.listdir(notes_path) if f.endswith(".md")],
        reverse=True,
    )

    if not notes:
        location = f" in notebook '{sanitize_filename(notebook)}'" if notebook else ""
        print(f"No notes found{location}.")
        return

    header = f" [{sanitize_filename(notebook)}]" if notebook else ""
    print(f"\n{'#':<4} {'Title':<40} {'Date':<12}{header}")
    print("-" * 56)
    for i, note in enumerate(notes, 1):
        title = get_note_title(os.path.join(notes_path, note))
        date = note[:8]
        formatted_date = f"{date[:4]}-{date[4:6]}-{date[6:8]}"
        print(f"{i:<4} {title:<40} {formatted_date:<12}")


def view_note(identifier: str, notebook: str | None = None) -> None:
    """View a note by number or filename.

    Args:
        identifier: Note number or filename.
        notebook: Optional notebook to look in.
    """
    filepath = resolve_note(identifier, notebook)
    if not filepath:
        return

    with open(filepath, "r") as f:
        print(f.read())


def delete_note(identifier: str, notebook: str | None = None) -> None:
    """Delete a note by number or filename.

    Args:
        identifier: Note number or filename.
        notebook: Optional notebook to look in.
    """
    filepath = resolve_note(identifier, notebook)
    if not filepath:
        return

    filename = os.path.basename(filepath)
    os.remove(filepath)
    print(f"Deleted: {filename}")


def resolve_note(identifier: str, notebook: str | None = None) -> str | None:
    """Resolve a note identifier (number or filename) to a filepath.

    Args:
        identifier: Note number or filename.
        notebook: Optional notebook to look in.

    Returns:
        The filepath of the resolved note, or None if not found.
    """
    notes_path = ensure_notebook_dir(notebook)
    notes = sorted(
        [f for f in os.listdir(notes_path) if f.endswith(".md")],
        reverse=True,
    )

    if not notes:
        location = f" in notebook '{sanitize_filename(notebook)}'" if notebook else ""
        print(f"No notes found{location}.")
        return None

    # Try as a number
    try:
        index = int(identifier) - 1
        if 0 <= index < len(notes):
            return os.path.join(notes_path, notes[index])
        else:
            print(f"Invalid note number. Use 1-{len(notes)}.")
            return None
    except ValueError:
        pass

    # Try as filename
    filepath = os.path.join(notes_path, identifier)
    if os.path.exists(filepath):
        return filepath

    print(f"Note not found: {identifier}")
    return None


def get_note_title(filepath: str) -> str:
    """Extract the title from a note file.

    Args:
        filepath: Path to the note file.

    Returns:
        The extracted title, or 'Untitled' on failure.
    """
    try:
        with open(filepath, "r") as f:
            first_line = f.readline().strip()
            return first_line.lstrip("# ") if first_line.startswith("#") else "Untitled"
    except (IOError, OSError):
        return "Untitled"


def sanitize_filename(name: str) -> str:
    """Convert a string to a safe filename.

    Args:
        name: The raw string to sanitize.

    Returns:
        A filesystem-safe version of the string.
    """
    return "".join(c if c.isalnum() or c in "-_ " else "" for c in name).strip().replace(" ", "_")


def search_notes(keyword: str, notebook: str | None = None) -> None:
    """Search notes by keyword in title or content (case-insensitive).

    Args:
        keyword: The search keyword.
        notebook: Optional notebook to scope the search to.
    """
    ensure_notes_dir()

    # Determine which directories to search
    if notebook:
        dirs_to_search = [ensure_notebook_dir(notebook)]
    else:
        # Search root notes and all notebooks
        dirs_to_search = [NOTES_DIR]
        for entry in os.listdir(NOTES_DIR):
            entry_path = os.path.join(NOTES_DIR, entry)
            if os.path.isdir(entry_path):
                dirs_to_search.append(entry_path)

    keyword_lower = keyword.lower()
    matches: list[tuple[str, str, str]] = []  # (note filename, title, notebook name)

    for search_dir in dirs_to_search:
        notebook_name = (
            os.path.basename(search_dir) if search_dir != NOTES_DIR else ""
        )
        notes = sorted(
            [f for f in os.listdir(search_dir) if f.endswith(".md")],
            reverse=True,
        )
        for note in notes:
            filepath = os.path.join(search_dir, note)
            title = get_note_title(filepath)
            try:
                with open(filepath, "r") as f:
                    content = f.read()
            except (IOError, OSError):
                content = ""

            if keyword_lower in title.lower() or keyword_lower in content.lower():
                matches.append((note, title, notebook_name))

    if not matches:
        print(f"No notes matching '{keyword}' found.")
        return

    print(f"\n{'#':<4} {'Title':<35} {'Date':<12} {'Notebook':<15}")
    print("-" * 66)
    for i, (note, title, nb_name) in enumerate(matches, 1):
        date = note[:8]
        formatted_date = f"{date[:4]}-{date[4:6]}-{date[6:8]}"
        nb_display = nb_name if nb_name else "(root)"
        print(f"{i:<4} {title:<35} {formatted_date:<12} {nb_display:<15}")


def move_note(identifier: str, target_notebook: str, source_notebook: str | None = None) -> None:
    """Move a note from one location to another notebook.

    Args:
        identifier: Note number or filename in the source location.
        target_notebook: The destination notebook name.
        source_notebook: Optional source notebook (None = root).
    """
    filepath = resolve_note(identifier, source_notebook)
    if not filepath:
        return

    target_dir = ensure_notebook_dir(target_notebook)
    filename = os.path.basename(filepath)
    target_path = os.path.join(target_dir, filename)

    if os.path.exists(target_path):
        print(f"A note with the same filename already exists in '{sanitize_filename(target_notebook)}'.")
        return

    shutil.move(filepath, target_path)
    source_label = f"'{sanitize_filename(source_notebook)}'" if source_notebook else "root"
    print(f"Moved '{filename}' from {source_label} to '{sanitize_filename(target_notebook)}'.")


def print_help() -> None:
    """Print usage information."""
    print("""
Markdown Note Keeper
====================

Usage:
  python notes.py create <title> [content] [-n notebook]   Create a new note
  python notes.py list [-n notebook]                        List all notes
  python notes.py search <keyword> [-n notebook]            Search notes by keyword
  python notes.py view <number|filename> [-n notebook]      View a note
  python notes.py delete <number|filename> [-n notebook]    Delete a note
  python notes.py move <number|filename> <target_notebook> [-n source_notebook]
                                                            Move a note to a notebook

Notebook Commands:
  python notes.py notebook create <name>    Create a new notebook
  python notes.py notebook list             List all notebooks
  python notes.py notebook delete <name>    Delete a notebook and its notes

Options:
  -n, --notebook <name>    Specify notebook for the operation

  python notes.py help     Show this help
""")


def extract_notebook_flag(args: list[str]) -> tuple[list[str], str | None]:
    """Extract the -n / --notebook flag and its value from the argument list.

    Args:
        args: The raw argument list.

    Returns:
        A tuple of (remaining args, notebook name or None).
    """
    notebook = None
    remaining: list[str] = []
    i = 0
    while i < len(args):
        if args[i] in ("-n", "--notebook") and i + 1 < len(args):
            notebook = args[i + 1]
            i += 2
        else:
            remaining.append(args[i])
            i += 1
    return remaining, notebook


def main() -> None:
    """Entry point for the CLI application."""
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1].lower()

    if command == "create":
        args, notebook = extract_notebook_flag(sys.argv[2:])
        if len(args) < 1:
            print("Usage: python notes.py create <title> [content] [-n notebook]")
            return
        title = args[0]
        if not title.strip():
            print("Error: Title cannot be empty.")
            return
        content = " ".join(args[1:]) if len(args) > 1 else ""
        create_note(title, content, notebook)

    elif command == "list":
        _, notebook = extract_notebook_flag(sys.argv[2:])
        list_notes(notebook)

    elif command == "search":
        args, notebook = extract_notebook_flag(sys.argv[2:])
        if len(args) < 1:
            print("Usage: python notes.py search <keyword> [-n notebook]")
            return
        search_notes(args[0], notebook)

    elif command == "view":
        args, notebook = extract_notebook_flag(sys.argv[2:])
        if len(args) < 1:
            print("Usage: python notes.py view <number|filename> [-n notebook]")
            return
        view_note(args[0], notebook)

    elif command == "delete":
        args, notebook = extract_notebook_flag(sys.argv[2:])
        if len(args) < 1:
            print("Usage: python notes.py delete <number|filename> [-n notebook]")
            return
        delete_note(args[0], notebook)

    elif command == "move":
        args, notebook = extract_notebook_flag(sys.argv[2:])
        if len(args) < 2:
            print("Usage: python notes.py move <number|filename> <target_notebook> [-n source_notebook]")
            return
        move_note(args[0], args[1], notebook)

    elif command == "notebook":
        if len(sys.argv) < 3:
            print("Usage: python notes.py notebook <create|list|delete> [name]")
            return
        sub_command = sys.argv[2].lower()
        if sub_command == "create":
            if len(sys.argv) < 4:
                print("Usage: python notes.py notebook create <name>")
                return
            create_notebook(sys.argv[3])
        elif sub_command == "list":
            list_notebooks()
        elif sub_command == "delete":
            if len(sys.argv) < 4:
                print("Usage: python notes.py notebook delete <name>")
                return
            delete_notebook(sys.argv[3])
        else:
            print(f"Unknown notebook command: {sub_command}")

    elif command == "help":
        print_help()

    else:
        print(f"Unknown command: {command}")
        print_help()


if __name__ == "__main__":
    main()
