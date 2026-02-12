"use client";

import { useTranslations } from "next-intl";
import RoasterCard from "./RoasterCard";
import type { RoasterListItem } from "@/types/roaster";

interface RoasterListProps {
  roasters: RoasterListItem[];
  loading?: boolean;
}

export default function RoasterList({ roasters, loading }: RoasterListProps) {
  const t = useTranslations("common");

  if (loading) {
    return (
      <div className="space-y-3">
        {Array.from({ length: 5 }).map((_, i) => (
          <div
            key={i}
            className="rounded-xl border border-stone-200 bg-white animate-pulse p-4 flex gap-3"
          >
            <div className="w-14 h-14 rounded-lg bg-stone-100" />
            <div className="space-y-2 flex-1">
              <div className="h-4 bg-stone-100 rounded w-1/2" />
              <div className="h-3 bg-stone-100 rounded w-1/3" />
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (roasters.length === 0) {
    return (
      <div className="text-center py-12 text-stone-500">
        <span className="text-4xl block mb-2">🏭</span>
        <p>{t("noResults")}</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {roasters.map((roaster) => (
        <RoasterCard key={roaster.id} roaster={roaster} />
      ))}
    </div>
  );
}
