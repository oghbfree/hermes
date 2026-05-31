# Chat History Analysis — Profile Extraction Workflow

## When to Use

User provides raw chat export files (JSON from Claude, DeepSeek, Gemini, etc.) and asks you to extract their communication style, preferences, and project context to update memory/profile files.

## Export Formats

### DeepSeek
- **File**: `conversations.json` (array of conversation objects)
- **Structure**: Each conv has `title`, `mapping` (tree of message nodes), `inserted_at`
- **Message access**: `mapping[child_id].message.fragments[]` with `type: "REQUEST"` (user) / `"RESPONSE"` (assistant) / `"THINK"` (reasoning)
- **User messages**: Filter `fragments` where `type == "REQUEST"`, read `content` field
- **Subdirectories**: `d/` = DeepSeek export, contains `conversations.json` + `user.json`

### Claude (Anthropic)
- **File**: `conversations.json` (array of conversation objects)
- **Structure**: Each conv has `uuid`, `name`, `summary`, `created_at`, `chat_messages[]`
- **Message access**: `chat_messages[].text` (string) or `chat_messages[].content[].text` (array of content blocks)
- **User vs assistant**: Alternate even/odd index (0=user, 1=assistant) — but verify by content patterns
- **Subdirectories**: `h 2/` = Claude export, contains `conversations.json` + `memories.json` + `users.json` + `projects/` dir
- **Projects dir**: Contains per-project JSON files with `name`, `description`, `prompt_template`, `docs`
- **Root-level export**: `conversations.json` at top level has same structure but different `account.uuid`

### Key Differences
| | DeepSeek | Claude |
|---|---|---|
| Message tree | Nested `mapping` with parent/children | Flat `chat_messages` array |
| User msg key | `fragments[].content` (type=REQUEST) | `text` or `content[].text` |
| Metadata | `title`, `inserted_at` | `name`, `summary`, `created_at`, `updated_at` |
| Memory file | `memories.json` (array) | `memories.json` (array) |
| User file | `user.json` (single object) | `users.json` (array) |

## Extraction Workflow

### 1. Inventory
```python
import json
with open(path) as f:
    data = json.load(f)
print(f"{len(data)} conversations")
for i, conv in enumerate(data[:5]):
    title = conv.get('title', conv.get('name', 'Untitled'))
    msgs = conv.get('mapping', conv.get('chat_messages', {}))
    print(f"  [{i}] '{title}' — {len(msgs)} messages")
```

### 2. Extract User Messages
- DeepSeek: Traverse `mapping` tree BFS, collect all `fragments` with `type == "REQUEST"`
- Claude: Read `chat_messages[].text` for even-indexed messages
- Collect 20-50 representative messages across multiple conversations

### 3. Analyze Communication Style
Look for:
- **Sentence structure**: Run-on vs punctuated, capitalization habits
- **Tone**: Direct/casual/formal, use of please/thank-you
- **Task-giving pattern**: Stream-of-consciousness vs structured briefs
- **Vocabulary cues**: "formalise" = document, "tidy up" = structure, "crunch numbers" = calculate
- **Topic switching**: Single-topic vs multi-topic conversations
- **Length**: Short queries vs long context paragraphs

### 4. Extract Business/Project Context
- Identify recurring business names, projects, people
- Note financial figures, timelines, decisions
- Map relationships between entities
- Flag active vs historical projects

### 5. Update Memory Files
**Priority order** (memory has limited capacity ~2,200 chars):
1. Replace redundant entries first (consolidate before adding)
2. Write most critical facts to `memory` tool (identity, style, top projects)
3. Write detailed analysis to `memories/insights/chat-history-analysis-YYYY-MM-DD.md`
4. Update `memories/USER.md` with enriched profile (full name, DOB, contacts)

**Memory capacity management**:
- Check current usage before adding
- If >80%, consolidate existing entries: replace multiple entries with one dense entry
- Use `memories/<category>/` files for overflow (not everything fits in the memory tool)
- The memory tool injects into every session; the files are loaded on demand

### 6. Write Analysis Document
Save full extraction to `memories/insights/chat-history-analysis-YYYY-MM-DD.md`:
- Source files processed
- Identity findings
- Communication style (with examples)
- Business ecosystem map
- Family/personal context
- Key contacts
- Financial picture
- Active projects

## Pitfalls

1. **Assuming uniform structure** — Claude has 3 different export formats (root, h2/, projects/). Always inspect first.
2. **Mixing user/assistant messages** — DeepSeek's tree structure can have multiple REQUEST fragments per node. Collect only the first REQUEST per node for style analysis.
3. **Memory overflow** — The memory tool has a hard limit. You WILL hit it. Consolidate before adding.
4. **Overwriting good data** — When updating USER.md, use `patch` for targeted edits, not full rewrites. Preserve existing structure.
5. **Missing the "h 2" directory** — The space in the folder name causes shell escaping issues. Quote paths or use Python.
