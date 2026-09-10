#!/usr/bin/env python3
"""Serve the Root My Galaxy support feed over the LAN (no GitHub needed).

The app resolves a commit, then fetches the manifest and every artifact from
that commit. This server reproduces that protocol from a local payload
checkout:

    GET /api/commit
        -> {"object": {"sha": "<40-hex>"}}
    GET /raw/<sha>/support/targets-v3.json
        -> the feed with every artifact URL rewritten to this server
    GET /raw/<sha>/<path>
        -> the artifact file from the checkout

Usage:
    tools/feed_server.py --advertise http://192.168.3.247:8080
    # then build the app against it:
    #   ./gradlew :app:assembleDebug \
    #     -PfeedCommitApi=http://192.168.3.247:8080/api/commit \
    #     -PfeedRawBase=http://192.168.3.247:8080/raw

Only the exploit payload and KernelSU artifacts are served; paths are resolved
inside the checkout and traversal outside it is rejected.
"""
import argparse
import json
import re
import subprocess
import sys
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent


def head_sha():
    try:
        out = subprocess.check_output(
            ["git", "-C", str(REPO), "rev-parse", "HEAD"], text=True)
        return out.strip()
    except Exception as error:  # pragma: no cover - fallback only
        print(f"warning: git rev-parse failed ({error}); using zero sha", file=sys.stderr)
        return "0" * 40


class FeedHandler(BaseHTTPRequestHandler):
    server_version = "RMGFeed/1.0"
    sha = "0" * 40
    ref = "main"
    base = "http://127.0.0.1:8080"

    def log_message(self, fmt, *args):
        sys.stdout.write("%s - %s\n" % (self.address_string(), fmt % args))
        sys.stdout.flush()

    def _send(self, code, body, ctype):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):  # noqa: N802 - BaseHTTPRequestHandler API
        path = self.path.split("?", 1)[0]
        if path in ("/api/commit", "/commit"):
            body = json.dumps({
                "ref": "refs/heads/" + self.ref,
                "object": {"sha": self.sha, "type": "commit"},
            }).encode()
            self._send(200, body, "application/json")
            return

        match = re.match(r"^/raw/([0-9a-f]{40})/(.+)$", path)
        if not match:
            self._send(404, b"not found\n", "text/plain")
            return
        sha, relative = match.group(1), match.group(2)
        if sha != self.sha:
            self._send(404, b"unknown commit\n", "text/plain")
            return

        if relative == "support/targets-v3.json":
            manifest = json.loads((REPO / relative).read_text(encoding="utf-8"))
            marker = f"/{self.ref}/"
            for target in manifest["payloads"]:
                for key in ("exploit", "kernelsu"):
                    url = target[key]["url"]
                    index = url.find(marker)
                    if index >= 0:
                        target[key]["url"] = (
                            f"{self.base}/raw/{self.ref}/"
                            + url[index + len(marker):])
            body = json.dumps(manifest, ensure_ascii=False, indent=2).encode()
            self._send(200, body, "application/json")
            return

        candidate = (REPO / relative).resolve()
        if not str(candidate).startswith(str(REPO)) or not candidate.is_file():
            self._send(404, b"not found\n", "text/plain")
            return
        self._send(200, candidate.read_bytes(), "application/octet-stream")


def main():
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8080)
    parser.add_argument("--advertise", default=None,
                        help="URL base the phone uses, e.g. http://192.168.3.247:8080")
    parser.add_argument("--ref", default="main")
    args = parser.parse_args()

    FeedHandler.sha = head_sha()
    FeedHandler.ref = args.ref
    FeedHandler.base = args.advertise or f"http://127.0.0.1:{args.port}"

    print(f"payload checkout : {REPO}")
    print(f"commit           : {FeedHandler.sha}")
    print(f"advertised base  : {FeedHandler.base}")
    print(f"listening        : http://{args.host}:{args.port}")
    ThreadingHTTPServer((args.host, args.port), FeedHandler).serve_forever()


if __name__ == "__main__":
    main()
