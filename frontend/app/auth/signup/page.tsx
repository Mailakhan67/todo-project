// Sign-up page component
'use client';

import AuthGuard from '@/src/components/AuthGuard';
import SignUpForm from '@/src/components/SignUpForm';

const SignUpPage = () => {
  return (
    <AuthGuard requireAuth={false}>
      <SignUpForm />
    </AuthGuard>
  );
};

export default SignUpPage;