import re
import os
import sys
def fix_katex_error(katex_code, error_message):
    """
    修复KaTeX解析错误
    
    参数:
    katex_code (str): 包含KaTeX数学公式的代码
    error_message (str): KaTeX抛出的错误信息
    
    返回:
    str: 修复后的KaTeX代码
    """
    # 从错误信息中提取位置
    position_match = re.search(r'position (\d+):', error_message)
    if not position_match:
        print("无法从错误信息中提取位置信息")
        return katex_code
    
    error_position = int(position_match.group(1))
    
    # 检查错误类型
    if "Unexpected end of input in a macro argument, expected '}'" in error_message:
        # 处理缺少右花括号的情况
        return katex_code[:error_position] + '}' + katex_code[error_position:]
    
    elif "Unexpected character:" in error_message:
        # 处理意外字符
        return katex_code[:error_position] + katex_code[error_position+1:]
    
    elif "Double subscript" in error_message:
        # 处理双下标错误
        return katex_code[:error_position] + '{' + katex_code[error_position:]
    
    else:
        print(f"未知错误类型: {error_message}")
        return katex_code

def extract_katex_formulas(md_content):
    """从Markdown内容中提取所有KaTeX公式"""
    # 匹配行内公式 $...$
    inline_pattern = r'\$(.+?)\$'
    # 匹配块级公式 $$...$$
    block_pattern = r'\$\$(.+?)\$\$'
    
    formulas = []
    # 提取行内公式
    for match in re.finditer(inline_pattern, md_content):
        formulas.append((match.group(0), match.start(), match.end()))
    
    # 提取块级公式
    for match in re.finditer(block_pattern, md_content):
        formulas.append((match.group(0), match.start(), match.end()))
    
    return formulas

def process_markdown_file(input_file, error_log_file):
    """处理Markdown文件并修复KaTeX错误"""
    # 读取Markdown文件内容
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            md_content = f.read()
    except FileNotFoundError:
        print(f"错误：找不到文件 {input_file}")
        return
    
    # 读取错误日志文件
    try:
        with open(error_log_file, 'r', encoding='utf-8') as f:
            error_log = f.read()
    except FileNotFoundError:
        print(f"错误：找不到错误日志文件 {error_log_file}")
        return
    
    # 提取所有KaTeX公式
    formulas = extract_katex_formulas(md_content)
    
    # 修复错误
    for formula_text, start, end in formulas:
        # 检查错误日志中是否有此公式的错误
        if formula_text in error_log:
            # 提取与此公式相关的错误信息
            formula_errors = []
            lines = error_log.split('\n')
            for line in lines:
                if formula_text in line:
                    formula_errors.append(line)
            
            # 修复每个错误
            for error_msg in formula_errors:
                fixed_formula = fix_katex_error(formula_text, error_msg)
                # 替换Markdown内容中的公式
                md_content = md_content[:start] + fixed_formula + md_content[end:]
                print(f"已修复公式: {formula_text[:30]}...")
    
    # 写入修复后的文件
    output_file = os.path.splitext(input_file)[0] + '_fixed.md'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(md_content)
    
    print(f"修复完成，已保存到 {output_file}")

if __name__ == "__main__":
    # 设置Markdown文件路径和错误日志路径
    MARKDOWN_FILE = "D:\\作业\\大三下\\大模型技术及应用\\期末大作业\\demo\\extracted_files_29f1c480-16c0-4670-a7e2-ef5124df31cf\\full.md"  # 请修改为你的Markdown文件路径
    ERROR_LOG_FILE = "errors.log"  # 请修改为你的错误日志文件路径
    
    # 检查文件是否存在
    if not os.path.exists(MARKDOWN_FILE):
        print(f"错误：Markdown文件 {MARKDOWN_FILE} 不存在")
        sys.exit(1)
    
    if not os.path.exists(ERROR_LOG_FILE):
        print(f"错误：错误日志文件 {ERROR_LOG_FILE} 不存在")
        sys.exit(1)
    
    # 处理文件
    process_markdown_file(MARKDOWN_FILE, ERROR_LOG_FILE)