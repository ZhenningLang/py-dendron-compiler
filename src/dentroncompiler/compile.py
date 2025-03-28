import logging
import os
import re
import shutil
from pathlib import Path
from typing import Dict, List

import yaml
from dentroncompiler.compiler import MarkdownCompiler, MarkmapCompiler
from dentroncompiler.node import FileNode
from dentroncompiler.root import build_root_to_html


def parse_meta(content: str):
    # 替换跳转链接
    pattern = r'(\[\[(.*?)\]\])'
    found = re.findall(pattern, content)
    for item in found:
        link = item[0]
        link_name = item[1]
        content = content.replace(link, f"[{link_name}](./{link_name}.html)")
    
    # 替换图片链接
    pattern = r'(\!\[(.*?)\]\((.*?)\))'
    found = re.findall(pattern, content)
    for item in found:
        img = item[0]
        alt = item[1]
        link = item[2]
        if not link:
            continue
        if link.startswith("http"):
            continue
        new_img = f'![{alt}](../{link})'
        content = content.replace(img, new_img)
    
    # 提取 meta 信息
    pattern = r"^---\n(.*?)\n---\n(.*)"
    match = re.match(pattern, content, re.DOTALL)
    if match:
        try:
            metadata = yaml.safe_load(match.group(1))
            conent_without_meta = match.group(2)
            return content, metadata or {}, conent_without_meta
        except yaml.YAMLError:
            logging.error("Failed to parse YAML metadata.")
            return content, {}, content
    return content, {}, content


def build_tree(files: List[Path]) -> FileNode:
    root = FileNode(file_path=None, title="root")
    root.relative_to_root_path = './'
    root.depth = 0  # Root node has depth 0
    nodes: Dict[str, FileNode] = {"root": root}
    
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            _, metadata, _ = parse_meta(content)
        
        parts = file.stem.split('.')
        current_path = []
        
        for i, part in enumerate(parts):
            current_path.append(part)
            node_key = '.'.join(current_path)
            parent_key = '.'.join(current_path[:-1]) or "root"
            is_last_part = i == len(parts) - 1
            
            if node_key not in nodes:
                node = FileNode(
                    file_path=file if is_last_part else None,
                    title=part,
                    order=metadata.get('order', 0) if is_last_part else 0,
                    metadata=metadata if is_last_part else None
                )
                node.depth = len(current_path)  # Set depth based on path length
                nodes[node_key] = node
                nodes[parent_key].children.append(node)
            elif is_last_part:
                node = nodes[node_key]
                node.file_path = file
                node.title = part
                node.order = metadata.get('order', FileNode.MAX_ORDER)
                node.metadata = metadata
                node.depth = len(current_path)  # Update depth for existing node
    
    # Sort children by order and then by title
    for node in nodes.values():
        node.children.sort(key=lambda x: (x.order, x.title))
    
    return root


def compile_files(root: FileNode, output_dir: Path):
    compilers = {
        'markmap': MarkmapCompiler(),
        'markdown': MarkdownCompiler()
    }
    
    def process_node(node: FileNode, current_dir: Path):
        if node.file_path:
            with open(node.file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                content, metadata, content_without_meta = parse_meta(content)
            
            compiler_type = metadata.get('gramma', 'markdown')
            compiler = compilers.get(compiler_type, MarkdownCompiler())
            html_content = compiler.compile(content, metadata, content_without_meta)
            
            output_path = current_dir / f"{node.file_path.stem}.html"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            node.relative_to_root_path = str(output_path.relative_to(output_dir))
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            logging.info(f"Compiled {node.file_path} to {output_path}")
        
        for child in node.children:
            process_node(child, current_dir)
    
    output_dir.mkdir(parents=True, exist_ok=True)
    process_node(root, output_dir)
    build_root_to_html(root, output_dir)


def run(dendron_repo: str, *, force_delete: bool = False):
    repo_path = Path(dendron_repo)
    if not repo_path.exists():
        raise ValueError(f"Repository path does not exist: {dendron_repo}")
    
    md_files = list(repo_path.rglob("*.md"))
    root = build_tree(md_files)
    
    output_dir = repo_path / "dist"
    if output_dir.exists():
        if not force_delete:
            delete = input(f"Output directory '{output_dir}' already exists. Do you want to delete it? (y/n): ").strip().lower()
            if delete == 'n':
                logging.info("Exiting without deleting the output directory.")
                return
            elif delete != 'y':
                logging.info("Invalid input. Exiting without deleting the output directory.")
                return
        shutil.rmtree(output_dir)
        logging.info(f"Deleting old dist directory: {output_dir}")
    
    os.mkdir(output_dir)
    logging.info(f"Creating dist directory: {output_dir}")
    compile_files(root, output_dir)


def get_dendron_repo_path_from_args():
    import sys
    if len(sys.argv) != 2:
        print("Usage: python compile.py <dendron-repository>")
        sys.exit(1)
    
    return sys.argv[1]


def setup_logging():
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.getLogger().setLevel(logging.INFO)


def main():
    setup_logging()
    path = get_dendron_repo_path_from_args()
    logging.info(f"Compiling Dendron repository at {path}")
    run(path)


if __name__ == "__main__":
    main()
