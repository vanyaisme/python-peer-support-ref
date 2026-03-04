import os
import re

def validate_skill(filepath):
    dir_name = os.path.basename(os.path.dirname(filepath))
    file_name = os.path.basename(filepath)
    
    if file_name != "SKILL.md":
        return f"Warning: {filepath} is not named SKILL.md"

    try:
        with open(filepath, 'r') as f:
            content = f.read()
    except Exception as e:
        return f"Error reading {filepath}: {e}"

    if not content.startswith('---'):
        return f"Error: No frontmatter in {filepath}"

    parts = content.split('---', 2)
    if len(parts) < 3:
        return f"Error: Malformed frontmatter in {filepath}"

    frontmatter_str = parts[1]
    
    name_match = re.search(r'^name:\s*(.*?)\s*$', frontmatter_str, re.MULTILINE)
    desc_match = re.search(r'^description:\s*(.*?)\s*$', frontmatter_str, re.MULTILINE | re.DOTALL)
    
    errors = []
    
    if not name_match:
        errors.append("Missing 'name'")
    else:
        name = name_match.group(1).strip()
        if name != dir_name:
            errors.append(f"'name' ({name}) does not match directory name ({dir_name})")
        if len(name) > 64:
            errors.append(f"'name' is too long ({len(name)} > 64)")
        if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
            errors.append(f"'name' ({name}) has invalid characters or format")

    if not desc_match:
        errors.append("Missing 'description'")
    else:
        desc = desc_match.group(1).strip()
        # strip out other keys that might be matched if DOTALL is used blindly
        # Actually DOTALL is bad if there are other keys. 
        # Better parse line by line
        pass

    # safer line-by-line parse
    name = None
    desc = None
    in_desc = False
    desc_lines = []
    
    for line in frontmatter_str.split('\n'):
        if line.startswith('name:'):
            name = line.split('name:', 1)[1].strip()
        elif line.startswith('description:'):
            in_desc = True
            desc_lines.append(line.split('description:', 1)[1].strip())
        elif re.match(r'^[a-z\-]+:', line):
            if in_desc:
                in_desc = False
        elif in_desc:
            desc_lines.append(line.strip())
            
    if not name:
        pass # already caught
    else:
        if name != dir_name:
            errors.append(f"'name' ({name}) does not match directory name ({dir_name})")
        if len(name) > 64:
            errors.append(f"'name' is too long ({len(name)} > 64)")
        if not re.match(r'^[a-z0-9]+(-[a-z0-9]+)*$', name):
            errors.append(f"'name' ({name}) has invalid characters or format")

    if not desc_lines:
        pass # already caught
    else:
        desc = " ".join(desc_lines)
        if len(desc) > 1024:
            errors.append(f"'description' is too long ({len(desc)} > 1024)")

    if errors:
        return f"Failed {filepath}:\n  - " + "\n  - ".join(errors)
    return None

skill_dir = "/Users/withvanko./.config/opencode/skills"
failed = False
for root, dirs, files in os.walk(skill_dir):
    for f in files:
        if f.endswith(".md"):
            filepath = os.path.join(root, f)
            res = validate_skill(filepath)
            if res:
                print(res)
                failed = True

if not failed:
    print("All SKILL.md files are valid!")
