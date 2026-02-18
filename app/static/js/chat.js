/**
 * Chat Interface Script
 * Handles message sending, display, and dark mode styling
 */

document.addEventListener('DOMContentLoaded', function() {
    const chatContainer = document.getElementById('chat-container');
    const userInput = document.getElementById('user-input');
    const sendBtn = document.getElementById('send-btn');

    /**
     * Append a message to the chat container
     * @param {string} role - Message sender ('AI', 'You', 'System')
     * @param {string} text - Message content
     * @param {boolean} isError - Whether this is an error message
     */
    function appendMessage(role, text, isError = false) {
        // Determine message alignment and styling
        const isUserMessage = role === 'You';
        const messageClass = isUserMessage ? 'user-message' : 'ai-message';
        const messageType = isError ? 'system' : (isUserMessage ? 'user' : 'ai');

        const html = `
            <div class="chat-message ${messageClass}">
                <div class="chat-message-bubble ${messageType}">
                    <strong>${role}:</strong> ${text}
                </div>
            </div>
        `;

        chatContainer.insertAdjacentHTML('beforeend', html);
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    /**
     * Send a message to the AI API
     */
    async function sendMessage() {
        const message = userInput.value.trim();
        if (!message) return;

        // Display user message
        appendMessage('You', message);
        userInput.value = '';

        // Disable input while processing
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
            console.error('Chat API Error:', error);
        } finally {
            // Re-enable input
            userInput.disabled = false;
            sendBtn.disabled = false;
            userInput.focus();
        }
    }

    // Attach event listeners
    if (userInput) {
        userInput.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }

    if (sendBtn) {
        sendBtn.addEventListener('click', sendMessage);
    }
});
