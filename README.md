# simple-server

一行命令把当前目录变成可访问的静态文件服务器，局域网 / Tailscale 秒开。

## 使用

```bash
python3 server.py              # 当前目录，端口 8080
python3 server.py -p 3000      # 指定端口
python3 server.py -d ./dist    # 指定目录
python3 server.py -q           # 安静模式（不输出访问日志）
```

启动后会自动打印可用的访问地址：

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

## 场景

- 临时分享 HTML 文件 / 前端页面给同局域网的人看
- 配合 Tailscale 跨网络访问，无需端口转发
- 快速预览构建产物（`python3 server.py -d ./dist`）
- 替代 `python3 -m http.server`，自动检测 IP 地址

## 参数

| 参数 | 简写 | 默认值 | 说明 |
|------|------|--------|------|
| `--port` | `-p` | `8080` | 监听端口 |
| `--dir` | `-d` | `.` | 服务目录 |
| `--quiet` | `-q` | `false` | 安静模式 |

## 依赖

Python 3.8+，无第三方依赖。
