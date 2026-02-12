"use client";

import { useTranslations } from "next-intl";
import ReviewCard from "./ReviewCard";
import type { Review } from "@/types/review";

interface ReviewListProps {
  reviews: Review[];
  loading?: boolean;
}

export default function ReviewList({ reviews, loading }: ReviewListProps) {
  const t = useTranslations();

  if (loading) {
    return (
      <div className="space-y-4">
        {Array.from({ length: 3 }).map((_, i) => (
          <div key={i} className="animate-pulse border-b border-stone-100 py-4">
            <div className="flex gap-2 mb-2">
              <div className="w-8 h-8 rounded-full bg-stone-100" />
              <div className="space-y-1">
                <div className="h-3 w-24 bg-stone-100 rounded" />
                <div className="h-2 w-16 bg-stone-100 rounded" />
              </div>
            </div>
            <div className="h-3 w-3/4 bg-stone-100 rounded" />
          </div>
        ))}
      </div>
    );
  }

  if (reviews.length === 0) {
    return (
      <div className="text-center py-8 text-stone-500">
        <p>{t("beans.noReviews")}</p>
      </div>
    );
  }

  return (
    <div>
      {reviews.map((review) => (
        <ReviewCard key={review.id} review={review} />
      ))}
    </div>
  );
}
