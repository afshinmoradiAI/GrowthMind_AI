"use client";

import Image from "next/image";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import { useAuth } from "@/lib/auth-context";
import {
  searchLeadsFromICP,
  type LeadSearchResponse,
  type LeadWithOutreach,
  type Tier,
} from "@/lib/api";

const TIER_STYLES: Record<
  Tier,
  { badge: string; dot: string; bar: string; label: string }
> = {
  hot: {
    badge:
      "bg-emerald-50 text-emerald-700 ring-1 ring-emerald-500/30 dark:bg-emerald-950/50 dark:text-emerald-300",
    dot: "bg-emerald-500 shadow-[0_0_12px_rgba(16,185,129,0.7)]",
    bar: "bg-emerald-500",
    label: "HOT — go!",
  },
  warm: {
    badge:
      "bg-amber-50 text-amber-700 ring-1 ring-amber-500/30 dark:bg-amber-950/50 dark:text-amber-300",
    dot: "bg-amber-500 shadow-[0_0_12px_rgba(245,158,11,0.6)]",
    bar: "bg-amber-500",
    label: "WARM — nurture",
  },
  cold: {
    badge:
      "bg-red-50 text-red-700 ring-1 ring-red-500/30 dark:bg-red-950/50 dark:text-red-300",
    dot: "bg-red-500 shadow-[0_0_12px_rgba(239,68,68,0.6)]",
    bar: "bg-red-500",
    label: "COLD — skip",
  },
};

