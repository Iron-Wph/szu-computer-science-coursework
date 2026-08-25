#!/usr/bin/env python3
"""
配置测试脚本
用于检查环境变量和RAG系统是否正确配置
"""

import os
import sys
from dotenv import load_dotenv

# 加载环境变量
load_dotenv(os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '.env'))

def test_env_variables():
    """测试环境变量配置"""
    print("=== 环境变量测试 ===")
    
    required_vars = [
        'DASHSCOPE_API_KEY',
        'DASHSCOPE_API_BASE', 
        'DASHSCOPE_MODEL',
        'DASHSCOPE_EMBEDDING_MODEL'
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if value:
            print(f"✓ {var}: {value[:10]}..." if len(value) > 10 else f"✓ {var}: {value}")
        else:
            print(f"✗ {var}: 未设置")
            missing_vars.append(var)
    
    if missing_vars:
        print(f"\n❌ 缺少必要的环境变量: {', '.join(missing_vars)}")
        print("请在项目根目录创建 .env 文件并配置相应的API密钥")
        return False
    else:
        print("\n✅ 所有环境变量配置正确")
        return True

def test_rag_system():
    """测试RAG系统初始化"""
    print("\n=== RAG系统测试 ===")
    
    try:
        # 添加父目录到路径
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        from utils.retrieval_qa import RetrievalQA
        from utils.document_processor import DocumentProcessor
        
        print("✓ 成功导入RAG模块")
        
        # 测试DocumentProcessor
        doc_processor = DocumentProcessor()
        print("✓ DocumentProcessor初始化成功")
        
        # 测试RetrievalQA
        qa_system = RetrievalQA()
        print("✓ RetrievalQA初始化成功")
        
        # 测试简单问答
        test_question = "你好"
        try:
            result = qa_system.invoke(test_question)
            print(f"✓ RAG系统问答测试成功")
            return True
        except Exception as e:
            print(f"✗ RAG系统问答测试失败: {str(e)}")
            return False
            
    except ImportError as e:
        print(f"✗ 导入RAG模块失败: {str(e)}")
        return False
    except Exception as e:
        print(f"✗ RAG系统初始化失败: {str(e)}")
        return False

def main():
    """主函数"""
    print("AI聊天系统配置测试")
    print("=" * 50)
    
    # 测试环境变量
    env_ok = test_env_variables()
    
    # 测试RAG系统
    rag_ok = test_rag_system()
    
    print("\n" + "=" * 50)
    if env_ok and rag_ok:
        print("✅ 所有测试通过！系统配置正确")
        print("可以启动前端服务: python app.py")
    else:
        print("❌ 配置存在问题，请检查上述错误信息")
        if not env_ok:
            print("\n解决方案:")
            print("1. 在项目根目录创建 .env 文件")
            print("2. 配置阿里云百炼API密钥")
            print("3. 参考 config_setup.md 文件")

if __name__ == "__main__":
    main() 