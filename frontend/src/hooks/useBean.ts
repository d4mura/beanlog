"use client";

import { useQuery } from "@tanstack/react-query";
import { fetchBeans, fetchBean } from "@/lib/api/beans";

export function useBeans(params: Record<string, string | number | undefined> = {}) {
  return useQuery({
    queryKey: ["beans", params],
    queryFn: () => fetchBeans(params),
  });
}

export function useBean(id: string) {
  return useQuery({
    queryKey: ["bean", id],
    queryFn: () => fetchBean(id),
    enabled: !!id,
  });
}
