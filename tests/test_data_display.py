"""
Tests for the data display component.
"""

import pytest
from textual.app import App, ComposeResult
from redis_tui.components.data_display import DataDisplay

class DisplayTestApp(App):
    """Test application for DataDisplay widget."""
    
    def compose(self) -> ComposeResult:
        yield DataDisplay()

@pytest.mark.asyncio
async def test_data_display_initialization():
    """Test data display initialization."""
    async with DisplayTestApp().run_test() as pilot:
        display = pilot.app.query_one(DataDisplay)
        assert display is not None
        assert display.show_raw is False
        assert display.current_key == ""

@pytest.mark.asyncio
async def test_string_display():
    """Test displaying string values."""
    async with DisplayTestApp().run_test() as pilot:
        display = pilot.app.query_one(DataDisplay)
        await display.update_content(
            "test:key",
            "Hello, World!",
            "string"
        )
        assert "Hello, World!" in display.render()

@pytest.mark.asyncio
async def test_hash_display():
    """Test displaying hash values."""
    async with DisplayTestApp().run_test() as pilot:
        display = pilot.app.query_one(DataDisplay)
        test_hash = {
            "name": "John Doe",
            "email": "john@example.com"
        }
        await display.update_content(
            "user:1000",
            test_hash,
            "hash"
        )
        rendered = display.render()
        assert "name: John Doe" in rendered
        assert "email: john@example.com" in rendered

@pytest.mark.asyncio
async def test_list_display():
    """Test displaying list values."""
    async with DisplayTestApp().run_test() as pilot:
        display = pilot.app.query_one(DataDisplay)
        test_list = ["item1", "item2", "item3"]
        await display.update_content(
            "test:list",
            test_list,
            "list"
        )
        rendered = display.render()
        for item in test_list:
            assert item in rendered

@pytest.mark.asyncio
async def test_set_display():
    """Test displaying set values."""
    async with DisplayTestApp().run_test() as pilot:
        display = pilot.app.query_one(DataDisplay)
        test_set = {"value1", "value2", "value3"}
        await display.update_content(
            "test:set",
            test_set,
            "set"
        )
        rendered = display.render()
        for value in test_set:
            assert value in rendered

@pytest.mark.asyncio
async def test_zset_display():
    """Test displaying sorted set values."""
    async with DisplayTestApp().run_test() as pilot:
        display = pilot.app.query_one(DataDisplay)
        test_zset = [("member1", 1.0), ("member2", 2.0)]
        await display.update_content(
            "test:zset",
            test_zset,
            "zset"
        )
        rendered = display.render()
        for member, score in test_zset:
            assert f"{member}: {score}" in rendered

@pytest.mark.asyncio
async def test_toggle_view():
    """Test toggling between raw and formatted views."""
    async with DisplayTestApp().run_test() as pilot:
        display = pilot.app.query_one(DataDisplay)
        
        # Set initial content
        test_hash = {"name": "John Doe"}
        await display.update_content("test:key", test_hash, "hash")
        
        # Check formatted view
        assert not display.show_raw
        assert "name: John Doe" in display.render()
        
        # Toggle to raw view
        display.toggle_view()
        assert display.show_raw
        assert str(test_hash) in display.render()
        
        # Toggle back to formatted view
        display.toggle_view()
        assert not display.show_raw
        assert "name: John Doe" in display.render() 