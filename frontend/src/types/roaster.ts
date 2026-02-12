export interface RoasterListItem {
  id: string;
  name: string;
  name_en?: string | null;
  location?: string | null;
  bean_count: number;
  avg_rating?: number | null;
  image_url?: string | null;
}

export interface RoasterBeanSummary {
  id: string;
  name: string;
  avg_rating?: number | null;
  review_count: number;
}

export interface RoasterDetail {
  id: string;
  name: string;
  name_en?: string | null;
  description?: string | null;
  description_en?: string | null;
  location?: string | null;
  prefecture?: string | null;
  website_url?: string | null;
  instagram_url?: string | null;
  image_url?: string | null;
  bean_count: number;
  avg_rating?: number | null;
  beans: RoasterBeanSummary[];
  created_at: string;
}
