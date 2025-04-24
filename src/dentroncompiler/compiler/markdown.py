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
        /* Add styling for lists */
        ul, ol {
            margin-left: 20px;
        }
        ul ul, ol ol, ul ol, ol ul {
            margin-top: 5px;
            margin-bottom: 5px;
        }
        </style>
        """
        
        # Preprocess content
        content_processed = self._preprocess_content(content_without_meta)
        
        # Enable extensions for code blocks (fenced_code) and tables
        html = markdown.markdown(
            content_processed,
            extensions=[
                'markdown.extensions.fenced_code',
                'markdown.extensions.tables',
                'markdown.extensions.codehilite',
                'markdown.extensions.nl2br',  # Convert newlines to <br> tags
                'markdown.extensions.sane_lists'  # Better list handling
            ]
        )
        return css + html
    
    def _preprocess_content(self, content):
        """Preprocess markdown content to ensure proper formatting."""
        # First fix table formatting
        processed = self._fix_table_formatting(content)
        
        # Then fix list formatting
        processed = self._fix_list_formatting(processed)
        
        return processed
        
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
    
    def _fix_list_formatting(self, content):
        """Ensure lists are properly formatted for Python-Markdown."""
        lines = content.split('\n')
        result = []
        
        in_list = False
        # Improved regex to better match list items
        list_indent_pattern = re.compile(r'^(\s*)([\*\-\+]|\d+\.)\s+(.*)')
        
        for i, line in enumerate(lines):
            # Check for list items
            list_match = list_indent_pattern.match(line)
            
            if list_match:
                # This is a list item
                indent, marker, text = list_match.groups()
                
                if not in_list:
                    # Starting a new list - add empty line before if needed
                    if i > 0 and result and result[-1].strip():
                        result.append('')
                    in_list = True
                
                # Check if we need to preserve indentation for nested list items
                indent_level = len(indent) // 2  # Convert 2-space indents to levels
                
                # Create properly formatted list item with 4 spaces per level
                formatted_line = "    " * indent_level + marker + " " + text
                result.append(formatted_line)
            else:
                # Check if this is a continuation of a list item (indented content)
                if in_list and line.strip() and line.startswith('  '):
                    # Find the indentation level
                    spaces_count = 0
                    for char in line:
                        if char == ' ':
                            spaces_count += 1
                        else:
                            break
                    
                    # Calculate the proper indentation level (in multiples of 4 spaces)
                    indent_level = (spaces_count // 2) + 1  # +1 because it's continuation text
                    formatted_line = "    " * indent_level + line.strip()
                    result.append(formatted_line)
                else:
                    # Not a list item
                    if in_list and line.strip():
                        # End of list - add empty line if moving to non-empty content
                        result.append('')
                        in_list = False
                    
                    # Add the line
                    result.append(line)
        
        # Make sure the content ends with a newline
        if result and result[-1].strip():
            result.append('')
            
        return '\n'.join(result)
