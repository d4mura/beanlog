"use client";

import { useLocale, useTranslations } from "next-intl";
import { Link } from "@/i18n/routing";
import Card, { CardContent } from "@/components/ui/Card";
import Badge from "@/components/ui/Badge";
import type { BeanListItem } from "@/types/bean";

interface BeanCardProps {
  bean: BeanListItem;
}

export default function BeanCard({ bean }: BeanCardProps) {
  const t = useTranslations();
  const locale = useLocale();

  const name = locale === "en" && bean.name_en ? bean.name_en : bean.name;

  return (
    <Link href={`/beans/${bean.id}`}>
      <Card hover>
        {bean.image_url && (
          <div className="aspect-[4/3] bg-stone-100 overflow-hidden">
            <img
              src={bean.image_url}
              alt={name}
              className="w-full h-full object-cover"
            />
          </div>
        )}
        {!bean.image_url && (
          <div className="aspect-[4/3] bg-gradient-to-br from-amber-50 to-amber-100 flex items-center justify-center">
            <span className="text-4xl">☕</span>
          </div>
        )}
        <CardContent>
          <h3 className="font-semibold text-stone-900 text-sm line-clamp-2 mb-1">
            {name}
          </h3>

          {bean.roaster && (
            <p className="text-xs text-stone-500 mb-2">{bean.roaster.name}</p>
          )}

          <div className="flex items-center gap-2 mb-2">
            {bean.avg_rating != null && (
              <div className="flex items-center gap-1">
                <span className="text-amber-500 text-sm">★</span>
                <span className="text-sm font-medium text-stone-700">
                  {bean.avg_rating.toFixed(1)}
                </span>
              </div>
            )}
            <span className="text-xs text-stone-400">
              {t("beans.reviewCount", { count: bean.review_count })}
            </span>
          </div>

          <div className="flex flex-wrap gap-1">
            {bean.roast_level && (
              <Badge variant="primary">
                {t(`roastLevels.${bean.roast_level}` as any)}
              </Badge>
            )}
            {bean.origin && (
              <Badge variant="outline">
                {locale === "en" ? bean.origin.name_en : bean.origin.name}
              </Badge>
            )}
          </div>

          {bean.flavor_notes.length > 0 && (
            <div className="flex flex-wrap gap-1 mt-2">
              {bean.flavor_notes.slice(0, 3).map((slug) => (
                <Badge key={slug} variant="secondary">
                  {slug}
                </Badge>
              ))}
            </div>
          )}
        </CardContent>
      </Card>
    </Link>
  );
}
