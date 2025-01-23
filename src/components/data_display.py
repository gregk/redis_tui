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
from textual.widgets import Static, RichLog
from textual.reactive import reactive
from textual.message import Message
from textual.containers import Container, Vertical, ScrollableContainer
from rich.console import Group, RenderableType, Console
from textual.widget import Widget
import logging

logger = logging.getLogger(__name__)

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
    """Display Redis data."""
    
    DEFAULT_CSS = """
    DataDisplay {
        background: $surface;
        color: $text;
        height: 100%;
        border: solid $primary;
        padding: 1;
        overflow-y: auto;
        width: 100%;
    }
    """
    
    def __init__(self):
        """Initialize the display."""
        super().__init__("")
        self.console = Console()
    
    def on_mount(self) -> None:
        """Handle mount event."""
        self.update(Panel("Welcome to Redis TUI\nSelect a key to view its data"))
    
    def update_content(self, key: str, data: str) -> None:
        """Update display content."""
        try:
            # Create a list to hold renderable objects
            rendered = []
            
            # Add key header
            rendered.append(Panel(f"Key: {key}", title="Redis Key"))
            
            # Try to parse and format as JSON
            try:
                parsed = json.loads(data) if isinstance(data, str) else data
                json_str = json.dumps(parsed, indent=2)
                syntax = Syntax(json_str, "json", theme="monokai", word_wrap=True)
                rendered.append(Panel(syntax, title="Data"))
            except:
                # Fallback to raw display
                rendered.append(Panel(str(data), title="Raw Data"))
            
            # Join all renderables with newlines
            output = "\n".join(str(r) for r in rendered)
            
            # Update the widget
            self.update(output)
            logger.debug("Display updated successfully")
            
        except Exception as e:
            logger.error(f"Error updating display: {e}", exc_info=True)
            self.update(Panel(f"Error displaying data: {e}"))

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