import React from 'react';

const TypingIndicator = () => {
  return (
    <div className="flex items-center space-x-1.5">
      <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce [animation-delay:-0.3s]"></div>
      <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce [animation-delay:-0.15s]"></div>
      <div className="w-2 h-2 bg-white/60 rounded-full animate-bounce"></div>
    </div>
  );
};

export default TypingIndicator;