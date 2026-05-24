"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState } from "react";
import { useAuth } from "@/lib/auth-context";

export default function SiteHeader() {
  const { user, loading, logout } = useAuth();
  const router = useRouter();
  const [menuOpen, setMenuOpen] = useState(false);

  async function handleLogout() {
    await logout();
    setMenuOpen(false);
    router.push("/");
  }

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

          {loading ? (
            <span className="ml-2 inline-block h-7 w-20 animate-pulse rounded-full bg-zinc-100 dark:bg-zinc-900" />
          ) : user ? (
            <div className="relative ml-2">
              <button
                onClick={() => setMenuOpen((v) => !v)}
                className="flex items-center gap-2 rounded-full border border-emerald-200 bg-emerald-50 px-3 py-1.5 text-sm font-medium text-emerald-800 hover:bg-emerald-100 dark:border-emerald-900/50 dark:bg-emerald-950/40 dark:text-emerald-200"
              >
                <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-emerald-600 text-xs font-semibold text-white">
                  {(user.display_name || user.email)[0].toUpperCase()}
                </span>
                <span className="max-w-[160px] truncate">
                  {user.display_name || user.email}
                </span>
              </button>
              {menuOpen && (
                <div
                  className="absolute right-0 mt-2 w-48 overflow-hidden rounded-xl border border-zinc-200 bg-white shadow-lg dark:border-zinc-800 dark:bg-zinc-950"
                  onMouseLeave={() => setMenuOpen(false)}
                >
                  <div className="border-b border-zinc-100 px-4 py-3 text-xs dark:border-zinc-800">
                    <p className="font-medium text-zinc-900 dark:text-zinc-100">
                      {user.display_name || "Signed in"}
                    </p>
                    <p className="mt-0.5 truncate text-zinc-500">
                      {user.email}
                    </p>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="block w-full px-4 py-2 text-left text-sm text-red-600 hover:bg-red-50 dark:text-red-400 dark:hover:bg-red-950/30"
                  >
                    Sign out
                  </button>
                </div>
              )}
            </div>
          ) : (
            <>
              <Link
                href="/login"
                className="rounded-full px-4 py-1.5 text-zinc-700 transition-colors hover:bg-emerald-50 hover:text-emerald-700 dark:text-zinc-300 dark:hover:bg-emerald-950/40"
              >
                Sign in
              </Link>
              <Link
                href="/register"
                className="ml-1 rounded-full bg-emerald-600 px-4 py-1.5 font-medium text-white shadow-sm shadow-emerald-600/30 transition-colors hover:bg-emerald-700"
              >
                Start free
              </Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}
