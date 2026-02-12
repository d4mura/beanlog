"use client";

import { useTranslations } from "next-intl";
import Badge from "@/components/ui/Badge";
import type { Review } from "@/types/review";

interface ReviewCardProps {
  review: Review;
}

export default function ReviewCard({ review }: ReviewCardProps) {
  const t = useTranslations();

  const stars = "★".repeat(Math.round(review.rating)) +
    "☆".repeat(5 - Math.round(review.rating));

  return (
    <div className="border-b border-stone-100 py-4 last:border-0">
      <div className="flex items-start justify-between mb-2">
        <div className="flex items-center gap-2">
          <div className="w-8 h-8 rounded-full bg-amber-200 flex items-center justify-center text-xs font-medium text-amber-900">
            {review.user.username[0]?.toUpperCase()}
          </div>
          <div>
            <p className="text-sm font-medium text-stone-800">
              {review.user.username}
            </p>
            <p className="text-xs text-stone-400">
              {new Date(review.created_at).toLocaleDateString()}
            </p>
          </div>
        </div>
        <div className="flex items-center gap-1">
          <span className="text-amber-500 text-sm">{stars}</span>
          <span className="text-sm font-semibold text-stone-700 ml-1">
            {review.rating.toFixed(1)}
          </span>
        </div>
      </div>

      {review.brew_method && (
        <p className="text-xs text-stone-500 mb-1">
          {t("reviews.brewMethod")}: {t(`brewMethods.${review.brew_method}` as any)}
        </p>
      )}

      {review.flavor_notes.length > 0 && (
        <div className="flex flex-wrap gap-1 mb-2">
          {review.flavor_notes.map((slug) => (
            <Badge key={slug} variant="secondary">
              {slug}
            </Badge>
          ))}
        </div>
      )}

      {review.comment && (
        <p className="text-sm text-stone-600 leading-relaxed">{review.comment}</p>
      )}
    </div>
  );
}
