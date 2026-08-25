"""
MapReduce-style word count for a single text file.

Features:
- Streams the file in configurable blocks to handle multi-GB inputs without loading everything into memory.
- Tokenizes words with English-style rules (字母数字，可含内部单引号)，统一转为小写计数。
- Writes output as Sta_<input_name>.txt sorted by frequency desc, then word asc.
- Records processing time for the single file.

Example:
    python wordcount_mapreduce.py input.txt --block-size-mb 8
"""

from __future__ import annotations

import argparse
import re
import time
from collections import Counter
from pathlib import Path
from typing import Counter as CounterType, Tuple

# 英文单词匹配：字母数字起始，可包含内部单引号（如 don't）
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:'[A-Za-z0-9]+)*")


def map_chunk(text: str) -> CounterType[str]:
    """Map step: find words in a chunk and count them (lowercased)."""
    counts: CounterType[str] = Counter()
    for match in WORD_RE.finditer(text):
        counts[match.group(0).lower()] += 1
    return counts


def reduce_counts(dest: CounterType[str], src: CounterType[str]) \
    -> CounterType[str]:
    """Reduce step: merge two Counters."""
    dest.update(src)
    return dest


def count_words_in_file(path: Path, block_size: int = 8 * 1024 * 1024) -> CounterType[str]:
    """
    按块流式读取文件，Map 每个块并 Reduce 合并计数。
    使用 leftover 缓冲处理块边界被截断的单词（依赖 WORD_RE 的匹配）。
    """
    counts: CounterType[str] = Counter()
    leftover = ""
    with path.open("r", encoding="utf-8", errors="ignore") as f:
        while True:
            chunk = f.read(block_size)
            if not chunk:
                break
            data = leftover + chunk
            leftover = ""
            is_full = len(chunk) == block_size
            # 在当前数据中查找单词；若满块且最后一个匹配恰好到末尾，则暂存为残留
            for match in WORD_RE.finditer(data):
                word = match.group(0)
                if is_full and match.end() == len(data):
                    leftover = word
                    break
                counts[word.lower()] += 1
    # 处理最后残留的单词
    if leftover:
        counts[leftover.lower()] += 1

    return counts


def write_counts(counts: CounterType[str], output_path: Path) -> None:
    sorted_items = sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as f:
        for word, freq in sorted_items:
            f.write(f"{word}\t{freq}\n")


def process_file(input_path: Path, output_path: Path, block_size: int) \
    -> Tuple[Path, Path, float, int, int]:
    start = time.perf_counter()
    counts = count_words_in_file(input_path, block_size=block_size)
    elapsed = time.perf_counter() - start

    write_counts(counts, output_path)
    total_terms = sum(counts.values())
    unique_terms = len(counts)
    return input_path, output_path, elapsed, total_terms, unique_terms


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="MapReduce-style word count for a single text file.")
    parser.add_argument("input_file", help="Path to the input text file.")
    parser.add_argument(
        "--output",
        default=None,
        help="Path to the output file (default: Sta_<input_name>.txt in the input file directory).",
    )
    parser.add_argument("--block-size-mb", type=int, default=8, help="Read size per chunk in MB (default: 8).")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_path = Path(args.input_file).resolve()
    if not input_path.is_file():
        raise FileNotFoundError(f"Input file not found: {input_path}")

    output_path = Path(args.output).resolve() if args.output else input_path.with_name(f"Sta_{input_path.name}")
    block_size = max(args.block_size_mb, 1) * 1024 * 1024

    print(f"Input file: {input_path}")
    print(f"Output file: {output_path}")
    print(f"Block size: {block_size // (1024 * 1024)} MB")

    total_start = time.perf_counter()
    input_path, output_path, elapsed, total_terms, \
        unique_terms = process_file(input_path, output_path, block_size)
    total_elapsed = time.perf_counter() - total_start

    print(f"{input_path.name}: {elapsed:.2f}s | tokens={total_terms} | unique={unique_terms} -> {output_path.name}")
    print(f"Total time: {total_elapsed:.2f}s for 1 file")


if __name__ == "__main__":
    main()
