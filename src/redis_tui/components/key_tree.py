"""
A tree-based browser for Redis keys.

This module provides a Textual tree widget for browsing Redis keys
with support for patterns and filtering.
"""

from typing import Dict, List, Optional
from textual.widgets import Tree
from textual.widgets._tree import TreeNode
from textual.message import Message

class KeyTree(Tree):
    """A tree widget for displaying Redis keys hierarchically."""
    
    class KeySelected(Message):
        """Message sent when a key is selected."""
        def __init__(self, key: str) -> None:
            """Initialize message.
            
            Args:
                key: The selected Redis key
            """
            self.key = key
            super().__init__()
    
    def __init__(self) -> None:
        """Initialize the tree widget."""
        super().__init__("Redis Keys")
        self.root.expand()
        
    async def update_keys(self, keys: list[str]) -> None:
        """Update the tree with Redis keys.
        
        Args:
            keys: List of Redis keys to display
        """
        # Clear existing tree
        self.root.remove_children()
        
        # Group keys by prefix
        key_groups: Dict[str, Dict] = {}
        for key in keys:
            parts = key.split(":")
            current_dict = key_groups
            
            # Build nested dictionary structure
            for i, part in enumerate(parts):
                if i == len(parts) - 1:
                    # Last part - store full key
                    if isinstance(current_dict, dict):
                        current_dict[part] = key
                else:
                    # Not last part - create/get dict
                    if part not in current_dict:
                        current_dict[part] = {}
                    current_dict = current_dict[part]

        # Build tree from grouped keys
        await self._build_tree(self.root, key_groups)
        
    async def _build_tree(self, parent: TreeNode, key_groups: Dict[str, Dict]) -> None:
        """Build tree from grouped keys.
        
        Args:
            parent: Parent node to add children to
            key_groups: Dictionary of grouped keys
        """
        # Sort keys for consistent display
        for key in sorted(key_groups.keys()):
            value = key_groups[key]
            if isinstance(value, str):
                # Leaf node - add with full key as data
                parent.add_leaf(key, data={"key": value})
            else:
                # Branch node - add and recurse
                node = parent.add(key)
                await self._build_tree(node, value)

    async def on_tree_node_selected(self, event: Tree.NodeSelected) -> None:
        """Handle node selection.
        
        Args:
            event: The node selected event
        """
        if not event.node.children:
            # Only send message for leaf nodes
            key = event.node.data.get("key")
            if key:
                self.post_message(self.KeySelected(key))

    def build_from_data(self, data: dict) -> None:
        """Build the tree from Redis key data.

        Args:
            data: Dictionary containing Redis keys and values
        """
        self.clear()
        self._build_tree(self.root, data)

    def get_selected_key(self) -> Optional[str]:
        """Get the full Redis key of the currently selected node.

        Returns:
            The full Redis key if a node is selected, None otherwise
        """
        if self.cursor_node is None:
            return None
        return self.cursor_node.data.get("key") if self.cursor_node.data else None 