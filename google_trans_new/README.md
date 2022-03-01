
## Problem
Problem 1. `json.decoder.JSONDecodeError: Extra data: line 1 column 340 (char 339)`
Solution: Open `google_trans_new.py` in line 151. Modified `response = (decoded_line + ']')` to `response = decoded_line`.
