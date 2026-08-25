// 全局变量
let currentChatId = null;
let chatSessions = {};

// DOM 元素
let chatContainer, messageInput, sendBtn, chatHistoryContainer, welcomeMessage, loadingOverlay;

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    // 获取DOM元素
    chatContainer = document.getElementById('chatContainer');
    messageInput = document.getElementById('messageInput');
    sendBtn = document.getElementById('sendBtn');
    chatHistoryContainer = document.getElementById('chatHistory');
    welcomeMessage = document.getElementById('welcomeMessage');
    loadingOverlay = document.getElementById('loadingOverlay');
    
    loadChatSessions();
    setupEventListeners();
    autoResizeTextarea();
    initWatermark(); // 初始化水印
});

// 初始化水印
function initWatermark() {
    const watermarkContent = document.getElementById('watermarkContent');
    if (!watermarkContent) return;
    
    // 清空现有内容
    watermarkContent.innerHTML = '';
    
    // 水印文本
    const watermarkText = '王培鸿&&张泽鹏制作';
    
    // 计算需要多少个水印才能覆盖整个屏幕
    const screenWidth = window.innerWidth;
    const screenHeight = window.innerHeight;
    
    // 每个水印元素的大致尺寸
    const watermarkWidth = 200;
    const watermarkHeight = 100;
    
    // 计算行列数 (多加几个确保覆盖)
    const cols = Math.ceil(screenWidth / watermarkWidth) * 2;
    const rows = Math.ceil(screenHeight / watermarkHeight) * 2;
    
    // 生成水印
    for (let i = 0; i < rows * cols; i++) {
        const watermark = document.createElement('div');
        watermark.className = 'watermark-text';
        watermark.innerHTML = `<i class="fas fa-shield-alt"></i>${watermarkText}`;
        watermarkContent.appendChild(watermark);
    }
}

// 窗口大小改变时重新计算水印
window.addEventListener('resize', initWatermark);

// 设置事件监听器
function setupEventListeners() {
    // 输入框自动调整高度
    if (messageInput) {
        messageInput.addEventListener('input', autoResizeTextarea);
    }
    
    // 点击外部关闭侧边栏（移动端）
    document.addEventListener('click', function(e) {
        if (window.innerWidth <= 768) {
            const sidebar = document.getElementById('sidebar');
            const target = e.target;
            
            if (sidebar && !sidebar.contains(target) && !target.closest('.sidebar-toggle')) {
                sidebar.classList.remove('active');
            }
        }
    });
}

// 自动调整文本框高度
function autoResizeTextarea() {
    if (!messageInput) return;
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
}

// 处理键盘事件
function handleKeyDown(event) {
    if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
}

// 开始新会话
function startNewChat() {
    currentChatId = generateChatId();
    chatSessions[currentChatId] = {
        id: currentChatId,
        title: '新会话',
        messages: [],
        timestamp: new Date().toISOString()
    };
    
    clearChatDisplay();
    updateChatHistory();
    saveChatSessions();
    
    // 显示欢迎消息
    showWelcomeMessage();
}

// 发送消息
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message) return;
    
    // 如果没有当前会话，创建新会话
    if (!currentChatId) {
        startNewChat();
    }
    
    // 添加用户消息到界面
    addMessageToDisplay('user', message);
    
    // 保存消息到会话
    chatSessions[currentChatId].messages.push({
        role: 'user',
        content: message,
        timestamp: new Date().toISOString()
    });
    
    // 更新会话标题（如果是第一条消息）
    if (chatSessions[currentChatId].messages.length === 1) {
        chatSessions[currentChatId].title = message.substring(0, 30) + (message.length > 30 ? '...' : '');
        updateChatHistory();
    }
    
    // 清空输入框
    messageInput.value = '';
    autoResizeTextarea();
    
    // 创建AI消息容器（用于显示思考过程）
    const aiMessageDiv = createAIMessageContainer();
    chatContainer.appendChild(aiMessageDiv);
    
    try {
        console.log('发送消息到后端:', message);
        
        // 使用流式输出
        await streamResponse(message, aiMessageDiv);
        
    } catch (error) {
        console.error('发送消息失败:', error);
        
        let errorMessage = '抱歉，我遇到了一些问题。请稍后再试。';
        
        if (error.message.includes('Failed to fetch')) {
            errorMessage = '无法连接到服务器，请检查后端服务是否启动。';
        } else if (error.message.includes('HTTP error')) {
            errorMessage = '服务器响应错误，请检查后端日志。';
        } else if (error.message.includes('后端响应格式错误')) {
            errorMessage = '服务器响应格式错误，请联系管理员。';
        }
        
        // 更新AI消息内容
        updateAIMessageContent(aiMessageDiv, errorMessage);
    }
    
    // 保存会话
    saveChatSessions();
    
    // 滚动到底部
    scrollToBottom();
}

