#!/bin/bash
failed=0
for skill_dir in /Users/withvanko./.config/opencode/skills/*/; do
    skill_name=$(basename "$skill_dir")
    skill_file="${skill_dir}SKILL.md"
    
    if [ ! -f "$skill_file" ]; then
        echo "Missing SKILL.md in $skill_name"
        failed=1
        continue
    fi
    
    # Extract frontmatter
    frontmatter=$(awk '/^---/{if (in_fm) {exit} else {in_fm=1; next}} in_fm{print}' "$skill_file")
    
    name=$(echo "$frontmatter" | grep -i "^name:" | sed 's/^name: *//' | tr -d '\r')
    desc=$(echo "$frontmatter" | grep -i "^description:" | sed 's/^description: *//' | tr -d '\r')
    
    errors=""
    
    if [ -z "$name" ]; then
        errors="$errors\n  - Missing name field"
    else
        if [ "$name" != "$skill_name" ]; then
            errors="$errors\n  - Name '$name' does not match directory '$skill_name'"
        fi
        if ! echo "$name" | grep -qE '^[a-z0-9]+(-[a-z0-9]+)*$'; then
            errors="$errors\n  - Name '$name' is invalid (only lowercase alphanumeric and hyphens allowed, no consecutive or leading/trailing hyphens)"
        fi
        if [ ${#name} -gt 64 ]; then
            errors="$errors\n  - Name is too long (> 64 chars)"
        fi
    fi
    
    if [ -z "$desc" ]; then
        errors="$errors\n  - Missing description field"
    else
        # Approximate length check for description
        desc_len=${#desc}
        if [ $desc_len -gt 1024 ]; then
            errors="$errors\n  - Description may be too long"
        fi
    fi
    
    if [ -n "$errors" ]; then
        echo -e "Failed $skill_name:$errors"
        failed=1
    else
        echo "Valid: $skill_name"
    fi
done

if [ $failed -eq 0 ]; then
    echo "ALL VALID!"
fi
