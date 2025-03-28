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

# 确保输出目录存在
output_dir = os.path.join(project_root, 'output', 'tool')
os.makedirs(output_dir, exist_ok=True)

# 模板映射
TEMPLATE_MAPPING = {
    'AI-Assisted Development & Code Generation': 'dev_tool.html',
    'AI Image Generation': 'image_tool.html',
    # 可以添加更多类别的模板映射
}

# 为每个工具生成页面
for category in data['categories']:
    category_name = category['name']
    template_name = TEMPLATE_MAPPING.get(category_name, 'base.html')
    template = env.get_template(template_name)
    
    for tool in category['tools']:
        # 处理tutorial步骤
        tutorial = tool.get('tutorial', '')
        tutorial_steps = []
        if tutorial:
            # 如果tutorial包含数字编号的步骤，将其拆分
            if '(1)' in tutorial:
                steps = tutorial.split(';')
                tutorial = ''  # 清空原tutorial
                for step in steps:
                    step = step.strip()
                    if step:
                        # 移除数字编号
                        step = step.split(')', 1)[-1].strip()
                        tutorial_steps.append(step)
        
        # 准备工具数据
        tool_data = {
            'tool': {
                'name': tool['name'],
                'category': category_name,
                'description': tool['description'],
                'url': tool['url'],
                'evaluation': tool.get('evaluation', ''),
                'comparison': tool.get('comparison', ''),
                'tutorial': tutorial,
                'tutorial_steps': tutorial_steps,
                'free_alternatives': tool.get('free_alternatives', ''),
                # 根据不同类型的工具添加特定字段
                'features': tool.get('features', []),
                'code_examples': tool.get('code_examples', []),
                'supported_languages': tool.get('supported_languages', []),
                'integrations': tool.get('integrations', []),
                'pricing': tool.get('pricing', ''),
                # 图像工具特定字段
                'examples': tool.get('examples', []),
                'prompt_guide': tool.get('prompt_guide', {}),
                'style_options': tool.get('style_options', []),
                'supported_formats': tool.get('supported_formats', []),
                'max_resolution': tool.get('max_resolution', ''),
                'generation_speed': tool.get('generation_speed', '')
            }
        }
        
        # 生成页面
        output = template.render(**tool_data)
        
        # 创建文件名
        filename = tool['name'].lower().replace(' ', '-')
        
        # 保存文件
        output_path = os.path.join(output_dir, f'{filename}.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f'生成页面: {filename}.html')

print('所有工具页面生成完成！') 