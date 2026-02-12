export interface UserPublic {
  id: string;
  username: string;
  avatar_url?: string | null;
}

export interface Review {
  id: string;
  bean_id: string;
  user: UserPublic;
  rating: number;
  flavor_notes: string[];
  brew_method?: string | null;
  comment?: string | null;
  created_at: string;
  updated_at: string;
}

export interface ReviewCreate {
  rating: number;
  flavor_notes?: string[];
  brew_method?: string;
  comment?: string;
}

export interface ReviewUpdate {
  rating?: number;
  flavor_notes?: string[];
  brew_method?: string;
  comment?: string;
}
