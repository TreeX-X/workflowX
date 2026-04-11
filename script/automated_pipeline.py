import json
import socket
import subprocess
import time
from pathlib import Path

# --- agentWorkFlowX 配置 ---
HOST = "127.0.0.1"
PORT = 8765
CLI_COMMAND = "claude"
WORKSPACE_DIR = Path(__file__).resolve().parents[1]
POLL_INTERVAL_SECONDS = 1.0
TASK_IDLE_SECONDS = 3.0
ALLOWED_EXTENSIONS = (
    ".py", ".js", ".ts", ".tsx", ".jsx", ".html", ".css",
    ".java", ".cpp", ".go", ".rs", ".md", ".json", ".yaml", ".yml"
)
IGNORE_DIR_NAMES = {".git", ".idea", ".vscode", "node_modules", "__pycache__"}


def is_ignored(file_path: Path) -> bool:
    for part in file_path.parts:
        if part in IGNORE_DIR_NAMES:
            return True
    return False


def iter_candidate_files():
    for path in WORKSPACE_DIR.rglob("*"):
        if not path.is_file():
            continue
        if is_ignored(path):
            continue
        if path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue
        yield path.resolve()


def snapshot_workspace() -> dict[str, tuple[int, int]]:
    # value: (mtime_ns, size)
    state = {}
    for file_path in iter_candidate_files():
        try:
            stat = file_path.stat()
        except OSError:
            continue
        state[str(file_path)] = (stat.st_mtime_ns, stat.st_size)
    return state


def collect_changed_files(before: dict[str, tuple[int, int]], after: dict[str, tuple[int, int]]) -> list[str]:
    changed = []
    for path, new_meta in after.items():
        old_meta = before.get(path)
        if old_meta != new_meta:
            changed.append(path)
    return sorted(changed)


def send_event(payload: dict) -> None:
    packet = (json.dumps(payload, ensure_ascii=False) + "\n").encode("utf-8")
    with socket.create_connection((HOST, PORT), timeout=1.5) as conn:
        conn.sendall(packet)


def push_batch_review(paths: list[str]) -> None:
    if not paths:
        return
    payload = {
        "type": "batch_review",
        "paths": sorted(paths),
        "count": len(paths),
        "ts": time.time(),
    }
    send_event(payload)


def start_pipeline():
    print(f"[agentWorkFlowX] write pipeline start: {WORKSPACE_DIR}")

    last_snapshot = snapshot_workspace()
    task_files = set()
    last_change_ts = 0.0

    try:
        proc = subprocess.Popen(CLI_COMMAND, shell=True, cwd=str(WORKSPACE_DIR))
    except KeyboardInterrupt:
        print("[agentWorkFlowX] interrupted before claude launch.")
        return

    while True:
        time.sleep(POLL_INTERVAL_SECONDS)

        current_snapshot = snapshot_workspace()
        changed_now = collect_changed_files(last_snapshot, current_snapshot)
        last_snapshot = current_snapshot

        if changed_now:
            task_files.update(changed_now)
            last_change_ts = time.time()

        now = time.time()
        if task_files and last_change_ts and (now - last_change_ts >= TASK_IDLE_SECONDS):
            try:
                push_batch_review(sorted(task_files))
                print(f"[agentWorkFlowX] task done, pushed {len(task_files)} files.")
            except Exception as exc:
                print(f"[agentWorkFlowX] push failed: {exc}")
            finally:
                task_files.clear()
                last_change_ts = 0.0

        if proc.poll() is not None:
            break

    # claude 退出后最后再冲刷一次
    if task_files:
        try:
            push_batch_review(sorted(task_files))
            print(f"[agentWorkFlowX] exit flush, pushed {len(task_files)} files.")
        except Exception as exc:
            print(f"[agentWorkFlowX] push failed on exit: {exc}")

    print("[agentWorkFlowX] write pipeline stopped.")


if __name__ == "__main__":
    start_pipeline()
