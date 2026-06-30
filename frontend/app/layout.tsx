import type { Metadata } from "next";

import "./globals.css";

export const metadata: Metadata = {
  title: "StartupPilot AI",
  description: "AI SaaS for transforming startup ideas into complete MVP plans."
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body>{children}</body>
    </html>
  );
}
