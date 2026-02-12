"use client";

import { useTranslations } from "next-intl";
import { useBeans } from "@/hooks/useBean";
import BeanList from "@/components/beans/BeanList";
import { Link } from "@/i18n/routing";
import Button from "@/components/ui/Button";

export default function HomePage() {
  const t = useTranslations();
  const { data, isLoading } = useBeans({ sort: "created_desc", per_page: 8 });

  return (
    <div className="space-y-8">
      {/* Hero */}
      <div className="text-center py-8">
        <h1 className="text-3xl font-bold text-amber-900 mb-2">
          ☕ {t("common.appName")}
        </h1>
        <p className="text-stone-600">
          コーヒー豆のレビュー＆発見プラットフォーム
        </p>
      </div>

      {/* Latest Beans */}
      <section>
        <div className="flex items-center justify-between mb-4">
          <h2 className="text-lg font-bold text-stone-800">
            {t("beans.title")}
          </h2>
          <Link href="/beans">
            <Button variant="ghost" size="sm">
              {t("common.seeAll")} →
            </Button>
          </Link>
        </div>
        <BeanList beans={data?.data || []} loading={isLoading} />
      </section>
    </div>
  );
}
