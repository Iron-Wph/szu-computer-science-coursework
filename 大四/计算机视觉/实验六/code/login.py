from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # 自动匹配ChromeDriver
import os
from train_cnn import CNN
import torch
from recognition import recognition, recognition2
from PIL import Image

# 全局加载模型，避免每次请求重复加载
cnn_model = CNN()
cnn_model.load_state_dict(torch.load('D:\作业\大四\自然语言处理\codebase\model_50.pth', map_location='cpu'))
cnn_model.eval()

# 账号密码配置
count = "17535691556"
pwd = '123456'
# 验证码图片保存路径（本地临时文件）
VERIFY_CODE_PATH = "verify_code.png"


def get_verify_code_image(driver):
    """
    步骤1：通过Selenium获取验证码图片（截图验证码区域）
    :param driver: Chrome驱动实例
    :return: 验证码图片保存路径
    """
    try:
        verify_img_element = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '/html/body/form[1]/div[4]/div[4]/img'))
        )

        if os.path.exists(VERIFY_CODE_PATH):
            os.remove(VERIFY_CODE_PATH)

        driver.execute_script("arguments[0].scrollIntoView(true);", verify_img_element)
        WebDriverWait(driver, 5).until(
            lambda d: driver.execute_script(
                "return arguments[0].complete && arguments[0].naturalWidth > 0",
                verify_img_element,
            )
        )
        verify_img_element.screenshot(VERIFY_CODE_PATH)

        print(f"验证码图片已保存到：{VERIFY_CODE_PATH}")
        return VERIFY_CODE_PATH
    except Exception as e:
        print(f"获取验证码图片失败：{e}")
        return None


def auto_recognize_verify_code(img_path):
    """
    步骤2：用ddddocr本地识别验证码（支持数字、字母、简单混合验证码）
    :param img_path: 验证码图片路径
    :return: 识别后的验证码字符串
    """
    if not img_path or not os.path.exists(img_path):
        print("验证码图片不存在")
        return ""

    try:

        # 1. 读取并预处理图像
        image = Image.open(img_path).convert('RGB')
        
        # 2. 根据图像尺寸选择识别函数（逻辑与原始Tkinter代码一致）
        size = image.size
        preds_cls, crops = recognition(image, cnn_model)
        
        # # 读取图片文件并识别
        # with open(img_path, "rb") as f:
        #     img_bytes = f.read()
        # result = ocr.classification(img_bytes)  # 识别验证码

        print(f"自动识别验证码结果：{preds_cls}")
        return "".join(preds_cls).strip()  # 去除空格等无关字符
    except Exception as e:
        print(f"验证码识别失败：{e}")
        return ""


def login(url='https://www.guwendao.net/user/login.aspx'):
    """
    步骤3：整合登录流程（自动获取验证码→识别→填充→登录）
    """
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
        driver.get(url)
        time.sleep(2)  # 等待页面加载完成（避免元素未渲染）

        count_box = driver.find_element(by=By.XPATH, value='//*[@id="email"]')
        count_box.send_keys(count)

        pwd_box = driver.find_element(by=By.XPATH, value='//*[@id="pwd"]')
        pwd_box.send_keys(pwd)

        img_path = get_verify_code_image(driver)
        verify_code = auto_recognize_verify_code(img_path)

        if not verify_code:
            verify_code = input("自动识别验证码失败，请手动输入：")

        verify_box = driver.find_element(by=By.XPATH, value='//*[@id="code"]')
        verify_box.send_keys(verify_code)

        login_button = driver.find_element(by=By.XPATH, value='//*[@id="denglu"]')
        login_button.click()
        time.sleep(13)  # 等待登录结果

        page_source = driver.page_source
        if "我的收藏" in page_source:
            print("登录成功")
        else:
            print("登录失败（可能是验证码识别错误或账号密码问题）")

        # if os.path.exists(VERIFY_CODE_PATH):
        #     os.remove(VERIFY_CODE_PATH)

        driver.close()
    except Exception as e:
        print(f"登录异常：{e}")
        # 清理临时文件
        # if os.path.exists(VERIFY_CODE_PATH):
        #     os.remove(VERIFY_CODE_PATH)
        # if os.path.exists("full_page.png"):
        #     os.remove("full_page.png")


if __name__ == '__main__':
    login_url = 'https://www.guwendao.net/user/login.aspx'
    login(login_url)
