import type { Review, ReviewCreate, ReviewUpdate } from "@/types/review";
import type { PaginatedResponse, SingleResponse, DeleteResponse } from "@/types/api";
import { apiFetch } from "./client";

export async function fetchBeanReviews(
  beanId: string,
  page = 1,
  perPage = 20
): Promise<PaginatedResponse<Review>> {
  return apiFetch<PaginatedResponse<Review>>(
    `/beans/${beanId}/reviews?page=${page}&per_page=${perPage}`
  );
}

export async function fetchUserReviews(
  userId: string,
  page = 1,
  perPage = 20
): Promise<PaginatedResponse<Review>> {
  return apiFetch<PaginatedResponse<Review>>(
    `/users/${userId}/reviews?page=${page}&per_page=${perPage}`
  );
}

export async function createReview(
  beanId: string,
  data: ReviewCreate,
  token: string
): Promise<SingleResponse<Review>> {
  return apiFetch<SingleResponse<Review>>(
    `/beans/${beanId}/reviews`,
    { method: "POST", body: JSON.stringify(data) },
    token
  );
}

export async function updateReview(
  reviewId: string,
  data: ReviewUpdate,
  token: string
): Promise<SingleResponse<Review>> {
  return apiFetch<SingleResponse<Review>>(
    `/reviews/${reviewId}`,
    { method: "PATCH", body: JSON.stringify(data) },
    token
  );
}

export async function deleteReview(
  reviewId: string,
  token: string
): Promise<DeleteResponse> {
  return apiFetch<DeleteResponse>(
    `/reviews/${reviewId}`,
    { method: "DELETE" },
    token
  );
}
