#!/bin/bash

# Script to extract all files from a git repository into a single AI.txt file
# Each file will be prefixed with its filename in comments

# Check if current directory is a git repository
if [ ! -d .git ]; then
  echo "Error: Current directory is not a git repository."
  echo "Please run this script from the root of a git repository."
  exit 1
fi

# Create or overwrite AI.txt
echo "# Git Repository Content Extraction" >AI.txt
echo "# Generated on $(date)" >>AI.txt
echo "# Repository: $(git config --get remote.origin.url)" >>AI.txt
echo "" >>AI.txt

# Function to add file content to AI.txt
add_file_content() {
  local file="$1"

  # Skip the AI.txt file itself
  if [ "$file" == "AI.txt" ]; then
    return
  fi

  # Skip binary files
  if file "$file" | grep -q "binary"; then
    echo "Skipping binary file: $file"
    return
  fi

  echo "Processing: $file"

  # Add file header with filename
  echo "############################################################" >>AI.txt
  echo "# File: $file" >>AI.txt
  echo "############################################################" >>AI.txt
  echo "" >>AI.txt

  # Add file content
  cat "$file" >>AI.txt

  # Add newlines for separation
  echo "" >>AI.txt
  echo "" >>AI.txt
}

# Get list of all files tracked by git
git ls-files | while read -r file; do
  # Check if file exists (not deleted)
  if [ -f "$file" ]; then
    add_file_content "$file"
  fi
done

echo "Content extraction complete. All files have been consolidated into AI.txt"
