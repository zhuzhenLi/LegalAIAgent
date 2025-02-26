import React from 'react';

const ActionButtons = ({ onAction }) => {
  const actions = [
    { id: 'TASK1', label: 'Analyze Documents' },
    { id: 'TASK2', label: 'Build Persuasive Arguments' },
    { id: 'TASK3', label: 'Refine Legal Strategy' },
    { id: 'TASK4', label: 'Ask About the Law' },
    { id: 'TASK5', label: 'Find a Case' }
    // 注意：如果需要支持所有7个按钮，后端需要添加TASK6和TASK7
  ];

  return (
    <div className="flex flex-wrap gap-2">
      {actions.map(action => (
        <button
          key={action.id}
          onClick={() => onAction(action.id, action.label)}
          className="px-3 py-1.5 text-sm bg-white border border-secondary-300 rounded-full text-secondary-700 hover:bg-secondary-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
        >
          {action.label}
        </button>
      ))}
    </div>
  );
};

export default ActionButtons; 