"use client";

import { useTranslations } from "next-intl";
import { Link } from "@/i18n/routing";
import Card, { CardContent } from "@/components/ui/Card";
import type { RoasterListItem } from "@/types/roaster";

interface RoasterCardProps {
  roaster: RoasterListItem;
}

export default function RoasterCard({ roaster }: RoasterCardProps) {
  const t = useTranslations();

  return (
    <Link href={`/roasters/${roaster.id}`}>
      <Card hover>
        <div className="flex items-center gap-3 p-4">
          <div className="w-14 h-14 rounded-lg bg-amber-50 flex items-center justify-center flex-shrink-0 overflow-hidden">
            {roaster.image_url ? (
              <img
                src={roaster.image_url}
                alt={roaster.name}
                className="w-full h-full object-cover"
              />
            ) : (
              <span className="text-2xl">🏭</span>
            )}
          </div>
          <div className="min-w-0 flex-1">
            <h3 className="font-semibold text-stone-900 text-sm truncate">
              {roaster.name}
            </h3>
            {roaster.location && (
              <p className="text-xs text-stone-500 truncate">{roaster.location}</p>
            )}
            <div className="flex items-center gap-3 mt-1">
              <span className="text-xs text-stone-400">
                {t("roasters.beanCount", { count: roaster.bean_count })}
              </span>
              {roaster.avg_rating != null && (
                <span className="text-xs text-amber-600">
                  ★ {roaster.avg_rating.toFixed(1)}
                </span>
              )}
            </div>
          </div>
        </div>
      </Card>
    </Link>
  );
}
