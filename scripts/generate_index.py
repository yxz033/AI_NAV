import json
import os
from jinja2 import Environment, FileSystemLoader
import sys

# 获取脚本所在目录的父目录（项目根目录）
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# 添加项目根目录到系统路径
sys.path.append(project_root)

# 配置Jinja2环境
env = Environment(loader=FileSystemLoader(os.path.join(project_root, 'templates')))

# 读取工具数据
json_path = os.path.join(project_root, 'ai-tools-json.json')
with open(json_path, 'r', encoding='utf-8') as f:
    data = json.load(f)

# 准备所有工具的数据
all_tools = []
for category in data['categories']:
    for tool in category['tools']:
        tool_data = {
            'name': tool['name'],
            'category': category['name'],
            'description': tool['description'],
            'url': tool['url'],
            'monthly_visitors': '475.0K' if tool['name'] == 'Claude' else ('328.5K' if tool['name'] == 'Midjourney' else 'New'),
            'rating': '44' if tool['name'] == 'Claude' else ('38' if tool['name'] == 'Midjourney' else '0'),
            'tags': []
        }
        
        # 根据类别添加标签
        if category['name'] == 'AI-Assisted Development & Code Generation':
            tool_data['tags'] = ['AI Assistant', 'Code Generation']
        elif category['name'] == 'AI Image Generation':
            tool_data['tags'] = ['Image Generation', 'Art']
        # 可以添加更多类别的标签
        
        all_tools.append(tool_data)

# 获取所有类别
categories = ['All'] + [cat['name'].replace(' & ', ' ').split(' ')[0] for cat in data['categories']]

# 准备模板数据
template_data = {
    'tools': all_tools,
    'categories': categories
}

# 读取模板
with open(os.path.join(project_root, 'templates', 'index.html'), 'r', encoding='utf-8') as f:
    template_content = f.read()

# 创建模板对象
template = env.from_string(template_content)

# 生成页面
output = template.render(**template_data)

# 保存文件
with open(os.path.join(project_root, 'index.html'), 'w', encoding='utf-8') as f:
    f.write(output)

print('首页生成完成！') 