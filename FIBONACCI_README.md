# Fibonacci Sequence Tracker

This project implements an automated Fibonacci sequence generator that runs via GitHub Actions.

## How It Works

1. **Scheduled Execution**: The workflow runs automatically Monday through Friday at 9 AM, 12 PM, and 4 PM UTC.
2. **Incremental Generation**: Each run generates the next number in the Fibonacci sequence.
3. **State Persistence**: The sequence and penalty state are stored in `fibonacci_log.json`.
4. **Penalty Tracking**: If a run fails, the penalty variable accumulates the negative value of what would have been the next number.

## Sequence Details

- Starting point: f(0) = 0, f(1) = 1
- First generated number: f(2) = 1
- Sequence: 0, 1, 1, 2, 3, 5, 8, 13, 21, 34, ...

## Example Behavior

Given the sequence: `[0, 1, 1, 2, 3, 5, 8]`, penalty = 0

**If the 8th trigger succeeds:**
- Sequence becomes: `[0, 1, 1, 2, 3, 5, 8, 13]`
- Penalty remains: 0

**If the 8th trigger fails:**
- Sequence remains: `[0, 1, 1, 2, 3, 5, 8]`
- Penalty becomes: -13

**If the 9th trigger also fails:**
- Sequence remains: `[0, 1, 1, 2, 3, 5, 8]`
- Penalty becomes: -26

**If the 10th trigger succeeds:**
- Sequence becomes: `[0, 1, 1, 2, 3, 5, 8, 13]`
- Penalty remains: -26

## Manual Testing

You can manually trigger the workflow from the Actions tab:
- Regular run: Leave "Add penalty for failed run" as `false`
- Simulate failure: Set "Add penalty for failed run" to `true`

## Files

- `fibonacci_tracker.py`: Python script that generates the sequence
- `.github/workflows/fibonacci.yml`: GitHub Actions workflow configuration
- `fibonacci_log.json`: State file (created on first run)
