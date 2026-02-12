"use client";

import { use } from "react";
import { useTranslations, useLocale } from "next-intl";
import { useQuery } from "@tanstack/react-query";
import { fetchRoaster } from "@/lib/api/roasters";
import { Link } from "@/i18n/routing";
import Card, { CardContent } from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import Button from "@/components/ui/Button";

export default function RoasterDetailPage({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = use(params);
  const t = useTranslations();
  const locale = useLocale();
  const { data, isLoading } = useQuery({
    queryKey: ["roaster", id],
    queryFn: () => fetchRoaster(id),
  });

  if (isLoading) {
    return (
      <div className="animate-pulse space-y-4">
        <div className="h-8 bg-stone-100 rounded w-1/2" />
        <div className="h-4 bg-stone-100 rounded w-1/3" />
      </div>
    );
  }

  const roaster = data?.data;
  if (!roaster) {
    return (
      <div className="text-center py-12">
        <p className="text-stone-500">{t("common.notFound")}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex items-start gap-4">
        <div className="w-20 h-20 rounded-xl bg-amber-50 flex items-center justify-center flex-shrink-0 overflow-hidden">
          {roaster.image_url ? (
            <img
              src={roaster.image_url}
              alt={roaster.name}
              className="w-full h-full object-cover"
            />
          ) : (
            <span className="text-3xl">🏭</span>
          )}
        </div>
        <div>
          <h1 className="text-xl font-bold text-stone-900">{roaster.name}</h1>
          {roaster.location && (
            <p className="text-sm text-stone-500">{roaster.location}</p>
          )}
          <div className="flex gap-3 mt-2">
            <Badge variant="primary">
              {t("roasters.beanCount", { count: roaster.bean_count })}
            </Badge>
            {roaster.avg_rating != null && (
              <Badge variant="secondary">★ {roaster.avg_rating.toFixed(1)}</Badge>
            )}
          </div>
        </div>
      </div>

      {/* Description */}
      {roaster.description && (
        <p className="text-stone-600 text-sm leading-relaxed">
          {locale === "en" && roaster.description_en
            ? roaster.description_en
            : roaster.description}
        </p>
      )}

      {/* Links */}
      <div className="flex gap-3">
        {roaster.website_url && (
          <a href={roaster.website_url} target="_blank" rel="noopener noreferrer">
            <Button variant="outline" size="sm">
              🌐 {t("roasters.website")}
            </Button>
          </a>
        )}
        {roaster.instagram_url && (
          <a href={roaster.instagram_url} target="_blank" rel="noopener noreferrer">
            <Button variant="outline" size="sm">
              📷 {t("roasters.instagram")}
            </Button>
          </a>
        )}
      </div>

      {/* Beans */}
      {roaster.beans.length > 0 && (
        <section>
          <h2 className="text-lg font-bold text-stone-800 mb-3">
            {t("roasters.beans")}
          </h2>
          <div className="space-y-2">
            {roaster.beans.map((bean) => (
              <Link key={bean.id} href={`/beans/${bean.id}`}>
                <Card hover>
                  <CardContent>
                    <div className="flex items-center justify-between">
                      <div>
                        <p className="text-sm font-medium text-stone-800">
                          {bean.name}
                        </p>
                        <p className="text-xs text-stone-400">
                          {t("beans.reviewCount", { count: bean.review_count })}
                        </p>
                      </div>
                      {bean.avg_rating != null && (
                        <div className="flex items-center gap-1">
                          <span className="text-amber-500">★</span>
                          <span className="text-sm font-medium">
                            {bean.avg_rating.toFixed(1)}
                          </span>
                        </div>
                      )}
                    </div>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        </section>
      )}
    </div>
  );
}
