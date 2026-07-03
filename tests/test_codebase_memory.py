#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CBM = ROOT / "dist/integrations/codebase-memory"
INSTALL = ROOT / "dist/install/install.sh"


def run(*args: str, ok: bool = True, env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    cp = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, env=env)
    if ok and cp.returncode:
        raise AssertionError(f"{args}\nstdout={cp.stdout}\nstderr={cp.stderr}")
    if not ok and cp.returncode == 0:
        raise AssertionError(f"expected failure: {args}")
    return cp


def fake_binary(root: Path) -> Path:
    path = root / "codebase-memory-mcp"
    path.write_text(
        "#!/usr/bin/env bash\n"
        "if [[ ${1:-} == --version ]]; then echo 'codebase-memory-mcp 0.8.1'; exit 0; fi\n"
        "if [[ ${1:-} == cli ]]; then echo '{\"status\":\"indexed\"}'; exit 0; fi\n"
        "echo '{\"jsonrpc\":\"2.0\",\"result\":{}}'\n",
        "utf-8",
    )
    path.chmod(0o755)
    return path


def main() -> None:
    with tempfile.TemporaryDirectory(prefix="powerpack-cbm-test-") as td:
        base = Path(td); binary = fake_binary(base); target = base / "project"; target.mkdir()
        (target / ".codex").mkdir()
        config = target / ".codex/config.toml"
        config.write_text('[mcp_servers.existing]\ncommand = "keep-me"\n', "utf-8")
        agents = target / "AGENTS.md"; agents.write_text("User rules stay.\n", "utf-8")

        # Clean install over existing user config and instructions.
        run(str(CBM / "install.sh"), "--target", str(target), "--binary", str(binary), "--backup")
        text = config.read_text("utf-8")
        assert "keep-me" in text and text.count("[mcp_servers.codebase-memory]") == 1
        assert "User rules stay." in agents.read_text("utf-8")
        state = json.loads((target / ".codex-powerpack/state/codebase-memory.json").read_text())
        assert state["mcp_scope"] == "project" and state["binary_sha256"]

        # Repeated install is idempotent and index/doctor/restore paths work.
        run(str(CBM / "install.sh"), "--target", str(target), "--binary", str(binary))
        assert config.read_text("utf-8").count("[mcp_servers.codebase-memory]") == 1
        run(str(CBM / "index.sh"), "--target", str(target))
        run(str(CBM / "doctor.sh"), "--target", str(target))
        run(str(CBM / "restore-tools.sh"), "--target", str(target))

        # Dry-run performs no writes.
        dry = base / "dry"; dry.mkdir()
        run(str(CBM / "install.sh"), "--target", str(dry), "--binary", str(binary), "--dry-run")
        assert not (dry / ".codex-powerpack").exists()

        # Existing unmanaged section is not overwritten; a candidate is emitted.
        conflict = base / "conflict"; (conflict / ".codex").mkdir(parents=True)
        cconfig = conflict / ".codex/config.toml"
        cconfig.write_text('[mcp_servers.codebase-memory]\ncommand = "user-owned"\n', "utf-8")
        run(str(CBM / "configure.sh"), "--target", str(conflict), "--binary", str(binary), ok=False)
        assert "user-owned" in cconfig.read_text("utf-8") and cconfig.with_name("config.toml.new").exists()

        # Uninstall preserves cache by default, retains user text/config, and can clear cache.
        cache_file = target / ".codex-powerpack/cache/codebase-memory/keep.db"
        cache_file.write_text("cache", "utf-8")
        run(str(CBM / "uninstall.sh"), "--target", str(target))
        assert cache_file.exists() and "keep-me" in config.read_text("utf-8")
        assert "codebase-memory" not in config.read_text("utf-8")
        assert "User rules stay." in agents.read_text("utf-8")
        run(str(CBM / "install.sh"), "--target", str(target), "--binary", str(binary))
        run(str(CBM / "uninstall.sh"), "--target", str(target), "--clear-cache")
        assert not cache_file.parent.exists()

        # Full distribution orchestrator installs actual Skills and agents.
        product = base / "product"; product.mkdir()
        run(str(INSTALL), "--target", str(product), "--profile", "minimal", "--with-codebase-memory", "--codebase-memory-binary", str(binary))
        assert (product / ".agents/skills/caveman/SKILL.md").exists()
        assert (product / ".agents/skills/humanizer/SKILL.md").exists()
        assert (product / ".codex/agents/explorer.toml").exists()
        run(str(ROOT / "dist/install/uninstall.sh"), "--target", str(product), "--clear-cache")
        assert not (product / ".agents/skills/caveman").exists()

        # Static safety gates: no upstream broad installer or pipe-to-shell path.
        installer = (CBM / "install.sh").read_text("utf-8")
        assert " install -y" not in installer and "| bash" not in installer and "| sh" not in installer
        assert "checksum mismatch" in installer and "unsupported architecture" in installer

        # Unsupported architecture fails before any download.
        fake_path = base / "fake-path"; fake_path.mkdir()
        uname = fake_path / "uname"
        uname.write_text('#!/usr/bin/env bash\n[[ "$1" == "-s" ]] && { echo Linux; exit; }\n[[ "$1" == "-m" ]] && { echo mips64; exit; }\nexec /usr/bin/uname "$@"\n', "utf-8")
        uname.chmod(0o755)
        env = os.environ.copy(); env["PATH"] = str(fake_path) + os.pathsep + env["PATH"]
        bad_arch = base / "bad-arch"; bad_arch.mkdir()
        cp = run(str(CBM / "install.sh"), "--target", str(bad_arch), ok=False, env=env)
        assert "unsupported architecture" in cp.stderr

        # A locally served checksum that differs from the pinned release is rejected.
        web = base / "web"; web.mkdir()
        archive = "codebase-memory-mcp-linux-amd64-portable.tar.gz"
        (web / archive).write_bytes(b"not an archive")
        (web / "checksums.txt").write_text("0" * 64 + "  " + archive + "\n", "utf-8")
        with socket.socket() as sock:
            sock.bind(("127.0.0.1", 0)); port = sock.getsockname()[1]
        server = subprocess.Popen([sys.executable, "-m", "http.server", str(port), "--bind", "127.0.0.1", "--directory", str(web)], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        try:
            for _ in range(50):
                try:
                    with urllib.request.urlopen(f"http://127.0.0.1:{port}/checksums.txt", timeout=0.2):
                        break
                except Exception:
                    if server.poll() is not None:
                        raise AssertionError("checksum fixture server exited during startup")
                    time.sleep(0.05)
            else:
                raise AssertionError("checksum fixture server did not become ready")
            env = os.environ.copy(); env["CBM_POWERPACK_RELEASE_BASE_URL"] = f"http://127.0.0.1:{port}"
            wrong = base / "wrong-checksum"; wrong.mkdir()
            cp = run(str(CBM / "install.sh"), "--target", str(wrong), ok=False, env=env)
            assert "pinned checksum" in cp.stderr, (cp.stdout, cp.stderr)
        finally:
            server.terminate(); server.wait(timeout=5)

        # Missing network is a clear failure and leaves no configured MCP section.
        env = os.environ.copy(); env["CBM_POWERPACK_RELEASE_BASE_URL"] = "http://127.0.0.1:9"
        offline = base / "offline"; offline.mkdir()
        run(str(CBM / "install.sh"), "--target", str(offline), ok=False, env=env)
        assert not (offline / ".codex/config.toml").exists()

    print("OK: Codebase Memory integration scenarios passed")


if __name__ == "__main__":
    main()
