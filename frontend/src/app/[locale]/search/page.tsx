"use client";

import { useState } from "react";
import { useTranslations } from "next-intl";
import { useBeans } from "@/hooks/useBean";
import BeanList from "@/components/beans/BeanList";
import SearchBar from "@/components/search/SearchBar";
import SearchFilters from "@/components/search/SearchFilters";

export default function SearchPage() {
  const t = useTranslations();
  const [query, setQuery] = useState("");
  const [filters, setFilters] = useState<Record<string, string>>({});

  const { data, isLoading } = useBeans({
    q: query || undefined,
    ...filters,
    per_page: 20,
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-stone-800">
        {t("search.title")}
      </h1>

      <SearchBar value={query} onChange={setQuery} />

      <SearchFilters
        filters={filters}
        onChange={(key, val) =>
          setFilters((prev) => ({ ...prev, [key]: val || undefined }))
        }
        onClear={() => setFilters({})}
      />

      <BeanList beans={data?.data || []} loading={isLoading} />
    </div>
  );
}
