"""Tests for the Note Templates feature."""

import os
import shutil
import subprocess
import sys
import tempfile
import unittest

# Import the module under test
sys.path.insert(0, os.path.dirname(__file__))
import notes


class TestTemplates(unittest.TestCase):
    """Test template definitions and the list_templates command."""

    def test_templates_defined(self):
        """All expected templates exist."""
        self.assertIn("meeting", notes.TEMPLATES)
        self.assertIn("todo", notes.TEMPLATES)
        self.assertIn("journal", notes.TEMPLATES)

    def test_templates_have_description(self):
        """Each template has a non-empty description."""
        for name, tmpl in notes.TEMPLATES.items():
            self.assertIn("description", tmpl)
            self.assertTrue(len(tmpl["description"]) > 0, f"{name} has empty description")

    def test_templates_have_content(self):
        """Each template has non-empty content."""
        for name, tmpl in notes.TEMPLATES.items():
            self.assertIn("content", tmpl)
            self.assertTrue(len(tmpl["content"]) > 0, f"{name} has empty content")

    def test_meeting_template_structure(self):
        """Meeting template includes expected sections."""
        content = notes.TEMPLATES["meeting"]["content"]
        self.assertIn("## Attendees", content)
        self.assertIn("## Agenda", content)
        self.assertIn("## Action Items", content)

    def test_todo_template_structure(self):
        """Todo template includes priority sections."""
        content = notes.TEMPLATES["todo"]["content"]
        self.assertIn("## High Priority", content)
        self.assertIn("## Medium Priority", content)
        self.assertIn("## Low Priority", content)

    def test_journal_template_structure(self):
        """Journal template includes expected prompts."""
        content = notes.TEMPLATES["journal"]["content"]
        self.assertIn("## How I'm Feeling", content)
        self.assertIn("## What I Accomplished Today", content)
        self.assertIn("## Goals for Tomorrow", content)


class TestCreateWithTemplate(unittest.TestCase):
    """Test creating notes with templates."""

    def setUp(self):
        """Set up a temporary notes directory."""
        self.original_notes_dir = notes.NOTES_DIR
        self.tmp_dir = tempfile.mkdtemp()
        notes.NOTES_DIR = self.tmp_dir

    def tearDown(self):
        """Restore original notes directory and clean up."""
        notes.NOTES_DIR = self.original_notes_dir
        shutil.rmtree(self.tmp_dir)

    def test_create_with_meeting_template(self):
        """Creating a note with meeting template includes template content."""
        filename = notes.create_note("Standup 2025-01-15", template_name="meeting")
        self.assertIsNotNone(filename)

        filepath = os.path.join(self.tmp_dir, filename)
        with open(filepath, "r") as f:
            content = f.read()

        self.assertIn("# Standup 2025-01-15", content)
        self.assertIn("## Attendees", content)
        self.assertIn("## Agenda", content)
        self.assertIn("## Action Items", content)

    def test_create_with_todo_template(self):
        """Creating a note with todo template includes template content."""
        filename = notes.create_note("Sprint Tasks", template_name="todo")
        self.assertIsNotNone(filename)

        filepath = os.path.join(self.tmp_dir, filename)
        with open(filepath, "r") as f:
            content = f.read()

        self.assertIn("# Sprint Tasks", content)
        self.assertIn("## High Priority", content)
        self.assertIn("- [ ]", content)

    def test_create_with_journal_template(self):
        """Creating a note with journal template includes template content."""
        filename = notes.create_note("Monday Reflection", template_name="journal")
        self.assertIsNotNone(filename)

        filepath = os.path.join(self.tmp_dir, filename)
        with open(filepath, "r") as f:
            content = f.read()

        self.assertIn("# Monday Reflection", content)
        self.assertIn("## How I'm Feeling", content)
        self.assertIn("## Goals for Tomorrow", content)

    def test_create_with_invalid_template(self):
        """Creating a note with unknown template prints error and returns None."""
        filename = notes.create_note("Test Note", template_name="nonexistent")
        self.assertIsNone(filename)

    def test_create_with_template_and_content(self):
        """Template content and additional content are both included."""
        filename = notes.create_note(
            "Team Sync", content="Extra notes here", template_name="meeting"
        )
        self.assertIsNotNone(filename)

        filepath = os.path.join(self.tmp_dir, filename)
        with open(filepath, "r") as f:
            content = f.read()

        self.assertIn("## Attendees", content)
        self.assertIn("Extra notes here", content)

    def test_create_without_template(self):
        """Creating a note without a template still works as before."""
        filename = notes.create_note("Plain Note", content="Just text")
        self.assertIsNotNone(filename)

        filepath = os.path.join(self.tmp_dir, filename)
        with open(filepath, "r") as f:
            content = f.read()

        self.assertIn("# Plain Note", content)
        self.assertIn("Just text", content)
        self.assertNotIn("## Attendees", content)


class TestCLITemplateIntegration(unittest.TestCase):
    """Integration tests for CLI template commands."""

    def setUp(self):
        """Set up a temporary directory for notes."""
        self.tmp_dir = tempfile.mkdtemp()
        self.env = os.environ.copy()

    def tearDown(self):
        """Clean up temporary directory."""
        shutil.rmtree(self.tmp_dir)

    def run_cli(self, args):
        """Run the CLI with given arguments."""
        result = subprocess.run(
            [sys.executable, os.path.join(os.path.dirname(__file__), "notes.py")] + args,
            capture_output=True,
            text=True,
            cwd=self.tmp_dir,
            env=self.env,
        )
        return result

    def test_templates_command(self):
        """The templates command lists available templates."""
        result = self.run_cli(["templates"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("meeting", result.stdout)
        self.assertIn("todo", result.stdout)
        self.assertIn("journal", result.stdout)

    def test_create_with_template_flag(self):
        """The --template flag creates a note with template structure."""
        result = self.run_cli(["create", "--template", "meeting", "Standup 2025-01-15"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Created:", result.stdout)

        # Verify the file was created in the temp dir
        notes_dir = os.path.join(self.tmp_dir, "my_notes")
        files = os.listdir(notes_dir)
        self.assertEqual(len(files), 1)

        with open(os.path.join(notes_dir, files[0]), "r") as f:
            content = f.read()
        self.assertIn("## Attendees", content)
        self.assertIn("## Agenda", content)

    def test_create_with_invalid_template_flag(self):
        """Using an invalid template name prints an error."""
        result = self.run_cli(["create", "--template", "invalid", "Test Note"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Unknown template", result.stdout)

    def test_create_template_missing_title(self):
        """Using --template without enough args prints usage."""
        result = self.run_cli(["create", "--template", "meeting"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("Usage:", result.stdout)

    def test_help_mentions_templates(self):
        """The help output mentions templates."""
        result = self.run_cli(["help"])
        self.assertEqual(result.returncode, 0)
        self.assertIn("--template", result.stdout)
        self.assertIn("templates", result.stdout)


if __name__ == "__main__":
    unittest.main()
