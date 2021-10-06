#!/bin/bash

# Exit if any of the intermediate steps fail
set -e

# Extract "filepath" from the input JSON into FILEPATH shell variable.
# jq will ensure that the values are properly quoted
# and escaped for consumption by the shell.
eval "$(jq -r '@sh "FILEPATH=\(.filepath)"')"

# Run mimetype on filepath to get the correct mime type.
MIME=$(mimetype --brief $FILEPATH)

# Safely produce a JSON object containing the result value.
# jq will ensure that the value is properly quoted
# and escaped to produce a valid JSON string.
jq -n --arg mime "$MIME" '{"mime":$mime}'