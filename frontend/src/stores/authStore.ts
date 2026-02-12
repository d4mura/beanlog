"use client";

import { create } from "zustand";

interface AuthState {
  user: any | null;
  session: any | null;
  setAuth: (user: any, session: any) => void;
  clearAuth: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  session: null,
  setAuth: (user, session) => set({ user, session }),
  clearAuth: () => set({ user: null, session: null }),
}));
