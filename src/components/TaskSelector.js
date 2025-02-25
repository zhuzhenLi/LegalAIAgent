import React from 'react';

function TaskSelector({ onTaskSelected, disabled }) {
  const handleChange = (e) => {
    onTaskSelected(e.target.value);
  };

  return (
    <div className="w-full">
      <label htmlFor="task-select" className="block text-sm font-medium text-gray-700 mb-1">
        选择任务
      </label>
      <select
        id="task-select"
        onChange={handleChange}
        disabled={disabled}
        className={`block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm
          ${disabled ? 'opacity-50 cursor-not-allowed' : ''}
        `}
        defaultValue=""
      >
        <option value="" disabled>请选择任务类型</option>
        <option value="lawsuit">生成诉讼书</option>
        <option value="defense">生成应诉书</option>
      </select>
    </div>
  );
}

export default TaskSelector; 