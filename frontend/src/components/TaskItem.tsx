// TaskItem component
'use client';

import React, { useState } from 'react';
import { Task } from '../lib/types';
import { apiClient } from '../lib/api-client';
import LoadingSpinner from './LoadingSpinner';

interface TaskItemProps {
  task: Task;
  onTaskUpdate?: (updatedTask: Task) => void;
  onTaskDelete?: (taskId: string) => void;
}

const TaskItem: React.FC<TaskItemProps> = ({ task, onTaskUpdate, onTaskDelete }) => {
  const [isDeleting, setIsDeleting] = useState(false);
  const [isCompleting, setIsCompleting] = useState(false);
  const [localTask, setLocalTask] = useState(task);

  const handleToggleComplete = async () => {
    if (isCompleting) return;
    
    setIsCompleting(true);
    try {
      const updatedTask = await apiClient.toggleTaskCompletion(localTask.id, !localTask.completed);
      setLocalTask(updatedTask);
      if (onTaskUpdate) {
        onTaskUpdate(updatedTask);
      }
    } catch (error) {
      console.error('Failed to update task completion:', error);
    } finally {
      setIsCompleting(false);
    }
  };

  const handleDelete = async () => {
    if (isDeleting) return;
    
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }
    
    setIsDeleting(true);
    try {
      await apiClient.deleteTask(localTask.id);
      if (onTaskDelete) {
        onTaskDelete(localTask.id);
      }
    } catch (error) {
      console.error('Failed to delete task:', error);
      setIsDeleting(false);
    }
  };

  return (
    <div className={`border rounded-lg p-4 mb-3 transition-all duration-200 ${localTask.completed ? 'bg-green-50 border-green-200' : 'bg-white border-gray-200'}`}>
      <div className="flex items-start">
        <input
          type="checkbox"
          checked={localTask.completed}
          onChange={handleToggleComplete}
          disabled={isCompleting}
          className="mt-1 h-5 w-5 text-blue-600 rounded focus:ring-blue-500"
        />
        
        <div className="ml-3 flex-1">
          <h3 className={`text-lg font-medium ${localTask.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
            {localTask.title}
          </h3>
          
          {localTask.description && (
            <p className={`mt-1 text-gray-600 ${localTask.completed ? 'line-through' : ''}`}>
              {localTask.description}
            </p>
          )}
          
          <div className="mt-2 flex items-center text-sm text-gray-500">
            <span>Created: {new Date(localTask.createdAt).toLocaleDateString()}</span>
            {localTask.updatedAt !== localTask.createdAt && (
              <span className="ml-3">Updated: {new Date(localTask.updatedAt).toLocaleDateString()}</span>
            )}
          </div>
        </div>
        
        <div className="flex space-x-2">
          <a
            href={`/tasks/${localTask.id}`}
            className="text-green-600 hover:text-green-900"
            title="View Task"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M10 12a2 2 0 100-4 2 2 0 000 4z" />
              <path fillRule="evenodd" d="M.458 10C1.732 5.943 5.522 3 10 3s8.268 2.943 9.542 7c-1.274 4.057-5.064 7-9.542 7S1.732 14.057.458 10zM14 10a4 4 0 11-8 0 4 4 0 018 0z" clipRule="evenodd" />
            </svg>
          </a>

          <a
            href={`/tasks/${localTask.id}/edit`}
            className="text-blue-600 hover:text-blue-900"
            title="Edit Task"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
            </svg>
          </a>

          <button
            onClick={handleDelete}
            disabled={isDeleting}
            className="text-red-600 hover:text-red-900 disabled:opacity-50"
            title="Delete Task"
          >
            {isDeleting ? (
              <LoadingSpinner size="sm" />
            ) : (
              <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clipRule="evenodd" />
              </svg>
            )}
          </button>
        </div>
      </div>
    </div>
  );
};

export default TaskItem;