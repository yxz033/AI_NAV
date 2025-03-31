import os
import re

def update_ga_code(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # 检查是否已经包含GA代码
    if 'googletagmanager.com/gtag/js?id=G-7CM8CMB4EH' in content:
        print(f"文件 {file_path} 已包含GA代码,跳过")
        return
    
    # 在head标签后添加GA代码
    ga_code = '''    <!-- Google tag (gtag.js) -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-7CM8CMB4EH"></script>
    <script>
      window.dataLayer = window.dataLayer || [];
      function gtag(){dataLayer.push(arguments);}
      gtag('js', new Date());

      gtag('config', 'G-7CM8CMB4EH');
    </script>'''
    
    # 使用正则表达式在head标签后插入GA代码
    new_content = re.sub(r'(<head>.*?)', r'\1\n' + ga_code, content, flags=re.DOTALL)
    
    # 写入更新后的内容
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    print(f"已更新文件: {file_path}")

def process_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.html'):
                file_path = os.path.join(root, file)
                update_ga_code(file_path)

if __name__ == '__main__':
    # 更新根目录下的HTML文件
    process_directory('.')
    print("所有HTML文件已更新完成!") 