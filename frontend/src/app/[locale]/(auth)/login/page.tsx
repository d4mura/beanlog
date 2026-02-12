"use client";

import { useTranslations } from "next-intl";
import { useAuth } from "@/hooks/useAuth";
import { useRouter } from "@/i18n/routing";
import { useEffect } from "react";
import Button from "@/components/ui/Button";
import Card, { CardContent } from "@/components/ui/Card";

export default function LoginPage() {
  const t = useTranslations();
  const { signInWithGoogle, isAuthenticated, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && isAuthenticated) {
      router.push("/");
    }
  }, [loading, isAuthenticated, router]);

  return (
    <div className="flex items-center justify-center min-h-[60vh]">
      <Card className="w-full max-w-sm">
        <CardContent className="p-8 text-center">
          <span className="text-5xl block mb-4">☕</span>
          <h1 className="text-xl font-bold text-stone-800 mb-2">
            {t("auth.loginTitle")}
          </h1>
          <p className="text-sm text-stone-500 mb-6">
            {t("auth.loginDescription")}
          </p>
          <Button
            onClick={signInWithGoogle}
            size="lg"
            className="w-full"
          >
            {t("auth.continueWithGoogle")}
          </Button>
        </CardContent>
      </Card>
    </div>
  );
}
