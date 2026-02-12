"use client";

import { useState } from "react";
import { useTranslations } from "next-intl";
import { useBeans } from "@/hooks/useBean";
import BeanList from "@/components/beans/BeanList";
import SearchBar from "@/components/search/SearchBar";
import SearchFilters from "@/components/search/SearchFilters";

export default function BeansPage() {
  const t = useTranslations();
  const [query, setQuery] = useState("");
  const [filters, setFilters] = useState<Record<string, string>>({});
  const [page, setPage] = useState(1);

  const { data, isLoading } = useBeans({
    q: query || undefined,
    ...filters,
    page,
    per_page: 20,
  });

  const handleFilterChange = (key: string, value: string) => {
    setFilters((prev) => {
      const next = { ...prev };
      if (value) {
        next[key] = value;
      } else {
        delete next[key];
      }
      return next;
    });
    setPage(1);
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-stone-800">{t("beans.title")}</h1>

      <SearchBar
        value={query}
        onChange={(v) => {
          setQuery(v);
          setPage(1);
        }}
        placeholder={t("beans.searchPlaceholder")}
      />

      <SearchFilters
        filters={filters}
        onChange={handleFilterChange}
        onClear={() => {
          setFilters({});
          setPage(1);
        }}
      />

      <BeanList beans={data?.data || []} loading={isLoading} />

      {/* Pagination */}
      {data?.meta && data.meta.total_pages > 1 && (
        <div className="flex justify-center gap-2 pt-4">
          {Array.from({ length: data.meta.total_pages }, (_, i) => i + 1).map(
            (p) => (
              <button
                key={p}
                onClick={() => setPage(p)}
                className={`px-3 py-1 rounded text-sm ${
                  p === page
                    ? "bg-amber-900 text-white"
                    : "bg-stone-100 text-stone-600 hover:bg-stone-200"
                }`}
              >
                {p}
              </button>
            )
          )}
        </div>
      )}
    </div>
  );
}
