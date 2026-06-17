import json
from pathlib import Path

from item import Item


class ItemStorage:
    """Handles loading and saving items from a local JSON file."""

    def __init__(self, file_path="items.json"):
        self.file_path = Path(file_path)

    def load_items(self):
        """Load saved items from disk when the program starts."""
        if not self.file_path.exists():
            return []

        try:
            with self.file_path.open("r", encoding="utf-8") as file:
                records = json.load(file)
        except json.JSONDecodeError:
            print(f"Warning: {self.file_path} is not valid JSON. Starting empty.")
            return []

        if not isinstance(records, list):
            print(f"Warning: {self.file_path} should contain a list. Starting empty.")
            return []

        items = []
        for record in records:
            try:
                items.append(Item.from_dict(record))
            except (KeyError, TypeError, ValueError):
                print("Warning: Skipped an invalid item record in the JSON file.")

        return items

    def save_items(self, items):
        """Save all current items to disk."""
        records = [item.to_dict() for item in items]

        with self.file_path.open("w", encoding="utf-8") as file:
            json.dump(records, file, indent=4)
