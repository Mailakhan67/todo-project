// Create new task page
'use client';

import AuthGuard from '@/src/components/AuthGuard';
import TaskForm from '@/src/components/TaskForm';

const NewTaskPage = () => {
  return (
    <AuthGuard requireAuth={true}>
      <TaskForm />
    </AuthGuard>
  );
};

export default NewTaskPage;