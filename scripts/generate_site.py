import json
import os
import sys
import shutil
from jinja2 import Environment, FileSystemLoader
from typing import Dict, List, Set

class SiteGenerator:
    def __init__(self):
        # 获取项目根目录
        self.project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        # 配置路径
        self.json_path = os.path.join(self.project_root, 'ai-tools-json.json')
        self.output_dir = os.path.join(self.project_root, 'output')
        self.tool_output_dir = os.path.join(self.output_dir, 'tool')
        self.category_output_dir = os.path.join(self.output_dir, 'category')
        self.template_dir = os.path.join(self.project_root, 'templates')
        self.assets_dir = os.path.join(self.project_root, 'assets')
        
        # 确保输出目录存在
        os.makedirs(self.tool_output_dir, exist_ok=True)
        os.makedirs(self.category_output_dir, exist_ok=True)
        os.makedirs(os.path.join(self.output_dir, 'assets'), exist_ok=True)
        
        # 配置Jinja2环境
        self.env = Environment(loader=FileSystemLoader(self.template_dir))
        
        # 添加自定义过滤器
        self.env.filters['fix_asset_path'] = self.fix_asset_path
        
        # 模板映射
        self.template_mapping = {
            'AI-Assisted Development & Code Generation': 'dev_tool.html',
            'AI Image Generation': 'image_tool.html',
            'Web Deployment & Hosting': 'base.html',
            'Domain Registration & Management': 'base.html',
            'SEO & Traffic Analysis': 'base.html',
            'Game Development & Resources': 'base.html',
            'Keyword Research & Market Analysis': 'base.html'
        }

        # 分类组映射
        self.category_groups = [
            {
                'name': 'Development & Code',
                'categories': [
                    'AI-Assisted Development & Code Generation',
                    'Web Deployment & Hosting',
                    'Game Development & Resources'
                ]
            },
            {
                'name': 'Domain & SEO',
                'categories': [
                    'Domain Registration & Management',
                    'SEO & Traffic Analysis',
                    'Keyword Research & Market Analysis'
                ]
            },
            {
                'name': 'AI & Creative',
                'categories': [
                    'AI Image Generation'
                ]
            }
        ]

    def fix_asset_path(self, path: str) -> str:
        """修复资源文件路径"""
        if path.startswith('/assets/'):
            return '../../assets' + path[7:]
        return path

    def copy_assets(self):
        """复制静态资源文件"""
        output_assets_dir = os.path.join(self.output_dir, 'assets')
        if os.path.exists(output_assets_dir):
            shutil.rmtree(output_assets_dir)
        shutil.copytree(self.assets_dir, output_assets_dir)
        print('静态资源复制完成！')

    def load_json_data(self) -> dict:
        """加载JSON数据"""
        try:
            with open(self.json_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading JSON file: {e}")
            sys.exit(1)

    def get_existing_tools(self) -> Set[str]:
        """获取已存在的工具页面"""
        existing_tools = set()
        if os.path.exists(self.tool_output_dir):
            for filename in os.listdir(self.tool_output_dir):
                if filename.endswith('.html'):
                    existing_tools.add(filename[:-5])  # 移除.html后缀
        return existing_tools

    def process_tutorial(self, tutorial: str) -> tuple:
        """处理教程文本，分离步骤"""
        tutorial_steps = []
        if tutorial and '(1)' in tutorial:
            steps = tutorial.split(';')
            tutorial = ''  # 清空原tutorial
            for step in steps:
                step = step.strip()
                if step:
                    # 移除数字编号
                    step = step.split(')', 1)[-1].strip()
                    tutorial_steps.append(step)
        return tutorial, tutorial_steps

    def prepare_tool_data(self, tool: dict, category_name: str) -> dict:
        """准备工具数据"""
        # 处理教程步骤
        tutorial, tutorial_steps = self.process_tutorial(tool.get('tutorial', ''))
        
        return {
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
                'features': tool.get('features', []),
                'code_examples': tool.get('code_examples', []),
                'supported_languages': tool.get('supported_languages', []),
                'integrations': tool.get('integrations', []),
                'pricing': tool.get('pricing', ''),
                'examples': tool.get('examples', []),
                'prompt_guide': tool.get('prompt_guide', {}),
                'style_options': tool.get('style_options', []),
                'supported_formats': tool.get('supported_formats', []),
                'max_resolution': tool.get('max_resolution', ''),
                'generation_speed': tool.get('generation_speed', '')
            }
        }

    def generate_tool_page(self, tool: dict, category_name: str):
        """生成工具详情页"""
        template_name = self.template_mapping.get(category_name, 'base.html')
        template = self.env.get_template(template_name)
        
        # 准备数据
        tool_data = self.prepare_tool_data(tool, category_name)
        
        # 生成页面
        output = template.render(**tool_data)
        
        # 创建文件名
        filename = tool['name'].lower().replace(' ', '-')
        output_path = os.path.join(self.tool_output_dir, f'{filename}.html')
        
        # 保存文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f'生成页面: {filename}.html')

    def generate_category_page(self, category: dict):
        """生成分类详情页"""
        template = self.env.get_template('category_detail.html')
        
        # 准备数据
        category_data = {
            'category': {
                'name': category['name'],
                'description': category['description'],
                'tools': category['tools'],
                'total_monthly_visitors': sum(
                    int(tool.get('monthly_visitors', 0)) 
                    for tool in category['tools']
                )
            }
        }
        
        # 生成页面
        output = template.render(**category_data)
        
        # 创建文件名
        filename = category['name'].lower().replace(' ', '-')
        output_path = os.path.join(self.category_output_dir, f'{filename}.html')
        
        # 保存文件
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output)
        print(f'生成分类页面: {filename}.html')

    def generate_categories_page(self, data: dict):
        """生成分类列表页面"""
        template = self.env.get_template('categories.html')
        
        # 准备数据
        categories_data = self.prepare_category_data(data['categories'])
        
        # 生成页面
        output = template.render(**categories_data)
        
        # 保存文件
        output_path = os.path.join(self.project_root, 'categories.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output)
        print('分类页面生成完成！')

    def generate_index(self, data: dict):
        """生成首页"""
        template = self.env.get_template('index.html')
        output = template.render(categories=data['categories'])
        
        output_path = os.path.join(self.project_root, 'index.html')
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(output)
        print('首页生成完成！')

    def cleanup_removed_tools(self, current_tools: Set[str], existing_tools: Set[str]):
        """清理已删除的工具页面"""
        removed_tools = existing_tools - current_tools
        for tool_name in removed_tools:
            file_path = os.path.join(self.tool_output_dir, f'{tool_name}.html')
            try:
                os.remove(file_path)
                print(f'删除页面: {tool_name}.html')
            except Exception as e:
                print(f"Error deleting {tool_name}.html: {e}")

    def update_template_mapping(self, categories: list):
        """更新模板映射，处理新的分类"""
        # 获取当前所有分类名称
        current_categories = set(cat['name'] for cat in categories if cat['tools'])
        mapped_categories = set(self.template_mapping.keys())
        
        # 添加新分类
        new_categories = current_categories - mapped_categories
        for category in new_categories:
            self.template_mapping[category] = 'base.html'
            print(f'添加新分类: {category}')
        
        # 删除空分类
        empty_categories = mapped_categories - current_categories
        for category in empty_categories:
            del self.template_mapping[category]
            print(f'删除空分类: {category}')

    def clean_empty_categories(self, data: dict) -> dict:
        """清理没有工具的分类"""
        data['categories'] = [cat for cat in data['categories'] if cat['tools']]
        return data

    def prepare_category_data(self, categories: List[dict]) -> dict:
        """准备分类页面数据"""
        # 计算每个分类的统计信息
        for category in categories:
            category['total_monthly_visitors'] = sum(
                int(tool.get('monthly_visitors', 0)) 
                for tool in category['tools']
            )
            # 添加分类描述
            category['description'] = f"Explore {len(category['tools'])} AI tools in the {category['name']} category."

        # 按组织分类
        category_groups = []
        for group in self.category_groups:
            group_categories = []
            for cat_name in group['categories']:
                for category in categories:
                    if category['name'] == cat_name:
                        group_categories.append(category)
                        break
            if group_categories:
                category_groups.append({
                    'name': group['name'],
                    'categories': group_categories
                })

        return {
            'category_groups': category_groups,
            'total_categories': len(categories)
        }

    def generate_site(self):
        """生成整个站点"""
        # 加载数据
        data = self.load_json_data()
        
        # 清理空分类
        data = self.clean_empty_categories(data)
        
        # 更新模板映射
        self.update_template_mapping(data['categories'])
        
        # 获取现有工具页面
        existing_tools = self.get_existing_tools()
        
        # 记录当前工具
        current_tools = set()
        
        # 生成工具页面
        for category in data['categories']:
            category_name = category['name']
            # 生成分类详情页
            self.generate_category_page(category)
            # 生成工具页面
            for tool in category['tools']:
                tool_name = tool['name'].lower().replace(' ', '-')
                current_tools.add(tool_name)
                self.generate_tool_page(tool, category_name)
        
        # 清理已删除的页面
        self.cleanup_removed_tools(current_tools, existing_tools)
        
        # 生成分类列表页面
        self.generate_categories_page(data)
        
        # 生成首页
        self.generate_index(data)
        
        # 复制静态资源
        self.copy_assets()
        
        print('站点生成完成！')

if __name__ == '__main__':
    generator = SiteGenerator()
    generator.generate_site() 