#!/bin/bash
# Review remaining Gospel chapters with Opus 4.7
# Mark 4-16, Luke 1-24, John 1-21
# Scheduled to run at 4:00 MESZ when API load is low

cd /Users/dfoerd/Documents/projekte/bibel/bible-reader
source .env
export ANTHROPIC_API_KEY
export REVIEW_MODEL=claude-opus-4-7

LOG="review_gospels_$(date +%Y%m%d_%H%M).log"

echo "=== Starting Gospel review at $(date) ===" | tee "$LOG"

# Mark chapters 4-16
for ch in $(seq 4 16); do
  echo "=== Mark chapter $ch ===" | tee -a "$LOG"
  python3 review_annotations.py 41 $ch 2>&1 | tee -a "$LOG"
  echo "" | tee -a "$LOG"
done

# Luke chapters 1-24
for ch in $(seq 1 24); do
  echo "=== Luke chapter $ch ===" | tee -a "$LOG"
  python3 review_annotations.py 42 $ch 2>&1 | tee -a "$LOG"
  echo "" | tee -a "$LOG"
done

# John chapters 1-21
for ch in $(seq 1 21); do
  echo "=== John chapter $ch ===" | tee -a "$LOG"
  python3 review_annotations.py 43 $ch 2>&1 | tee -a "$LOG"
  echo "" | tee -a "$LOG"
done

echo "=== Finished at $(date) ===" | tee -a "$LOG"
