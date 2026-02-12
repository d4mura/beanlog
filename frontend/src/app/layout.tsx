import type { Metadata, Viewport } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "BeanLog",
  description: "コーヒー豆のレビュー＆発見プラットフォーム",
  manifest: "/manifest.json",
};

export const viewport: Viewport = {
  themeColor: "#4A2C2A",
  width: "device-width",
  initialScale: 1,
  maximumScale: 1,
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
