#!/usr/bin/env python3
"""
Fibonacci Sequence Tracker
Generates Fibonacci sequence incrementally, one number per GitHub Actions trigger.
Maintains a log of the sequence and tracks penalties for failed runs.
"""

import json
import os
from pathlib import Path


class FibonacciTracker:
    def __init__(self, log_file="fibonacci_log.json"):
        self.log_file = Path(log_file)
        self.state = self._load_state()
    
    def _load_state(self):
        """Load the current state from the log file."""
        if self.log_file.exists():
            try:
                with open(self.log_file, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load state from {self.log_file}: {e}")
                print("Initializing with default state.")
        
        # Initialize with f(0)=0 and f(1)=1, starting from f(2)
        return {
            "sequence": [0, 1],
            "penalty": 0,
            "last_two": [0, 1],  # Track last two numbers for calculation
            "index": 2  # Next index to generate
        }
    
    def _save_state(self):
        """Save the current state to the log file."""
        with open(self.log_file, 'w') as f:
            json.dump(self.state, f, indent=2)
    
    def generate_next(self):
        """Generate the next Fibonacci number and add it to the sequence."""
        # Calculate next Fibonacci number
        next_fib = self.state["last_two"][0] + self.state["last_two"][1]
        
        # Add to sequence
        self.state["sequence"].append(next_fib)
        
        # Update last two numbers for next calculation
        self.state["last_two"] = [self.state["last_two"][1], next_fib]
        
        # Increment index
        self.state["index"] += 1
        
        # Save state
        self._save_state()
        
        return next_fib
    
    def add_penalty(self):
        """Add penalty when a run fails."""
        # Calculate what the next number would be
        next_fib = self.state["last_two"][0] + self.state["last_two"][1]
        
        # Add as negative to penalty
        self.state["penalty"] -= next_fib
        
        # Save state (but don't advance the sequence)
        self._save_state()
        
        return next_fib
    
    def get_status(self):
        """Get current status of the tracker."""
        last_num = None
        if self.state["sequence"]:
            last_num = self.state["sequence"][-1]
        
        return {
            "sequence": self.state["sequence"],
            "penalty": self.state["penalty"],
            "next_index": self.state["index"],
            "last_number": last_num
        }


def main():
    """Main function to run the Fibonacci tracker."""
    tracker = FibonacciTracker()
    
    # Check if this is a manual trigger to add penalty
    add_penalty = os.environ.get("ADD_PENALTY", "false").lower() == "true"
    
    if add_penalty:
        penalty_value = tracker.add_penalty()
        print(f"❌ Run failed. Added penalty: -{penalty_value}")
        print(f"Total penalty: {tracker.state['penalty']}")
        print(f"Sequence remains: {tracker.state['sequence']}")
    else:
        # Normal run - generate next number
        next_num = tracker.generate_next()
        print(f"✅ Generated next Fibonacci number: {next_num}")
        
        # Display current status
        status = tracker.get_status()
        print(f"\nCurrent sequence: {status['sequence']}")
        print(f"Total penalty: {status['penalty']}")
        print(f"Next index: f({status['next_index']})")
        print(f"\nFull state saved to: {tracker.log_file.absolute()}")


if __name__ == "__main__":
    main()
