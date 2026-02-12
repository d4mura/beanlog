"use client";

import { use, useEffect, useState } from "react";
import { useTranslations, useLocale } from "next-intl";
import { useRouter } from "@/i18n/routing";
import { useAuth } from "@/hooks/useAuth";
import { useBean } from "@/hooks/useBean";
import { useCreateReview } from "@/hooks/useReview";
import ReviewForm from "@/components/reviews/ReviewForm";
import { fetchFlavors, type FlavorNote } from "@/lib/api/master";

export default function WriteReviewPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = use(params);
  const t = useTranslations();
  const locale = useLocale();
  const router = useRouter();
  const { isAuthenticated, loading: authLoading } = useAuth();
  const { data: beanData } = useBean(id);
  const createReview = useCreateReview(id);
  const [flavors, setFlavors] = useState<FlavorNote[]>([]);

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [authLoading, isAuthenticated, router]);

  useEffect(() => {
    fetchFlavors().then((res) => setFlavors(res.data));
  }, []);

  const handleSubmit = async (data: any) => {
    try {
      await createReview.mutateAsync(data);
      router.push(`/beans/${id}`);
    } catch (error) {
      console.error("Failed to create review:", error);
    }
  };

  if (authLoading) {
    return <div className="text-center py-12">{t("common.loading")}</div>;
  }

  const beanName =
    locale === "en" && beanData?.data?.name_en
      ? beanData.data.name_en
      : beanData?.data?.name;

  const flavorItems = flavors.map((f) => ({
    slug: f.slug,
    name: locale === "en" ? f.name_en : f.name,
    category: locale === "en" ? f.category_en : f.category,
  }));

  return (
    <div className="max-w-lg mx-auto">
      <h1 className="text-xl font-bold text-stone-800 mb-2">
        {t("reviews.writeReview")}
      </h1>
      {beanName && (
        <p className="text-sm text-stone-500 mb-6">{beanName}</p>
      )}
      <ReviewForm
        flavors={flavorItems}
        onSubmit={handleSubmit}
        isSubmitting={createReview.isPending}
      />
    </div>
  );
}
