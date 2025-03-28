# AI 导航网站

这是一个展示和分类各种AI工具的导航网站。网站使用纯静态HTML构建，支持工具搜索、分类过滤等功能。

## 项目结构

```
ai-nav-site/
├── assets/          # 静态资源文件
│   └── css/         # CSS样式文件
├── scripts/         # Python脚本
│   └── generate_index.py  # 生成首页的脚本
├── templates/       # HTML模板
│   ├── index.html   # 首页模板
│   └── dev_tool.html # AI开发工具详情页模板
├── output/          # 生成的工具详情页
├── ai-tools-json.json  # AI工具数据
└── index.html       # 生成的首页
```

## 使用方法

1. 添加或修改工具：
   - 编辑 `ai-tools-json.json` 文件
   - 按照既定格式添加新的工具信息

2. 生成首页：
   ```bash
   cd ai-nav-site
   python scripts/generate_index.py
   ```

3. 本地预览：
   ```bash
   cd ai-nav-site
   python -m http.server 8000
   ```
   然后访问 http://localhost:8000

## 功能特点

- 工具分类展示
- 实时搜索过滤
- 分类标签筛选
- 访问量和评分统计
- 响应式布局设计

## 开发计划

- [ ] 添加更多工具分类
- [ ] 优化移动端体验
- [ ] 添加工具评论功能
- [ ] 集成更多工具数据来源 "# AI_NAV" 
