"use client";

import { useTranslations } from "next-intl";
import { Link, usePathname } from "@/i18n/routing";
import { clsx } from "clsx";

const navItems = [
  { href: "/", label: "home", icon: "🏠" },
  { href: "/beans", label: "beans", icon: "☕" },
  { href: "/roasters", label: "roasters", icon: "🏭" },
  { href: "/search", label: "search", icon: "🔍" },
  { href: "/profile", label: "profile", icon: "👤" },
] as const;

export default function Navigation() {
  const t = useTranslations("nav");
  const pathname = usePathname();

  return (
    <nav className="fixed bottom-0 left-0 right-0 z-50 bg-white border-t border-stone-200 safe-bottom">
      <div className="max-w-5xl mx-auto flex justify-around">
        {navItems.map((item) => {
          const isActive =
            item.href === "/"
              ? pathname === "/" || pathname === ""
              : pathname.startsWith(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              className={clsx(
                "flex flex-col items-center py-2 px-3 text-xs transition-colors",
                isActive
                  ? "text-amber-900 font-medium"
                  : "text-stone-400 hover:text-stone-600"
              )}
            >
              <span className="text-lg mb-0.5">{item.icon}</span>
              <span>{t(item.label)}</span>
            </Link>
          );
        })}
      </div>
    </nav>
  );
}
