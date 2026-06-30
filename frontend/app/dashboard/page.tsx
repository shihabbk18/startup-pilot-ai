import { ArrowUpRight, Bot, FileText, FolderKanban, Library, Users } from "lucide-react";
import Link from "next/link";

import { Sidebar } from "@/components/sidebar";
import { Button } from "@/components/ui/button";
import { generators } from "@/lib/generators";

const cards = [
  { label: "Projects", value: "12", icon: FolderKanban },
  { label: "Recent generations", value: "48", icon: Bot },
  { label: "Saved reports", value: "31", icon: FileText },
  { label: "Documents indexed", value: "146", icon: Library }
];

export default function DashboardPage() {
  return (
    <main className="grid min-h-screen grid-cols-1 bg-background xl:grid-cols-[280px_1fr]">
      <Sidebar />
      <section className="p-5 md:p-8">
        <header className="mb-6 flex flex-col gap-4 md:flex-row md:items-end md:justify-between">
          <div>
            <p className="mb-2 text-sm font-black uppercase text-accent">Workspace dashboard</p>
            <h2 className="text-4xl font-black tracking-normal md:text-5xl">MVP planning command center</h2>
          </div>
          <Button>New startup plan</Button>
        </header>

        <section className="mb-6 grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {cards.map((card) => (
            <article className="rounded-lg border border-border bg-card p-5" key={card.label}>
              <card.icon className="mb-5 h-5 w-5 text-accent" />
              <span className="block text-4xl font-black">{card.value}</span>
              <p className="mt-1 text-sm font-bold text-muted">{card.label}</p>
            </article>
          ))}
        </section>

        <section className="grid gap-4 xl:grid-cols-[1.2fr_0.8fr]">
          <article className="rounded-lg border border-border bg-card p-5">
            <div className="mb-5 flex items-center justify-between">
              <div>
                <p className="text-xs font-black uppercase text-accent">Generators</p>
                <h3 className="text-2xl font-black">Build any MVP artifact</h3>
              </div>
              <ArrowUpRight className="h-5 w-5 text-muted" />
            </div>
            <div className="grid gap-3 md:grid-cols-2">
              {generators.map((generator) => (
                <Link
                  className="rounded-lg border border-border p-4 font-bold text-muted transition hover:border-primary hover:text-foreground"
                  href={`/generators/${generator.slug}`}
                  key={generator.slug}
                >
                  {generator.shortTitle}
                </Link>
              ))}
            </div>
          </article>

          <article className="rounded-lg border border-border bg-card p-5">
            <p className="text-xs font-black uppercase text-accent">Team and readiness</p>
            <h3 className="mt-1 text-2xl font-black">Investor readiness score</h3>
            <div className="my-6 h-3 overflow-hidden rounded-full bg-white/10">
              <div className="h-full w-[74%] rounded-full bg-accent" />
            </div>
            <p className="text-sm leading-6 text-muted">
              Current workspace is strong on product clarity and roadmap, but needs more market
              evidence, financial assumptions, and competitor proof before investor outreach.
            </p>
            <div className="mt-6 flex items-center gap-3 rounded-lg border border-border p-4">
              <Users className="h-5 w-5 text-accent" />
              <div>
                <strong>5 team members</strong>
                <p className="text-sm text-muted">Owner, admin, editor, and viewer roles enabled.</p>
              </div>
            </div>
          </article>
        </section>
      </section>
    </main>
  );
}
