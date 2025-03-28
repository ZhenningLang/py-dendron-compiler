from pathlib import Path
from typing import Dict, List


class FileNode:
    
    MAX_ORDER: int = 99999
    
    def __init__(self, *, 
                 file_path: Path, 
                 title: str, 
                 order: int = MAX_ORDER,
                 metadata: Dict = None):
        self.depth: int = 0
        self.file_path: Path = file_path
        self.relative_to_root_path: str = None
        self.title: str = title
        self.order: int = order
        self.children: List[FileNode] = []
        self.metadata: Dict = metadata if metadata is not None else {}
    