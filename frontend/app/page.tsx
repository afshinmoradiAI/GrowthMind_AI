import Image from "next/image";
import Link from "next/link";

const features = [
  {
    href: "/leads",
    title: "Lead Finder",
    description:
      "Describe your ideal customer in plain English. We find real local businesses, extract decision-makers, score each lead, and draft a 3-touch sequence.",
    cta: "Find leads",
    available: true,
    accent: "emerald",
  },
  {
    href: "/",
    title: "Content Studio",
    description:
      "Platform-native posts for X, LinkedIn, Instagram, Facebook & TikTok — plus an AI image prompt tuned to each platform's aspect ratio.",
    cta: "Generate content",
    available: false,
    accent: "emerald",
  },
  {
    href: "/",
    title: "Pipeline CRM",
    description:
      "Track imported leads, move them through New → Contacted → Won, and mark each outreach touch as sent.",
    cta: "Open CRM",
    available: false,
    accent: "emerald",
  },
];

const stats = [
  { label: "AI agents", value: "6" },
  { label: "Outreach touches per lead", value: "3" },
  { label: "Average pipeline ROI", value: "12×" },
];

export default function Home() {
  return (
    <>
      {/* HERO */}
      <section className="relative isolate overflow-hidden">
        <div className="absolute inset-0 -z-10">
          <Image
            src="https://images.unsplash.com/photo-1556761175-b413da4baf72?auto=format&fit=crop&w=2000&q=80"
            alt="Sales team collaborating"
            fill
            priority
            className="object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-br from-emerald-950/85 via-emerald-900/70 to-black/80" />
          <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,rgba(16,185,129,0.35),transparent_60%)]" />
        </div>

        <div className="mx-auto max-w-6xl px-6 pt-20 pb-28 sm:pt-28 sm:pb-36">
          <div className="inline-flex items-center gap-2 rounded-full border border-emerald-400/30 bg-emerald-500/10 px-4 py-1.5 text-xs font-medium uppercase tracking-wider text-emerald-300 backdrop-blur">
            <span className="inline-block h-1.5 w-1.5 animate-pulse rounded-full bg-emerald-400" />
            Live AI sales intelligence
          </div>

          <h1 className="mt-6 max-w-3xl text-4xl font-semibold leading-tight tracking-tight text-white sm:text-5xl lg:text-6xl">
            Turn a single sentence into a{" "}
            <span className="bg-gradient-to-r from-emerald-300 to-emerald-500 bg-clip-text text-transparent">
              qualified sales pipeline.
            </span>
          </h1>

          <p className="mt-6 max-w-2xl text-lg text-emerald-50/80">
            GrowthMind AI discovers real local businesses, finds their
            decision-makers, scores every lead, and writes a personalised
            3-touch outreach sequence — all in under a minute.
          </p>

          <div className="mt-10 flex flex-wrap items-center gap-4">
            <Link
              href="/leads"
              className="inline-flex items-center justify-center rounded-full bg-emerald-500 px-7 py-3 text-sm font-semibold text-white shadow-lg shadow-emerald-500/30 transition-all hover:bg-emerald-400 hover:shadow-emerald-400/40"
            >
              Find leads now →
            </Link>
            <a
              href="#how-it-works"
              className="inline-flex items-center justify-center rounded-full border border-white/20 bg-white/5 px-7 py-3 text-sm font-medium text-white backdrop-blur transition-colors hover:bg-white/10"
            >
              See how it works
            </a>
          </div>

          <dl className="mt-16 grid grid-cols-3 gap-6 sm:max-w-lg">
            {stats.map((s) => (
              <div key={s.label} className="border-l-2 border-emerald-400/50 pl-4">
                <dt className="text-xs uppercase tracking-wide text-emerald-200/70">
                  {s.label}
                </dt>
                <dd className="mt-1 text-2xl font-semibold text-white">
                  {s.value}
                </dd>
              </div>
            ))}
          </dl>
        </div>
      </section>

      {/* FEATURE CARDS */}
      <section id="how-it-works" className="mx-auto w-full max-w-6xl px-6 py-20">
        <div className="mb-10 max-w-2xl">
          <p className="text-sm font-medium uppercase tracking-wider text-emerald-600">
            Three products. One AI pipeline.
          </p>
          <h2 className="mt-2 text-3xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-50">
            Everything sales needs, without the bloat.
          </h2>
        </div>

        <div className="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {features.map((f) => (
            <FeatureCard key={f.title} {...f} />
          ))}
        </div>
      </section>

      {/* SIGNAL ROW */}
      <section className="border-y border-emerald-100/70 bg-gradient-to-br from-emerald-50/60 to-white py-16 dark:border-emerald-900/30 dark:from-emerald-950/30 dark:to-[#060b09]">
        <div className="mx-auto max-w-6xl px-6">
          <p className="text-sm font-medium uppercase tracking-wider text-emerald-600">
            How leads are scored
          </p>
          <h2 className="mt-2 text-2xl font-semibold tracking-tight text-zinc-900 dark:text-zinc-50">
            Every lead lands in one of three lanes — instantly.
          </h2>

          <div className="mt-10 grid gap-5 sm:grid-cols-3">
            <SignalCard
              tier="hot"
              label="Hot — go!"
              score="80–100"
              description="Strong ICP fit, named decision-maker, verified email domain. Open the door today."
            />
            <SignalCard
              tier="warm"
              label="Warm — nurture"
              score="50–79"
              description="Decent fit but a signal is missing. Worth a softer first touch."
            />
            <SignalCard
              tier="cold"
              label="Cold — skip"
              score="0–49"
              description="Weak match or missing contact. Save your inbox capacity for better leads."
            />
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="mx-auto w-full max-w-6xl px-6 py-20">
        <div className="overflow-hidden rounded-3xl border border-emerald-200/50 bg-gradient-to-br from-emerald-600 to-emerald-800 p-10 text-white shadow-xl shadow-emerald-900/20 sm:p-14">
          <h2 className="max-w-2xl text-3xl font-semibold leading-tight tracking-tight">
            Stop scraping LinkedIn. Start closing deals.
          </h2>
          <p className="mt-3 max-w-xl text-emerald-50/90">
            Plug in your ICP. We&apos;ll do the rest — discovery, enrichment,
            scoring, and copywriting.
          </p>
          <Link
            href="/leads"
            className="mt-8 inline-flex items-center justify-center rounded-full bg-white px-7 py-3 text-sm font-semibold text-emerald-800 shadow-md transition-colors hover:bg-emerald-50"
          >
            Run my first search →
          </Link>
        </div>
      </section>
    </>
  );
}

