#!/bin/bash
cd /Users/dfoerd/Documents/projekte/bibel/bible-reader
source .env
export ANTHROPIC_API_KEY
export REVIEW_MODEL=claude-opus-4-7

LOG="review_gospels_$(date +%Y%m%d_%H%M).log"
echo "=== Starting at $(date) ===" | tee "$LOG"

# Mark 15 (KeyError last time)
echo "=== Mark chapter 15 ===" | tee -a "$LOG"
/usr/bin/python3 review_annotations.py 41 15 2>&1 | tee -a "$LOG"

# Luke 4-24 (1-3 already done)
for ch in $(seq 4 24); do
  echo "=== Luke chapter $ch ===" | tee -a "$LOG"
  /usr/bin/python3 review_annotations.py 42 $ch 2>&1 | tee -a "$LOG"
done

# John 1-21
for ch in $(seq 1 21); do
  echo "=== John chapter $ch ===" | tee -a "$LOG"
  /usr/bin/python3 review_annotations.py 43 $ch 2>&1 | tee -a "$LOG"
done

echo "=== Finished at $(date) ===" | tee -a "$LOG"