export default function LeadsPage() {
  const router = useRouter();
  const { user, loading: authLoading } = useAuth();
  const [query, setQuery] = useState(
    "Find dental clinics in Melbourne to pitch cosmetic dentistry on LinkedIn"
  );
  const [maxResults, setMaxResults] = useState(5);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [results, setResults] = useState<LeadSearchResponse | null>(null);

  useEffect(() => {
    if (!authLoading && !user) {
      router.replace("/login?next=/leads");
    }
  }, [authLoading, user, router]);

  if (authLoading || !user) {
    return (
      <div className="mx-auto max-w-6xl px-6 py-24 text-center text-sm text-zinc-500">
        <Link href="/login" className="text-emerald-600 hover:underline">
          Redirecting to sign-in…
        </Link>
      </div>
    );
  }

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setLoading(true);
    setError(null);
    setResults(null);
    try {
      const data = await searchLeadsFromICP({
        query,
        max_results: maxResults,
      });
      setResults(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      {/* Sub-hero */}
      <section className="relative isolate overflow-hidden">
        <div className="absolute inset-0 -z-10">
          <Image
            src="https://images.unsplash.com/photo-1521791136064-7986c2920216?auto=format&fit=crop&w=2000&q=80"
            alt="Business handshake"
            fill
            priority
            className="object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-br from-emerald-950/90 via-emerald-900/80 to-black/85" />
        </div>
        <div className="mx-auto max-w-6xl px-6 py-14">
          <p className="text-sm font-medium uppercase tracking-wider text-emerald-300">
            Lead Finder
          </p>
          <h1 className="mt-2 text-4xl font-semibold tracking-tight text-white">
            Describe your ideal customer.
          </h1>
          <p className="mt-3 max-w-2xl text-base text-emerald-50/80">
            One sentence in. A scored, contactable pipeline out. Hot leads turn
            green. Cold ones turn red. You decide where to spend your time.
          </p>
        </div>
      </section>

      <div className="mx-auto -mt-10 max-w-6xl px-6 pb-20">
        {/* Search card */}
        <form
          onSubmit={handleSubmit}
          className="rounded-2xl border border-emerald-100 bg-white p-6 shadow-xl shadow-emerald-100/40 dark:border-emerald-900/40 dark:bg-zinc-950 dark:shadow-black/30"
        >
          <label className="block text-sm font-semibold text-zinc-800 dark:text-zinc-200">
            What kind of leads do you want?
          </label>
          <textarea
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            rows={3}
            className="mt-3 block w-full resize-none rounded-xl border border-zinc-200 bg-white px-4 py-3 text-sm text-zinc-900 placeholder:text-zinc-400 focus:border-emerald-500 focus:outline-none focus:ring-2 focus:ring-emerald-500/20 dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-100"
            placeholder="e.g. Find boutique cafes in Surry Hills for an Instagram growth campaign"
            required
            minLength={10}
          />

          <div className="mt-5 flex flex-wrap items-end gap-4">
            <div>
              <label className="block text-xs font-medium uppercase tracking-wide text-zinc-500 dark:text-zinc-500">
                Max results
              </label>
              <input
                type="number"
                min={1}
                max={20}
                value={maxResults}
                onChange={(e) => setMaxResults(Number(e.target.value))}
                className="mt-2 w-24 rounded-lg border border-zinc-200 bg-white px-3 py-2 text-sm dark:border-zinc-800 dark:bg-zinc-900 dark:text-zinc-100"
              />
            </div>
            <button
              type="submit"
              disabled={loading}
              className="ml-auto inline-flex items-center justify-center rounded-full bg-emerald-600 px-7 py-2.5 text-sm font-semibold text-white shadow-lg shadow-emerald-600/30 transition-all hover:bg-emerald-500 hover:shadow-emerald-500/40 disabled:opacity-50"
            >
              {loading ? (
                <>
                  <span className="mr-2 inline-block h-2 w-2 animate-pulse rounded-full bg-white" />
                  Hunting…
                </>
              ) : (
                <>Find leads →</>
              )}
            </button>
          </div>
        </form>

        {error && (
          <div className="mt-6 flex items-start gap-3 rounded-xl border border-red-200 bg-red-50 p-4 text-sm text-red-700 dark:border-red-900 dark:bg-red-950/40 dark:text-red-300">
            <span className="mt-0.5 inline-block h-2 w-2 shrink-0 rounded-full bg-red-500" />
            <div>
              <p className="font-semibold">Search failed</p>
              <p className="mt-0.5">{error}</p>
            </div>
          </div>
        )}

        {loading && (
          <div className="mt-12 flex flex-col items-center text-center">
            <div className="flex gap-1.5">
              {[0, 150, 300].map((d) => (
                <span
                  key={d}
                  className="h-2 w-2 animate-pulse rounded-full bg-emerald-500"
                  style={{ animationDelay: `${d}ms` }}
                />
              ))}
            </div>
            <p className="mt-4 text-sm font-medium text-zinc-700 dark:text-zinc-300">
              Running the pipeline
            </p>
            <p className="mt-1 max-w-md text-xs text-zinc-500 dark:text-zinc-500">
              ICP parser → Places search → website scrape → decision-maker
              extraction → email guessing → AI scoring → 3-touch sequencing
            </p>
            <p className="mt-2 text-xs text-zinc-400">~20–60 seconds</p>
          </div>
        )}

        {results && (
          <section className="mt-12">
            <div className="mb-6 flex items-baseline justify-between">
              <div>
                <h2 className="text-xl font-semibold text-zinc-900 dark:text-zinc-50">
                  {results.count} leads
                </h2>
                <p className="text-sm text-zinc-500 dark:text-zinc-500">
                  {results.business_type} · {results.location} · sorted by
                  score
                </p>
              </div>
              <ResultsLegend results={results} />
            </div>

            <div className="space-y-5">
              {results.leads.map((item) => (
                <LeadCard key={item.lead.place_id} item={item} />
              ))}
            </div>
          </section>
        )}
      </div>
    </>
  );
}

function ResultsLegend({ results }: { results: LeadSearchResponse }) {
  const counts = { hot: 0, warm: 0, cold: 0 };
  for (const l of results.leads) {
    if (l.score) counts[l.score.tier] += 1;
  }
  return (
    <div className="flex gap-4 text-xs">
      {(["hot", "warm", "cold"] as Tier[]).map((t) => (
        <div key={t} className="flex items-center gap-1.5">
          <span className={`inline-block h-2 w-2 rounded-full ${TIER_STYLES[t].dot}`} />
          <span className="font-medium text-zinc-700 dark:text-zinc-300">
            {counts[t]}
          </span>
          <span className="text-zinc-500 dark:text-zinc-500">{t}</span>
        </div>
      ))}
    </div>
  );
}

function LeadCard({ item }: { item: LeadWithOutreach }) {
  const { lead, score, outreach } = item;
  const primaryContact = lead.decision_makers[0];
  const tierStyle = score ? TIER_STYLES[score.tier] : null;

  return (
    <article className="overflow-hidden rounded-2xl border border-zinc-200 bg-white shadow-sm transition-all hover:border-emerald-300 hover:shadow-md dark:border-zinc-800 dark:bg-zinc-950 dark:hover:border-emerald-700">
      {tierStyle && (
        <div className={`h-1 w-full ${tierStyle.bar}`} />
      )}
      <div className="p-6">
        <header className="flex items-start justify-between gap-4">
          <div className="min-w-0">
            <h3 className="truncate text-lg font-semibold text-zinc-900 dark:text-zinc-50">
              {lead.name}
            </h3>
            {lead.address && (
              <p className="mt-1 text-sm text-zinc-600 dark:text-zinc-400">
                {lead.address}
              </p>
            )}
            <div className="mt-2 flex flex-wrap gap-x-4 gap-y-1 text-xs text-zinc-500 dark:text-zinc-500">
              {lead.rating !== null && (
                <span className="inline-flex items-center gap-1">
                  <span className="text-amber-500">★</span>
                  {lead.rating.toFixed(1)} · {lead.review_count ?? 0} reviews
                </span>
              )}
              {lead.phone && <span>{lead.phone}</span>}
              {lead.website && (
                <a
                  href={lead.website}
                  target="_blank"
                  rel="noreferrer"
                  className="text-emerald-600 hover:underline dark:text-emerald-400"
                >
                  Website ↗
                </a>
              )}
            </div>
          </div>
          {score && tierStyle && (
            <div className="shrink-0 text-right">
              <div
                className={`inline-flex items-center gap-2 rounded-full px-3 py-1 text-xs font-semibold ${tierStyle.badge}`}
              >
                <span className={`inline-block h-1.5 w-1.5 rounded-full ${tierStyle.dot}`} />
                {tierStyle.label}
              </div>
              <p className="mt-2 font-mono text-2xl font-semibold text-zinc-900 dark:text-zinc-50">
                {score.score}
                <span className="text-sm text-zinc-400">/100</span>
              </p>
            </div>
          )}
        </header>

        {score && score.reasons.length > 0 && (
          <ul className="mt-4 grid gap-1 text-xs text-zinc-600 dark:text-zinc-400 sm:grid-cols-2">
            {score.reasons.map((reason, i) => (
              <li key={i} className="flex items-start gap-1.5">
                <span className="mt-1.5 inline-block h-1 w-1 shrink-0 rounded-full bg-emerald-500" />
                {reason}
              </li>
            ))}
          </ul>
        )}

        {primaryContact && (
          <div className="mt-5 rounded-xl border border-emerald-100 bg-gradient-to-br from-emerald-50/70 to-white p-4 text-sm dark:border-emerald-900/40 dark:from-emerald-950/30 dark:to-zinc-950">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="font-semibold text-zinc-900 dark:text-zinc-100">
                  {primaryContact.name}
                  {primaryContact.title && (
                    <span className="font-normal text-zinc-500 dark:text-zinc-400">
                      {" "}· {primaryContact.title}
                    </span>
                  )}
                </p>
                {primaryContact.email ? (
                  <p className="mt-1 font-mono text-xs text-emerald-700 dark:text-emerald-400">
                    {primaryContact.email}
                  </p>
                ) : primaryContact.email_candidates.length > 0 ? (
                  <p className="mt-1 text-xs text-zinc-500 dark:text-zinc-500">
                    Likely:{" "}
                    <span className="font-mono text-zinc-700 dark:text-zinc-300">
                      {primaryContact.email_candidates.slice(0, 3).join(", ")}
                    </span>
                  </p>
                ) : null}
              </div>
              {primaryContact.email_domain_verified && (
                <span className="inline-flex shrink-0 items-center gap-1 rounded-full bg-emerald-100 px-2 py-0.5 text-xs font-medium text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-300">
                  ✓ MX verified
                </span>
              )}
            </div>
          </div>
        )}

        <div className="mt-5">
          <h4 className="text-xs font-semibold uppercase tracking-wide text-zinc-500 dark:text-zinc-500">
            3-touch outreach sequence
          </h4>
          <div className="mt-3 space-y-3">
            {outreach.touches.map((touch, i) => (
              <div
                key={i}
                className="rounded-xl border border-zinc-200 bg-zinc-50/50 p-4 dark:border-zinc-800 dark:bg-zinc-900/40"
              >
                <div className="flex items-center justify-between text-xs">
                  <span className="inline-flex items-center gap-1.5 font-semibold text-emerald-700 dark:text-emerald-400">
                    <span className="inline-block h-1.5 w-1.5 rounded-full bg-emerald-500" />
                    Day {touch.day_offset}
                  </span>
                  <span className="text-zinc-500 dark:text-zinc-500">
                    {touch.purpose}
                  </span>
                </div>
                {touch.subject && (
                  <p className="mt-3 text-sm font-semibold text-zinc-900 dark:text-zinc-100">
                    {touch.subject}
                  </p>
                )}
                <p className="mt-2 whitespace-pre-wrap text-sm leading-relaxed text-zinc-700 dark:text-zinc-300">
                  {touch.body}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>
    </article>
  );
}
