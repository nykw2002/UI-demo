export const getStatusColor = (status, dueDate) => {
    const today = new Date();
    const dueDateTime = new Date(dueDate);
    const timeDiff = dueDateTime.getTime() - today.getTime();
    const daysDiff = Math.ceil(timeDiff / (1000 * 3600 * 24));
  
    if (status === 'Finalizat') return 'bg-green-100 border-green-500';
    if (status === 'În progres') return 'bg-blue-100 border-blue-500';
    if (status === 'Urgent' || daysDiff <= 3) return 'bg-red-100 border-red-500';
    return 'bg-gray-100 border-gray-500';
  };