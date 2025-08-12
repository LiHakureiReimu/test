// 打卡地图交互功能
class CheckInMap {
    constructor() {
        this.stampedLocations = new Set();
        this.init();
    }

    init() {
        this.bindEvents();
        this.loadProgress();
        this.updateProgress();
    }

    bindEvents() {
        // 为每个打卡地点添加点击事件
        document.querySelectorAll('.location-card').forEach(card => {
            card.addEventListener('click', (e) => {
                this.handleLocationClick(e, card);
            });
        });

        // 添加键盘快捷键支持
        document.addEventListener('keydown', (e) => {
            this.handleKeyboardShortcuts(e);
        });
    }

    handleLocationClick(e, card) {
        const locationId = card.dataset.location;
        const stampArea = card.querySelector('.stamp-area');
        
        if (this.stampedLocations.has(locationId)) {
            // 如果已经打卡，显示提示
            this.showNotification('该地点已经打卡完成！', 'info');
        } else {
            // 模拟打卡过程
            this.simulateStamp(locationId, stampArea, card);
        }
    }

    simulateStamp(locationId, stampArea, card) {
        // 显示打卡确认对话框
        const confirmed = confirm(`确认完成"${card.querySelector('h3').textContent}"活动吗？`);
        
        if (confirmed) {
            // 添加打卡效果
            this.addStampEffect(locationId, stampArea);
            
            // 保存进度
            this.saveProgress();
            
            // 更新进度显示
            this.updateProgress();
            
            // 显示成功提示
            this.showNotification('打卡成功！', 'success');
            
            // 检查是否完成所有打卡
            if (this.stampedLocations.size === 5) {
                this.showCompletionMessage();
            }
        }
    }

    addStampEffect(locationId, stampArea) {
        // 添加到已打卡集合
        this.stampedLocations.add(locationId);
        
        // 添加印章样式
        stampArea.classList.add('stamped');
        
        // 更新印章区域内容
        const placeholder = stampArea.querySelector('.stamp-placeholder');
        placeholder.innerHTML = '✅ 已打卡<br><small>完成时间: ' + new Date().toLocaleTimeString() + '</small>';
        
        // 添加完成动画
        stampArea.style.animation = 'stampEffect 0.5s ease';
        
        // 移除动画类，以便可以重复触发
        setTimeout(() => {
            stampArea.style.animation = '';
        }, 500);
    }

    updateProgress() {
        const progressFill = document.getElementById('progressFill');
        const progressCount = document.getElementById('progressCount');
        
        const progress = (this.stampedLocations.size / 5) * 100;
        progressFill.style.width = progress + '%';
        progressCount.textContent = this.stampedLocations.size;
        
        // 根据进度改变进度条颜色
        if (progress === 100) {
            progressFill.style.background = 'linear-gradient(90deg, #00ff00, #00ffff)';
        } else if (progress >= 60) {
            progressFill.style.background = 'linear-gradient(90deg, #ffff00, #00ff00)';
        }
    }

    showNotification(message, type = 'info') {
        // 创建通知元素
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        
        // 添加样式
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 20px;
            border-radius: 8px;
            color: white;
            font-weight: bold;
            z-index: 1000;
            animation: slideIn 0.3s ease;
            max-width: 300px;
        `;
        
        // 根据类型设置背景色
        switch (type) {
            case 'success':
                notification.style.background = 'linear-gradient(45deg, #00ff00, #00cc00)';
                break;
            case 'info':
                notification.style.background = 'linear-gradient(45deg, #00ffff, #0099cc)';
                break;
            case 'warning':
                notification.style.background = 'linear-gradient(45deg, #ffff00, #ffcc00)';
                break;
            case 'error':
                notification.style.background = 'linear-gradient(45deg, #ff0000, #cc0000)';
                break;
        }
        
        // 添加到页面
        document.body.appendChild(notification);
        
        // 3秒后自动移除
        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }

    showCompletionMessage() {
        // 创建完成庆祝效果
        setTimeout(() => {
            this.showNotification('🎉 恭喜！你已完成所有打卡任务！', 'success');
            
            // 添加页面庆祝效果
            this.addCelebrationEffect();
        }, 1000);
    }

    addCelebrationEffect() {
        // 创建庆祝动画元素
        for (let i = 0; i < 20; i++) {
            setTimeout(() => {
                this.createConfetti();
            }, i * 100);
        }
    }

    createConfetti() {
        const confetti = document.createElement('div');
        confetti.innerHTML = ['🎉', '✨', '🎊', '🌟', '💫'][Math.floor(Math.random() * 5)];
        confetti.style.cssText = `
            position: fixed;
            top: -20px;
            left: ${Math.random() * 100}vw;
            font-size: 2rem;
            z-index: 1000;
            animation: confettiFall 3s linear forwards;
            pointer-events: none;
        `;
        
        document.body.appendChild(confetti);
        
        // 动画结束后移除
        setTimeout(() => {
            if (confetti.parentNode) {
                confetti.parentNode.removeChild(confetti);
            }
        }, 3000);
    }

    handleKeyboardShortcuts(e) {
        // 数字键1-5快速打卡
        if (e.key >= '1' && e.key <= '5') {
            const locationId = e.key;
            const card = document.querySelector(`[data-location="${locationId}"]`);
            if (card) {
                this.handleLocationClick(e, card);
            }
        }
        
        // R键重置进度
        if (e.key === 'r' || e.key === 'R') {
            if (confirm('确定要重置所有打卡进度吗？')) {
                this.resetProgress();
            }
        }
    }

    resetProgress() {
        this.stampedLocations.clear();
        
        // 移除所有印章效果
        document.querySelectorAll('.stamp-area').forEach(area => {
            area.classList.remove('stamped');
            const placeholder = area.querySelector('.stamp-placeholder');
            placeholder.textContent = '盖章区域';
        });
        
        // 更新进度
        this.updateProgress();
        this.saveProgress();
        
        this.showNotification('进度已重置', 'info');
    }

    saveProgress() {
        const progress = Array.from(this.stampedLocations);
        localStorage.setItem('checkInProgress', JSON.stringify(progress));
    }

    loadProgress() {
        const saved = localStorage.getItem('checkInProgress');
        if (saved) {
            try {
                const progress = JSON.parse(saved);
                this.stampedLocations = new Set(progress);
                
                // 恢复印章效果
                this.stampedLocations.forEach(locationId => {
                    const card = document.querySelector(`[data-location="${locationId}"]`);
                    if (card) {
                        const stampArea = card.querySelector('.stamp-area');
                        stampArea.classList.add('stamped');
                        const placeholder = stampArea.querySelector('.stamp-placeholder');
                        placeholder.innerHTML = '✅ 已打卡<br><small>之前完成</small>';
                    }
                });
            } catch (e) {
                console.error('加载进度失败:', e);
            }
        }
    }
}

// 添加CSS动画
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }
    
    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
    
    @keyframes confettiFall {
        to {
            transform: translateY(100vh) rotate(360deg);
        }
    }
`;
document.head.appendChild(style);

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', () => {
    new CheckInMap();
    
    // 添加使用说明
    console.log(`
🎉 周年庆打卡地图使用说明：
- 点击任意打卡地点进行打卡
- 使用数字键1-5快速选择打卡地点
- 按R键重置所有进度
- 进度会自动保存到本地存储
- 完成所有打卡会触发庆祝效果！
    `);
});