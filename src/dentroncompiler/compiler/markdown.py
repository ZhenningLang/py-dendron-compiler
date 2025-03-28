from typing import Dict
import markdown


class MarkdownCompiler:
    
    def compile(self, 
                content: str,
                metadata: Dict, 
                content_without_meta: str) -> str:
        css = """
        <style>
        blockquote {
            border-left: 4px solid #ccc;
            margin: 1.5em 10px;
            padding: 0.5em 10px;
            background-color: #f9f9f9;
            color: #666;
        }
        img {
            max-width: 600px;
            height: auto;
        }
        </style>
        """
        html = markdown.markdown(content_without_meta)
        return css + html
