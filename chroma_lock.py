"""Trava exclusiva do Chroma para não corromper o HNSW no Windows (0xC0000005)."""
from __future__ import annotations

import atexit
import os
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

CHROMA_PATH = Path(os.environ.get("RAG_CHROMA_PATH", "C:/Users/gusta/obsidian/.chroma_db"))
LOCK_PATH = CHROMA_PATH.parent / ".chroma_index.lock"
SERVER_PID_PATH = CHROMA_PATH.parent / ".chroma_server.pid"
RAG_PORT = int(os.environ.get("RAG_PORT", os.environ.get("PORT", "7332")))

_lock_file = None


def porta_em_uso(porta: int = RAG_PORT) -> bool:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(0.3)
    try:
        sock.connect(("127.0.0.1", porta))
        return True
    except OSError:
        return False
    finally:
        sock.close()


def pid_servidor_registrado() -> int | None:
    if not SERVER_PID_PATH.exists():
        return None
    try:
        pid = int(SERVER_PID_PATH.read_text(encoding="utf-8").strip())
    except (ValueError, OSError):
        return None
    return pid if _pid_vivo(pid) else None


def _pid_vivo(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except OSError:
        return False


def registrar_servidor(pid: int | None = None) -> None:
    SERVER_PID_PATH.write_text(str(pid or os.getpid()), encoding="utf-8")


def limpar_pid_servidor() -> None:
    try:
        SERVER_PID_PATH.unlink(missing_ok=True)
    except OSError:
        pass


def parar_servidor_local() -> bool:
    """Encerra o --server na porta 7332 para poder recriar o banco com segurança."""
    pids: set[int] = set()
    registered = pid_servidor_registrado()
    if registered:
        pids.add(registered)
    if sys.platform == "win32":
        try:
            cmd = (
                f"(Get-NetTCPConnection -LocalPort {RAG_PORT} -State Listen "
                "-ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess)"
            )
            raw = subprocess.check_output(
                ["powershell", "-NoProfile", "-Command", cmd],
                text=True,
                stderr=subprocess.DEVNULL,
            )
            for line in raw.split():
                if line.isdigit():
                    pids.add(int(line))
        except Exception:
            pass
    stopped = False
    for pid in pids:
        if pid == os.getpid() or not _pid_vivo(pid):
            continue
        try:
            if sys.platform == "win32":
                subprocess.run(
                    ["taskkill", "/PID", str(pid), "/F"],
                    check=False,
                    capture_output=True,
                )
            else:
                os.kill(pid, signal.SIGTERM)
            stopped = True
            print(f"Servidor RAG local encerrado (pid {pid}).")
        except OSError as exc:
            print(f"Não foi possível encerrar pid {pid}: {exc}", file=sys.stderr)
    limpar_pid_servidor()
    for _ in range(20):
        if not porta_em_uso():
            break
        time.sleep(0.25)
    return stopped


def acquire_index_lock() -> None:
    global _lock_file
    LOCK_PATH.parent.mkdir(parents=True, exist_ok=True)
    _lock_file = open(LOCK_PATH, "a+b")
    if _lock_file.tell() == 0:
        _lock_file.write(b"0")
        _lock_file.flush()
    _lock_file.seek(0)
    try:
        if sys.platform == "win32":
            import msvcrt

            msvcrt.locking(_lock_file.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl

            fcntl.flock(_lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError:
        print(
            "Outro indexar/servidor está usando o Chroma. "
            "Não abra o mesmo .chroma_db em dois processos — isso corrompe o HNSW no Windows.",
            file=sys.stderr,
        )
        sys.exit(2)
    atexit.register(release_index_lock)


def release_index_lock() -> None:
    global _lock_file
    if not _lock_file:
        return
    try:
        _lock_file.seek(0)
        if sys.platform == "win32":
            import msvcrt

            msvcrt.locking(_lock_file.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            import fcntl

            fcntl.flock(_lock_file.fileno(), fcntl.LOCK_UN)
    except OSError:
        pass
    try:
        _lock_file.close()
    except OSError:
        pass
    _lock_file = None


def fechar_cliente_chroma(client, col) -> None:
    """Força flush do mmap HNSW antes de outro processo abrir o banco."""
    try:
        del col
    except Exception:
        pass
    try:
        system = getattr(client, "_system", None)
        if system is not None and hasattr(system, "stop"):
            system.stop()
    except Exception:
        pass
    try:
        del client
    except Exception:
        pass
    import gc

    gc.collect()
    time.sleep(0.4)
