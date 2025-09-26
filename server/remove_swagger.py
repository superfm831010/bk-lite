import os
import re

def remove_swagger_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    new_lines = []
    i = 0
    while i < len(lines):
        line = lines[i]
        
        # 移除 drf_yasg 导入
        if line.strip().startswith('from drf_yasg'):
            i += 1
            continue
            
        # 检查是否是 @swagger_auto_schema 装饰器的开始
        if '@swagger_auto_schema' in line:
            # 找到装饰器的结束位置
            if line.strip().endswith(')'):
                # 单行装饰器
                i += 1
                continue
            else:
                # 多行装饰器，需要找到结束的 )
                paren_count = line.count('(') - line.count(')')
                i += 1
                while i < len(lines) and paren_count > 0:
                    paren_count += lines[i].count('(') - lines[i].count(')')
                    i += 1
                continue
        
        # 移除注释的装饰器
        if line.strip().startswith('# @swagger_auto_schema'):
            i += 1
            continue
            
        new_lines.append(line)
        i += 1
    
    # 写回文件
    with open(file_path, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

# 处理所有Python文件
for root, dirs, files in os.walk('apps'):
    for file in files:
        if file.endswith('.py'):
            file_path = os.path.join(root, file)
            try:
                remove_swagger_from_file(file_path)
                print(f'Processed: {file_path}')
            except Exception as e:
                print(f'Error processing {file_path}: {e}')
