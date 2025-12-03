import React from 'react';

const QuickChips = ({ chips = [], onSelect }) => {
  const defaultChips = [
    'Exercise', 'Read', 'Meditate', 'Drink Water', 
    'Learn a Skill', 'Sleep Early', 'Practice Coding',
    'Journal', 'Healthy Eating', 'Study', 'Morning Routine'
  ];

  const chipsToDisplay = chips.length > 0 ? chips : defaultChips;

  return (
    <div className="px-4 py-3">
      <p className="text-sm text-gray-500 dark:text-gray-400 mb-3 text-center">
        Try one of these common goals:
      </p>
      <div className="flex flex-wrap gap-2 justify-center">
        {chipsToDisplay.map((chip, index) => (
          <button
            key={index}
            onClick={() => onSelect && onSelect(chip)}
            className="px-4 py-2 bg-gray-100 dark:bg-gray-800 hover:bg-gray-200 dark:hover:bg-gray-700 text-gray-800 dark:text-gray-200 rounded-full text-sm font-medium transition-all duration-200 hover:scale-105 hover:shadow-sm active:scale-95"
          >
            {chip}
          </button>
        ))}
      </div>
    </div>
  );
};

export default QuickChips;