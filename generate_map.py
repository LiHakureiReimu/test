#!/usr/bin/env python3
"""
周年庆活动打卡地图生成器
将HTML地图转换为PNG图片
"""

import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from PIL import Image
import io

def setup_chrome_driver():
    """设置Chrome浏览器驱动"""
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--window-size=1920,1080')
    chrome_options.add_argument('--force-device-scale-factor=2')  # 提高分辨率
    
    # 尝试使用系统的Chrome/Chromium
    try:
        driver = webdriver.Chrome(options=chrome_options)
    except:
        # 如果失败，尝试使用chromium-browser
        chrome_options.binary_location = '/usr/bin/chromium-browser'
        driver = webdriver.Chrome(options=chrome_options)
    
    return driver

def html_to_png(html_file, output_file):
    """将HTML文件转换为PNG图片"""
    driver = None
    try:
        print("正在初始化浏览器...")
        driver = setup_chrome_driver()
        
        # 加载HTML文件
        file_url = f"file://{os.path.abspath(html_file)}"
        print(f"正在加载HTML文件: {file_url}")
        driver.get(file_url)
        
        # 等待页面完全加载
        time.sleep(3)
        
        # 获取地图容器元素
        map_element = driver.find_element(By.ID, "mapContainer")
        
        # 获取元素的位置和大小
        location = map_element.location
        size = map_element.size
        
        # 截取整个页面
        print("正在截取地图...")
        png = driver.get_screenshot_as_png()
        
        # 使用PIL裁剪图片到地图区域
        im = Image.open(io.BytesIO(png))
        
        # 由于设置了2倍的缩放因子，需要相应调整坐标
        left = location['x'] * 2
        top = location['y'] * 2
        right = left + size['width'] * 2
        bottom = top + size['height'] * 2
        
        # 裁剪图片
        im = im.crop((left, top, right, bottom))
        
        # 保存为PNG
        im.save(output_file, 'PNG', quality=95, dpi=(300, 300))
        print(f"地图已成功保存为: {output_file}")
        
        # 获取文件大小
        file_size = os.path.getsize(output_file) / 1024 / 1024
        print(f"文件大小: {file_size:.2f} MB")
        
    except Exception as e:
        print(f"转换过程中出现错误: {e}")
        raise
    finally:
        if driver:
            driver.quit()

def main():
    """主函数"""
    html_file = "/workspace/stamp_map.html"
    output_file = "/workspace/anniversary_stamp_map.png"
    
    print("=" * 50)
    print("周年庆活动打卡地图生成器")
    print("=" * 50)
    
    # 检查HTML文件是否存在
    if not os.path.exists(html_file):
        print(f"错误: HTML文件 {html_file} 不存在!")
        return
    
    # 转换为PNG
    html_to_png(html_file, output_file)
    
    print("=" * 50)
    print("地图生成完成！")
    print(f"输出文件: {output_file}")
    print("您可以下载此PNG文件用于打印或电子版使用")
    print("=" * 50)

if __name__ == "__main__":
    main()