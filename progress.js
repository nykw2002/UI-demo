import React from 'react';

const CustomProgressBar = ({ subtasks }) => {
  if (!Array.isArray(subtasks) || subtasks.length === 0) {
    return <div className="w-full h-4 bg-gray-200 rounded-full" />;
  }

  const totalDuration = subtasks.reduce((total, subtask) => {
    if (!subtask.startDate || !subtask.dueDate) return total;
    const start = new Date(subtask.startDate);
    const end = new Date(subtask.dueDate);
    return total + Math.max(0, end - start);
  }, 0);

  const getStatusColor = (status) => {
    switch (status) {
      case 'completed': return 'bg-green-500';
      case 'in_progress': return 'bg-blue-500';
      case 'not_started': return 'bg-gray-300';
      case 'overdue': return 'bg-red-500';
      default: return 'bg-gray-300';
    }
  };

  return (
    <div className="w-full h-4 bg-gray-200 rounded-full overflow-hidden">
      {subtasks.map((subtask, index) => {
        if (!subtask.startDate || !subtask.dueDate) return null;
        const start = new Date(subtask.startDate);
        const end = new Date(subtask.dueDate);
        const duration = Math.max(0, end - start);
        const width = totalDuration > 0 ? (duration / totalDuration) * 100 : 0;
        
        return (
          <div
            key={index}
            className={`h-full ${getStatusColor(subtask.status)}`}
            style={{
              width: `${width}%`,
              display: 'inline-block',
            }}
            title={`${subtask.name}: ${subtask.status}`}
          />
        );
      })}
    </div>
  );
};

export default CustomProgressBar;