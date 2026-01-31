// DOM Elements
const chatHistory = document.getElementById('chat-history');
const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');

// Request stats updates every 3 seconds using simple polling
setInterval(function() {
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

// Initial stats request
document.addEventListener('DOMContentLoaded', function() {
    fetch('/api/system-stats')
        .then(response => response.json())
        .then(data => {
            updateSystemStats(data);
        })
        .catch(error => {
            console.error('Error fetching initial system stats:', error);
        });
    
    fetch('/api/miner-stats')
        .then(response => response.json())
        .then(data => {
            updateMiningStats(data);
        })
        .catch(error => {
            console.error('Error fetching initial mining stats:', error);
        });
});

// Update system stats display
function updateSystemStats(stats) {
    if (stats.cpu_usage !== undefined) {
        document.getElementById('cpu-usage').textContent = `${stats.cpu_usage.toFixed(1)}%`;
    }
    
    if (stats.memory_usage !== undefined) {
        document.getElementById('memory-usage').textContent = `${stats.memory_usage.toFixed(1)}%`;
    }
    
    if (stats.temperature !== undefined && stats.temperature !== null) {
        document.getElementById('temperature').textContent = `${stats.temperature.toFixed(1)}°C`;
    }
    
    if (stats.uptime !== undefined && stats.uptime !== null) {
        document.getElementById('uptime').textContent = `${stats.uptime.toFixed(1)} hrs`;
    }
}

// Update mining stats display
function updateMiningStats(stats) {
    if (stats.hashrate !== undefined) {
        document.getElementById('hashrate').textContent = `${Math.round(stats.hashrate)} H/s`;
    }
    
    if (stats.total_mined !== undefined) {
        document.getElementById('total-mined').textContent = `${stats.total_mined.toFixed(8)} XMR`;
    }
    
    if (stats.uptime !== undefined) {
        const hours = (stats.uptime / 3600).toFixed(1);
        document.getElementById('miner-uptime').textContent = `${hours} hrs`;
    }
    
    if (stats.estimated_daily_yield !== undefined) {
        document.getElementById('daily-yield').textContent = `${stats.estimated_daily_yield.toFixed(8)} XMR`;
    }
}

// Handle chat form submission
chatForm.addEventListener('submit', function(e) {
    e.preventDefault();
    
    const message = userInput.value.trim();
    if (!message) return;
    
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
    .then(response => response.json())
    .then(data => {
        // Remove loading indicator
        loadingMsg.remove();
        
        // Add AI response to chat
        if (data.response) {
            addMessageToChat(data.response.content, 'assistant');
        } else if (data.error) {
            addMessageToChat(`Error: ${data.error}`, 'assistant');
        } else {
            addMessageToChat('Sorry, I did not understand that.', 'assistant');
        }
    })
    .catch(error => {
        // Remove loading indicator
        loadingMsg.remove();
        
        // Add error message to chat
        addMessageToChat(`Error: ${error.message}`, 'assistant');
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
    const messageDiv = document.createElement('div');
    messageDiv.classList.add('message');
    messageDiv.classList.add(`${sender}-message`);
    
    const contentDiv = document.createElement('div');
    contentDiv.classList.add('message-content');
    
    if (isLoading) {
        contentDiv.innerHTML = '<div class="loading"></div>';
    } else if (sender === 'assistant') {
        // Parse markdown content
        contentDiv.innerHTML = marked.parse(content);
    } else {
        contentDiv.textContent = content;
    }
    
    messageDiv.appendChild(contentDiv);
    chatHistory.appendChild(messageDiv);
    
    // Scroll to bottom
    chatHistory.scrollTop = chatHistory.scrollHeight;
    
    return messageDiv;
}

// Handle Enter key for submitting chat
userInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        chatForm.dispatchEvent(new Event('submit'));
    }
});