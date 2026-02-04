// DOM Elements
const chatHistory = document.getElementById('chat-history');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');

// Sanitize HTML to prevent XSS
function sanitizeHTML(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML;
}

// Request stats updates every 3 seconds using simple polling
let statsInterval = setInterval(function() {
    // Fetch system stats
    fetch('/api/system-stats')
        .then(response => response.json())
        .then(data => {
            updateSystemStats(data);
        })
        .catch(error => {
            console.error('Error fetching system stats:', error);
        });
    
    // Fetch mining stats
    fetch('/api/miner-stats')
        .then(response => response.json())
        .then(data => {
            updateMiningStats(data);
        })
        .catch(error => {
            console.error('Error fetching mining stats:', error);
        });
}, 3000);

// Stop polling when page is hidden to save resources
document.addEventListener('visibilitychange', function() {
    if (document.hidden) {
        clearInterval(statsInterval);
    } else {
        statsInterval = setInterval(function() {
            fetchSystemStats();
            fetchMiningStats();
        }, 3000);
    }
});

function fetchSystemStats() {
    fetch('/api/system-stats')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            updateSystemStats(data);
        })
        .catch(error => {
            console.error('Error fetching system stats:', error);
        });
}

function fetchMiningStats() {
    fetch('/api/miner-stats')
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            updateMiningStats(data);
        })
        .catch(error => {
            console.error('Error fetching mining stats:', error);
        });
}

// Initial stats request
document.addEventListener('DOMContentLoaded', function() {
    fetchSystemStats();
    fetchMiningStats();
});

// Update system stats display
function updateSystemStats(stats) {
    if (!stats || typeof stats !== 'object') {
        return;
    }
    
    if (typeof stats.cpu_usage === 'number') {
        document.getElementById('cpu-usage').textContent = `${stats.cpu_usage.toFixed(1)}%`;
    }
    
    if (typeof stats.memory_usage === 'number') {
        document.getElementById('memory-usage').textContent = `${stats.memory_usage.toFixed(1)}%`;
    }
    
    if (typeof stats.temperature === 'number' && stats.temperature !== null) {
        document.getElementById('temperature').textContent = `${stats.temperature.toFixed(1)}°C`;
    }
    
    if (typeof stats.uptime === 'number' && stats.uptime !== null) {
        document.getElementById('uptime').textContent = `${stats.uptime.toFixed(1)} hrs`;
    }
}

// Update mining stats display
function updateMiningStats(stats) {
    if (!stats || typeof stats !== 'object') {
        return;
    }
    
    if (typeof stats.hashrate === 'number') {
        document.getElementById('hashrate').textContent = `${Math.round(stats.hashrate)} H/s`;
    }
    
    if (typeof stats.total_mined === 'number') {
        document.getElementById('total-mined').textContent = `${stats.total_mined.toFixed(4)} DUCO`;
    }
    
    if (typeof stats.uptime === 'number') {
        const hours = (stats.uptime / 3600).toFixed(1);
        document.getElementById('miner-uptime').textContent = `${hours} hrs`;
    }
    
    if (typeof stats.estimated_daily_yield === 'number') {
        document.getElementById('daily-yield').textContent = `${stats.estimated_daily_yield.toFixed(4)} DUCO`;
    }
}

// Handle chat form submission
chatForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const message = userInput.value.trim();
    if (!message || message.length === 0) return;
    
    // Validate message length
    if (message.length > 2000) {
        const errorDiv = document.createElement('div');
        errorDiv.className = 'message assistant-message';
        errorDiv.innerHTML = '<div class="message-content">Message too long (max 2000 characters)</div>';
        chatHistory.appendChild(errorDiv);
        return;
    }
    
    // Add user message to chat
    addMessageToChat(message, 'user');
    
    // Clear input
    userInput.value = '';
    
    // Disable input while processing
    userInput.disabled = true;
    const submitButton = chatForm.querySelector('button');
    submitButton.disabled = true;
    
    // Show loading indicator
    const loadingMsg = addMessageToChat('...', 'assistant', true);
    
    // Send request to server
    fetch('/api/chat', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ message: message })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json();
    })
    .then(data => {
        // Remove loading indicator
        if (loadingMsg && loadingMsg.parentNode) {
            loadingMsg.remove();
        }
        
        // Add AI response to chat
        if (data.response && data.response.content) {
            addMessageToChat(data.response.content, 'assistant');
        } else if (data.error) {
            addMessageToChat(`Error: ${sanitizeHTML(data.error)}`, 'assistant');
        } else {
            addMessageToChat('Sorry, I did not understand that.', 'assistant');
        }
    })
    .catch(error => {
        // Remove loading indicator
        if (loadingMsg && loadingMsg.parentNode) {
            loadingMsg.remove();
        }
        
        // Add error message to chat
        addMessageToChat(`Error: ${sanitizeHTML(error.message)}`, 'assistant');
    })
    .finally(() => {
        // Re-enable input
        userInput.disabled = false;
        submitButton.disabled = false;
        userInput.focus();
    });
});

// Add message to chat history
function addMessageToChat(content, sender, isLoading = false) {
    if (!content || typeof content !== 'string') {
        return null;
    }
    
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(`${sender}-message`);
    
    const contentDiv = document.createElement('div');
    contentDiv.classList.add('message-content');
    
    if (isLoading) {
        contentDiv.innerHTML = '<div class="loading"></div>';
    } else if (sender === 'assistant') {
        // Parse markdown content safely with DOMPurify-like sanitization
        try {
            if (typeof marked !== 'undefined' && typeof marked.parse === 'function') {
                const rawHTML = marked.parse(content);
                // Create temporary element to sanitize
                const temp = document.createElement('div');
                temp.textContent = content;
                // Only use marked if content doesn't contain script tags
                if (!/<script|javascript:/i.test(content)) {
                    contentDiv.innerHTML = rawHTML;
                } else {
                    contentDiv.textContent = content;
                }
            } else {
                contentDiv.textContent = content;
            }
        } catch (e) {
            console.error('Error parsing markdown:', e);
            contentDiv.textContent = content;
        }
    } else {
        contentDiv.textContent = content;
    }
    
    messageDiv.appendChild(contentDiv);
    chatHistory.appendChild(messageDiv);
    
    // Scroll to bottom
    chatHistory.scrollTop = chatHistory.scrollHeight;
    
    return messageDiv;
}

// Handle Enter key for submitting chat (removed duplicate handler)
// Form submission is already handled by the submit event listener above