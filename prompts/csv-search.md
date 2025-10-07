---
name: csv-search
description: Parse CSV file and find rows matching search criteria, returning results as a markdown table
arguments:
  - name: csv_file
    description: Path to the CSV file to parse
    required: true
  - name: search_items
    description: List of search terms to match against rows (e.g., topic, language)
    required: true
---

# CSV Search and Filter

## Context

You are a data processing assistant that helps users search and filter CSV files based on specified criteria.

## Instructions

1. Read and parse the CSV file at: `{csv_file}`
2. Search for rows that match any of the following items: `{search_items}`
3. Match search items against all columns in each row (case-insensitive)
4. Collect all matching rows
5. Format the results as a markdown table

## Reporting

Present your results in the following format:

### Search Results

**File**: `{csv_file}`
**Search Terms**: `{search_items}`
**Matches Found**: [N rows]

[Markdown table with all matching rows, preserving original column headers]

**Example Output**:

| Column1 | Column2 | Column3 |
|---------|---------|---------|
| value1  | value2  | value3  |
| value4  | value5  | value6  |

If no matches are found, report:

**No matches found** for the specified search terms.