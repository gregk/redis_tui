"""
Sample Redis data for demonstration purposes.

This module provides functions to load sample data into Redis,
showcasing different data types and naming patterns.
"""

from typing import Dict, Any
import json
from .redis_client import RedisClient

SAMPLE_DATA = {
    # Game of Thrones Data
    "got:houses:stark": {
        "type": "hash",
        "value": {
            "name": "House Stark",
            "words": "Winter is Coming",
            "seat": "Winterfell",
            "region": "The North"
        }
    },
    "got:houses:stark:members": {
        "type": "list",
        "value": [
            "Eddard Stark",
            "Catelyn Stark",
            "Robb Stark",
            "Sansa Stark",
            "Arya Stark",
            "Bran Stark",
            "Rickon Stark",
            "Jon Snow"
        ]
    },
    "got:characters:ned_stark": {
        "type": "hash",
        "value": {
            "name": "Eddard Stark",
            "title": "Lord of Winterfell",
            "status": "Deceased",
            "house": "Stark"
        }
    },
    "got:characters:arya_stark": {
        "type": "hash",
        "value": {
            "name": "Arya Stark",
            "title": "Princess of Winterfell",
            "status": "Alive",
            "house": "Stark",
            "aliases": json.dumps(["A Girl", "No One"])
        }
    },
    
    # Modern Music Library
    "music:artists:green_day": {
        "type": "hash",
        "value": {
            "name": "Green Day",
            "genre": "Punk Rock",
            "formed": "1987",
            "origin": "Berkeley, California",
            "members": json.dumps(["Billie Joe Armstrong", "Mike Dirnt", "Tré Cool"])
        }
    },
    "music:albums:green_day:american_idiot": {
        "type": "hash",
        "value": {
            "title": "American Idiot",
            "artist": "Green Day",
            "year": "2004",
            "genre": "Punk Rock",
            "tracks": json.dumps([
                "American Idiot",
                "Jesus of Suburbia",
                "Holiday",
                "Boulevard of Broken Dreams",
                "Wake Me Up When September Ends"
            ]),
            "awards": "Grammy Award for Best Rock Album"
        }
    },
    "music:tracks:green_day:boulevard": {
        "type": "hash",
        "value": {
            "title": "Boulevard of Broken Dreams",
            "album": "American Idiot",
            "length": "4:20",
            "writers": json.dumps(["Billie Joe Armstrong", "Green Day"]),
            "awards": "Grammy Award for Record of the Year"
        }
    },
    
    "music:artists:billie_eilish": {
        "type": "hash",
        "value": {
            "name": "Billie Eilish",
            "birth_name": "Billie Eilish Pirate Baird O'Connell",
            "genre": json.dumps(["Pop", "Alternative", "Electropop"]),
            "birth_year": "2001",
            "origin": "Los Angeles, California"
        }
    },
    "music:albums:billie_eilish:happier_than_ever": {
        "type": "hash",
        "value": {
            "title": "Happier Than Ever",
            "artist": "Billie Eilish",
            "year": "2021",
            "producer": "FINNEAS",
            "tracks": json.dumps([
                "Getting Older",
                "I Didn't Change My Number",
                "Billie Bossa Nova",
                "Happier Than Ever",
                "NDA"
            ])
        }
    },
    "music:tracks:billie_eilish:happier": {
        "type": "hash",
        "value": {
            "title": "Happier Than Ever",
            "album": "Happier Than Ever",
            "length": "4:58",
            "producer": "FINNEAS",
            "streams": "1.5 billion"
        }
    },
    
    "music:artists:split_chain": {
        "type": "hash",
        "value": {
            "name": "Split Chain",
            "genre": json.dumps(["Electronic", "Breakbeat", "Drum and Bass"]),
            "formed": "2019",
            "origin": "London, UK",
            "members": json.dumps(["Alex Turner", "Sarah Chen"])
        }
    },
    "music:albums:split_chain:digital_horizon": {
        "type": "hash",
        "value": {
            "title": "Digital Horizon",
            "artist": "Split Chain",
            "year": "2023",
            "genre": json.dumps(["Electronic", "Breakbeat"]),
            "tracks": json.dumps([
                "Neural Network",
                "Digital Dawn",
                "Quantum Break",
                "Circuit Dreams",
                "Binary Sunset"
            ]),
            "features": json.dumps(["AI-generated soundscapes", "Live hardware synthesis"])
        }
    },
    "music:tracks:split_chain:neural_network": {
        "type": "hash",
        "value": {
            "title": "Neural Network",
            "album": "Digital Horizon",
            "duration": "6:45",
            "bpm": "174",
            "key": "F minor",
            "synthesizers": json.dumps(["Moog Matriarch", "Elektron Digitone"]),
            "streaming_platforms": json.dumps(["Spotify", "SoundCloud", "Bandcamp"])
        }
    },
    
    # Code Components
    "code:key_tree": {
        "type": "code",
        "value": {
            "metadata": {
                "name": "KeyTree",
                "type": "class",
                "module": "redis_tui.components.key_tree",
                "description": "A tree widget for displaying Redis keys hierarchically",
                "methods": [
                    {
                        "name": "_build_tree",
                        "description": "Recursively builds the tree structure from Redis keys",
                        "parameters": "parent: TreeNode, key_groups: Dict[str, List[str]]",
                        "returns": "None"
                    },
                    {
                        "name": "update_keys",
                        "description": "Update the tree with Redis keys",
                        "parameters": "keys: List[str]",
                        "returns": "None"
                    }
                ]
            },
            "code": """class KeyTree(Tree):
    \"\"\"A tree widget for displaying Redis keys hierarchically.
    
    This widget organizes Redis keys into a collapsible tree structure,
    grouping them by their prefixes for easier navigation.
    \"\"\"
    
    def __init__(self):
        super().__init__("Redis Keys")
        self.root.expand()
        
    def update_keys(self, keys: list[str]) -> None:
        \"\"\"Update the tree with a new list of Redis keys.\"\"\"
        self.clear()
        key_groups = self._group_keys(keys)
        self._build_tree(self.root, key_groups)"""
        }
    },
    
    "code:data_display": {
        "type": "code",
        "value": {
            "metadata": {
                "name": "DataDisplay",
                "type": "class",
                "module": "redis_tui.components.data_display",
                "description": "A widget for displaying Redis data with syntax highlighting",
                "methods": [
                    {
                        "name": "update_content",
                        "description": "Update the display with new data",
                        "parameters": "key: str, data: Any",
                        "returns": "None"
                    },
                    {
                        "name": "toggle_view",
                        "description": "Toggle between raw and formatted views",
                        "parameters": "None",
                        "returns": "None"
                    }
                ]
            },
            "code": """class DataDisplay(TextLog):
    \"\"\"A widget for displaying Redis data with syntax highlighting.
    
    Supports different display formats based on the data type:
    - Code: Syntax highlighted with line numbers
    - JSON: Pretty printed with proper indentation
    - Other: Cleanly formatted text
    \"\"\"
    
    def __init__(self):
        super().__init__()
        self._current_key = None
        self._current_data = None
        
    def update_content(self, key: str, data: Any) -> None:
        \"\"\"Update the display with new data.\"\"\"
        self._current_key = key
        self._current_data = data
        self._refresh_display()"""
        }
    }
}

async def load_sample_data(client: RedisClient) -> None:
    """Load sample data into Redis.
    
    Args:
        client: Redis client instance
    """
    for key, data in SAMPLE_DATA.items():
        data_type = data["type"]
        value = data["value"]
        
        if data_type == "string":
            await client.client.set(key, value)
        elif data_type == "hash":
            # Convert all values to strings
            string_value = {k: str(v) for k, v in value.items()}
            await client.client.hset(key, mapping=string_value)
        elif data_type == "list":
            await client.client.rpush(key, *value)
        elif data_type == "set":
            await client.client.sadd(key, *value)
        elif data_type == "zset":
            for member, score in value:
                await client.client.zadd(key, {member: score})
                
        # Set TTL if specified
        if "ttl" in data:
            await client.client.expire(key, data["ttl"])
        elif data_type == "code":
            # Store code components as JSON strings
            await client.client.set(key, json.dumps(value)) 