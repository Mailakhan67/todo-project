// Individual task view page
'use client';

import { useState, useEffect } from 'react';
import { useParams, useRouter } from 'next/navigation';
import { Task } from '../../../src/lib/types';
import { apiClient } from '../../../src/lib/api-client';
import AuthGuard from '../../../src/components/AuthGuard';
import LoadingSpinner from '../../../src/components/LoadingSpinner';
import ErrorMessage from '../../../src/components/ErrorMessage';

const ViewTaskPage = () => {
  const { id } = useParams();
  const router = useRouter();
  const [task, setTask] = useState<Task | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTask = async () => {
      try {
        setIsLoading(true);
        setError(null);
        const fetchedTask = await apiClient.getTask(id as string);
        setTask(fetchedTask);
      } catch (err: any) {
        console.error('Error fetching task:', err);
        setError(err.message || 'Failed to fetch task');
      } finally {
        setIsLoading(false);
      }
    };

    if (id) {
      fetchTask();
    } else {
      setError('Task ID is missing');
      setIsLoading(false);
    }
  }, [id]);

  const handleEdit = () => {
    router.push(`/tasks/${id}/edit`);
  };

  const handleBack = () => {
    router.back();
  };

  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-64">
        <LoadingSpinner size="lg" />
      </div>
    );
  }

  if (error) {
    return (
      <div className="max-w-2xl mx-auto p-4">
        <ErrorMessage message={error} />
        <div className="mt-4">
          <a
            href="/tasks"
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Back to Tasks
          </a>
        </div>
      </div>
    );
  }

  if (!task) {
    return (
      <div className="max-w-2xl mx-auto p-4">
        <ErrorMessage message="Task not found" />
        <div className="mt-4">
          <a
            href="/tasks"
            className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
          >
            Back to Tasks
          </a>
        </div>
      </div>
    );
  }

  return (
    <AuthGuard requireAuth={true}>
      <div className="max-w-2xl mx-auto p-4">
        <div className="mb-6">
          <button
            onClick={handleBack}
            className="flex items-center text-blue-600 hover:text-blue-800 mb-4"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 mr-1" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M9.707 16.707a1 1 0 01-1.414 0l-6-6a1 1 0 010-1.414l6-6a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l4.293 4.293a1 1 0 010 1.414z" clipRule="evenodd" />
            </svg>
            Back to Tasks
          </button>

          <div className="flex justify-between items-start">
            <h1 className="text-2xl font-bold text-gray-800">Task Details</h1>
            <button
              onClick={handleEdit}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Edit Task
            </button>
          </div>
        </div>

        <div className={`border rounded-lg p-6 ${task.completed ? 'bg-green-50 border-green-200' : 'bg-white border-gray-200'}`}>
          <div className="flex items-start mb-4">
            <input
              type="checkbox"
              checked={task.completed}
              readOnly
              className="mt-1 h-5 w-5 text-blue-600 rounded focus:ring-blue-500 cursor-default"
            />
            <div className="ml-3">
              <h2 className={`text-xl font-semibold ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                {task.title}
              </h2>
            </div>
          </div>

          {task.description && (
            <div className="mb-6">
              <h3 className="text-sm font-medium text-gray-500 mb-1">Description</h3>
              <p className={`text-gray-700 ${task.completed ? 'line-through' : ''}`}>
                {task.description}
              </p>
            </div>
          )}

          <div className="grid grid-cols-2 gap-4 mb-6">
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">Status</h3>
              <p className={`font-medium ${task.completed ? 'text-green-600' : 'text-yellow-600'}`}>
                {task.completed ? 'Completed' : 'Pending'}
              </p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">Created</h3>
              <p className="text-gray-700">
                {new Date(task.createdAt).toLocaleString()}
              </p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">Last Updated</h3>
              <p className="text-gray-700">
                {new Date(task.updatedAt).toLocaleString()}
              </p>
            </div>
            <div>
              <h3 className="text-sm font-medium text-gray-500 mb-1">ID</h3>
              <p className="text-gray-700 font-mono text-sm">
                {task.id}
              </p>
            </div>
          </div>

          <div className="flex space-x-3">
            <button
              onClick={handleEdit}
              className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              Edit Task
            </button>

            <button
              onClick={handleBack}
              className="px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 focus:outline-none focus:ring-2 focus:ring-gray-500"
            >
              Back to Tasks
            </button>
          </div>
        </div>
      </div>
    </AuthGuard>
  );
};

export default ViewTaskPage;