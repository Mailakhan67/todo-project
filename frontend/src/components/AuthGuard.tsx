// AuthGuard component to protect routes
'use client';

import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { useAuth } from '../hooks/useAuth';

interface AuthGuardProps {
  children: React.ReactNode;
  requireAuth?: boolean; // If true, requires authentication; if false, redirects away if authenticated
}

const AuthGuard = ({ children, requireAuth = true }: AuthGuardProps) => {
  const { isAuthenticated, isLoading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!isLoading) {
      // If route requires auth but user is not authenticated
      if (requireAuth && !isAuthenticated) {
        router.push('/auth/signin');
      }
      
      // If route should not be accessible when authenticated (e.g., sign-in page)
      if (!requireAuth && isAuthenticated) {
        router.push('/tasks');
      }
    }
  }, [isAuthenticated, isLoading, requireAuth, router]);

  // Show nothing while checking auth status
  if (isLoading) {
    return (
      <div className="flex justify-center items-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-t-2 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  // If auth requirement is met, render children
  const shouldRender = 
    (requireAuth && isAuthenticated) || 
    (!requireAuth && !isAuthenticated);

  return shouldRender ? <>{children}</> : null;
};

export default AuthGuard;