document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    function appendMessage(role, text, isError = false) {
        const align = role === 'You' ? 'justify-content-end' : 'justify-content-start';
        const bg = role === 'You' ? 'bg-primary text-white' : 'bg-white border shadow-sm';
        const textClass = isError ? 'text-danger' : '';
        
        const html = `
            <div class="d-flex ${align} mb-3">
                <div class="p-3 rounded ${bg} ${textClass}" style="max-width: 80%;">
                    <strong>${role}:</strong> ${text}
                </div>
            </div>
        `;
        chatContainer.insertAdjacentHTML('beforeend', html);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        appendMessage('You', message);
        userInput.value = '';
        
        // Disable input to prevent multiple sends
        userInput.disabled = true;
        sendBtn.disabled = true;

        try {
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ message: message })
            });
            
            const data = await response.json();
            if (data.error) {
                appendMessage('System', 'Error: ' + data.error, true);
            } else {
                appendMessage('AI', data.response);
            }
        } catch (error) {
            appendMessage('System', 'Network error occurred.', true);
        } finally {
            userInput.disabled = false;
            sendBtn.disabled = false;
            userInput.focus();
        }
    }

    if (userInput) {
        userInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') sendMessage();
        });
    }

    if (sendBtn) {
        sendBtn.addEventListener('click', sendMessage);
    }
});