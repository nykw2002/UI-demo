import React, { useState } from 'react';
import { Edit2, Trash2, UserPlus, PlusCircle, X } from 'lucide-react';
import { Alert, AlertDescription } from '@/components/ui/alert';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import CustomProgressBar from './CustomProgressBar';
import { getStatusColor } from './utils';

const ProjectPipeline = () => {
  const [tasks, setTasks] = useState([
    { 
      id: 1, 
      name: 'Planificare proiect', 
      status: 'În progres', 
      dueDate: '2024-07-15', 
      assignees: [
        { initials: 'AP', image: '/api/placeholder/32/32' },
        { initials: 'MN', image: '/api/placeholder/32/32' }
      ],
      subtasks: [
        { id: 1, name: 'Definire obiective', startDate: '2024-07-01', dueDate: '2024-07-05', status: 'completed', assignee: { initials: 'AP', image: '/api/placeholder/32/32' } },
        { id: 2, name: 'Alocare resurse', startDate: '2024-07-06', dueDate: '2024-07-10', status: 'in_progress', assignee: null },
        { id: 3, name: 'Stabilire timeline', startDate: '2024-07-11', dueDate: '2024-07-15', status: 'not_started', assignee: null }
      ]
    },
    // ... other tasks
  ]);
  const [editingTask, setEditingTask] = useState(null);
  const [editingSubtask, setEditingSubtask] = useState(null);
  const [newTask, setNewTask] = useState({ name: '', status: 'Neînceput', dueDate: '', assignees: [], subtasks: [] });

  const addTask = () => {
    if (newTask.name && newTask.dueDate) {
      setTasks([...tasks, { ...newTask, id: tasks.length + 1 }]);
      setNewTask({ name: '', status: 'Neînceput', dueDate: '', assignees: [], subtasks: [] });
    }
  };

  const updateTask = (id, updatedTask) => {
    setTasks(tasks.map(task => task.id === id ? { ...task, ...updatedTask } : task));
    setEditingTask(null);
  };

  const deleteTask = (id) => {
    setTasks(tasks.filter(task => task.id !== id));
  };

  const addAssignee = (taskId) => {
    const initials = prompt("Introduceți inițialele noului responsabil:");
    if (initials) {
      setTasks(tasks.map(task => 
        task.id === taskId 
          ? { ...task, assignees: [...task.assignees, { initials: initials.toUpperCase(), image: '/api/placeholder/32/32' }] }
          : task
      ));
    }
  };

  const addSubtask = (taskId) => {
    const newSubtask = { 
      id: Math.max(0, ...tasks.find(t => t.id === taskId).subtasks.map(st => st.id)) + 1, 
      name: '', 
      startDate: '', 
      dueDate: '', 
      status: 'not_started', 
      assignee: null 
    };
    setTasks(tasks.map(task => 
      task.id === taskId 
        ? { ...task, subtasks: [...task.subtasks, newSubtask] }
        : task
    ));
    setEditingSubtask({ taskId, subtaskId: newSubtask.id });
  };

  const updateSubtask = (taskId, subtaskId, updatedSubtask) => {
    setTasks(tasks.map(task => 
      task.id === taskId 
        ? { ...task, subtasks: task.subtasks.map(subtask => 
            subtask.id === subtaskId ? { ...subtask, ...updatedSubtask } : subtask
          )}
        : task
    ));
    setEditingSubtask(null);
  };

  const toggleSubtask = (taskId, subtaskId) => {
    setTasks(tasks.map(task => 
      task.id === taskId 
        ? { ...task, subtasks: task.subtasks.map(subtask => 
            subtask.id === subtaskId ? { ...subtask, status: subtask.status === 'completed' ? 'in_progress' : 'completed' } : subtask
          )}
        : task
    ));
  };

  const deleteSubtask = (taskId, subtaskId) => {
    setTasks(tasks.map(task => 
      task.id === taskId 
        ? { ...task, subtasks: task.subtasks.filter(subtask => subtask.id !== subtaskId) }
        : task
    ));
  };

  return (
    <div className="max-w-4xl mx-auto p-4 font-sans bg-gray-50">
      <h1 className="text-3xl font-bold mb-6 text-gray-800">Managementul Proiectului</h1>
      
      {/* Add new task form */}
      <div className="mb-6 flex items-center space-x-2">
        <input
          type="text"
          placeholder="Nume sarcină"
          value={newTask.name}
          onChange={(e) => setNewTask({...newTask, name: e.target.value})}
          className="border rounded-full p-2 flex-grow"
        />
        <input
          type="date"
          value={newTask.dueDate}
          onChange={(e) => setNewTask({...newTask, dueDate: e.target.value})}
          className="border rounded-full p-2"
        />
        <button onClick={addTask} className="bg-blue-500 text-white rounded-full p-2 hover:bg-blue-600 transition-colors">
          <UserPlus size={24} />
        </button>
      </div>

      {/* Tasks list */}
      <div className="space-y-6">
        {tasks.map(task => (
          <div key={task.id} className={`p-6 rounded-xl shadow-lg ${getStatusColor(task.status, task.dueDate)} border-l-4 relative overflow-hidden`}>
            {/* Task edit and delete buttons */}
            <div className="absolute top-2 right-2 flex space-x-2">
              <button onClick={() => setEditingTask(task.id)} className="text-gray-600 hover:text-blue-500 transition-colors">
                <Edit2 size={18} />
              </button>
              <button onClick={() => deleteTask(task.id)} className="text-gray-600 hover:text-red-500 transition-colors">
                <Trash2 size={18} />
              </button>
            </div>
            
            {editingTask === task.id ? (
              // Task edit form
              <div className="space-y-2">
                <input
                  type="text"
                  value={task.name}
                  onChange={(e) => updateTask(task.id, { name: e.target.value })}
                  className="border rounded-full p-2 w-full"
                />
                <input
                  type="date"
                  value={task.dueDate}
                  onChange={(e) => updateTask(task.id, { dueDate: e.target.value })}
                  className="border rounded-full p-2 w-full"
                />
                <select
                  value={task.status}
                  onChange={(e) => updateTask(task.id, { status: e.target.value })}
                  className="border rounded-full p-2 w-full"
                >
                  <option value="Neînceput">Neînceput</option>
                  <option value="În progres">În progres</option>
                  <option value="Urgent">Urgent</option>
                  <option value="Finalizat">Finalizat</option>
                </select>
                <button onClick={() => setEditingTask(null)} className="bg-green-500 text-white rounded-full p-2 w-full hover:bg-green-600 transition-colors">
                  Salvează
                </button>
              </div>
            ) : (
              // Task display
              <div>
                <h3 className="font-bold text-xl mb-2">{task.name}</h3>
                <p className="text-sm text-gray-600">Termen limită: {task.dueDate}</p>
                <p className="text-sm text-gray-600 mb-4">Status: {task.status}</p>
                
                {/* Task assignees */}
                <div className="flex items-center space-x-2 mb-4">
                  {task.assignees.map((assignee, index) => (
                    <Avatar key={index} className="w-8 h-8">
                      <AvatarImage src={assignee.image} alt={assignee.initials} />
                      <AvatarFallback>{assignee.initials}</AvatarFallback>
                    </Avatar>
                  ))}
                  <button onClick={() => addAssignee(task.id)} className="bg-gray-200 rounded-full p-1 hover:bg-gray-300 transition-colors">
                    <UserPlus size={16} />
                  </button>
                </div>

                {/* Subtasks */}
                <div className="space-y-2 mb-4">
                  {task.subtasks.map(subtask => (
                    <div key={subtask.id} className="flex items-center justify-between">
                      <div className="flex items-center space-x-2">
                        <input
                          type="checkbox"
                          checked={subtask.status === 'completed'}
                          onChange={() => toggleSubtask(task.id, subtask.id)}
                          className="rounded"
                        />
                        <span className={subtask.status === 'completed' ? 'line-through text-gray-500' : ''}>
                          {subtask.name} (până la {subtask.dueDate})
                        </span>
                      </div>
                      <div className="flex items-center space-x-2">
                        {subtask.assignee && (
                          <Avatar className="w-6 h-6">
                            <AvatarImage src={subtask.assignee.image} alt={subtask.assignee.initials} />
                            <AvatarFallback>{subtask.assignee.initials}</AvatarFallback>
                          </Avatar>
                        )}
                        <Dialog>
                          <DialogTrigger asChild>
                            <Button variant="outline" size="sm">
                              <Edit2 size={14} />
                            </Button>
                          </DialogTrigger>
                          <DialogContent className="sm:max-w-[425px]">
                            <DialogHeader>
                              <DialogTitle>Editare mini-sarcină</DialogTitle>
                            </DialogHeader>
                            <div className="grid gap-4 py-4">
                              <div className="grid grid-cols-4 items-center gap-4">
                                <Label htmlFor="name" className="text-right">
                                  Nume
                                </Label>
                                <Input
                                  id="name"
                                  defaultValue={subtask.name}
                                  className="col-span-3"
                                  onChange={(e) => updateSubtask(task.id, subtask.id, { name: e.target.value })}
                                />
                              </div>
                              <div className="grid grid-cols-4 items-center gap-4">
                                <Label htmlFor="startDate" className="text-right">
                                  Data început
                                </Label>
                                <Input
                                  id="startDate"
                                  type="date"
                                  defaultValue={subtask.startDate}
                                  className="col-span-3"
                                  onChange={(e) => updateSubtask(task.id, subtask.id, { startDate: e.target.value })}
                                />
                              </div>
                              <div className="grid grid-cols-4 items-center gap-4">
                                <Label htmlFor="dueDate" className="text-right">
                                  Data sfârșit
                                </Label>
                                <Input
                                  id="dueDate"
                                  type="date"
                                  defaultValue={subtask.dueDate}
                                  className="col-span-3"
                                  onChange={(e) => updateSubtask(task.id, subtask.id, { dueDate: e.target.value })}
                                />
                              </div>
                              <div className="grid grid-cols-4 items-center gap-4">
                                <Label htmlFor="assignee" className="text-right">
                                  Responsabil
                                </Label>
                                <Input
                                  id="assignee"
                                  defaultValue={subtask.assignee?.initials || ''}
                                  className="col-span-3"
                                  onChange={(e) => updateSubtask(task.id, subtask.id, { assignee: { initials: e.target.value.toUpperCase(), image: '/api/placeholder/32/32' } })}
                                />
                              </div>
                            </div>
                          </DialogContent>
                        </Dialog>
                        <Button variant="outline" size="sm" onClick={() => deleteSubtask(task.id, subtask.id)}>
                          <X size={14} />
                        </Button>
                      </div>
                    </div>
                  ))}
                  <button onClick={() => addSubtask(task.id)} className="text-blue-500 hover:text-blue-700 transition-colors flex items-center">
                    <PlusCircle size={16} className="mr-1" /> Adaugă mini-sarcină
                  </button>
                </div>

                {/* Progress bar */}
                <CustomProgressBar subtasks={task.subtasks} />
                <div className="flex justify-between text-xs text-gray-600 mt-1">
                  <span>{task.subtasks[0]?.startDate || 'N/A'}</span>
                  <span>{task.dueDate}</span>
                </div>
              </div>
            )}
          </div>
        ))}
      </div>

      <Alert className="mt-6">
        <AlertDescription>
          Sfat: Folosiți mini-sarcinile pentru a diviza și urmări progresul fiecărei sarcini principale. Puteți adăuga responsabili individuali pentru fiecare mini-sarcină.
        </AlertDescription>
      </Alert>
    </div>
  );
};

export default ProjectPipeline;