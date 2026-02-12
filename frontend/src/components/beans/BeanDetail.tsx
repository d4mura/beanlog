"use client";

import { useLocale, useTranslations } from "next-intl";
import Badge from "@/components/ui/Badge";
import Button from "@/components/ui/Button";
import { Link } from "@/i18n/routing";
import type { BeanDetail as BeanDetailType } from "@/types/bean";

interface BeanDetailProps {
  bean: BeanDetailType;
}

export default function BeanDetailView({ bean }: BeanDetailProps) {
  const t = useTranslations();
  const locale = useLocale();

  const name = locale === "en" && bean.name_en ? bean.name_en : bean.name;
  const description =
    locale === "en" && bean.description_en
      ? bean.description_en
      : bean.description;

  return (
    <div className="space-y-6">
      {/* Hero Image */}
      <div className="aspect-[16/9] bg-gradient-to-br from-amber-50 to-amber-100 rounded-xl overflow-hidden">
        {bean.image_url ? (
          <img
            src={bean.image_url}
            alt={name}
            className="w-full h-full object-cover"
          />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <span className="text-6xl">☕</span>
          </div>
        )}
      </div>

      {/* Title & Rating */}
      <div>
        <h1 className="text-2xl font-bold text-stone-900 mb-1">{name}</h1>
        {bean.roaster && (
          <Link
            href={`/roasters/${bean.roaster.id}`}
            className="text-amber-700 hover:underline text-sm"
          >
            {bean.roaster.name}
          </Link>
        )}
        <div className="flex items-center gap-3 mt-2">
          {bean.avg_rating != null && (
            <div className="flex items-center gap-1">
              <span className="text-amber-500 text-lg">★</span>
              <span className="text-lg font-bold text-stone-800">
                {bean.avg_rating.toFixed(1)}
              </span>
            </div>
          )}
          <span className="text-sm text-stone-500">
            {t("beans.reviewCount", { count: bean.review_count })}
          </span>
        </div>
      </div>

      {/* Description */}
      {description && (
        <p className="text-stone-600 text-sm leading-relaxed">{description}</p>
      )}

      {/* Details Grid */}
      <div className="grid grid-cols-2 gap-3">
        {bean.origin && (
          <DetailItem
            label={t("beans.origin")}
            value={`${locale === "en" ? bean.origin.name_en : bean.origin.name}${
              bean.origin.region
                ? ` / ${locale === "en" ? bean.origin.region_en : bean.origin.region}`
                : ""
            }`}
          />
        )}
        {bean.roast_level && (
          <DetailItem
            label={t("beans.roastLevel")}
            value={t(`roastLevels.${bean.roast_level}` as any)}
          />
        )}
        {bean.process && (
          <DetailItem
            label={t("beans.process")}
            value={t(`processes.${bean.process}` as any)}
          />
        )}
        {bean.variety && (
          <DetailItem label={t("beans.variety")} value={bean.variety} />
        )}
        {(bean.altitude_min || bean.altitude_max) && (
          <DetailItem
            label={t("beans.altitude")}
            value={`${bean.altitude_min || "?"}–${bean.altitude_max || "?"}m`}
          />
        )}
      </div>

      {/* Flavor Notes */}
      {bean.flavor_notes.length > 0 && (
        <div>
          <h3 className="text-sm font-medium text-stone-700 mb-2">
            {t("beans.flavor")}
          </h3>
          <div className="flex flex-wrap gap-2">
            {bean.flavor_notes.map((slug) => (
              <Badge key={slug} variant="primary">
                {slug}
              </Badge>
            ))}
          </div>
        </div>
      )}

      {/* CTA */}
      <div className="flex gap-3">
        <Link href={`/beans/${bean.id}/review`} className="flex-1">
          <Button className="w-full" size="lg">
            {t("reviews.writeReview")}
          </Button>
        </Link>
        {bean.purchase_url && (
          <a
            href={bean.purchase_url}
            target="_blank"
            rel="noopener noreferrer"
            className="flex-1"
          >
            <Button variant="outline" className="w-full" size="lg">
              {t("beans.purchaseLink")}
            </Button>
          </a>
        )}
      </div>
    </div>
  );
}

function DetailItem({ label, value }: { label: string; value: string }) {
  return (
    <div className="bg-stone-50 rounded-lg p-3">
      <p className="text-xs text-stone-500 mb-0.5">{label}</p>
      <p className="text-sm font-medium text-stone-800">{value}</p>
    </div>
  );
}
