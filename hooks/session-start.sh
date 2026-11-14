#!/bin/sh
# Only in a job-search folder: a pack next to the session (./me) or JOB_SEARCH_ME.
# The output goes into the session's context, so the kit's rules are read first.
# It prints fixed text and two paths only: nothing from the pack's files reaches the session through it.
pack=""
if [ -n "$JOB_SEARCH_ME" ]; then
  if [ ! -d "$JOB_SEARCH_ME" ]; then   # one pack lookup: a wrong value is said, never replaced by ./me
    echo "job-search-kit: JOB_SEARCH_ME is set but is not a folder; fix it or unset it before using a pack."
    exit 0
  fi
  pack="$JOB_SEARCH_ME"
elif [ -f ./me/profile.yaml ]; then
  pack="./me"
fi
[ -z "$pack" ] && exit 0
here=$(cd "$pack" 2>/dev/null && pwd -P)
echo "job-search-kit: a candidate pack is here. Before anything else, load the job-search-kit skill (the kit's rules: Claude prepares, the candidate sends) and say in one line which pack is connected."
[ -n "$here" ] && echo "job-search-kit: the pack's folder is $here"
# The kit's own folder changes with every plugin version: scheduled runs and commands use this one
[ -n "$CLAUDE_PLUGIN_ROOT" ] && echo "job-search-kit: the kit (plugin) is at $CLAUDE_PLUGIN_ROOT; a cron line or a schedule that names another version's folder must be re-pointed here"
# paths.pack in the profile names the candidate's own pack by its absolute path; a me/ that came
# with a cloned project has another path, a relative one, a placeholder, or none
# read as YAML would: `pack:` at the first level inside the top-level `paths:` block, nowhere else;
# written more than once (where a reader would take the last), it counts as not recorded
recorded=$(awk -v q="'" '
  NR == 1 { sub(/^\357\273\277/, "") }   # a profile saved with a BOM
  /^[^[:space:]#]/ { inpaths = ($0 ~ /^paths:[[:space:]]*(#.*)?$/); child = -1; next }
  inpaths && /^[[:space:]]+[^[:space:]#]/ {
    match($0, /^[[:space:]]+/); ind = RLENGTH
    if (child < 0) child = ind
    if (ind == child && $0 ~ /^[[:space:]]+pack:/) {
      v = $0; sub(/^[[:space:]]+pack:[[:space:]]*/, "", v); sub(/[[:space:]]+#.*$/, "", v)
      sub(/[[:space:]]+$/, "", v); gsub("^[\"" q "]|[\"" q "]$", "", v); n++; last = v
    }
  }
  END { if (n == 1) print last }' "$pack/profile.yaml" 2>/dev/null)
case "$recorded" in "~"*) recorded="$HOME${recorded#\~}" ;; esac   # the value is data: never evaluated
want=""
case "$recorded" in
  //*|*/./*|*/../*|*/.|*/..|*/proc/*|/dev/*|/sys/*) want="" ;;      # a disguised path, or not a folder anyone keeps a pack in
  /*) if [ "$recorded" = "$here" ] || [ "$recorded" = "$(cd "$pack" 2>/dev/null && pwd -L)" ]; then
        want="$here"                                                # the same path, written either way
      else
        want=$(cd / && cd -- "$recorded" 2>/dev/null && pwd -P)      # from /, so a «current folder» link means /
      fi ;;
esac
if [ -z "$want" ] || [ "$here" != "$want" ]; then
  echo "job-search-kit: this pack's profile does not record this folder as its own (paths.pack, an absolute path). It may have come with something else, such as a cloned project: ask the candidate before using it."
fi
exit 0
