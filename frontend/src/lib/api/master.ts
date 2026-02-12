import { apiFetch } from "./client";

export interface FlavorNote {
  id: string;
  slug: string;
  name: string;
  name_en: string;
  category: string;
  category_en: string;
  sort_order: number;
}

export interface Origin {
  id: string;
  country_code: string;
  name: string;
  name_en: string;
  region?: string;
  region_en?: string;
}

export interface MasterItem {
  value: string;
  name: string;
  name_en: string;
}

export async function fetchOrigins(): Promise<{ data: Origin[] }> {
  return apiFetch<{ data: Origin[] }>("/master/origins");
}

export async function fetchFlavors(): Promise<{ data: FlavorNote[] }> {
  return apiFetch<{ data: FlavorNote[] }>("/master/flavors");
}

export async function fetchProcesses(): Promise<{ data: MasterItem[] }> {
  return apiFetch<{ data: MasterItem[] }>("/master/processes");
}

export async function fetchRoastLevels(): Promise<{ data: MasterItem[] }> {
  return apiFetch<{ data: MasterItem[] }>("/master/roast-levels");
}

export async function fetchBrewMethods(): Promise<{ data: MasterItem[] }> {
  return apiFetch<{ data: MasterItem[] }>("/master/brew-methods");
}
