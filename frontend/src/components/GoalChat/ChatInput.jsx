import React, { useState } from 'react';

const ChatInput = ({ onSend, placeholder = "I want to...", isLoading = false }) => {
  const [message, setMessage] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (message.trim() && !isLoading) {
      onSend(message.trim());
      setMessage('');
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="w-full">
      <div className="relative">
        <input
          type="text"
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder={placeholder}
          disabled={isLoading}
          className="w-full px-5 py-4 pr-14 bg-white dark:bg-surface-dark border border-gray-300 dark:border-border-dark rounded-xl text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500 focus:outline-none focus:ring-2 focus:ring-primary focus:border-transparent text-base transition-all duration-200"
          autoFocus
        />
        <button
          type="submit"
          disabled={!message.trim() || isLoading}
          className={`absolute right-3 top-1/2 -translate-y-1/2 p-2 rounded-lg transition-all duration-200 ${
            message.trim() && !isLoading
              ? 'bg-primary hover:bg-primary-dark text-white hover:scale-110'
              : 'bg-gray-200 dark:bg-gray-700 text-gray-400 dark:text-gray-500 cursor-not-allowed'
          }`}
          aria-label="Send message"
        >
          <span className="material-symbols-outlined">
            {isLoading ? 'schedule' : 'send'}
          </span>
        </button>
      </div>
      <p className="text-xs text-gray-500 dark:text-gray-400 mt-2 text-center">
        Press Enter to send • Shift+Enter for new line
      </p>
    </form>
  );
};

export default ChatInput;