#!/bin/bash
set -e

tasks=()
mapfile -t lines < <(grep -E '^- \[[ x]\]' TASKS.md || true)
for line in "${lines[@]}"; do
  status="${line:3:1}"
  title="${line:6}"
  title="${title%% *}"
  # convert spaces to underscores for array parsing -- easier with delimiter
  # Actually use null delimiter
  title_clean="${line:6}"
  # category from previous ## line
  category=""
  # read previous lines to find last ##
  category=$(grep -E '^## ' TASKS.md | tail -n1 | sed 's/^## //')
  # We'll trim later; for now push "status|title|category"
  tasks+=("${status}|${title_clean}|${category}")
done

get_board() {
  hermes kanban list
}

# Get board output
board=$(get_board)

# Build title->list of lines
declare -A title_lines
while IFS= read -r line; do
  title_lines["$line"]=1
done < <(echo "$board" | grep -E '^[✓⊘▶]')

# For each task, find matching lines and parse ids
for t in "${tasks[@]}"; do
  status="${t%%|*}"
  t="${t#*|}"
  title="${t%%|*}"
  t="${t#*|}"
  category="$t"

  # Search board for lines containing exact title substring
  matches=()
  while IFS= read -r line; do
    matches+=("$line")
  done < <(echo "$board" | grep -F "$title" || true)

  needs_create=0

  if [ "$status" = " " ]; then
    # pending
    if [ "${#matches[@]}" -eq 0 ]; then
      needs_create=1
    fi
  else
    # done
    if [ "${#matches[@]}" -eq 0 ]; then
      needs_create=1
    fi
  fi

  if [ "$needs_create" -eq 1 ]; then
    echo "CREATE: $title (category: $category)"
    hermes kanban create "$title" --assignee default --body "Category: $category"
    # Refresh board to capture new card
    board=$(get_board)
    matches=($(echo "$board" | grep -F "$title"))
  fi

  # For done tasks, complete any non-done cards
  if [ "$status" = "x" ]; then
    for line in "${matches[@]}"; do
      line_status="${line:0:1}"
      if [ "$line_status" != "✓" ]; then
        card_id=$(echo "$line" | awk '{print $1}')
        echo "COMPLETE: $title -> $card_id"
        hermes kanban complete "$card_id"
      fi
    done
  fi
done

echo "SYNC DONE"
