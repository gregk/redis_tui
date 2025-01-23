"""
Redis TUI main application.

This module provides a terminal user interface for browsing and
managing Redis data using Textual.
"""

from typing import Optional
import argparse
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Header, Footer
from textual.binding import Binding

from .components.data_display import DataDisplay
from .components.key_tree import KeyTree
from .data.redis_client import RedisClient
from .data.sample_data import load_sample_data

class RedisTUI(App):
    """Redis Terminal User Interface application."""
    
    CSS = """
    Screen {
        layout: grid;
        grid-size: 2;
        grid-columns: 1fr 2fr;
    }
    
    KeyTree {
        width: 100%;
        height: 100%;
        border: solid green;
    }
    
    DataDisplay {
        width: 100%;
        height: 100%;
        border: solid blue;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("r", "refresh", "Refresh"),
        Binding("f", "toggle_focus", "Toggle Focus"),
        Binding("d", "toggle_raw", "Toggle Raw"),
    ]
    
    def __init__(
        self,
        host: str = "localhost",
        port: int = 6379,
        db: int = 0,
        password: Optional[str] = None,
        load_samples: bool = False
    ) -> None:
        """Initialize the application.
        
        Args:
            host: Redis host
            port: Redis port
            db: Redis database number
            password: Optional Redis password
            load_samples: Whether to load sample data
        """
        super().__init__()
        self.redis = RedisClient(host, port, db, password)
        self.load_samples = load_samples
        
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        yield KeyTree()
        yield DataDisplay()
        yield Footer()
        
    async def on_mount(self) -> None:
        """Handle app mount event."""
        if self.load_samples:
            await load_sample_data(self.redis)
        await self.refresh_keys()
        
    def action_refresh(self) -> None:
        """Refresh Redis keys."""
        self.refresh_keys()
        
    def action_toggle_focus(self) -> None:
        """Toggle focus between tree and display."""
        if self.focused is self.query_one(KeyTree):
            self.query_one(DataDisplay).focus()
        else:
            self.query_one(KeyTree).focus()
            
    def action_toggle_raw(self) -> None:
        """Toggle raw data view."""
        display = self.query_one(DataDisplay)
        display.toggle_view()
        
    async def refresh_keys(self) -> None:
        """Refresh Redis keys in the tree."""
        tree = self.query_one(KeyTree)
        keys = await self.redis.get_keys()
        await tree.update_keys(keys)
        
    async def on_key_tree_key_selected(self, message: KeyTree.KeySelected) -> None:
        """Handle key selection in tree.
        
        Args:
            message: Key selection message
        """
        key = message.key
        value = await self.redis.get_value(key)
        key_type = await self.redis.get_type(key)
        display = self.query_one(DataDisplay)
        await display.update_content(key, value, key_type)
        
    async def on_unmount(self) -> None:
        """Handle app unmount event."""
        await self.redis.close()

def main():
    """Entry point for the application."""
    parser = argparse.ArgumentParser(description="Redis Terminal User Interface")
    parser.add_argument("--host", default="localhost", help="Redis host")
    parser.add_argument("--port", type=int, default=6379, help="Redis port")
    parser.add_argument("--db", type=int, default=0, help="Redis database number")
    parser.add_argument("--password", help="Redis password")
    parser.add_argument("--samples", action="store_true", help="Load sample data")
    
    args = parser.parse_args()
    
    app = RedisTUI(
        host=args.host,
        port=args.port,
        db=args.db,
        password=args.password,
        load_samples=args.samples
    )
    app.run() 