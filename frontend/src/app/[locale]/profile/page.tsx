"use client";

import { useEffect } from "react";
import { useTranslations } from "next-intl";
import { useRouter } from "@/i18n/routing";
import { useAuth } from "@/hooks/useAuth";
import { useQuery } from "@tanstack/react-query";
import { fetchUserReviews } from "@/lib/api/reviews";
import ReviewList from "@/components/reviews/ReviewList";
import Button from "@/components/ui/Button";
import Card, { CardContent } from "@/components/ui/Card";

export default function ProfilePage() {
  const t = useTranslations();
  const router = useRouter();
  const { user, isAuthenticated, loading: authLoading, signOut } = useAuth();

  useEffect(() => {
    if (!authLoading && !isAuthenticated) {
      router.push("/login");
    }
  }, [authLoading, isAuthenticated, router]);

  const { data: reviewsData, isLoading: reviewsLoading } = useQuery({
    queryKey: ["userReviews", user?.id],
    queryFn: () => fetchUserReviews(user!.id),
    enabled: !!user?.id,
  });

  if (authLoading) {
    return <div className="text-center py-12">{t("common.loading")}</div>;
  }

  if (!user) return null;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-stone-800">
        {t("profile.title")}
      </h1>

      {/* Profile Card */}
      <Card>
        <CardContent className="p-6">
          <div className="flex items-center gap-4">
            <div className="w-16 h-16 rounded-full bg-amber-200 flex items-center justify-center text-2xl font-bold text-amber-900">
              {user.email?.[0]?.toUpperCase() || "U"}
            </div>
            <div>
              <p className="font-semibold text-stone-800">{user.email}</p>
              <p className="text-sm text-stone-500">
                {t("profile.myReviews")}: {reviewsData?.meta?.total || 0}
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Reviews */}
      <section>
        <h2 className="text-lg font-bold text-stone-800 mb-4">
          {t("profile.myReviews")}
        </h2>
        <ReviewList
          reviews={reviewsData?.data || []}
          loading={reviewsLoading}
        />
      </section>

      {/* Actions */}
      <Button variant="outline" onClick={signOut} className="w-full">
        {t("common.logout")}
      </Button>
    </div>
  );
}
