import React, { useState, useEffect, useRef } from 'react';
import SideNav from '../components/GoalChat/SideNav';
import ChatMessage from '../components/GoalChat/ChatMessage';
import QuickChips from '../components/GoalChat/QuickChips';
import ChatInput from '../components/GoalChat/ChatInput';

const GoalChatPage = () => {
  const [messages, setMessages] = useState([
    { id: 1, sender: 'ai', text: "Hello! I'm your AI habit coach. What new habit would you like to build? You can type your own goal or select from the suggestions below.", time: "2:30 PM" },
    { id: 2, sender: 'user', text: "I want to exercise more consistently.", time: "2:31 PM" },
  ]);
  
  const [isTyping, setIsTyping] = useState(false);
  const [currentStep, setCurrentStep] = useState(1);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isTyping]);

  const handleSendMessage = (text) => {
    // Add user message
    const newUserMessage = {
      id: messages.length + 1,
      sender: 'user',
      text,
      time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    };
    
    setMessages(prev => [...prev, newUserMessage]);
    setIsTyping(true);
    
    // Simulate AI response after delay
    setTimeout(() => {
      const aiResponses = [
        "Great choice! Exercising regularly has amazing benefits. How many days per week would you like to commit to?",
        "That's an excellent goal! What type of exercise are you interested in? (e.g., running, yoga, strength training)",
        "Consistency is key! Would you like to start with 3 days a week and build from there?",
        "Wonderful! Let's make this achievable. What's your current fitness level?",
      ];
      
      const randomResponse = aiResponses[Math.floor(Math.random() * aiResponses.length)];
      
      const newAIMessage = {
        id: messages.length + 2,
        sender: 'ai',
        text: randomResponse,
        time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
      };
      
      setMessages(prev => [...prev, newAIMessage]);
      setIsTyping(false);
      
      // Progress to next step
      if (currentStep < 4) {
        setCurrentStep(prev => prev + 1);
      }
    }, 1500);
  };

  const handleChipSelect = (chip) => {
    handleSendMessage(`I want to ${chip.toLowerCase()}`);
  };

  const handleStepClick = (step) => {
    setCurrentStep(step);
  };

  return (
    <div className="min-h-screen bg-background-light dark:bg-background-dark font-display">
      <div className="flex h-screen">
        {/* Mobile Header */}
        <header className="lg:hidden fixed top-0 left-0 right-0 z-50 bg-white dark:bg-surface-dark border-b border-gray-200 dark:border-border-dark p-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-3">
              <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-primary to-purple-600 flex items-center justify-center">
                <span className="material-symbols-outlined text-white">
                  all_inclusive
                </span>
              </div>
              <div>
                <h1 className="text-lg font-bold text-gray-900 dark:text-white">Consistency30</h1>
                <div className="flex items-center gap-2">
                  <div className="text-xs text-gray-500 dark:text-gray-400">
                    Step {currentStep} of 4
                  </div>
                  <div className="w-24 bg-gray-200 dark:bg-gray-700 rounded-full h-1">
                    <div 
                      className="bg-gradient-to-r from-primary to-primary-light h-1 rounded-full transition-all duration-500"
                      style={{ width: `${(currentStep / 4) * 100}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            </div>
            <button className="lg:hidden p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800">
              <span className="material-symbols-outlined text-gray-600 dark:text-gray-400">
                menu
              </span>
            </button>
          </div>
        </header>

        {/* Side Navigation - Hidden on mobile */}
        <SideNav currentStep={currentStep} onStepClick={handleStepClick} />

        {/* Main Chat Area */}
        <main className="flex-1 flex flex-col lg:ml-0">
          {/* Chat Container */}
          <div className="flex-1 flex flex-col pt-16 lg:pt-0">
            {/* Chat Header for Desktop */}
            <div className="hidden lg:flex items-center justify-between p-6 border-b border-gray-200 dark:border-border-dark">
              <div>
                <h1 className="text-xl font-bold text-gray-900 dark:text-white">Goal Setting Chat</h1>
                <p className="text-sm text-gray-500 dark:text-gray-400">
                  Talk with your AI coach to build the perfect habit plan
                </p>
              </div>
              <div className="flex items-center gap-4">
                <div className="px-3 py-1 rounded-full bg-primary/10 text-primary text-sm font-medium">
                  Step {currentStep}/4
                </div>
                <button className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-800">
                  <span className="material-symbols-outlined text-gray-600 dark:text-gray-400">
                    help
                  </span>
                </button>
              </div>
            </div>

            {/* Messages Container */}
            <div className="flex-1 overflow-y-auto px-4 sm:px-6 py-4">
              <div className="max-w-3xl mx-auto">
                {/* Welcome Card */}
                <div className="mb-6 bg-gradient-to-r from-primary/5 to-purple-500/5 dark:from-primary/10 dark:to-purple-500/10 border border-primary/20 rounded-xl p-4 animate-slide-up">
                  <div className="flex items-center gap-3 mb-3">
                    <div className="w-10 h-10 rounded-full bg-gradient-to-br from-primary to-purple-600 flex items-center justify-center">
                      <span className="material-symbols-outlined text-white">
                        rocket_launch
                      </span>
                    </div>
                    <div>
                      <h3 className="font-bold text-gray-900 dark:text-white">Welcome to Goal Setting!</h3>
                      <p className="text-sm text-gray-600 dark:text-gray-300">
                        Your AI coach will guide you through creating a personalized habit plan.
                      </p>
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-2">
                    <div className="px-3 py-1 bg-white dark:bg-surface-dark rounded-full text-xs font-medium">
                      ⏱️ Takes 2-3 minutes
                    </div>
                    <div className="px-3 py-1 bg-white dark:bg-surface-dark rounded-full text-xs font-medium">
                      🎯 Personalized advice
                    </div>
                    <div className="px-3 py-1 bg-white dark:bg-surface-dark rounded-full text-xs font-medium">
                      📊 Progress tracking
                    </div>
                  </div>
                </div>

                {/* Messages */}
                <div className="space-y-4">
                  {messages.map((msg) => (
                    <ChatMessage
                      key={msg.id}
                      message={msg.text}
                      sender={msg.sender}
                      time={msg.time}
                    />
                  ))}
                  
                  {isTyping && (
                    <ChatMessage
                      message=""
                      sender="ai"
                      isTyping={true}
                    />
                  )}
                  
                  <div ref={messagesEndRef} />
                </div>

                {/* Quick Chips */}
                {currentStep === 1 && (
                  <QuickChips onSelect={handleChipSelect} />
                )}
              </div>
            </div>

            {/* Chat Input */}
            <div className="border-t border-gray-200 dark:border-border-dark bg-white dark:bg-surface-dark p-4">
              <div className="max-w-3xl mx-auto">
                <ChatInput
                  onSend={handleSendMessage}
                  placeholder="Tell me what habit you want to build..."
                  isLoading={isTyping}
                />
              </div>
            </div>
          </div>
        </main>
      </div>

      {/* Mobile Step Indicator */}
      <div className="lg:hidden fixed bottom-0 left-0 right-0 bg-white dark:bg-surface-dark border-t border-gray-200 dark:border-border-dark p-3">
        <div className="flex items-center justify-between">
          <div className="flex-1">
            <div className="flex items-center justify-between text-sm mb-1">
              <span className="text-gray-600 dark:text-gray-400">Step {currentStep} of 4</span>
              <span className="font-medium text-primary">{Math.round((currentStep / 4) * 100)}%</span>
            </div>
            <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
              <div 
                className="bg-gradient-to-r from-primary to-primary-light h-2 rounded-full transition-all duration-500"
                style={{ width: `${(currentStep / 4) * 100}%` }}
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default GoalChatPage;