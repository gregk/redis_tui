"""
A generic data display component for Redis data types.

This module provides a Textual widget for displaying different Redis data types
in a formatted and interactive way.
"""

from typing import Any, Dict, Optional
import json
from rich.syntax import Syntax
from rich.text import Text
from rich.panel import Panel
from textual.widgets import Static
from textual.reactive import reactive
from textual.message import Message
from textual.containers import Container, Vertical
from rich.console import Group, RenderableType
from textual.widget import Widget

class SplitDisplay(Container):
    """A container that displays content in a split view."""
    
    DEFAULT_CSS = """
    SplitDisplay {
        layout: vertical;
        height: 100%;
        width: 100%;
    }
    
    .top-panel {
        height: 30%;
        border-bottom: solid $primary;
        padding: 1;
    }
    
    .bottom-panel {
        height: 70%;
        padding: 1;
    }
    """
    
    def __init__(self) -> None:
        """Initialize the split display container."""
        super().__init__()
        self.top_panel = Static(classes="top-panel")
        self.bottom_panel = Static(classes="bottom-panel")
        
    def compose(self):
        """Compose the split display layout."""
        yield self.top_panel
        yield self.bottom_panel
        
    def update_content(self, top_content: RenderableType, bottom_content: RenderableType) -> None:
        """Update the content of both panels."""
        self.top_panel.update(top_content)
        self.bottom_panel.update(bottom_content)

class DataDisplay(Static):
    """A widget for displaying Redis data with different view modes."""
    
    DEFAULT_CSS = """
    DataDisplay {
        height: 100%;
        width: 100%;
    }
    """
    
    class ToggleView(Message):
        """Message sent when view mode is toggled."""

    # Reactive variables for state management
    show_raw: reactive[bool] = reactive(False)
    current_key: reactive[str] = reactive("")
    
    def __init__(self) -> None:
        """Initialize the data display widget."""
        super().__init__("")
        self._raw_content: Any = None
        self._formatted_content: RenderableType = ""
        self.split_display = SplitDisplay()
        
    def compose(self):
        """Compose the widget layout."""
        yield self.split_display
        
    async def update_content(self, key: str, value: Any, data_type: str) -> None:
        """Update the display with new Redis data.
        
        Args:
            key: The Redis key
            value: The value to display
            data_type: The Redis data type (string, hash, list, set, zset, code)
        """
        self.current_key = key
        self._raw_content = value
        
        try:
            # Parse the data if it's a string
            if isinstance(value, str):
                data = json.loads(value)
            else:
                data = value
                
            # Check if there's a code field
            code = None
            if isinstance(data, dict):
                code = data.pop("code", None)
            
            # Format the remaining data as JSON
            data_json = Syntax(
                json.dumps(data, indent=2),
                "json",
                theme="monokai",
                word_wrap=True
            )
            
            # If there's code, show it in the bottom panel
            if code:
                code_syntax = Syntax(
                    code.strip(),
                    "python",
                    theme="monokai",
                    line_numbers=True,
                    word_wrap=True
                )
                bottom_content = Panel(code_syntax, title="Source Code (Python)")
            else:
                bottom_content = Panel("", title="No Source Code")
                
            self.split_display.update_content(
                Panel(data_json, title=f"Data for {key}"),
                bottom_content
            )
            
        except Exception as e:
            # If we can't parse as JSON, format based on data type
            formatted = self._format_data(value, data_type)
            self.split_display.update_content(
                Panel(formatted, title=f"Data for {key}"),
                Panel("", title="No Source Code")
            )
            
    def _format_data(self, value: Any, data_type: str) -> str:
        """Format Redis data based on its type.
        
        Args:
            value: The value to format
            data_type: The Redis data type
            
        Returns:
            Formatted string representation of the data
        """
        if data_type == "string":
            try:
                # Try to parse as JSON for pretty printing
                data = json.loads(value)
                return Syntax(json.dumps(data, indent=2), "json", theme="monokai")
            except (json.JSONDecodeError, TypeError):
                return str(value)
        elif data_type == "hash":
            return "\n".join(f"{k}: {v}" for k, v in value.items())
        elif data_type in ("list", "set"):
            return "\n".join(str(item) for item in value)
        elif data_type == "zset":
            return "\n".join(f"{item}: {score}" for item, score in value)
        return str(value)
            
    def toggle_view(self) -> None:
        """Toggle between raw and formatted views."""
        self.show_raw = not self.show_raw
        self.post_message(self.ToggleView()) 