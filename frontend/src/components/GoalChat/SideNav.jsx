import React, { useState } from 'react';

const SideNav = ({ currentStep = 1, onStepClick }) => {
  const steps = [
    { id: 1, icon: 'check_circle', label: 'Define Goal', description: 'What do you want to achieve?' },
    { id: 2, icon: 'calendar_today', label: 'Set Frequency', description: 'How often will you do it?' },
    { id: 3, icon: 'schedule', label: 'Schedule Time', description: 'When will you do it?' },
    { id: 4, icon: 'spark', label: 'Confirm Plan', description: 'Review and commit' },
  ];

  return (
    <aside className="hidden lg:flex w-72 flex-col border-r border-gray-200 dark:border-border-dark bg-white dark:bg-surface-dark h-screen sticky top-0">
      <div className="p-6">
        {/* Logo */}
        <div className="flex items-center gap-3 mb-8">
          <div className="w-10 h-10 rounded-lg bg-gradient-to-br from-primary to-purple-600 flex items-center justify-center">
            <span className="material-symbols-outlined text-white text-xl">
              all_inclusive
            </span>
          </div>
          <div>
            <h1 className="text-lg font-bold text-gray-900 dark:text-white">Consistency30</h1>
            <p className="text-sm text-gray-500 dark:text-gray-400">Build Your Habits</p>
          </div>
        </div>

        {/* Progress Steps */}
        <div className="space-y-2">
          <h2 className="text-sm font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-4">
            Setup Progress
          </h2>
          
          {steps.map((step) => {
            const isActive = step.id === currentStep;
            const isCompleted = step.id < currentStep;
            
            return (
              <button
                key={step.id}
                onClick={() => onStepClick && onStepClick(step.id)}
                className={`w-full flex items-center gap-3 p-3 rounded-lg transition-all duration-200 ${
                  isActive
                    ? 'bg-primary/10 dark:bg-primary/20 border border-primary/20'
                    : 'hover:bg-gray-100 dark:hover:bg-gray-800'
                }`}
              >
                <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  isCompleted
                    ? 'bg-green-500 text-white'
                    : isActive
                    ? 'bg-primary text-white'
                    : 'bg-gray-200 dark:bg-gray-700 text-gray-500 dark:text-gray-400'
                }`}>
                  <span className="material-symbols-outlined text-lg">
                    {isCompleted ? 'check' : step.icon}
                  </span>
                </div>
                <div className="flex-1 text-left">
                  <p className={`text-sm font-medium ${
                    isActive || isCompleted
                      ? 'text-primary dark:text-primary-light'
                      : 'text-gray-700 dark:text-gray-300'
                  }`}>
                    {step.label}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400">
                    {step.description}
                  </p>
                </div>
                {isActive && (
                  <div className="w-2 h-2 rounded-full bg-primary animate-pulse"></div>
                )}
              </button>
            );
          })}
        </div>

        {/* Progress Bar */}
        <div className="mt-8">
          <div className="flex justify-between text-sm text-gray-600 dark:text-gray-400 mb-2">
            <span>Progress</span>
            <span>{Math.round((currentStep / steps.length) * 100)}%</span>
          </div>
          <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
            <div 
              className="bg-gradient-to-r from-primary to-primary-light h-2 rounded-full transition-all duration-500"
              style={{ width: `${(currentStep / steps.length) * 100}%` }}
            ></div>
          </div>
        </div>

        {/* Current Goal Preview */}
        <div className="mt-8 p-4 bg-gradient-to-r from-primary/5 to-purple-500/5 dark:from-primary/10 dark:to-purple-500/10 rounded-lg border border-primary/20">
          <h3 className="text-sm font-semibold text-gray-900 dark:text-white mb-2">
            Current Goal
          </h3>
          <p className="text-sm text-gray-600 dark:text-gray-300">
            {currentStep === 1 ? "Not set yet" : 
             currentStep === 2 ? "Defining frequency..." :
             currentStep === 3 ? "Setting schedule..." :
             "Ready to confirm!"}
          </p>
        </div>
      </div>
    </aside>
  );
};

export default SideNav;