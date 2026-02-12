import { useTranslations } from "next-intl";

export default function Footer() {
  const t = useTranslations("common");

  return (
    <footer className="border-t border-stone-200 bg-stone-50 mt-auto">
      <div className="max-w-5xl mx-auto px-4 py-6 text-center text-sm text-stone-500">
        <p>© 2026 {t("appName")}. All rights reserved.</p>
      </div>
    </footer>
  );
}
