"use client";

import { useTranslations } from "next-intl";
import BeanCard from "./BeanCard";
import type { BeanListItem } from "@/types/bean";

interface BeanListProps {
  beans: BeanListItem[];
  loading?: boolean;
}

export default function BeanList({ beans, loading }: BeanListProps) {
  const t = useTranslations("common");

  if (loading) {
    return (
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {Array.from({ length: 8 }).map((_, i) => (
          <div
            key={i}
            className="rounded-xl border border-stone-200 bg-white animate-pulse"
          >
            <div className="aspect-[4/3] bg-stone-100" />
            <div className="p-4 space-y-2">
              <div className="h-4 bg-stone-100 rounded w-3/4" />
              <div className="h-3 bg-stone-100 rounded w-1/2" />
              <div className="h-3 bg-stone-100 rounded w-1/4" />
            </div>
          </div>
        ))}
      </div>
    );
  }

  if (beans.length === 0) {
    return (
      <div className="text-center py-12 text-stone-500">
        <span className="text-4xl block mb-2">☕</span>
        <p>{t("noResults")}</p>
      </div>
    );
  }

  return (
    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
      {beans.map((bean) => (
        <BeanCard key={bean.id} bean={bean} />
      ))}
    </div>
  );
}
