export interface RoasterSummary {
  id: string;
  name: string;
  name_en?: string | null;
}

export interface OriginInfo {
  code: string;
  name: string;
  name_en: string;
  region?: string | null;
  region_en?: string | null;
}

export interface BeanListItem {
  id: string;
  name: string;
  name_en?: string | null;
  roaster?: RoasterSummary | null;
  origin?: OriginInfo | null;
  roast_level?: string | null;
  process?: string | null;
  flavor_notes: string[];
  avg_rating?: number | null;
  review_count: number;
  image_url?: string | null;
  created_at: string;
}

export interface RatingDistribution {
  five: number;
  four: number;
  three: number;
  two: number;
  one: number;
}

export interface BeanDetail extends BeanListItem {
  description?: string | null;
  description_en?: string | null;
  variety?: string | null;
  altitude_min?: number | null;
  altitude_max?: number | null;
  barcode?: string | null;
  rating_distribution?: RatingDistribution | null;
  purchase_url?: string | null;
  updated_at: string;
}
