import Link from "next/link";

import { Button } from "@/components/ui/button";

export default function HomePage() {
  return (
    <main className="min-h-screen bg-background p-6">
      <section className="mx-auto grid min-h-[calc(100vh-48px)] max-w-6xl content-center gap-8">
        <div className="max-w-4xl">
          <p className="mb-4 text-sm font-black uppercase text-accent">AI startup planning SaaS</p>
          <h1 className="text-5xl font-black leading-none tracking-normal md:text-7xl">
            Turn a raw startup idea into an investor-ready MVP plan.
          </h1>
          <p className="mt-6 max-w-2xl text-lg text-muted">
            StartupPilot AI generates business plans, canvases, roadmap, API design, database
            schema, architecture, pitch material, and risk analysis from one founder idea.
          </p>
          <div className="mt-8 flex flex-wrap gap-3">
            <Link href="/dashboard">
              <Button>Open dashboard</Button>
            </Link>
            <Link href="/generators">
              <Button variant="secondary">Explore generators</Button>
            </Link>
          </div>
        </div>
      </section>
    </main>
  );
}

