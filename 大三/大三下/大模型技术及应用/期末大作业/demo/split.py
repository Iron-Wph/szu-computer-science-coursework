import re

def split_markdown_by_heading(input_file_path: str):
    """
    将 Markdown 文件按一级标题（# 开头）分割为多个独立文件。
    :param input_file_path: 原始 Markdown 文件路径
    """
    # 1. 读取原始文件内容
    with open(input_file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 2. 按一级标题分割内容（正则匹配 ^# 开头的行，保留分隔符）
    #    re.MULTILINE 使 ^ 匹配每行开头，re.DOTALL 使 . 匹配换行
    parts = re.split(r'(^# \S+)', content, flags=re.MULTILINE | re.DOTALL)
    
    # 3. 处理分割后的块（标题 + 内容）
    blocks = []
    # 处理「标题前的前置内容」（若存在）
    if parts[0].strip():
        blocks.append(("前言", parts[0].strip()))
    # 处理「标题 + 内容」对（parts 结构：['前置内容', '# 标题1', '内容1', '# 标题2', '内容2'...]）
    for i in range(1, len(parts), 2):
        heading = parts[i].strip()       # 提取标题（如 "# 复习思考题"）
        text = parts[i+1].strip() if (i+1 < len(parts)) else ""  # 提取标题下的内容
        blocks.append((heading, text))
    
    # 4. 为每个块生成独立文件
    for idx, (heading, text) in enumerate(blocks):
        # 提取标题名（去掉 # 和前后空格）
        title = heading.lstrip("# ").strip()
        # 处理文件名（避免特殊字符，如替换 / \ : 等，这里简单示例用标题名）
        filename = f"./files/{title}.txt"
        # 写入内容（保留原标题格式 + 内容）
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(heading + "\n\n" + text + "\n")  # 标题与内容间加空行分隔
    
    print(f"✅ 成功分割！原始文件包含 {len(blocks)} 个块（含前置内容），已生成 {len(blocks)} 个新文件。")


# ------------------- 调用示例 -------------------
if __name__ == "__main__":
    input_file = "markdown.txt"  # 替换为你的 Markdown 文件路径
    split_markdown_by_heading(input_file)