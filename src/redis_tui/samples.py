"""
Sample data for demonstrating the Redis TUI viewer.

This module provides sample datasets of varying complexity to showcase
the Redis TUI's capabilities for different use cases.
"""

import json
from typing import Dict

def load_sample_data() -> Dict[str, str]:
    """Load sample data sets of varying complexity.
    
    Returns:
        Dictionary mapping Redis keys to their string values
    """
    samples = {}
    
    # Simple Example: Game of Thrones Houses and Characters
    got_data = {
        "got:house:stark": json.dumps({
            "name": "House Stark",
            "words": "Winter is Coming",
            "seat": "Winterfell"
        }),
        "got:house:stark:members:ned": json.dumps({
            "name": "Eddard Stark",
            "title": "Lord of Winterfell",
            "status": "Deceased"
        }),
        "got:house:stark:members:arya": json.dumps({
            "name": "Arya Stark",
            "title": "Princess",
            "status": "Alive"
        }),
        "got:house:lannister": json.dumps({
            "name": "House Lannister", 
            "words": "Hear Me Roar!",
            "seat": "Casterly Rock"
        }),
        "got:house:lannister:members:tyrion": json.dumps({
            "name": "Tyrion Lannister",
            "title": "Hand of the Queen",
            "status": "Alive"
        })
    }
    samples.update(got_data)
    
    # Moderate Example: Music Library
    music_data = {
        "music:artist:radiohead:info": json.dumps({
            "name": "Radiohead",
            "formed": 1985,
            "genre": ["Alternative Rock", "Art Rock", "Electronic"],
            "origin": "Abingdon, England"
        }),
        "music:artist:radiohead:album:ok_computer": json.dumps({
            "title": "OK Computer",
            "year": 1997,
            "rating": 9.5,
            "tracks": [
                "Airbag",
                "Paranoid Android",
                "Exit Music (For a Film)"
            ],
            "credits": {
                "producer": "Nigel Godrich",
                "studio": "Abbey Road Studios",
                "label": "Parlophone"
            }
        }),
        "music:artist:radiohead:album:ok_computer:track:paranoid_android": json.dumps({
            "title": "Paranoid Android",
            "duration": "6:23",
            "composers": ["Thom Yorke", "Jonny Greenwood", "Ed O'Brien", "Colin Greenwood", "Phil Selway"],
            "lyrics_excerpt": "Please could you stop the noise, I'm trying to get some rest",
            "key_signatures": ["B minor", "C major"],
            "time_signatures": ["4/4", "7/8"]
        })
    }
    samples.update(music_data)
    
    # Complex Example: Redis TUI Source Code with Metadata
    code_data = {
        "code:redis_tui:components:key_tree:metadata": json.dumps({
            "name": "KeyTree",
            "type": "class",
            "file": "key_tree.py",
            "module": "redis_tui.components",
            "author": "Gregory K",
            "version": "0.1.0",
            "dependencies": {
                "textual": ">=1.0.0",
                "typing-extensions": ">=4.8.0"
            },
            "interfaces": ["Tree"],
            "messages": ["KeySelected"],
            "methods": [
                "update_keys",
                "build_from_data",
                "get_selected_key"
            ]
        }),
        "code:redis_tui:components:key_tree:docstring": json.dumps({
            "summary": "A tree-based browser for Redis keys",
            "description": "This module provides a Textual tree widget for browsing Redis keys with support for patterns and filtering",
            "example": '''
tree = KeyTree()
await tree.update_keys([
    "users:1234:profile",
    "users:1234:settings",
    "users:5678:profile"
])
'''
        }),
        "code:redis_tui:components:key_tree:methods:update_keys": json.dumps({
            "name": "update_keys",
            "type": "async method",
            "signature": "async def update_keys(self, keys: List[str], pattern: Optional[str] = None) -> None",
            "parameters": {
                "keys": {
                    "type": "List[str]",
                    "description": "List of Redis keys to display"
                },
                "pattern": {
                    "type": "Optional[str]",
                    "description": "Optional pattern to filter keys",
                    "default": "None"
                }
            },
            "returns": {
                "type": "None",
                "description": "Updates the tree structure in place"
            },
            "complexity": {
                "time": "O(n * log n) where n is number of keys",
                "space": "O(n) for storing grouped keys"
            }
        })
    }
    samples.update(code_data)
    
    return samples 