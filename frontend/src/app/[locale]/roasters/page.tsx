"use client";

import { useState } from "react";
import { useTranslations } from "next-intl";
import { useQuery } from "@tanstack/react-query";
import { fetchRoasters } from "@/lib/api/roasters";
import RoasterList from "@/components/roasters/RoasterList";
import SearchBar from "@/components/search/SearchBar";

export default function RoastersPage() {
  const t = useTranslations();
  const [query, setQuery] = useState("");

  const { data, isLoading } = useQuery({
    queryKey: ["roasters", query],
    queryFn: () => fetchRoasters({ q: query || undefined }),
  });

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-stone-800">
        {t("roasters.title")}
      </h1>

      <SearchBar
        value={query}
        onChange={setQuery}
        placeholder={t("roasters.searchPlaceholder")}
      />

      <RoasterList roasters={data?.data || []} loading={isLoading} />
    </div>
  );
}
