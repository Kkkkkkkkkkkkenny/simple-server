# simple-server

即插即用的静态文件服务器。把脚本扔进项目目录，一行命令，局域网 / Tailscale 直连访问。

## 使用

```bash
./server.py                # 服务当前目录，端口 8080
./server.py index.html     # 指定某个 HTML 文件
./server.py ./dist/        # 指定目录
./server.py -p 3000        # 指定端口
./server.py -q             # 安静模式
```

启动后自动打印访问地址：

```
  ╔══════════════════════════════════════════╗
  ║         simple-server 已启动             ║
  ╚══════════════════════════════════════════╝

  本机:      http://localhost:8080
  局域网:    http://192.168.1.5:8080
  Tailscale: http://100.81.74.3:8080

  目录:      /home/user/my-project
  PID:       12345

  Ctrl+C 停止服务
```

其他设备打开 `http://192.168.x.x:8080` 就能访问你的页面。

## 场景

| 场景 | 命令 |
|------|------|
| 临时分享页面给别人看 | `./server.py` |
| 分享单个 HTML 文件 | `./server.py login.html` |
| 预览构建产物 | `./server.py ./dist/` |
| 后台静默运行 | `./server.py -q &` |

## 参数

| 参数 | 默认值 | 说明 |
|------|--------|------|
| `target` | `.` | 要服务的文件或目录 |
| `-p` / `--port` | 8080 | 监听端口 |
| `-q` / `--quiet` | — | 安静模式，不输出日志 |

## 原理

详见 [原理.md](./原理.md)，涵盖 IP/端口、局域网通信、NAT 端口转发、
Tailscale 虚拟组网、WSL2 网络模型、HTTP 协议等底层原理。

## 依赖

Python 3.8+，无需第三方库。
