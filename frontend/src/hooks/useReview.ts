"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import {
  fetchBeanReviews,
  createReview,
  updateReview,
  deleteReview,
} from "@/lib/api/reviews";
import type { ReviewCreate, ReviewUpdate } from "@/types/review";
import { useAuthStore } from "@/stores/authStore";

export function useBeanReviews(beanId: string, page = 1) {
  return useQuery({
    queryKey: ["reviews", beanId, page],
    queryFn: () => fetchBeanReviews(beanId, page),
    enabled: !!beanId,
  });
}

export function useCreateReview(beanId: string) {
  const queryClient = useQueryClient();
  const { session } = useAuthStore();

  return useMutation({
    mutationFn: (data: ReviewCreate) =>
      createReview(beanId, data, session?.access_token || ""),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["reviews", beanId] });
      queryClient.invalidateQueries({ queryKey: ["bean", beanId] });
    },
  });
}

export function useUpdateReview(reviewId: string, beanId: string) {
  const queryClient = useQueryClient();
  const { session } = useAuthStore();

  return useMutation({
    mutationFn: (data: ReviewUpdate) =>
      updateReview(reviewId, data, session?.access_token || ""),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["reviews", beanId] });
      queryClient.invalidateQueries({ queryKey: ["bean", beanId] });
    },
  });
}

export function useDeleteReview(reviewId: string, beanId: string) {
  const queryClient = useQueryClient();
  const { session } = useAuthStore();

  return useMutation({
    mutationFn: () => deleteReview(reviewId, session?.access_token || ""),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["reviews", beanId] });
      queryClient.invalidateQueries({ queryKey: ["bean", beanId] });
    },
  });
}
