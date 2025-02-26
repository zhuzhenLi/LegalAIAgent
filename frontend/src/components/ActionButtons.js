import React from 'react';

const ActionButtons = ({ onAction }) => {
  const actions = [
    { id: 'analyze', label: 'Analyze Documents' },
    { id: 'persuasive', label: 'Build Persuasive Arguments' },
    { id: 'legal', label: 'Refine Legal Strategy' },
    { id: 'law', label: 'Ask About the Law' },
    { id: 'case', label: 'Find a Case' },
    { id: 'memo', label: 'Generate Research Memo' },
    { id: 'draft', label: 'Automate First Draft' }
  ];

  return (
    <div className="flex flex-wrap gap-2">
      {actions.map(action => (
        <button
          key={action.id}
          onClick={() => onAction(action.label)}
          className="px-3 py-1.5 text-sm bg-white border border-secondary-300 rounded-full text-secondary-700 hover:bg-secondary-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
        >
          {action.label}
        </button>
      ))}
    </div>
  );
};

export default ActionButtons; 