#!/bin/bash
cd /Users/dfoerd/Documents/projekte/bibel/bible-reader
source .env
export ANTHROPIC_API_KEY
export REVIEW_MODEL=claude-opus-4-7

LOG="review_gospels_$(date +%Y%m%d_%H%M).log"

echo "=== Starting Gospel review at $(date) ===" | tee "$LOG"

# Matthew chapters 2-28 (chapter 1 already done)
for ch in $(seq 2 28); do
  echo "=== Matthew chapter $ch ===" | tee -a "$LOG"
  python3 review_annotations.py 40 $ch 2>&1 | tee -a "$LOG"
  echo "" | tee -a "$LOG"
done

# Mark chapters 1-16
for ch in $(seq 1 16); do
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
