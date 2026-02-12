"use client";

import { useTranslations } from "next-intl";
import Select from "@/components/ui/Select";
import Button from "@/components/ui/Button";

interface SearchFiltersProps {
  filters: {
    origin?: string;
    roast_level?: string;
    process?: string;
    sort?: string;
  };
  onChange: (key: string, value: string) => void;
  onClear: () => void;
}

export default function SearchFilters({
  filters,
  onChange,
  onClear,
}: SearchFiltersProps) {
  const t = useTranslations();

  const originOptions = [
    { value: "ET", label: "🇪🇹 " + t("common.appName") === "BeanLog" ? "エチオピア" : "Ethiopia" },
    { value: "CO", label: "🇨🇴 コロンビア" },
    { value: "GT", label: "🇬🇹 グアテマラ" },
    { value: "KE", label: "🇰🇪 ケニア" },
    { value: "BR", label: "🇧🇷 ブラジル" },
    { value: "CR", label: "🇨🇷 コスタリカ" },
    { value: "PA", label: "🇵🇦 パナマ" },
    { value: "RW", label: "🇷🇼 ルワンダ" },
    { value: "ID", label: "🇮🇩 インドネシア" },
    { value: "HN", label: "🇭🇳 ホンジュラス" },
  ];

  const roastOptions = [
    { value: "light", label: t("roastLevels.light") },
    { value: "medium_light", label: t("roastLevels.medium_light") },
    { value: "medium", label: t("roastLevels.medium") },
    { value: "medium_dark", label: t("roastLevels.medium_dark") },
    { value: "dark", label: t("roastLevels.dark") },
  ];

  const processOptions = [
    { value: "washed", label: t("processes.washed") },
    { value: "natural", label: t("processes.natural") },
    { value: "honey", label: t("processes.honey") },
    { value: "anaerobic", label: t("processes.anaerobic") },
    { value: "carbonic_maceration", label: t("processes.carbonic_maceration") },
  ];

  const sortOptions = [
    { value: "created_desc", label: t("search.sortNewest") },
    { value: "rating_desc", label: t("search.sortRating") },
    { value: "name_asc", label: t("search.sortName") },
  ];

  return (
    <div className="space-y-3">
      <div className="grid grid-cols-2 gap-2">
        <Select
          label={t("beans.origin")}
          options={originOptions}
          placeholder="---"
          value={filters.origin || ""}
          onChange={(e) => onChange("origin", e.target.value)}
        />
        <Select
          label={t("beans.roastLevel")}
          options={roastOptions}
          placeholder="---"
          value={filters.roast_level || ""}
          onChange={(e) => onChange("roast_level", e.target.value)}
        />
        <Select
          label={t("beans.process")}
          options={processOptions}
          placeholder="---"
          value={filters.process || ""}
          onChange={(e) => onChange("process", e.target.value)}
        />
        <Select
          label={t("search.sortBy")}
          options={sortOptions}
          value={filters.sort || "created_desc"}
          onChange={(e) => onChange("sort", e.target.value)}
        />
      </div>
      <Button variant="ghost" size="sm" onClick={onClear}>
        {t("search.clearFilters")}
      </Button>
    </div>
  );
}