// 发送请求到后端
async function sendToBackend(message) {
    // 只发送消息，不再包含文件
    const formData = new FormData();
    formData.append('message', message);
    
    // 添加会话ID
    if (currentChatId) {
        formData.append('session_id', currentChatId);
    }
    
    // 修改为Flask后端的地址
    const response = await fetch('http://127.0.0.1:5000/api/chat', {
        method: 'POST',
        body: formData
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    return await response.json();
}

// 流式响应处理
async function streamResponse(message, aiMessageDiv) {
    const formData = new FormData();
    formData.append('message', message);
    formData.append('stream', 'true');
    
    // 添加会话ID
    if (currentChatId) {
        formData.append('session_id', currentChatId);
    }
    
    const response = await fetch('http://127.0.0.1:5000/api/chat', {
        method: 'POST',
        body: formData
    });
    
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const reader = response.body.getReader();
    const decoder = new TextDecoder();
    let finalAnswer = '';
    
    try {
        while (true) {
            const { done, value } = await reader.read();
            if (done) break;
            
            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');
            
            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    try {
                        const data = JSON.parse(line.slice(6));
                        
                        switch (data.type) {
                            case 'thinking_start':
                                updateAIMessageContent(aiMessageDiv, data.content, true);
                                break;
                                
                            case 'thinking':
                                updateAIMessageContent(aiMessageDiv, data.content, true);
                                break;
                                
                            case 'answer':
                                finalAnswer = data.content; // 保存原始格式的回答
                                updateAIMessageContent(aiMessageDiv, data.content, false);
                                break;
                                
                            case 'thinking_end':
                                // 思考结束，可以在这里添加一些结束动画
                                break;
                        }
                    } catch (e) {
                        console.error('解析流数据失败:', e);
                    }
                }
            }
        }
    } finally {
        reader.releaseLock();
    }
    
    // 保存AI回复到会话
    chatSessions[currentChatId].messages.push({
        role: 'assistant',
        content: finalAnswer,
        timestamp: new Date().toISOString()
    });
}

// 创建AI消息容器
function createAIMessageContainer() {
    const messageDiv = document.createElement('div');
    messageDiv.className = 'message assistant';
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = '<i class="fas fa-robot"></i>';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    messageContent.id = 'ai-message-content';
    
    // 添加思考指示器
    const thinkingIndicator = document.createElement('div');
    thinkingIndicator.className = 'thinking-indicator';
    thinkingIndicator.innerHTML = '<span class="thinking-dot"></span><span class="thinking-dot"></span><span class="thinking-dot"></span>';
    
    messageContent.appendChild(thinkingIndicator);
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);
    
    return messageDiv;
}

// 更新AI消息内容
function updateAIMessageContent(aiMessageDiv, content, isThinking = false) {
    const messageContent = aiMessageDiv.querySelector('.message-content');
    if (!messageContent) return;
    
    // 处理换行符，转换为HTML段落
    const formattedContent = content.replace(/\n\s*\n/g, '</p><p>').replace(/\n/g, '<br>');
    const wrappedContent = `<p>${formattedContent}</p>`;
    
    if (isThinking) {
        // 思考状态：显示内容 + 思考指示器
        messageContent.innerHTML = `
            <div class="thinking-content">${wrappedContent}</div>
            <div class="thinking-indicator">
                <span class="thinking-dot"></span>
                <span class="thinking-dot"></span>
                <span class="thinking-dot"></span>
            </div>
        `;
    } else {
        // 最终答案：只显示内容
        messageContent.innerHTML = `<div class="final-answer">${wrappedContent}</div>`;
    }
    
    // 滚动到底部
    scrollToBottom();
}

