"use client";

import { useEffect, useState } from "react";
import { createClient } from "@/lib/supabase/client";
import { useAuthStore } from "@/stores/authStore";

export function useAuth() {
  const { user, session, setAuth, clearAuth } = useAuthStore();
  const [loading, setLoading] = useState(true);
  const supabase = createClient();

  useEffect(() => {
    const getSession = async () => {
      const {
        data: { session },
      } = await supabase.auth.getSession();
      if (session) {
        setAuth(session.user, session);
      }
      setLoading(false);
    };
    getSession();

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event: string, session: any) => {
      if (session) {
        setAuth(session.user, session);
      } else {
        clearAuth();
      }
      setLoading(false);
    });

    return () => subscription.unsubscribe();
  }, [supabase, setAuth, clearAuth]);

  const signInWithGoogle = async () => {
    const { error } = await supabase.auth.signInWithOAuth({
      provider: "google",
      options: {
        redirectTo: `${window.location.origin}/ja/callback`,
      },
    });
    if (error) throw error;
  };

  const signOut = async () => {
    const { error } = await supabase.auth.signOut();
    if (error) throw error;
    clearAuth();
  };

  return {
    user,
    session,
    loading,
    signInWithGoogle,
    signOut,
    isAuthenticated: !!user,
  };
}
