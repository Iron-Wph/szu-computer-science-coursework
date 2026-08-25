import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import time
import re
from typing import List, Set, Dict
import os
from datetime import datetime

class WebCrawler:
    def __init__(self, base_url: str, output_dir: str = "../documents/crawled_docs"):
        """
        初始化爬虫
        :param base_url: 要爬取的网站根URL
        :param output_dir: 输出目录
        """
        self.base_url = base_url
        self.domain = urlparse(base_url).netloc
        self.visited_urls: Set[str] = set()
        self.output_dir = output_dir
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0'
        }
        
        # 创建输出目录
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def is_valid_url(self, url: str) -> bool:
        try:
            parsed = urlparse(url)
            return bool(parsed.netloc) and parsed.netloc.lower() == self.domain.lower()
        except:
            return False

    def get_page_content(self, url: str) -> str:
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            content_type = response.headers.get('Content-Type', '')
            if 'text/html' not in content_type:
                print(f"跳过非 HTML 资源: {url} (Content-Type: {content_type})")
                return ""
            
            return response.text
        except Exception as e:
            print(f"获取页面 {url} 失败: {str(e)}")
            return ""

    def extract_links(self, html: str, base_url: str) -> List[str]:
        """
        提取页面中的所有链接
        """
        soup = BeautifulSoup(html, 'html.parser')
        links = []
        
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(base_url, href)
            if self.is_valid_url(full_url):
                links.append(full_url)
                # print(f"提取到的链接: {full_url}")
        
        # print(f"提取到的链接: {links}")
        return list(set(links))  # 去重

    def clean_text(self, text: str) -> str:
        """
        清理文本内容
        """
        # 移除HTML标签
        text = BeautifulSoup(text, 'html.parser').get_text()
        
        # 移除多余空白
        text = re.sub(r'\s+', ' ', text)
        
        # 移除特殊字符
        text = re.sub(r'[^\u4e00-\u9fa5a-zA-Z0-9\s\.,;:!?，。！？、：；""''（）【】《》]', '', text)
        
        return text.strip()

    def extract_content(self, html: str) -> Dict[str, str]:
        """
        提取页面主要内容
        """
        soup = BeautifulSoup(html, 'html.parser')
        
        # 移除不需要的元素
        for element in soup.find_all(['script', 'style', 'nav', 'footer', 'header']):
            element.decompose()
        
        # 获取标题
        title = soup.find('title')
        title_text = title.get_text() if title else "无标题"
        
        # 获取主要内容
        main_content = ""
        for p in soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']):
            text = p.get_text().strip()
            if text:
                if p.name.startswith('h'):
                    main_content += f"\n\n## {text}\n"
                else:
                    main_content += f"\n{text}"
        
        return {
            'title': title_text,
            'content': self.clean_text(main_content)
        }

    def crawl_page(self, url: str) -> Dict[str, str]:
        """
        爬取单个页面
        """
        if url in self.visited_urls:
            return {}
        
        print(f"正在爬取: {url}")
        self.visited_urls.add(url)
        
        html = self.get_page_content(url)
        if not html:
            return {}
        
        content = self.extract_content(html)
        content['url'] = url
        
        # 添加延迟，避免请求过快
        time.sleep(1)
        
        return content

    def crawl_website(self, max_pages: int = 10) -> List[Dict[str, str]]:
        pages_content = []
        urls_to_visit = [self.base_url]
        
        while urls_to_visit and len(pages_content) < max_pages:
            current_url = urls_to_visit.pop(0)
            
            if current_url in self.visited_urls:
                continue
            self.visited_urls.add(current_url)

            print(f"正在爬取: {current_url}")
            html = self.get_page_content(current_url)
            if not html:
                continue

            content = self.extract_content(html)
            content['url'] = current_url
            pages_content.append(content)

            # 仅在处理 base_url 页面时提取子链接
            if current_url == self.base_url:
                new_links = self.extract_links(html, current_url)
                urls_to_visit.extend([
                    link for link in new_links 
                    if link not in self.visited_urls and link != current_url
                ])

            time.sleep(1)

        return pages_content

    def save_to_markdown(self, pages_content: List[Dict[str, str]], filename: str = None) -> str:
        """
        将爬取的内容保存为Markdown文件
        """
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"crawled_content_{timestamp}.md"
        
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            # f.write(f"# 网站内容爬取结果\n\n")
            # f.write(f"爬取时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            # f.write(f"源网站: {self.base_url}\n\n")
            
            for page in pages_content:
                f.write(f"## {page['title']}\n")
                # f.write(f"URL: {page['url']}\n\n")
                f.write(f"{page['content']}\n\n")
        
        return filepath

def crawl_website_to_markdown(base_url: str, max_pages: int = 1000, output_dir: str = "documents/crawled_docs") -> str:
    """
    爬取网站并保存为Markdown文件的API函数
    :param base_url: 要爬取的网站URL
    :param max_pages: 最大爬取页面数
    :param output_dir: 输出目录
    :return: 生成的Markdown文件路径
    """
    crawler = WebCrawler(base_url, output_dir)
    pages_content = crawler.crawl_website(max_pages)
    return crawler.save_to_markdown(pages_content)

# 使用示例
if __name__ == "__main__":
    # 示例：爬取一个网站
    target_url = "https://gymnasium.farama.org/"  # 替换为要爬取的网站
    output_file = crawl_website_to_markdown(target_url, max_pages=500)
    print(f"爬取完成，文件保存在: {output_file}") 