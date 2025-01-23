"""
Redis TUI main application.

This module provides a terminal user interface for browsing and
managing Redis data using Textual.
"""

from typing import Optional
import argparse
import asyncio
from textual.app import App, ComposeResult
from textual.containers import Horizontal, Container
from textual.widgets import Header, Footer, Tree
from textual.binding import Binding
import logging
from pathlib import Path

# Update these imports to be relative to src
from .components.data_display import DataDisplay
from .data.redis_client import RedisClient
from .data.sample_data import load_sample_data

# Set up logging
log_dir = Path.home() / ".redis_tui"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "redis_tui.log"

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file),
        # Removed StreamHandler to stop logging to stdout
    ]
)

logger = logging.getLogger(__name__)

class RedisTUI(App):
    """Redis Terminal User Interface application."""
    
    CSS = """
    Screen {
        layout: horizontal;
        background: $surface;
    }

    #left-pane {
        width: 30%;
        height: 100%;
        border-right: solid $primary;
    }

    #right-pane {
        width: 70%;
        height: 100%;
        background: $surface-darken-1;
        overflow: auto;
        padding: 1;
    }

    Tree {
        height: 100%;
        padding: 1;
        scrollbar-gutter: stable;
        overflow-y: auto;
    }

    DataDisplay {
        width: 100%;
        height: 100%;
        border: solid $primary;
        background: $boost;
    }
    """
    
    BINDINGS = [
        Binding("q", "quit", "Quit"),
        Binding("d", "toggle_dark", "Toggle dark mode"),
        Binding("r", "refresh", "Refresh"),
        Binding("f", "toggle_focus", "Toggle Focus"),
    ]
    
    def __init__(self, redis_client: RedisClient = None):
        """Initialize the application.
        
        Args:
            redis_client: Redis client
        """
        super().__init__()
        self.redis_client = redis_client or RedisClient()
        
    def compose(self) -> ComposeResult:
        """Create child widgets for the app."""
        yield Header()
        with Container():
            with Container(id="left-pane"):
                yield Tree("Redis Keys", id="redis-tree")
            with Container(id="right-pane"):
                yield DataDisplay()
        yield Footer()
        
    async def on_mount(self) -> None:
        """Handle app mount event."""
        await self.refresh_tree()
        
    async def refresh_tree(self) -> None:
        """Refresh the Redis key tree."""
        tree = self.query_one("#redis-tree", Tree)
        tree.clear()
        
        keys = await self.redis_client.get_all_keys()
        for namespace, namespace_keys in keys.items():
            namespace_node = tree.root.add(namespace, expand=True)
            # Group by subnamespace
            subgroups = {}
            for key in sorted(namespace_keys):
                parts = key.split(':')[1:]  # Skip the namespace
                if len(parts) > 1:
                    subgroup = parts[0]
                    if subgroup not in subgroups:
                        subgroups[subgroup] = namespace_node.add(subgroup, expand=True)
                    leaf = subgroups[subgroup].add(parts[-1])
                    leaf.allow_expand = False  # Mark as leaf node
                else:
                    leaf = namespace_node.add(parts[0])
                    leaf.allow_expand = False  # Mark as leaf node
        
    async def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Handle selection of tree nodes."""
        node = event.node
        logger.debug(f"Selected node: {node.label}, expandable: {node.allow_expand}")
        
        # Skip if it's a parent node without a value
        if not node.allow_expand:  # This is a leaf node
            # Build the full key by walking up the tree
            key_parts = []
            current = node
            while current.parent and current.parent.label != "Redis Keys":
                key_parts.insert(0, str(current.label))
                current = current.parent
            
            if key_parts:
                full_key = ":".join(key_parts)
                logger.debug(f"Constructed full key: {full_key}")
                data = await self.redis_client.get_key(full_key)
                logger.debug(f"Retrieved data: {data}")
                if data:
                    display = self.query_one(DataDisplay)
                    display.update_content(full_key, data)
                    logger.debug("Updated display")
                else:
                    # Try with the original key from Redis
                    keys = await self.redis_client.get_all_keys()
                    for namespace, keys_list in keys.items():
                        if any(k.endswith(full_key) for k in keys_list):
                            for k in keys_list:
                                if k.endswith(full_key):
                                    data = await self.redis_client.get_key(k)
                                    if data:
                                        display = self.query_one(DataDisplay)
                                        display.update_content(k, data)
                                        logger.debug(f"Updated display with full key: {k}")
                                        break
                    if not data:
                        logger.warning(f"No data found for key: {full_key}")
        
    def action_toggle_focus(self) -> None:
        """Toggle focus between tree and data display."""
        tree = self.query_one("#redis-tree", Tree)
        display = self.query_one(DataDisplay)
        if tree.has_focus:
            display.focus()
        else:
            tree.focus()
        
    async def action_refresh(self) -> None:
        """Refresh Redis keys."""
        await self.refresh_tree()
        
    def action_toggle_dark(self) -> None:
        """Toggle dark mode."""
        # Implementation of toggle_dark action
        pass
        
    async def on_unmount(self) -> None:
        """Handle app unmount event."""
        await self.redis_client.close()

async def run_app(args):
    """Run the application with the given arguments."""
    client = RedisClient(
        host=args.host,
        port=args.port,
        db=args.db,
        password=args.password
    )
    
    if args.samples:
        await load_sample_data(client)
    
    app = RedisTUI(redis_client=client)
    await app.run_async()

def main():
    """Entry point for the application."""
    parser = argparse.ArgumentParser(description="Redis Terminal User Interface")
    parser.add_argument("--host", default="localhost", help="Redis host")
    parser.add_argument("--port", type=int, default=6379, help="Redis port")
    parser.add_argument("--db", type=int, default=0, help="Redis database number")
    parser.add_argument("--password", help="Redis password")
    parser.add_argument("--samples", action="store_true", help="Load sample data")
    
    args = parser.parse_args()
    
    asyncio.run(run_app(args))

if __name__ == "__main__":
    main() 