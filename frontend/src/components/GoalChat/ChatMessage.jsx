import React from 'react';
import TypingIndicator from './TypingIndicator';

const ChatMessage = ({ message, sender, isTyping = false, time }) => {
  const isAI = sender === 'ai';
  
  return (
    <div className={`flex items-end gap-3 p-3 animate-fade-in ${isAI ? '' : 'justify-end'}`}>
      {isAI ? (
        <>
          {/* AI Avatar */}
          <div className="flex-shrink-0">
            <div 
              className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-purple-600 flex items-center justify-center overflow-hidden"
              title="AI Assistant"
            >
              <span className="material-symbols-outlined text-white text-lg">
                smart_toy
              </span>
            </div>
          </div>
          
          {/* AI Message */}
          <div className="flex flex-col gap-1 items-start max-w-[85%] sm:max-w-[75%]">
            <p className="text-xs text-gray-500 dark:text-gray-400 font-medium">AI Assistant</p>
            {isTyping ? (
              <div className="flex items-center justify-center min-h-[44px] px-4 py-3 bg-primary text-white rounded-xl rounded-tl-none">
                <TypingIndicator />
              </div>
            ) : (
              <div className="bg-primary text-white px-4 py-3 rounded-xl rounded-tl-none shadow-sm">
                <p className="text-base leading-relaxed whitespace-pre-wrap">{message}</p>
                {time && (
                  <span className="text-xs text-white/70 mt-1 block">{time}</span>
                )}
              </div>
            )}
          </div>
        </>
      ) : (
        <>
          {/* User Message */}
          <div className="flex flex-col gap-1 items-end max-w-[85%] sm:max-w-[75%]">
            <p className="text-xs text-gray-500 dark:text-gray-400 font-medium">You</p>
            <div className="bg-gray-200 dark:bg-gray-800 text-gray-900 dark:text-white px-4 py-3 rounded-xl rounded-br-none shadow-sm">
              <p className="text-base leading-relaxed whitespace-pre-wrap">{message}</p>
              {time && (
                <span className="text-xs text-gray-500 dark:text-gray-400 mt-1 block">{time}</span>
              )}
            </div>
          </div>
          
          {/* User Avatar */}
          <div className="flex-shrink-0">
            <div 
              className="w-10 h-10 rounded-full bg-gradient-to-br from-gray-400 to-gray-600 flex items-center justify-center overflow-hidden"
              title="You"
            >
              <span className="material-symbols-outlined text-white text-lg">
                person
              </span>
            </div>
          </div>
        </>
      )}
    </div>
  );
};

export default ChatMessage;