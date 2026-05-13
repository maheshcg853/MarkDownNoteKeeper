#!/usr/bin/env python3
"""Markdown Note Keeper - A simple CLI app to manage markdown notes."""

import os
import sys
from datetime import datetime

NOTES_DIR = "my_notes"

TEMPLATES = {
    "meeting": {
        "description": "Meeting notes with attendees, agenda, and action items",
        "content": (
            "## Attendees\n\n- \n\n"
            "## Agenda\n\n1. \n\n"
            "## Discussion Notes\n\n\n\n"
            "## Action Items\n\n- [ ] \n"
        ),
    },
    "todo": {
        "description": "Todo list with priority sections",
        "content": (
            "## High Priority\n\n- [ ] \n\n"
            "## Medium Priority\n\n- [ ] \n\n"
            "## Low Priority\n\n- [ ] \n"
        ),
    },
    "journal": {
        "description": "Daily journal entry with prompts",
        "content": (
            "## How I'm Feeling\n\n\n\n"
            "## What I Accomplished Today\n\n- \n\n"
            "## What I Learned\n\n- \n\n"
            "## Goals for Tomorrow\n\n- \n"
        ),
    },
}


def ensure_notes_dir():
    """Create the notes directory if it doesn't exist."""
    os.makedirs(NOTES_DIR, exist_ok=True)


def create_note(title, content="", template_name=None):
    """Create a new markdown note, optionally using a template."""
    if not title or not title.strip() or not sanitize_filename(title):
        print("Error: Title cannot be empty.")
        return None

    if template_name:
        if template_name not in TEMPLATES:
            print(f"Error: Unknown template '{template_name}'.")
            print("Available templates: " + ", ".join(sorted(TEMPLATES.keys())))
            return None
        template_content = TEMPLATES[template_name]["content"]
    else:
        template_content = None

    ensure_notes_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{timestamp}_{sanitize_filename(title)}.md"
    filepath = os.path.join(NOTES_DIR, filename)

    with open(filepath, "w") as f:
        f.write(f"# {title}\n\n")
        f.write(f"*Created: {datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n")
        if template_content:
            f.write(template_content)
        if content:
            f.write(content + "\n")

    print(f"Created: {filename}")
    return filename


def list_notes():
    """List all notes."""
    ensure_notes_dir()
    notes = sorted(
        [f for f in os.listdir(NOTES_DIR) if f.endswith(".md")],
        reverse=True,
    )

    if not notes:
        print("No notes found.")
        return

    print(f"\n{'#':<4} {'Title':<40} {'Date':<12}")
    print("-" * 56)
    for i, note in enumerate(notes, 1):
        title = get_note_title(os.path.join(NOTES_DIR, note))
        date = note[:8]
        formatted_date = f"{date[:4]}-{date[4:6]}-{date[6:8]}"
        print(f"{i:<4} {title:<40} {formatted_date:<12}")


def view_note(identifier):
    """View a note by number or filename."""
    filepath = resolve_note(identifier)
    if not filepath:
        return

    with open(filepath, "r") as f:
        print(f.read())


def delete_note(identifier):
    """Delete a note by number or filename."""
    filepath = resolve_note(identifier)
    if not filepath:
        return

    filename = os.path.basename(filepath)
    os.remove(filepath)
    print(f"Deleted: {filename}")


def resolve_note(identifier):
    """Resolve a note identifier (number or filename) to a filepath."""
    ensure_notes_dir()
    notes = sorted(
        [f for f in os.listdir(NOTES_DIR) if f.endswith(".md")],
        reverse=True,
    )

    if not notes:
        print("No notes found.")
        return None

    # Try as a number
    try:
        index = int(identifier) - 1
        if 0 <= index < len(notes):
            return os.path.join(NOTES_DIR, notes[index])
        else:
            print(f"Invalid note number. Use 1-{len(notes)}.")
            return None
    except ValueError:
        pass

    # Try as filename
    filepath = os.path.join(NOTES_DIR, identifier)
    if os.path.exists(filepath):
        return filepath

    print(f"Note not found: {identifier}")
    return None


