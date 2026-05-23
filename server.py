#!/usr/bin/env python3
"""
simple-server — 一行命令启动静态文件服务器，局域网 / Tailscale 直连访问。

用法:
  python3 server.py              # 当前目录，端口 8080
  python3 server.py --port 3000  # 指定端口
  python3 server.py --dir ./dist # 指定目录
  python3 server.py -q           # 安静模式
"""

import argparse
import http.server
import json
import os
import socket
import subprocess
import sys
import urllib.parse


def get_lan_ip() -> str | None:
    """获取本机局域网 IP（192.168/172.16-31/10.x）。"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.1)
        s.connect(("192.168.255.255", 1))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return None


def get_tailscale_ip() -> str | None:
    """获取 Tailscale 虚拟 IP（如有）。"""
    try:
        result = subprocess.run(
            ["tailscale", "ip", "-4"],
            capture_output=True, text=True, timeout=3
        )
        ip = result.stdout.strip()
        return ip if ip else None
    except Exception:
        return None


def get_wsl_host_ip() -> str | None:
    """获取 WSL 环境下 Windows 宿主的局域网 IP。"""
    try:
        route = subprocess.run(
            ["ip", "route"], capture_output=True, text=True, timeout=3
        )
        for line in route.stdout.splitlines():
            if line.startswith("default via "):
                parts = line.split()
                if len(parts) > 2:
                    return parts[2]
    except Exception:
        return None


def print_banner(port: int, quiet: bool):
    if quiet:
        return

    lan_ip = get_lan_ip()
    ts_ip = get_tailscale_ip()
    wsl_gw = get_wsl_host_ip()

    print()
    print("  ╔══════════════════════════════════════════╗")
    print("  ║         simple-server 已启动             ║")
    print("  ╚══════════════════════════════════════════╝")
    print()
    print(f"  本机:      http://localhost:{port}")
    if lan_ip:
        print(f"  局域网:    http://{lan_ip}:{port}")
    if ts_ip:
        print(f"  Tailscale: http://{ts_ip}:{port}")
    if wsl_gw and wsl_gw != "127.0.0.1":
        print(f"  WSL 转发:  http://<Windows-IP>:{port}")
    print()
    print(f"  目录:      {os.path.abspath(args.dir)}")
    print(f"  PID:       {os.getpid()}")
    print()
    print("  Ctrl+C 停止服务")
    print()


class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
    """不输出访问日志的 Handler。"""

    def log_message(self, format, *args):
        pass


def main():
    parser = argparse.ArgumentParser(
        description="simple-server — 一行命令启动静态文件服务器"
    )
    parser.add_argument(
        "--port", "-p", type=int, default=8080,
        help="监听端口（默认 8080）"
    )
    parser.add_argument(
        "--dir", "-d", type=str, default=".",
        help="要服务的目录（默认当前目录）"
    )
    parser.add_argument(
        "--quiet", "-q", action="store_true",
        help="安静模式，不打印日志"
    )
    args = parser.parse_args()

    serve_dir = os.path.abspath(args.dir)
    if not os.path.isdir(serve_dir):
        print(f"错误: 目录不存在 — {serve_dir}", file=sys.stderr)
        sys.exit(1)

    os.chdir(serve_dir)

    handler = QuietHTTPRequestHandler if args.quiet else http.server.SimpleHTTPRequestHandler
    server = http.server.HTTPServer(("0.0.0.0", args.port), handler)

    print_banner(args.port, args.quiet)

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  服务已停止")
        server.server_close()


if __name__ == "__main__":
    main()
