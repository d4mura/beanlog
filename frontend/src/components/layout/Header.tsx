"use client";

import { useTranslations } from "next-intl";
import { Link, usePathname, useRouter } from "@/i18n/routing";
import { useAuth } from "@/hooks/useAuth";
import Button from "@/components/ui/Button";

export default function Header() {
  const t = useTranslations();
  const { user, signOut, isAuthenticated } = useAuth();
  const pathname = usePathname();
  const router = useRouter();

  const toggleLocale = () => {
    const currentLocale = pathname.startsWith("/en") ? "en" : "ja";
    const newLocale = currentLocale === "ja" ? "en" : "ja";
    router.replace(pathname, { locale: newLocale });
  };

  return (
    <header className="sticky top-0 z-50 bg-white/95 backdrop-blur border-b border-stone-200">
      <div className="max-w-5xl mx-auto px-4 h-14 flex items-center justify-between">
        <Link href="/" className="flex items-center gap-2">
          <span className="text-xl">☕</span>
          <span className="font-bold text-lg text-amber-900">
            {t("common.appName")}
          </span>
        </Link>

        <div className="flex items-center gap-2">
          <button
            onClick={toggleLocale}
            className="px-2 py-1 text-xs rounded border border-stone-300 text-stone-600 hover:bg-stone-50"
          >
            {t("common.language")}
          </button>

          {isAuthenticated ? (
            <div className="flex items-center gap-2">
              <Link href="/profile">
                <div className="w-8 h-8 rounded-full bg-amber-200 flex items-center justify-center text-sm font-medium text-amber-900">
                  {user?.email?.[0]?.toUpperCase() || "U"}
                </div>
              </Link>
              <Button variant="ghost" size="sm" onClick={signOut}>
                {t("common.logout")}
              </Button>
            </div>
          ) : (
            <Link href="/login">
              <Button size="sm">{t("common.login")}</Button>
            </Link>
          )}
        </div>
      </div>
    </header>
  );
}