def get_note_title(filepath):
    """Extract the title from a note file."""
    try:
        with open(filepath, "r") as f:
            first_line = f.readline().strip()
            return first_line.lstrip("# ") if first_line.startswith("#") else "Untitled"
    except (IOError, OSError):
        return "Untitled"


def sanitize_filename(name):
    """Convert a string to a safe filename."""
    return "".join(c if c.isalnum() or c in "-_ " else "" for c in name).strip().replace(" ", "_")


def search_notes(keyword):
    """Search notes by keyword in title or content (case-insensitive)."""
    ensure_notes_dir()
    notes = sorted(
        [f for f in os.listdir(NOTES_DIR) if f.endswith(".md")],
        reverse=True,
    )

    if not notes:
        print("No notes found.")
        return

    keyword_lower = keyword.lower()
    matches = []

    for note in notes:
        filepath = os.path.join(NOTES_DIR, note)
        title = get_note_title(filepath)
        try:
            with open(filepath, "r") as f:
                content = f.read()
        except (IOError, OSError):
            content = ""

        if keyword_lower in title.lower() or keyword_lower in content.lower():
            matches.append((note, title))

    if not matches:
        print(f"No notes matching '{keyword}' found.")
        return

    print(f"\n{'#':<4} {'Title':<40} {'Date':<12}")
    print("-" * 56)
    for i, (note, title) in enumerate(matches, 1):
        date = note[:8]
        formatted_date = f"{date[:4]}-{date[4:6]}-{date[6:8]}"
        print(f"{i:<4} {title:<40} {formatted_date:<12}")


def list_templates():
    """List all available note templates."""
    print("\nAvailable Templates")
    print("=" * 40)
    for name in sorted(TEMPLATES.keys()):
        description = TEMPLATES[name]["description"]
        print(f"  {name:<12} {description}")
    print(f"\nUsage: python notes.py create --template <name> \"<title>\"")


def print_help():
    """Print usage information."""
    print("""
Markdown Note Keeper
====================

Usage:
  python notes.py create <title> [content]               Create a new note
  python notes.py create --template <name> <title>       Create a note from a template
  python notes.py templates                              List available templates
  python notes.py list                                   List all notes
  python notes.py search <keyword>                       Search notes by keyword
  python notes.py view <number|filename>                 View a note
  python notes.py delete <number|filename>               Delete a note
  python notes.py help                                   Show this help

Templates:
  meeting    Meeting notes with attendees, agenda, and action items
  todo       Todo list with priority sections
  journal    Daily journal entry with prompts
""")


def main():
    if len(sys.argv) < 2:
        print_help()
        return

    command = sys.argv[1].lower()

    if command == "create":
        if len(sys.argv) < 3:
            print("Usage: python notes.py create [--template <name>] <title> [content]")
            return

        # Parse --template flag
        template_name = None
        args = sys.argv[2:]

        if args[0] == "--template":
            if len(args) < 3:
                print("Usage: python notes.py create --template <name> <title> [content]")
                return
            template_name = args[1]
            args = args[2:]

        title = args[0]
        if not title.strip():
            print("Error: Title cannot be empty.")
            return
        content = " ".join(args[1:]) if len(args) > 1 else ""
        create_note(title, content, template_name=template_name)

    elif command == "templates":
        list_templates()

    elif command == "list":
        list_notes()

    elif command == "search":
        if len(sys.argv) < 3:
            print("Usage: python notes.py search <keyword>")
            return
        search_notes(sys.argv[2])

    elif command == "view":
        if len(sys.argv) < 3:
            print("Usage: python notes.py view <number|filename>")
            return
        view_note(sys.argv[2])

    elif command == "delete":
        if len(sys.argv) < 3:
            print("Usage: python notes.py delete <number|filename>")
            return
        delete_note(sys.argv[2])

    elif command == "help":
        print_help()

    else:
        print(f"Unknown command: {command}")
        print_help()


if __name__ == "__main__":
    main()
