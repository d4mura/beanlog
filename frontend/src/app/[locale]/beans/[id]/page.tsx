"use client";

import { use } from "react";
import { useTranslations } from "next-intl";
import { useBean } from "@/hooks/useBean";
import { useBeanReviews } from "@/hooks/useReview";
import BeanDetailView from "@/components/beans/BeanDetail";
import ReviewList from "@/components/reviews/ReviewList";

export default function BeanDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = use(params);
  const t = useTranslations();
  const { data: beanData, isLoading: beanLoading } = useBean(id);
  const { data: reviewsData, isLoading: reviewsLoading } = useBeanReviews(id);

  if (beanLoading) {
    return (
      <div className="animate-pulse space-y-4">
        <div className="aspect-[16/9] bg-stone-100 rounded-xl" />
        <div className="h-8 bg-stone-100 rounded w-3/4" />
        <div className="h-4 bg-stone-100 rounded w-1/2" />
      </div>
    );
  }

  if (!beanData?.data) {
    return (
      <div className="text-center py-12">
        <p className="text-stone-500">{t("common.notFound")}</p>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      <BeanDetailView bean={beanData.data} />

      <section>
        <h2 className="text-lg font-bold text-stone-800 mb-4">
          {t("reviews.title")} ({beanData.data.review_count})
        </h2>
        <ReviewList
          reviews={reviewsData?.data || []}
          loading={reviewsLoading}
        />
      </section>
    </div>
  );
}
