#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""一个使用 Python 标准库实现的 Python 学习网页。"""

from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs

HOST = "0.0.0.0"
PORT = 8000

LESSONS = [
    {
        "title": "第 1 课：变量与数据类型",
        "content": "Python 常见类型有 int、float、str、bool、list、dict。变量无需提前声明。",
        "example": "name = '小明'\nage = 18\nprint(name, age)",
    },
    {
        "title": "第 2 课：条件判断",
        "content": "使用 if / elif / else 根据条件执行不同代码分支。",
        "example": "score = 85\nif score >= 90:\n    print('优秀')\nelif score >= 60:\n    print('及格')\nelse:\n    print('不及格')",
    },
    {
        "title": "第 3 课：循环",
        "content": "for 循环用于遍历序列，while 循环用于条件循环。",
        "example": "for i in range(5):\n    print(i)",
    },
]


class LearningSiteHandler(BaseHTTPRequestHandler):
    def _send_html(self, html: str, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def do_GET(self):
        if self.path not in ["/", "/index"]:
            self._send_html("<h1>404 - 页面不存在</h1>", status=404)
            return

        lesson_cards = "\n".join(
            f"""
            <section class=\"card\">
                <h3>{lesson['title']}</h3>
                <p>{lesson['content']}</p>
                <pre><code>{lesson['example']}</code></pre>
            </section>
            """
            for lesson in LESSONS
        )

        html = f"""
<!DOCTYPE html>
<html lang=\"zh-CN\">
<head>
  <meta charset=\"UTF-8\" />
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1.0\" />
  <title>Python 学习网页</title>
  <style>
    body {{
      font-family: Arial, sans-serif;
      margin: 0;
      background: #f5f7fb;
      color: #1f2937;
    }}
    header {{
      background: linear-gradient(135deg, #2563eb, #7c3aed);
      color: #fff;
      padding: 32px 20px;
      text-align: center;
    }}
    main {{
      max-width: 900px;
      margin: 24px auto;
      padding: 0 16px 40px;
    }}
    .card {{
      background: #fff;
      border-radius: 12px;
      padding: 18px;
      margin-bottom: 16px;
      box-shadow: 0 4px 12px rgba(0,0,0,0.08);
    }}
    pre {{
      background: #111827;
      color: #e5e7eb;
      padding: 12px;
      border-radius: 8px;
      overflow-x: auto;
    }}
    .quiz button {{
      background: #2563eb;
      color: white;
      border: none;
      border-radius: 8px;
      padding: 10px 16px;
      cursor: pointer;
    }}
    .quiz button:hover {{
      background: #1d4ed8;
    }}
    footer {{
      text-align: center;
      color: #6b7280;
      margin-top: 20px;
    }}
  </style>
</head>
<body>
  <header>
    <h1>Python 学习网页</h1>
    <p>从零开始，轻松掌握 Python 编程基础</p>
  </header>
  <main>
    <h2>📚 课程目录</h2>
    {lesson_cards}

    <section class=\"card quiz\">
      <h3>🧠 小测验</h3>
      <p>Python 中用于循环 5 次的常见写法是？</p>
      <form method=\"post\" action=\"/\">
        <label><input type=\"radio\" name=\"answer\" value=\"a\" required /> a) loop(5)</label><br />
        <label><input type=\"radio\" name=\"answer\" value=\"b\" /> b) for i in range(5)</label><br />
        <label><input type=\"radio\" name=\"answer\" value=\"c\" /> c) repeat 5</label><br /><br />
        <button type=\"submit\">提交答案</button>
      </form>
    </section>
    <footer>使用 Python 标准库构建 · 可直接运行</footer>
  </main>
</body>
</html>
        """
        self._send_html(html)

    def do_POST(self):
        if self.path != "/":
            self._send_html("<h1>404 - 页面不存在</h1>", status=404)
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode("utf-8")
        answer = parse_qs(body).get("answer", [""])[0]

        if answer == "b":
            result = "✅ 回答正确！for i in range(5) 是常见写法。"
            color = "#166534"
        else:
            result = "❌ 回答不正确，再复习一下 for 循环吧。"
            color = "#991b1b"

        html = f"""
<!DOCTYPE html>
<html lang=\"zh-CN\">
<head><meta charset=\"UTF-8\"><title>测验结果</title></head>
<body style=\"font-family: Arial, sans-serif; padding: 40px;\">
  <h1>测验结果</h1>
  <p style=\"color:{color}; font-size: 20px;\">{result}</p>
  <a href=\"/\">返回课程首页</a>
</body>
</html>
        """
        self._send_html(html)


def run_server() -> None:
    server = HTTPServer((HOST, PORT), LearningSiteHandler)
    print(f"Python 学习网页运行中：http://{HOST}:{PORT}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()
