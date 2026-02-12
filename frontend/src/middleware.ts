import createMiddleware from "next-intl/middleware";
import { NextRequest } from "next/server";
import { routing } from "./i18n/routing";

const intlMiddleware = createMiddleware(routing);

export async function middleware(request: NextRequest) {
  // Apply i18n routing
  const intlResponse = intlMiddleware(request);

  // If Supabase is configured, update session cookies
  if (
    process.env.NEXT_PUBLIC_SUPABASE_URL &&
    process.env.NEXT_PUBLIC_SUPABASE_ANON_KEY
  ) {
    try {
      const { updateSession } = await import("./lib/supabase/middleware");
      const response = await updateSession(request);
      response.cookies.getAll().forEach((cookie) => {
        intlResponse.cookies.set(cookie.name, cookie.value);
      });
    } catch {
      // Supabase not available, skip
    }
  }

  return intlResponse;
}

export const config = {
  matcher: ["/((?!_next|api|health|icons|images|manifest.json|sw.js|favicon.ico).*)"],
};
