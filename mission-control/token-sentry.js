// Token Sentry State
let tokenState = {
    currentTokens: 4521,
    maxTokens: 10000,
    warningThreshold: 8000,
    dangerThreshold: 10000,
    messages: 12,
    contextDepth: 3
};

// Update token display
function updateTokenDisplay() {
    const percentage = (tokenState.currentTokens / tokenState.maxTokens) * 100;
    const fill = document.getElementById('token-fill');
    const count = document.getElementById('token-count');
    
    fill.style.width = percentage + '%';
    count.textContent = tokenState.currentTokens.toLocaleString() + ' / ' + tokenState.maxTokens.toLocaleString();
    
    // Update gauge color based on threshold
    fill.classList.remove('warning', 'danger');
    if (tokenState.currentTokens >= tokenState.dangerThreshold) {
        fill.classList.add('danger');
        document.getElementById('purge-btn').classList.add('danger');
    } else if (tokenState.currentTokens >= tokenState.warningThreshold) {
        fill.classList.add('warning');
    }
    
    // Update dashboard cards
    document.getElementById('dash-token-count').textContent = tokenState.currentTokens.toLocaleString();
    document.getElementById('dash-message-count').textContent = tokenState.messages;
    document.getElementById('dash-context-depth').textContent = tokenState.contextDepth;
}

// Purge context function
function purgeContext() {
    document.getElementById('purge-modal').classList.add('active');
}

// Confirm purge
document.getElementById('confirm-purge').addEventListener('click', function() {
    tokenState.currentTokens = 1000;
    tokenState.messages = 0;
    tokenState.contextDepth = 1;
    updateTokenDisplay();
    document.getElementById('purge-modal').classList.remove('active');
    
    // Visual feedback
    const fill = document.getElementById('token-fill');
    fill.style.transition = 'none';
    fill.style.width = '10%';
    setTimeout(() => {
        fill.style.transition = 'width 0.3s, background 0.3s';
    }, 50);
});

// Cancel purge
document.getElementById('cancel-purge').addEventListener('click', function() {
    document.getElementById('purge-modal').classList.remove('active');
});

// Close modal on overlay click
document.getElementById('purge-modal').addEventListener('click', function(e) {
    if (e.target === this) {
        this.classList.remove('active');
    }
});
