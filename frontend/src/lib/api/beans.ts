import type { BeanDetail, BeanListItem } from "@/types/bean";
import type { PaginatedResponse, SingleResponse } from "@/types/api";
import { apiFetch } from "./client";

interface BeanListParams {
  q?: string;
  origin?: string;
  roast_level?: string;
  process?: string;
  flavor?: string;
  roaster_id?: string;
  sort?: string;
  page?: number;
  per_page?: number;
}

export async function fetchBeans(
  params: BeanListParams = {}
): Promise<PaginatedResponse<BeanListItem>> {
  const searchParams = new URLSearchParams();
  Object.entries(params).forEach(([key, value]) => {
    if (value !== undefined && value !== null && value !== "") {
      searchParams.set(key, String(value));
    }
  });
  const query = searchParams.toString();
  return apiFetch<PaginatedResponse<BeanListItem>>(
    `/beans${query ? `?${query}` : ""}`
  );
}

export async function fetchBean(id: string): Promise<SingleResponse<BeanDetail>> {
  return apiFetch<SingleResponse<BeanDetail>>(`/beans/${id}`);
}

export async function fetchBeanByBarcode(
  code: string
): Promise<SingleResponse<BeanDetail>> {
  return apiFetch<SingleResponse<BeanDetail>>(`/beans/barcode/${code}`);
}
