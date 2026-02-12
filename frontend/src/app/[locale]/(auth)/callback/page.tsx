"use client";

import { useEffect } from "react";
import { useTranslations } from "next-intl";
import { useRouter } from "@/i18n/routing";
import { createClient } from "@/lib/supabase/client";

export default function CallbackPage() {
  const t = useTranslations("common");
  const router = useRouter();

  useEffect(() => {
    const supabase = createClient();

    const handleCallback = async () => {
      const { error } = await supabase.auth.exchangeCodeForSession(
        window.location.href.split("?")[1]?.includes("code=")
          ? window.location.href
          : ""
      );
      if (error) {
        console.error("Auth callback error:", error);
      }
      router.push("/");
    };

    handleCallback();
  }, [router]);

  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <div className="text-center">
        <span className="text-4xl block mb-4 animate-spin">☕</span>
        <p className="text-stone-500">{t("loading")}</p>
      </div>
    </div>
  );
}