function FeatureCard({
  href,
  title,
  description,
  cta,
  available,
}: {
  href: string;
  title: string;
  description: string;
  cta: string;
  available: boolean;
}) {
  const body = (
    <div className="group relative flex h-full flex-col overflow-hidden rounded-2xl border border-emerald-100/70 bg-white p-7 shadow-sm transition-all hover:-translate-y-1 hover:border-emerald-300 hover:shadow-lg hover:shadow-emerald-100/60 dark:border-emerald-900/40 dark:bg-zinc-950 dark:hover:border-emerald-700">
      <div className="absolute right-0 top-0 h-24 w-24 -translate-y-12 translate-x-12 rounded-full bg-emerald-500/10 blur-2xl transition-all group-hover:bg-emerald-500/30" />
      <h3 className="text-lg font-semibold text-zinc-900 dark:text-zinc-50">
        {title}
      </h3>
      <p className="mt-3 flex-1 text-sm leading-relaxed text-zinc-600 dark:text-zinc-400">
        {description}
      </p>
      <p
        className={`mt-6 inline-flex items-center gap-1.5 text-sm font-semibold ${
          available
            ? "text-emerald-600 dark:text-emerald-400"
            : "text-zinc-400 dark:text-zinc-600"
        }`}
      >
        {available ? (
          <>
            {cta} <span aria-hidden>→</span>
          </>
        ) : (
          <>
            <span className="inline-block h-1.5 w-1.5 rounded-full bg-red-500" />
            Coming soon
          </>
        )}
      </p>
    </div>
  );
  return available ? <Link href={href}>{body}</Link> : body;
}

function SignalCard({
  tier,
  label,
  score,
  description,
}: {
  tier: "hot" | "warm" | "cold";
  label: string;
  score: string;
  description: string;
}) {
  const styles = {
    hot: {
      ring: "ring-emerald-500/40",
      bg: "bg-emerald-50 dark:bg-emerald-950/40",
      dot: "bg-emerald-500 shadow-[0_0_12px_rgba(16,185,129,0.7)]",
      text: "text-emerald-700 dark:text-emerald-300",
    },
    warm: {
      ring: "ring-amber-500/40",
      bg: "bg-amber-50 dark:bg-amber-950/40",
      dot: "bg-amber-500 shadow-[0_0_12px_rgba(245,158,11,0.6)]",
      text: "text-amber-700 dark:text-amber-300",
    },
    cold: {
      ring: "ring-red-500/40",
      bg: "bg-red-50 dark:bg-red-950/40",
      dot: "bg-red-500 shadow-[0_0_12px_rgba(239,68,68,0.6)]",
      text: "text-red-700 dark:text-red-300",
    },
  }[tier];

  return (
    <div
      className={`rounded-2xl p-6 ring-1 ${styles.ring} ${styles.bg}`}
    >
      <div className="flex items-center gap-2">
        <span className={`inline-block h-2.5 w-2.5 rounded-full ${styles.dot}`} />
        <span className={`text-sm font-semibold uppercase tracking-wide ${styles.text}`}>
          {label}
        </span>
      </div>
      <p className="mt-3 font-mono text-2xl font-semibold text-zinc-900 dark:text-zinc-50">
        {score}
      </p>
      <p className="mt-2 text-sm text-zinc-600 dark:text-zinc-400">
        {description}
      </p>
    </div>
  );
}
