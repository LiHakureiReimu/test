#!/usr/bin/env python3
"""
周年庆活动打卡地图生成器（简化版）
使用html2image将HTML地图转换为PNG图片
"""

import os
import base64
from html2image import Html2Image

def generate_map_png():
    """生成地图PNG文件"""
    
    # 读取HTML文件
    html_file = "/workspace/stamp_map.html"
    output_file = "/workspace/anniversary_stamp_map.png"
    
    print("=" * 50)
    print("周年庆活动打卡地图生成器")
    print("=" * 50)
    
    # 检查HTML文件是否存在
    if not os.path.exists(html_file):
        print(f"错误: HTML文件 {html_file} 不存在!")
        return
    
    # 读取HTML内容
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print("正在生成PNG图片...")
    
    # 创建Html2Image实例
    hti = Html2Image(output_path='/workspace', size=(1200, 800))
    
    # 生成图片
    hti.screenshot(
        html_str=html_content,
        save_as='anniversary_stamp_map.png'
    )
    
    if os.path.exists(output_file):
        file_size = os.path.getsize(output_file) / 1024 / 1024
        print(f"地图已成功保存为: {output_file}")
        print(f"文件大小: {file_size:.2f} MB")
        print("=" * 50)
        print("地图生成完成！")
        print(f"输出文件: {output_file}")
        print("您可以下载此PNG文件用于打印或电子版使用")
        print("=" * 50)
    else:
        print("生成失败，请检查环境配置")

if __name__ == "__main__":
    generate_map_png()