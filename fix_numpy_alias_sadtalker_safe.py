#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fix_numpy_alias_sadtalker_safe2.py - AST 安全修复 SadTalker 项目 numpy 过期别名
特点：
- 自动识别 numpy 导入别名 (np, npy, 等)
- dtype 参数使用 np.float64 / np.int64 / np.bool_ 等
- 类型注解或变量赋值使用 Python 原生类型
- 支持 dry-run 和文件备份
- 兼容多种文件编码，自动跳过不可读文件
用法:
    python fix_numpy_alias_sadtalker_safe2.py /path/to/SadTalker [--dry-run]
"""

import ast
import astor  # pip install astor
import os
import shutil
import sys
import chardet

# numpy 别名映射: (Python 原生类型, NumPy 标量类型)
REPLACE_MAP = {
    'float': ('float', 'np.float64'),
    'int': ('int', 'np.int64'),
    'bool': ('bool', 'np.bool_'),
    'complex': ('complex', 'np.complex128'),
    'object': ('object', 'np.object_'),
    'str': ('str', 'np.str_'),
}

BACKUP_SUFFIX = '.bak'

def backup_file(file_path):
    backup_path = file_path + BACKUP_SUFFIX
    shutil.copy2(file_path, backup_path)
    print(f"[备份] {file_path} -> {backup_path}")

def read_file_auto_encoding(file_path):
    """尝试自动检测编码读取文件"""
    try:
        with open(file_path, 'rb') as f:
            raw = f.read()
        result = chardet.detect(raw)
        encoding = result['encoding'] or 'utf-8'
        return raw.decode(encoding, errors='ignore')
    except Exception as e:
        print(f"[跳过] 无法读取 {file_path}: {e}")
        return None

class NumpyAliasTransformer(ast.NodeTransformer):
    def __init__(self, np_aliases):
        self.np_aliases = np_aliases
        super().__init__()

    def visit_Attribute(self, node):
        if isinstance(node.value, ast.Name) and node.value.id in self.np_aliases:
            alias_type = node.attr
            if alias_type in REPLACE_MAP:
                py_type, np_type = REPLACE_MAP[alias_type]

                # 判断是否在 dtype 参数中
                parent = getattr(node, 'parent', None)
                while parent:
                    if isinstance(parent, ast.keyword) and parent.arg == 'dtype':
                        return ast.parse(np_type, mode='eval').body
                    parent = getattr(parent, 'parent', None)

                return ast.parse(py_type, mode='eval').body
        return node

def add_parent_info(tree):
    """给每个节点加 parent 属性"""
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            setattr(child, 'parent', node)

def find_numpy_aliases(tree):
    aliases = set()
    for node in ast.walk(tree):
        # import numpy as np / import numpy as npy
        if isinstance(node, ast.Import):
            for n in node.names:
                if n.name == 'numpy':
                    aliases.add(n.asname or 'numpy')
        # from numpy import ... 保守处理
        if isinstance(node, ast.ImportFrom):
            if node.module == 'numpy':
                aliases.add('numpy')
    return aliases

def fix_file(file_path, dry_run=False):
    source = read_file_auto_encoding(file_path)
    if source is None:
        return  # 无法读取文件，跳过

    try:
        tree = ast.parse(source)
    except Exception as e:
        print(f"[跳过] 解析失败 {file_path}: {e}")
        return

    add_parent_info(tree)
    np_aliases = find_numpy_aliases(tree)

    if not np_aliases:
        return  # 文件中没有 numpy 导入

    transformer = NumpyAliasTransformer(np_aliases)
    new_tree = transformer.visit(tree)
    new_source = astor.to_source(new_tree)

    if new_source != source:
        if dry_run:
            print(f"\n[Dry Run] {file_path} 将被修改为:")
            print("-"*50)
            print(new_source)
            print("-"*50)
        else:
            backup_file(file_path)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_source)
            print(f"[修改] {file_path}")

def scan_dir(root_dir, dry_run=False):
    for root, dirs, files in os.walk(root_dir):
        for file in files:
            if file.endswith('.py'):
                fix_file(os.path.join(root, file), dry_run=dry_run)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python fix_numpy_alias_sadtalker_safe2.py /path/to/SadTalker [--dry-run]")
        sys.exit(1)

    project_path = sys.argv[1]
    dry_run = '--dry-run' in sys.argv

    if not os.path.isdir(project_path):
        print(f"目录不存在: {project_path}")
        sys.exit(1)

    scan_dir(project_path, dry_run=dry_run)
    print("修复完成！")
