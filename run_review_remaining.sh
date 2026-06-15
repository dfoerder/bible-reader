#!/bin/bash
cd /Users/dfoerd/Documents/projekte/bibel/bible-reader
source .env
export ANTHROPIC_API_KEY
export REVIEW_MODEL=claude-opus-4-7

LOG="review_remaining_$(date +%Y%m%d_%H%M).log"

echo "=== Starting remaining Gospel review at $(date) ===" | tee "$LOG"

# Mark chapters 12-16 (12 was computed but not saved)
for ch in $(seq 12 16); do
  echo "=== Mark chapter $ch ===" | tee -a "$LOG"
  /usr/bin/python3 review_annotations.py 41 $ch 2>&1 | tee -a "$LOG"
  echo "" | tee -a "$LOG"
done

# Luke chapters 1-24
for ch in $(seq 1 24); do
  echo "=== Luke chapter $ch ===" | tee -a "$LOG"
  /usr/bin/python3 review_annotations.py 42 $ch 2>&1 | tee -a "$LOG"
  echo "" | tee -a "$LOG"
done

# John chapters 1-21
for ch in $(seq 1 21); do
  echo "=== John chapter $ch ===" | tee -a "$LOG"
  /usr/bin/python3 review_annotations.py 43 $ch 2>&1 | tee -a "$LOG"
  echo "" | tee -a "$LOG"
done

echo "=== Finished at $(date) ===" | tee -a "$LOG"
