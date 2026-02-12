import type { RoasterListItem, RoasterDetail } from "@/types/roaster";
import type { PaginatedResponse, SingleResponse } from "@/types/api";
import { apiFetch } from "./client";

interface RoasterListParams {
  q?: string;
  page?: number;
  per_page?: number;
}

export async function fetchRoasters(
  params: RoasterListParams = {}
): Promise<PaginatedResponse<RoasterListItem>> {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      searchParams.set(key, String(value));
    }
  });
  const query = searchParams.toString();
  return apiFetch<PaginatedResponse<RoasterListItem>>(
    `/roasters${query ? `?${query}` : ""}`
  );
}

export async function fetchRoaster(
  id: string
): Promise<SingleResponse<RoasterDetail>> {
  return apiFetch<SingleResponse<RoasterDetail>>(`/roasters/${id}`);
}
