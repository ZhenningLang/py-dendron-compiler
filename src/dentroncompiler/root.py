from pathlib import Path

from dentroncompiler.node import FileNode
from dentroncompiler.template import load_template_by_name


def _build_tree_html(node: FileNode) -> str:
    # 定义层级颜色，使用柔和的色调，从深到浅的渐变
    depth_colors = [
        "#2c3e50",  # 深蓝灰
        "#e74c3c",  # 鲜红
        "#27ae60",  # 翠绿
        "#8e44ad",  # 紫色
        "#f39c12",  # 橙色
        "#16a085",  # 青绿
    ]
    
    html = "<ul>"
    # Add root node first
    if node.title == "root":
        root_title = '首页'
        html += "<li>"
        if node.relative_to_root_path:
            html += f"<a href='{node.relative_to_root_path}' style='color: {depth_colors[0]}'>{root_title}</a>"
        else:
            html += f'<span class="no-link" style="color: {depth_colors[0]}">{root_title}</span>'
        
    # Then add children
    if node.children:
        html += "<ul>"
        for child in node.children:
            # 获取当前节点的深度对应的颜色，超过预设颜色数量则使用最后一个颜色
            color_index = min(child.depth, len(depth_colors) - 1)
            current_color = depth_colors[color_index]
            
            html += "<li>"
            if child.relative_to_root_path:
                file_type = "📄" if child.metadata.get('gramma', 'markdown') == 'markdown' else "🧠"
                html += f"<a href='{child.relative_to_root_path}' style='color: {current_color}'>{child.title}</a><span class='file-type-icon'>{file_type}</span>"
            else:
                html += f'<span class="no-link" style="color: {current_color}">{child.title}</span>'
            if child.children:
                html += _build_tree_html(child)
            html += "</li>"
        html += "</ul>"
    
    html += "</li></ul>"
    return html


def build_root_to_html(root: FileNode, output_dir: Path):
    # 生成树状结构HTML
    tree_html = _build_tree_html(root)
    
    # 渲染模板
    template = load_template_by_name("root")
    html_content = template.render(tree_html=tree_html)
    
    # 写入文件
    with open(output_dir / "index.html", 'w', encoding='utf-8') as f:
        f.write(html_content)
