"use client";

import { useState } from "react";
import { useTranslations } from "next-intl";
import { useRouter } from "@/i18n/routing";
import { fetchBeanByBarcode } from "@/lib/api/beans";
import Button from "@/components/ui/Button";
import Input from "@/components/ui/Input";
import Card, { CardContent } from "@/components/ui/Card";

export default function ScanPage() {
  const t = useTranslations();
  const router = useRouter();
  const [barcode, setBarcode] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSearch = async () => {
    if (!barcode.trim()) return;
    setError("");
    setLoading(true);
    try {
      const result = await fetchBeanByBarcode(barcode.trim());
      if (result?.data?.id) {
        router.push(`/beans/${result.data.id}`);
      }
    } catch {
      setError(t("scan.notFound"));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-stone-800">{t("scan.title")}</h1>
      <p className="text-stone-600 text-sm">{t("scan.description")}</p>

      <Card>
        <CardContent className="p-6 space-y-4">
          <div className="text-center text-6xl py-8">📷</div>
          <p className="text-center text-sm text-stone-400">
            {t("scan.description")}
          </p>

          {/* Manual barcode input */}
          <div className="space-y-3">
            <Input
              value={barcode}
              onChange={(e) => setBarcode(e.target.value)}
              placeholder="4900000000001"
              label={t("beans.barcode")}
            />
            <Button
              onClick={handleSearch}
              className="w-full"
              disabled={loading || !barcode.trim()}
            >
              {loading ? t("common.loading") : t("common.search")}
            </Button>
          </div>

          {error && (
            <p className="text-sm text-red-600 text-center">{error}</p>
          )}
        </CardContent>
      </Card>
    </div>
  );
}
