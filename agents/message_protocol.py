import json
import types
import inspect
from collections.abc import Generator, Iterator
from typing import Any


def is_generator_like(obj: Any) -> bool:
    """Check if an object is a generator or similar iterable that needs to be exhausted."""
    return (
        isinstance(obj, (Generator, Iterator, types.GeneratorType))
        or inspect.isgenerator(obj)
        or inspect.isgeneratorfunction(obj)
    )


def is_safe_for_iteration(obj: Any) -> bool:
    """Check if an object is safe to call list() on without causing errors."""
    try:
        iter(obj)
        # These types should not be converted to lists
        return not isinstance(obj, (str, bytes, dict))
    except TypeError:
        return False


def exhaust_generators(obj: Any) -> Any:
    """Convert all generators to lists recursively."""
    # Handle generators and other iterators
    if is_generator_like(obj):
        try:
            # Convert to list safely
            obj_list = list(obj)
            if len(obj_list) == 1:
                return exhaust_generators(obj_list[0])
            return [exhaust_generators(x) for x in obj_list]
        except (TypeError, StopIteration) as e:
            # If conversion fails, return as is
            print(f"Warning: Failed to convert {type(obj)} to list: {e}")
            return obj
    # Handle dictionaries
    elif isinstance(obj, dict):
        return {k: exhaust_generators(v) for k, v in obj.items()}
    # Handle lists and other iterables that should be preserved
    elif isinstance(obj, list):
        return [exhaust_generators(x) for x in obj]
    # Handle other non-str iterables that might be lazy or generators
    elif is_safe_for_iteration(obj) and not isinstance(obj, (str, bytes)):
        try:
            # Convert safely to list and process
            obj_list = list(obj)
            return [exhaust_generators(x) for x in obj_list]
        except (TypeError, StopIteration):
            # If conversion fails, return as is
            return obj
    # Leave all other types unchanged
    return obj


class AgentMessage:
    def __init__(self, sender, receiver, data):
        self.sender = sender
        self.receiver = receiver
        self.data = data

    def to_json(self):
        """
        Convert agent message to JSON, ensuring all generators are safely exhausted.
        Includes error handling for non-serializable objects.
        """
        try:
            # Ensure all generators in self.data are exhausted before serialization
            safe_data = exhaust_generators(self.data)
            return json.dumps(
                {"sender": self.sender, "receiver": self.receiver, "data": safe_data}
            )
        except TypeError as e:
            # If JSON serialization fails, try to convert to string
            print(f"Warning: JSON serialization failed: {e}")
            try:
                # Try to force convert data to string if serialization fails
                string_data = str(self.data)
                return json.dumps(
                    {
                        "sender": self.sender,
                        "receiver": self.receiver,
                        "data": string_data,
                    }
                )
            except Exception as e2:
                print(f"Error: Failed to convert to string: {e2}")
                # Last resort: return a safe error message
                return json.dumps(
                    {
                        "sender": self.sender,
                        "receiver": self.receiver,
                        "data": f"Error: Could not serialize data of type {type(self.data).__name__}",
                    }
                )

    @staticmethod
    def from_json(json_str):
        d = json.loads(json_str)
        return AgentMessage(d["sender"], d["receiver"], d["data"])
