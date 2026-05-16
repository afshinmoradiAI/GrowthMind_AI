import type { Metadata } from "next";
import Link from "next/link";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

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
        <SiteHeader />
        <main className="flex-1">{children}</main>
        <SiteFooter />
      </body>
    </html>
  );
}

function SiteHeader() {
  return (
    <header className="sticky top-0 z-40 border-b border-emerald-100/60 bg-white/80 backdrop-blur-md dark:border-emerald-900/40 dark:bg-[#060b09]/80">
      <div className="mx-auto flex max-w-6xl items-center justify-between px-6 py-4">
        <Link href="/" className="flex items-center gap-2">
          <span className="inline-block h-2.5 w-2.5 rounded-full bg-emerald-500 shadow-[0_0_12px_rgba(16,185,129,0.7)]" />
          <span className="text-base font-semibold tracking-tight text-zinc-900 dark:text-zinc-50">
            GrowthMind <span className="text-emerald-600">AI</span>
          </span>
        </Link>
        <nav className="flex items-center gap-1 text-sm">
          <Link
            href="/leads"
            className="rounded-full px-4 py-1.5 text-zinc-700 transition-colors hover:bg-emerald-50 hover:text-emerald-700 dark:text-zinc-300 dark:hover:bg-emerald-950/40 dark:hover:text-emerald-300"
          >
            Lead Finder
          </Link>
          <Link
            href="/"
            className="rounded-full px-4 py-1.5 text-zinc-700 transition-colors hover:bg-emerald-50 hover:text-emerald-700 dark:text-zinc-300 dark:hover:bg-emerald-950/40 dark:hover:text-emerald-300"
          >
            Content
          </Link>
          <Link
            href="/"
            className="rounded-full px-4 py-1.5 text-zinc-700 transition-colors hover:bg-emerald-50 hover:text-emerald-700 dark:text-zinc-300 dark:hover:bg-emerald-950/40 dark:hover:text-emerald-300"
          >
            CRM
          </Link>
          <Link
            href="/leads"
            className="ml-2 rounded-full bg-emerald-600 px-4 py-1.5 font-medium text-white shadow-sm shadow-emerald-600/30 transition-colors hover:bg-emerald-700"
          >
            Start free
          </Link>
        </nav>
      </div>
    </header>
  );
}

function SiteFooter() {
  return (
    <footer className="border-t border-emerald-100/60 bg-white/60 py-8 text-center text-xs text-zinc-500 dark:border-emerald-900/40 dark:bg-[#060b09]/60 dark:text-zinc-500">
      <p>
        © {new Date().getFullYear()} GrowthMind AI — Find. Score. Engage. Win.
      </p>
    </footer>
  );
}
