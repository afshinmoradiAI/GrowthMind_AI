import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/lib/auth-context";
import SiteHeader from "./_components/site-header";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "GrowthMind AI — B2B Lead Intelligence",
  description:
    "AI-powered content generation and B2B lead intelligence platform.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-[#f8faf9] dark:bg-[#060b09]">
        <AuthProvider>
          <SiteHeader />
          <main className="flex-1">{children}</main>
          <footer className="border-t border-emerald-100/60 bg-white/60 py-8 text-center text-xs text-zinc-500 dark:border-emerald-900/40 dark:bg-[#060b09]/60 dark:text-zinc-500">
            <p>
              © {new Date().getFullYear()} GrowthMind AI — Find. Score. Engage.
              Win.
            </p>
          </footer>
        </AuthProvider>
      </body>
    </html>
  );
}
