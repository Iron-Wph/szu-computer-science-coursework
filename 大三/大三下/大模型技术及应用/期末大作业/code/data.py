import json
import os
from typing import List, Dict, Any

def process_jsonl_file(file_path: str) -> List[Dict[str, str]]:
    """处理单个JSONL文件，提取question和answer字段"""
    processed_data = []


    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            try:
                # 解析JSON对象
                json_obj = json.loads(line.strip())
                # 提取question和answer字段
                for key, value in json_obj.items():
                    question = value.get('question', '')
                    answer = value.get('answer', '')
                    # 构造新的JSON对象
                    processed_data.append({
                        "instruction": question,
                        "output": answer
                    })
            except json.JSONDecodeError:
                print(f"Error decoding line in {file_path}: {line[:50]}...")
            except Exception as e:
                print(f"Unexpected error processing {file_path}: {e}")

    return processed_data

def merge_jsonl_files(input_dir: str, output_file: str, overwrite: bool = False) -> None:
    """合并目录下所有JSONL文件到一个输出文件"""
    # 检查输出文件是否存在
    if not overwrite and os.path.exists(output_file):
        raise FileExistsError(f"Output file {output_file} already exists. Use overwrite=True to overwrite.")
    
    all_data = []
    
    # 遍历目录中的所有文件
    for filename in os.listdir(input_dir):
        if filename.endswith('.jsonl'):
            file_path = os.path.join(input_dir, filename)
            print(f"Processing {file_path}...")
            file_data = process_jsonl_file(file_path)
            all_data.extend(file_data)
    
    # 写入合并后的JSONL文件
    with open(output_file, 'w', encoding='utf-8') as f:
        for item in all_data:
            f.write(json.dumps(item, ensure_ascii=False) + ',\n')
    
    print(f"Merged {len(all_data)} entries into {output_file}")

if __name__ == "__main__":
    # 配置参数
    INPUT_DIR = "./datas"  # 输入目录路径
    OUTPUT_FILE = "./output.json"  # 输出文件路径
    OVERWRITE = True  # 是否覆盖已存在的输出文件
    
    # 执行合并
    merge_jsonl_files(INPUT_DIR, OUTPUT_FILE, OVERWRITE)