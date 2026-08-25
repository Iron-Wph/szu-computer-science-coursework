import os
from dotenv import load_dotenv, find_dotenv
import requests
import zipfile

# 读取本地/项目的环境变量。
# find_dotenv()寻找并定位.env文件的路径
# load_dotenv()读取该.env文件，并将其中的环境变量加载到当前的运行环境中  
# 如果你设置的是全局的环境变量，这行代码则没有任何作用。
_ = load_dotenv(find_dotenv())

url='https://mineru.net/api/v4/file-urls/batch'
header = {
    'Content-Type': 'application/json',
    "Authorization": f'Bearer {os.getenv("MINERU_API_TOKEN")}'
}
data = {
    "enable_formula": True,
    "language": "auto",
    "enable_table": True,
    "files": [
        {"name":"D:\\作业\\大三下\\大模型技术及应用\\期末大作业\\demo\\documents\\利用导数定义求解极限_杨德志.pdf", "is_ocr": True, "data_id": "1"},
        {"name":"D:\\作业\\大三下\\大模型技术及应用\\期末大作业\\demo\\documents\\导数存在的一个充分必要条件_代丽美.pdf", "is_ocr": True, "data_id": "2"},
        {"name":"D:\\作业\\大三下\\大模型技术及应用\\期末大作业\\demo\\documents\\limit.pdf", "is_ocr": True, "data_id": "3"}
        
    ]
}
file_path = ["D:\\作业\\大三下\\大模型技术及应用\\期末大作业\\demo\\documents\\利用导数定义求解极限_杨德志.pdf",
             "D:\\作业\\大三下\\大模型技术及应用\\期末大作业\\demo\\documents\\导数存在的一个充分必要条件_代丽美.pdf",
             "D:\\作业\\大三下\\大模型技术及应用\\期末大作业\\demo\\documents\\limit.pdf"]
try:
    response = requests.post(url,headers=header,json=data)
    if response.status_code == 200:
        result = response.json()
        print('response success. result:{}'.format(result))
        if result["code"] == 0:
            batch_id = result["data"]["batch_id"]
            urls = result["data"]["file_urls"]
            print('batch_id:{},urls:{}'.format(batch_id, urls))
            for i in range(0, len(urls)):
                with open(file_path[i], 'rb') as f:
                    res_upload = requests.put(urls[i], data=f)
                    if res_upload.status_code == 200:
                        print(f"{urls[i]} upload success")
                    else:
                        print(f"{urls[i]} upload failed")
        else:
            print('apply upload url failed,reason:{}'.format(result.msg))
    else:
        print('response not success. status:{} ,result:{}'.format(response.status_code, response))
except Exception as err:
    print(err)
    
import time
time.sleep(40)

batch_id = result["data"]["batch_id"]
url = f'https://mineru.net/api/v4/extract-results/batch/{batch_id}'
header = {
    'Content-Type':'application/json',
    "Authorization": f'Bearer {os.getenv("MINERU_API_TOKEN")}'
}

res = requests.get(url, headers=header)
print(res.status_code)
print(res.json())
print(res.json()["data"])

urls = []
for i in res.json()["data"]["extract_result"]:
    urls.append(i["full_zip_url"])
    
print(urls)

# urls = ['https://cdn-mineru.openxlab.org.cn/pdf/f6c087a5-ae09-4e93-8174-4fd00a23ac8f.zip', 'https://cdn-mineru.openxlab.org.cn/pdf/ad8ec85f-3303-49f3-b1e4-0d58c6c64a8c.zip']
# 设置请求头部（如果需要）
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36 Edg/137.0.0.0'
}

# 下载文件
for url in urls:
    try:
        response = requests.get(url, headers=headers, stream=True)
        if response.status_code == 200:
            # 提取文件名
            file_name = url.split("/")[-1]
            # 保存文件到本地
            with open(file_name, "wb") as file:
                for chunk in response.iter_content(chunk_size=8192):
                    file.write(chunk)
            print(f"文件下载成功，保存为 {file_name}")
            # 解压文件
            # 创建独立的解压目录
            extract_path = f"extracted_files_{file_name.split('.')[0]}"  # 使用文件名作为目录名
            os.makedirs(extract_path, exist_ok=True)  # 确保目录存在
            
            with zipfile.ZipFile(file_name, 'r') as zip_ref:
                # 指定解压目录
                zip_ref.extractall(extract_path)
                print(f"文件已解压到 {extract_path}")
        else:
            print(f"下载失败，状态码：{response.status_code}")
    except Exception as e:
        print(f"下载失败，错误信息：{e}")