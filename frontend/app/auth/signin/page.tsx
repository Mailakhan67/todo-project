// Sign-in page component
'use client';

import AuthGuard from '@/src/components/AuthGuard';
import SignInForm from '@/src/components/SignInForm';

const SignInPage = () => {
  return (
    <AuthGuard requireAuth={false}>
      <SignInForm />
    </AuthGuard>
  );
};

export default SignInPage;