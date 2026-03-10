#!/usr/bin/env python3
"""水滴智店 API 签名工具 & 请求发送器。

用法:
    # 仅计算签名
    python scripts/drip_sign.py sign '{"mobile":"13800138000"}'

    # 发送 API 请求
    python scripts/drip_sign.py call /customer/getByMobile '{"mobile":"13800138000"}'

环境变量:
    DRIP_CLIENT_ID      - 平台分配的客户端标识
    DRIP_CLIENT_SECRET   - 平台分配的密钥
"""

import hashlib
import json
import os
import sys
import time
import urllib.request

BASE_URL = "https://zd.drip.im/open/zd"


def compute_sign(body: str, client_secret: str, ts: int) -> str:
    """双重 SHA256 签名: sign = sha256(sha256(body + secret + ts) + secret)"""
    inner = hashlib.sha256(f"{body}{client_secret}{ts}".encode()).hexdigest()
    return hashlib.sha256(f"{inner}{client_secret}".encode()).hexdigest()


def call_api(path: str, body: str, client_id: str, client_secret: str) -> dict:
    """发送 API 请求并返回响应。"""
    ts = int(time.time())
    sign = compute_sign(body, client_secret, ts)
    url = f"{BASE_URL}{path}?client_id={client_id}&ts={ts}&sign={sign}"

    req = urllib.request.Request(
        url,
        data=body.encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as resp:
        return json.loads(resp.read().decode())


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    command = sys.argv[1]

    if command == "sign":
        if len(sys.argv) < 3:
            print("用法: python scripts/drip_sign.py sign '<json_body>'")
            sys.exit(1)
        body = sys.argv[2]
        secret = os.environ.get("DRIP_CLIENT_SECRET", "")
        if not secret:
            print("错误: 请设置环境变量 DRIP_CLIENT_SECRET", file=sys.stderr)
            sys.exit(1)
        ts = int(time.time())
        sign = compute_sign(body, secret, ts)
        print(json.dumps({"ts": ts, "sign": sign}, indent=2))

    elif command == "call":
        if len(sys.argv) < 4:
            print("用法: python scripts/drip_sign.py call /path '<json_body>'")
            sys.exit(1)
        path = sys.argv[2]
        body = sys.argv[3]
        client_id = os.environ.get("DRIP_CLIENT_ID", "")
        client_secret = os.environ.get("DRIP_CLIENT_SECRET", "")
        if not client_id or not client_secret:
            print("错误: 请设置环境变量 DRIP_CLIENT_ID 和 DRIP_CLIENT_SECRET", file=sys.stderr)
            sys.exit(1)
        result = call_api(path, body, client_id, client_secret)
        print(json.dumps(result, indent=2, ensure_ascii=False))

    else:
        print(f"未知命令: {command}")
        print("可用命令: sign, call")
        sys.exit(1)


if __name__ == "__main__":
    main()
