"""
Tests for the key tree component.
"""

import pytest
from textual.app import App, ComposeResult
from redis_tui.components.key_tree import KeyTree

class TreeTestApp(App):
    """Test application for KeyTree widget."""
    
    def compose(self) -> ComposeResult:
        yield KeyTree()

@pytest.mark.asyncio
async def test_key_tree_initialization():
    """Test key tree initialization."""
    async with TreeTestApp().run_test() as pilot:
        tree = pilot.app.query_one(KeyTree)
        assert tree is not None
        assert tree.root.label == "Redis Keys"

@pytest.mark.asyncio
async def test_update_keys_no_pattern():
    """Test updating keys without pattern."""
    async with TreeTestApp().run_test() as pilot:
        tree = pilot.app.query_one(KeyTree)
        test_keys = [
            "user:1000",
            "user:1001",
            "product:1",
            "product:2"
        ]
        await tree.update_keys(test_keys)
        
        # Check root nodes
        assert "user" in [node.label for node in tree.root.children]
        assert "product" in [node.label for node in tree.root.children]

@pytest.mark.asyncio
async def test_update_keys_with_pattern():
    """Test updating keys with pattern filter."""
    async with TreeTestApp().run_test() as pilot:
        tree = pilot.app.query_one(KeyTree)
        test_keys = [
            "user:1000",
            "user:1001",
            "product:1",
            "product:2"
        ]
        await tree.update_keys(test_keys, pattern="user:*")
        
        # Check filtered nodes
        root_labels = [node.label for node in tree.root.children]
        assert "user" in root_labels
        assert "product" not in root_labels

@pytest.mark.asyncio
async def test_nested_key_grouping():
    """Test grouping of nested keys."""
    async with TreeTestApp().run_test() as pilot:
        tree = pilot.app.query_one(KeyTree)
        test_keys = [
            "category:electronics:laptops",
            "category:electronics:phones",
            "category:books:fiction",
            "category:books:nonfiction"
        ]
        await tree.update_keys(test_keys)
        
        # Check nested structure
        category_node = next(node for node in tree.root.children if node.label == "category")
        assert category_node is not None
        
        electronics_node = next(node for node in category_node.children if node.label == "electronics")
        assert electronics_node is not None
        assert "laptops" in [node.label for node in electronics_node.children]
        
        books_node = next(node for node in category_node.children if node.label == "books")
        assert books_node is not None
        assert "fiction" in [node.label for node in books_node.children]

@pytest.mark.asyncio
async def test_key_selection():
    """Test key selection events."""
    async with TreeTestApp().run_test() as pilot:
        tree = pilot.app.query_one(KeyTree)
        test_keys = ["user:1000"]
        await tree.update_keys(test_keys)
        
        # Get the leaf node
        user_node = tree.root.children[0]
        leaf_node = user_node.children[0]
        
        # Create a flag to track message receipt
        message_received = False
        
        def on_key_selected(message: KeyTree.KeySelected) -> None:
            nonlocal message_received
            message_received = True
            assert message.key == "user:1000"
        
        # Subscribe to key selected events
        tree.on_key_tree_key_selected = on_key_selected
        
        # Simulate selection
        tree.post_message(tree.NodeSelected(tree, leaf_node))
        assert message_received 