#!/bin/sh
# Only in a job-search folder: a pack next to the session (./me) or JOB_SEARCH_ME.
# The output goes into the session's context, so the kit's rules are read first.
# It prints fixed text only: nothing from the pack's files reaches the session through it.
pack=""
if [ -n "$JOB_SEARCH_ME" ] && [ -d "$JOB_SEARCH_ME" ]; then
  pack="$JOB_SEARCH_ME"
elif [ -f ./me/profile.yaml ]; then
  pack="./me"
fi
[ -z "$pack" ] && exit 0
echo "job-search-kit: a candidate pack is here. Before anything else, load the job-search-kit skill (the kit's rules: Claude prepares, the candidate sends) and say in one line which pack is connected."
# paths.pack in the profile names the candidate's own pack; a me/ that came with a cloned project does not match
recorded=$(sed -n 's/^[[:space:]]*pack:[[:space:]]*["'\'']\{0,1\}\([^"'\''#]*\).*/\1/p' "$pack/profile.yaml" 2>/dev/null | head -n 1 | sed 's/[[:space:]]*$//')
if [ -n "$recorded" ] && [ "${recorded#<}" = "$recorded" ]; then
  here=$(cd "$pack" 2>/dev/null && pwd -P)
  case "$recorded" in "~"*) recorded="$HOME${recorded#\~}" ;; esac   # the value is data: never evaluated
  want=$(cd -- "$recorded" 2>/dev/null && pwd -P)
  if [ -n "$here" ] && [ "$here" != "$want" ]; then
    echo "job-search-kit: this pack is not at the path its profile records (paths.pack). It may have come with something else, such as a cloned project: ask the candidate before using it."
  fi
fi
exit 0