// 添加消息到显示区域
function addMessageToDisplay(role, content) {
    if (!chatContainer) return;
    
    // 隐藏欢迎消息
    if (welcomeMessage) {
        welcomeMessage.style.display = 'none';
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;
    
    const avatar = document.createElement('div');
    avatar.className = 'message-avatar';
    avatar.innerHTML = role === 'user' ? '<i class="fas fa-user"></i>' : '<i class="fas fa-robot"></i>';
    
    const messageContent = document.createElement('div');
    messageContent.className = 'message-content';
    
    // 处理换行符，转换为HTML段落
    const formattedContent = content.replace(/\n\s*\n/g, '</p><p>').replace(/\n/g, '<br>');
    messageContent.innerHTML = `<p>${formattedContent}</p>`;
    
    messageDiv.appendChild(avatar);
    messageDiv.appendChild(messageContent);
    
    chatContainer.appendChild(messageDiv);
    
    // 滚动到底部
    scrollToBottom();
}

// 滚动到底部
function scrollToBottom() {
    if (!chatContainer) return;
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// 加载聊天会话
function loadChatSessions() {
    const saved = localStorage.getItem('chatSessions');
    if (saved) {
        chatSessions = JSON.parse(saved);
        updateChatHistory();
    }
}

// 保存聊天会话
function saveChatSessions() {
    localStorage.setItem('chatSessions', JSON.stringify(chatSessions));
}

// 更新聊天历史显示
function updateChatHistory() {
    if (!chatHistoryContainer) {
        console.warn('chatHistoryContainer not found');
        return;
    }
    
    chatHistoryContainer.innerHTML = '';
    const sessionIds = Object.keys(chatSessions).sort((a, b) => {
        return new Date(chatSessions[b].timestamp) - new Date(chatSessions[a].timestamp);
    });
    sessionIds.forEach(chatId => {
        const session = chatSessions[chatId];
        const chatItem = document.createElement('div');
        chatItem.className = 'chat-history-item';
        chatItem.innerHTML = `
            <span class="chat-title" onclick="loadChatSession('${chatId}')">${session.title}</span>
            <button class="delete-chat-btn" onclick="deleteChatSession('${chatId}')"><i class="fas fa-trash"></i></button>
        `;
        chatHistoryContainer.appendChild(chatItem);
    });
}

// 加载聊天会话
function loadChatSession(chatId) {
    currentChatId = chatId;
    const session = chatSessions[chatId];
    
    if (!session) return;
    
    clearChatDisplay();
    
    // 显示会话消息
    session.messages.forEach(msg => {
        addMessageToDisplay(msg.role, msg.content);
    });
    
    updateChatHistory();
    
    // 通知后端切换会话（可选）
    try {
        const formData = new FormData();
        formData.append('session_id', chatId);
        fetch('http://127.0.0.1:5000/api/switch-session', {
            method: 'POST',
            body: formData
        });
    } catch (e) {
        // 忽略错误
    }
}

// 清空聊天显示
function clearChatDisplay() {
    if (!chatContainer) return;
    chatContainer.innerHTML = '';
    showWelcomeMessage();
}

// 显示欢迎消息
function showWelcomeMessage() {
    if (welcomeMessage) {
        welcomeMessage.style.display = 'flex';
    }
}

// 显示/隐藏加载动画
function showLoading(show) {
    if (!loadingOverlay) return;
    if (show) {
        loadingOverlay.classList.add('show');
    } else {
        loadingOverlay.classList.remove('show');
    }
}

// 生成聊天ID
function generateChatId() {
    return 'chat_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
}

// 格式化日期
function formatDate(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    
    if (diff < 24 * 60 * 60 * 1000) {
        // 今天
        return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' });
    } else if (diff < 7 * 24 * 60 * 60 * 1000) {
        // 一周内
        const days = ['周日', '周一', '周二', '周三', '周四', '周五', '周六'];
        return days[date.getDay()];
    } else {
        // 更早
        return date.toLocaleDateString('zh-CN', { month: '2-digit', day: '2-digit' });
    }
}

// 导出聊天记录
function exportChat(chatId) {
    const session = chatSessions[chatId];
    if (!session) return;
    
    const content = session.messages.map(msg => 
        `${msg.role === 'user' ? '用户' : 'AI'}: ${msg.content}`
    ).join('\n\n');
    
    const blob = new Blob([content], { type: 'text/plain;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `${session.title}_${formatDate(session.timestamp)}.txt`;
    a.click();
    URL.revokeObjectURL(url);
}

// 删除聊天会话
async function deleteChatSession(chatId) {
    // 前端本地删除
    delete chatSessions[chatId];
    saveChatSessions();
    updateChatHistory();
    // 后端删除
    try {
        await fetch(`http://127.0.0.1:5000/api/sessions/${chatId}`, { method: 'DELETE' });
    } catch (e) {
        // 忽略错误
    }
}

// 清空所有会话
function clearAllChats() {
    if (confirm('确定要清空所有会话吗？此操作不可恢复。')) {
        // 清空前端会话数据
        chatSessions = {};
        currentChatId = null;
        clearChatDisplay();
        updateChatHistory();
        saveChatSessions();
        
        // 通知后端清空所有会话历史
        try {
            const formData = new FormData();
            fetch('http://127.0.0.1:5000/api/clear-history', {
                method: 'POST',
                body: formData
            });
        } catch (e) {
            console.error('清空历史记录失败:', e);
        }
    }
} 