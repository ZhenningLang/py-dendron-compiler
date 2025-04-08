from typing import Dict
import markdown
import re


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
        /* Add styling for code blocks */
        pre {
            background-color: #f5f5f5;
            padding: 10px;
            border-radius: 4px;
            overflow-x: auto;
        }
        code {
            font-family: monospace;
        }
        /* Add styling for tables */
        table {
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
        }
        </style>
        """
        
        # Fix table formatting
        content_processed = self._fix_table_formatting(content_without_meta)
        
        # Enable extensions for code blocks (fenced_code) and tables
        html = markdown.markdown(
            content_processed,
            extensions=[
                'markdown.extensions.fenced_code',
                'markdown.extensions.tables',
                'markdown.extensions.codehilite',
                'markdown.extensions.nl2br'  # Convert newlines to <br> tags
            ]
        )
        return css + html
        
    def _fix_table_formatting(self, content):
        """Ensure tables are properly formatted for Python-Markdown."""
        lines = content.split('\n')
        result = []
        in_table = False
        missing_header = False
        
        for i, line in enumerate(lines):
            # Check if this line might be the start of a table
            if re.match(r'^\|.*\|$', line.strip()):
                # Check if we're starting a new table
                if not in_table:
                    in_table = True
                    # Look if next line contains delimiter row (|---|---|)
                    if i+1 < len(lines) and re.match(r'^\|[\s*:?-]+\|.*$', lines[i+1].strip()):
                        # This is a proper table, add empty line before
                        result.append('')
                        result.append(line)
                    else:
                        # Table is missing header row, insert one
                        missing_header = True
                        cols = line.count('|') - 1
                        # Insert header row with proper number of columns
                        result.append('')
                        header = '|' + '|'.join(['Header' for _ in range(cols)]) + '|'
                        result.append(header)
                        result.append('|' + '|'.join(['---' for _ in range(cols)]) + '|')
                        result.append(line)
                else:
                    result.append(line)
            else:
                # Check if we're exiting a table
                if in_table and not line.strip().startswith('|'):
                    in_table = False
                    missing_header = False
                    result.append('')  # Add empty line after table
                result.append(line)
                
        return '\n'.join(result)