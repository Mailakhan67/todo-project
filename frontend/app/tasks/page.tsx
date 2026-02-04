// Tasks list page
'use client';

import AuthGuard from '@/src/components/AuthGuard';
import TaskList from '@/src/components/TaskList';

const TasksPage = () => {
  return (
    <AuthGuard requireAuth={true}>
      <TaskList />
    </AuthGuard>
  );
};

export default TasksPage;