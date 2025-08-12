#!/usr/bin/env node

/**
 * 周年庆活动打卡地图生成器
 * 使用Puppeteer将HTML地图转换为PNG图片
 */

const puppeteer = require('puppeteer');
const fs = require('fs');
const path = require('path');

async function generateMapPNG() {
    console.log('='.repeat(50));
    console.log('周年庆活动打卡地图生成器');
    console.log('='.repeat(50));
    
    const htmlFile = path.join(__dirname, 'stamp_map.html');
    const outputFile = path.join(__dirname, 'anniversary_stamp_map.png');
    
    // 检查HTML文件是否存在
    if (!fs.existsSync(htmlFile)) {
        console.error(`错误: HTML文件 ${htmlFile} 不存在!`);
        return;
    }
    
    console.log('正在启动浏览器...');
    
    // 启动浏览器
    const browser = await puppeteer.launch({
        headless: 'new',
        args: [
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-gpu'
        ]
    });
    
    try {
        const page = await browser.newPage();
        
        // 设置视口大小
        await page.setViewport({
            width: 1920,
            height: 1080,
            deviceScaleFactor: 2 // 提高分辨率
        });
        
        // 加载HTML文件
        const fileUrl = `file://${htmlFile}`;
        console.log(`正在加载HTML文件: ${fileUrl}`);
        await page.goto(fileUrl, {
            waitUntil: 'networkidle0',
            timeout: 30000
        });
        
        // 等待动画加载完成
        await page.waitForTimeout(3000);
        
        // 获取地图容器元素
        const element = await page.$('#mapContainer');
        
        if (!element) {
            throw new Error('找不到地图容器元素');
        }
        
        console.log('正在截取地图...');
        
        // 截取元素的屏幕截图
        await element.screenshot({
            path: outputFile,
            type: 'png'
        });
        
        // 获取文件大小
        const stats = fs.statSync(outputFile);
        const fileSizeMB = stats.size / (1024 * 1024);
        
        console.log(`地图已成功保存为: ${outputFile}`);
        console.log(`文件大小: ${fileSizeMB.toFixed(2)} MB`);
        console.log('='.repeat(50));
        console.log('地图生成完成！');
        console.log(`输出文件: ${outputFile}`);
        console.log('您可以下载此PNG文件用于打印或电子版使用');
        console.log('='.repeat(50));
        
    } catch (error) {
        console.error('生成过程中出现错误:', error);
    } finally {
        await browser.close();
    }
}

// 运行生成器
generateMapPNG().catch(console.error);