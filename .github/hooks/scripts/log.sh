#!/usr/bin/env sh

set -eu

# -- Resolve repository root from current hook working dir (.github/hooks) --
scriptDir="$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)"
hookDir="$(CDPATH= cd -- "$scriptDir/.." && pwd)"
repoRoot="$(CDPATH= cd -- "$hookDir/../.." && pwd)"

# -- Resolve Windows cache directory (LOCALAPPDATA preferred) --
cacheBase=""
if [ -n "${LOCALAPPDATA:-}" ]; then
  cacheBase="$LOCALAPPDATA/copilot-hook"
elif [ -n "${TEMP:-}" ]; then
  cacheBase="$TEMP/copilot-hook"
elif [ -n "${TMP:-}" ]; then
  cacheBase="$TMP/copilot-hook"
fi

if [ -z "$cacheBase" ]; then
  cacheBase="$hookDir/logs"
fi

logFile="$cacheBase/log.md"
today="$(date '+%Y-%m-%d')"
nowTs="$(date '+%Y-%m-%d %H:%M:%S')"

mkdir -p "$cacheBase"

# -- Read user requirement text from common hook env vars if available --
reqText="${COPILOT_USER_REQUEST:-${USER_REQUEST:-${PROMPT:-${INPUT_TEXT:-${COPILOT_PROMPT:-}}}}}"

if [ -z "$reqText" ] && [ -n "${COPILOT_TRANSCRIPT_PATH:-}" ] && [ -f "${COPILOT_TRANSCRIPT_PATH:-}" ]; then
  reqText="$(tail -n 80 "$COPILOT_TRANSCRIPT_PATH" 2>/dev/null || true)"
fi

if [ -z "$reqText" ] && [ ! -t 0 ]; then
  stdinText="$(cat 2>/dev/null || true)"
  if [ -n "$stdinText" ]; then
    reqText="$stdinText"
  fi
fi

if [ -z "$reqText" ]; then
  reqText="（未从 hook 上下文读取到本次对话需求文本）"
fi

# -- Collect git worktree changes --
cd "$repoRoot"

if command -v git >/dev/null 2>&1; then
  gitStatus="$(git --no-pager status --short 2>/dev/null || true)"
  stagedDiff="$(git --no-pager diff --cached -- . 2>/dev/null || true)"
  unstagedDiff="$(git --no-pager diff -- . 2>/dev/null || true)"
else
  gitStatus="（未检测到 git 命令）"
  stagedDiff=""
  unstagedDiff=""
fi

if [ -z "$gitStatus" ]; then
  gitStatus="（无工作树变化）"
fi

if [ -z "$stagedDiff" ]; then
  stagedDiff="（无已暂存变更）"
fi

if [ -z "$unstagedDiff" ]; then
  unstagedDiff="（无未暂存变更）"
fi

# -- Date check: clear log when day changed --
if [ -f "$logFile" ]; then
  firstDate="$(grep -m 1 '^# Date: ' "$logFile" | sed 's/^# Date: //' || true)"
  if [ -n "$firstDate" ] && [ "$firstDate" != "$today" ]; then
    : > "$logFile"
  fi
fi

# -- Initialize file header if file missing or empty --
if [ ! -s "$logFile" ]; then
  cat > "$logFile" <<EOF
# Date: $today

EOF
fi

# -- Append current record in order --
cat >> "$logFile" <<EOF
## Record: $nowTs

### 本次对话提出的需求和功能
\`\`\`text
$reqText
\`\`\`

### 对话产生的 Git 工作树代码变化（status）
\`\`\`text
$gitStatus
\`\`\`

### 已暂存代码差异（git diff --cached）
\`\`\`diff
$stagedDiff
\`\`\`

### 未暂存代码差异（git diff）
\`\`\`diff
$unstagedDiff
\`\`\`

---

EOF

exit 0
