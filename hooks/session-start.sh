#!/bin/sh
# Only in a job-search folder: a pack next to the session (./me) or JOB_SEARCH_ME.
# The output goes into the session's context, so the kit's rules are read first.
if { [ -n "$JOB_SEARCH_ME" ] && [ -d "$JOB_SEARCH_ME" ]; } || [ -f ./me/profile.yaml ]; then
  echo "job-search-kit: a candidate pack is here. Before anything else, load the job-search-kit skill (the kit's rules: Claude prepares, the candidate sends) and say in one line which pack is connected."
fi
exit 0
