// Edit task page
'use client';

import { useEffect, useState } from 'react';
import { useParams } from 'next/navigation';
import { Task } from '@/src/lib/types';
import { apiClient } from '@/src/lib/api-client';
import AuthGuard from '@/src/components/AuthGuard';
import TaskForm from '@/src/components/TaskForm';
import LoadingSpinner from '@/src/components/LoadingSpinner';
import ErrorMessage from '@/src/components/ErrorMessage';

const EditTaskPage = () => {
  const params = useParams();
  const taskId = params.id as string;
  const [task, setTask] = useState<Task | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchTask = async () => {
      try {
        setLoading(true);
        setError(null); // Clear previous errors
        const fetchedTask = await apiClient.getTask(taskId);
        setTask(fetchedTask);
      } catch (err: any) {
        console.error('Error fetching task:', err);
        setError(err.message || 'Failed to fetch task');
      } finally {
        setLoading(false);
      }
    };

    if (taskId) {
      fetchTask();
    } else {
      setError('Task ID is missing');
      setLoading(false);
    }
  }, [taskId]);

  if (loading) {
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
      <TaskForm taskId={task.id} initialData={task} />
    </AuthGuard>
  );
};

export default EditTaskPage;