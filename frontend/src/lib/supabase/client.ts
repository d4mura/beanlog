"use client";

import { createBrowserClient } from "@supabase/ssr";

export function createClient() {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL;
  const key = process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY;

  if (!url || !key) {
    // Return a stub that won't crash in dev mode without Supabase
    return {
      auth: {
        getSession: async () => ({ data: { session: null }, error: null }),
        getUser: async () => ({ data: { user: null }, error: null }),
        onAuthStateChange: (_event: string, _callback: unknown) => ({
          data: { subscription: { unsubscribe: () => {} } },
        }),
        signInWithOAuth: async () => ({ error: new Error("Supabase not configured") }),
        signOut: async () => ({ error: null }),
        exchangeCodeForSession: async () => ({ error: new Error("Supabase not configured") }),
      },
    } as any;
  }

  return createBrowserClient(url, key);
}
