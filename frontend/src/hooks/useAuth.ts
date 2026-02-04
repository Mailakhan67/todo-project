// Custom hook for authentication state management
'use client';

import { useState, useEffect } from 'react';
import { AuthState, User } from '../lib/types';
import { apiClient } from '../lib/api-client';
import { getUserSession, storeUserSession, clearUserSession, isAuthenticated } from '../lib/auth';

export const useAuth = () => {
  const [authState, setAuthState] = useState<AuthState>({
    user: null,
    isAuthenticated: false,
    isLoading: true,
    error: null,
  });

  // Check session on mount
  useEffect(() => {
    const initializeAuth = async () => {
      const { user, token } = getUserSession();

      if (user && token) {
        // Verify the session is still valid
        try {
          apiClient.setToken(token);
          const profile = await apiClient.getProfile();

          setAuthState({
            user: profile,
            isAuthenticated: true,
            isLoading: false,
            error: null,
          });
        } catch (error: any) {
          console.error('Session validation failed:', error);

          // Session is invalid, clear it
          clearUserSession();
          apiClient.clearToken();
          setAuthState({
            user: null,
            isAuthenticated: false,
            isLoading: false,
            error: null,
          });
        }
      } else {
        setAuthState({
          user: null,
          isAuthenticated: false,
          isLoading: false,
          error: null,
        });
      }
    };

    initializeAuth();
  }, []);

  const signUp = async (email: string, password: string, name?: string) => {
    setAuthState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      // Call the backend API to register the user
      const response = await apiClient.signUp({ email, password, name });

      // After successful registration, sign in the user automatically
      const signInResult = await signIn(email, password);

      if (signInResult.success) {
        // The signIn function already sets the auth state, so we don't need to do it again
        return { success: true };
      } else {
        throw new Error(signInResult.error || 'Sign in failed after registration');
      }
    } catch (error: any) {
      const errorMessage = error.message || 'Sign up failed';
      setAuthState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));
      return { success: false, error: errorMessage };
    }
  };

  const signIn = async (email: string, password: string) => {
    setAuthState(prev => ({ ...prev, isLoading: true, error: null }));

    try {
      // Call the backend API to authenticate the user
      const response = await apiClient.signIn({ email, password });

      // Extract token from the response
      const token = response.access_token;

      if (!response.user) {
        throw new Error('User data is missing from the sign-in response.');
      }

      // Store the user session with the received token
      storeUserSession(response.user, token);

      setAuthState({
        user: response.user,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      });

      return { success: true };
    } catch (error: any) {
      const errorMessage = error.message || 'Sign in failed';
      setAuthState(prev => ({
        ...prev,
        isLoading: false,
        error: errorMessage,
      }));
      return { success: false, error: errorMessage };
    }
  };

  const signOut = async () => {
    try {
      await apiClient.signOut();
    } catch (error: any) {
      // Even if API signout fails, we should clear local session
      console.error('Sign out API call failed:', error);
      const errorMessage = error.message || 'Sign out failed';
      setAuthState(prev => ({
        ...prev,
        error: errorMessage,
      }));
    } finally {
      clearUserSession();
      apiClient.clearToken();

      setAuthState({
        user: null,
        isAuthenticated: false,
        isLoading: false,
        error: null,
      });
    }
  };

  return {
    ...authState,
    signUp,
    signIn,
    signOut,
  };
};