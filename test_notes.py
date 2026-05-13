#!/usr/bin/env python3
"""Unit tests for Markdown Note Keeper."""

import os
import shutil
import tempfile
import unittest

import notes


class TestNotes(unittest.TestCase):
    """Test cases for the notes module."""

    def setUp(self):
        """Create a temporary directory for notes and patch NOTES_DIR."""
        self.test_dir = tempfile.mkdtemp()
        self._original_notes_dir = notes.NOTES_DIR
        notes.NOTES_DIR = self.test_dir

    def tearDown(self):
        """Remove the temporary directory and restore NOTES_DIR."""
        shutil.rmtree(self.test_dir, ignore_errors=True)
        notes.NOTES_DIR = self._original_notes_dir

    def test_create_note_returns_filename(self):
        """Test that create_note returns a valid filename."""
        result = notes.create_note("Test Note", "Some content")
        self.assertIsNotNone(result)
        self.assertTrue(result.endswith(".md"))

    def test_create_note_creates_file(self):
        """Test that create_note creates a file on disk."""
        filename = notes.create_note("My Note", "Hello world")
        filepath = os.path.join(self.test_dir, filename)
        self.assertTrue(os.path.exists(filepath))

    def test_create_note_content(self):
        """Test that created note contains the title and content."""
        filename = notes.create_note("My Title", "Body text")
        filepath = os.path.join(self.test_dir, filename)
        with open(filepath, "r") as f:
            content = f.read()
        self.assertIn("# My Title", content)
        self.assertIn("Body text", content)

    def test_create_note_empty_title_returns_none(self):
        """Test that create_note returns None for empty title."""
        result = notes.create_note("")
        self.assertIsNone(result)

    def test_create_note_whitespace_title_returns_none(self):
        """Test that create_note returns None for whitespace-only title."""
        result = notes.create_note("   ")
        self.assertIsNone(result)

    def test_list_notes_empty(self):
        """Test list_notes with no notes present."""
        # Should not raise an error
        notes.list_notes()

    def test_list_notes_with_notes(self):
        """Test list_notes when notes exist."""
        notes.create_note("First Note")
        notes.create_note("Second Note")
        # Should not raise an error
        notes.list_notes()

    def test_view_note_by_number(self):
        """Test viewing a note by its number."""
        notes.create_note("View Test", "View content")
        # Should not raise an error
        notes.view_note("1")

    def test_view_note_invalid_number(self):
        """Test viewing a note with an invalid number."""
        notes.create_note("Some Note")
        # Should not raise an error, just prints message
        notes.view_note("999")

    def test_delete_note_by_number(self):
        """Test deleting a note by its number."""
        filename = notes.create_note("Delete Me", "Temporary")
        filepath = os.path.join(self.test_dir, filename)
        self.assertTrue(os.path.exists(filepath))
        notes.delete_note("1")
        self.assertFalse(os.path.exists(filepath))

    def test_delete_note_invalid(self):
        """Test deleting a note with invalid identifier."""
        notes.create_note("Keep Me")
        # Should not raise, just prints error message
        notes.delete_note("999")

    def test_resolve_note_by_number(self):
        """Test resolving a note by its number."""
        filename = notes.create_note("Resolve Test")
        expected_path = os.path.join(self.test_dir, filename)
        result = notes.resolve_note("1")
        self.assertEqual(result, expected_path)

    def test_resolve_note_by_filename(self):
        """Test resolving a note by its filename."""
        filename = notes.create_note("File Resolve")
        expected_path = os.path.join(self.test_dir, filename)
        result = notes.resolve_note(filename)
        self.assertEqual(result, expected_path)

    def test_resolve_note_empty_list(self):
        """Test resolve_note when no notes exist."""
        result = notes.resolve_note("1")
        self.assertIsNone(result)

    def test_resolve_note_not_found(self):
        """Test resolve_note with a non-existent filename."""
        notes.create_note("Exists")
        result = notes.resolve_note("nonexistent.md")
        self.assertIsNone(result)

    def test_get_note_title(self):
        """Test extracting title from a note file."""
        filename = notes.create_note("Extract Title", "Body")
        filepath = os.path.join(self.test_dir, filename)
        title = notes.get_note_title(filepath)
        self.assertEqual(title, "Extract Title")

    def test_get_note_title_no_heading(self):
        """Test get_note_title when file has no markdown heading."""
        filepath = os.path.join(self.test_dir, "no_heading.md")
        with open(filepath, "w") as f:
            f.write("No heading here\n")
        title = notes.get_note_title(filepath)
        self.assertEqual(title, "Untitled")

    def test_get_note_title_missing_file(self):
        """Test get_note_title with a non-existent file."""
        title = notes.get_note_title("/nonexistent/path.md")
        self.assertEqual(title, "Untitled")

    def test_sanitize_filename_basic(self):
        """Test sanitize_filename with a normal string."""
        result = notes.sanitize_filename("Hello World")
        self.assertEqual(result, "Hello_World")

    def test_sanitize_filename_special_chars(self):
        """Test sanitize_filename strips special characters."""
        result = notes.sanitize_filename("My@Note!#$%")
        self.assertEqual(result, "MyNote")

    def test_sanitize_filename_preserves_hyphens(self):
        """Test sanitize_filename keeps hyphens and underscores."""
        result = notes.sanitize_filename("my-note_v2")
        self.assertEqual(result, "my-note_v2")

    def test_sanitize_filename_empty_string(self):
        """Test sanitize_filename with an empty string."""
        result = notes.sanitize_filename("")
        self.assertEqual(result, "")


if __name__ == "__main__":
    unittest.main()
