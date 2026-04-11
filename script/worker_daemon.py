import ctypes
import json
import socket
import subprocess
import threading
import time
from ctypes import wintypes
from pathlib import Path

# --- agentWorkFlowX 配置 ---
HOST = "127.0.0.1"
PORT = 8765
INTERACTIVE_CLI_COMMAND = "codex"
REVIEW_CMD_FORMAT = 'review "{filepath}"'
WORKSPACE_DIR = Path(__file__).resolve().parents[1]
INJECT_INTERVAL_SECONDS = 0.5  # 增加整个处理周期的间隔


def _build_input_structs():
    class KEY_EVENT_RECORD(ctypes.Structure):
        _fields_ = [
            ("bKeyDown", wintypes.BOOL),
            ("wRepeatCount", wintypes.WORD),
            ("wVirtualKeyCode", wintypes.WORD),
            ("wVirtualScanCode", wintypes.WORD),
            ("uChar", wintypes.WCHAR),
            ("dwControlKeyState", wintypes.DWORD),
        ]

    class EVENT_UNION(ctypes.Union):
        _fields_ = [("KeyEvent", KEY_EVENT_RECORD)]

    class INPUT_RECORD(ctypes.Structure):
        _fields_ = [
            ("EventType", wintypes.WORD),
            ("Event", EVENT_UNION),
        ]

    return KEY_EVENT_RECORD, INPUT_RECORD


def send_text_to_console(text: str) -> None:
    """把文本注入到当前控制台输入缓冲区（后台静默输入）。"""
    STD_INPUT_HANDLE = -10
    handle = ctypes.windll.kernel32.GetStdHandle(STD_INPUT_HANDLE)
    _, INPUT_RECORD = _build_input_structs()

    if not text:
        return

    records = (INPUT_RECORD * (len(text) * 2))()

    for i, char in enumerate(text):
        records[i * 2].EventType = 1
        records[i * 2].Event.KeyEvent.bKeyDown = True
        records[i * 2].Event.KeyEvent.wRepeatCount = 1
        records[i * 2].Event.KeyEvent.uChar = char

        records[i * 2 + 1].EventType = 1
        records[i * 2 + 1].Event.KeyEvent.bKeyDown = False
        records[i * 2 + 1].Event.KeyEvent.wRepeatCount = 1
        records[i * 2 + 1].Event.KeyEvent.uChar = char

    written = wintypes.DWORD(0)
    ctypes.windll.kernel32.WriteConsoleInputW(handle, records, len(records), ctypes.byref(written))


def send_enter_to_console() -> None:
    """向控制台注入极其严格的硬件级 Enter 键。"""
    STD_INPUT_HANDLE = -10
    handle = ctypes.windll.kernel32.GetStdHandle(STD_INPUT_HANDLE)
    _, INPUT_RECORD = _build_input_structs()

    events = []

    def add_event(is_down: bool):
        rec = INPUT_RECORD()
        rec.EventType = 1
        rec.Event.KeyEvent.bKeyDown = is_down
        rec.Event.KeyEvent.wRepeatCount = 1
        
        # 核心修复：必须是严格的组合
        rec.Event.KeyEvent.wVirtualKeyCode = 0x0D  # VK_RETURN
        rec.Event.KeyEvent.wVirtualScanCode = 0x1C # 硬件级 Enter 扫描码
        rec.Event.KeyEvent.uChar = "\r"            # 在 Windows 控制台底层，Enter 对应 \r
        rec.Event.KeyEvent.dwControlKeyState = 0
        
        events.append(rec)

    add_event(True)
    add_event(False)

    records = (INPUT_RECORD * len(events))(*events)
    written = wintypes.DWORD(0)
    ctypes.windll.kernel32.WriteConsoleInputW(handle, records, len(records), ctypes.byref(written))


def queue_review(file_path: Path) -> None:
    cmd_to_send = REVIEW_CMD_FORMAT.format(filepath=str(file_path.resolve()))
    
    send_text_to_console(cmd_to_send)
    
    # 核心修复：0.08s 极大概率被 CLI 的防抖/高亮/自动补全逻辑清空缓冲区给吃掉
    # 延长到 0.5s，等 codex 内部彻底把前面的字符串处理完，再塞入回车
    time.sleep(0.5) 
    
    send_enter_to_console()


def process_message(message: dict) -> None:
    msg_type = message.get("type")
    if msg_type not in ("file_modified", "batch_review"):
        return

    target_files = []
    if msg_type == "file_modified":
        target_file = message.get("path", "").strip()
        if target_file:
            target_files = [target_file]
    else:
        target_files = [str(p).strip() for p in message.get("paths", []) if str(p).strip()]

    if not target_files:
        return

    for item in target_files:
        file_path = Path(item)
        if not file_path.exists():
            continue

        queue_review(file_path)
        time.sleep(INJECT_INTERVAL_SECONDS)


def socket_listener() -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((HOST, PORT))
        server.listen(5)

        while True:
            try:
                conn, _ = server.accept()
                with conn:
                    chunks = []
                    while True:
                        part = conn.recv(4096)
                        if not part:
                            break
                        chunks.append(part)

                    if not chunks:
                        continue

                    data = b"".join(chunks)

                    lines = data.decode("utf-8", errors="ignore").splitlines()
                    for line in lines:
                        line = line.strip()
                        if not line:
                            continue
                        try:
                            message = json.loads(line)
                        except json.JSONDecodeError:
                            continue
                        process_message(message)
            except Exception as exc:
                print(f"⚠️ [agentWorkFlowX] 监听异常: {exc}")
                time.sleep(0.5)


def start_worker():
    print(f"[agentWorkFlowX] review daemon start: {HOST}:{PORT}")

    listener_thread = threading.Thread(target=socket_listener, daemon=True)
    listener_thread.start()

    try:
        # 使用原生控制台启动，完美接纳 WriteConsoleInputW 的输入
        subprocess.run(INTERACTIVE_CLI_COMMAND, shell=True, cwd=str(WORKSPACE_DIR))
    except KeyboardInterrupt:
        pass
    finally:
        print("[agentWorkFlowX] review daemon stopped.")


if __name__ == "__main__":
    start_worker()