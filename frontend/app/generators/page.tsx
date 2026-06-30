import Link from "next/link";

import { Sidebar } from "@/components/sidebar";
import { Button } from "@/components/ui/button";
import { generators } from "@/lib/generators";

export default function GeneratorsPage() {
  return (
    <main className="grid min-h-screen grid-cols-1 bg-background xl:grid-cols-[280px_1fr]">
      <Sidebar />
      <section className="p-5 md:p-8">
        <header className="mb-6 max-w-4xl">
          <p className="mb-2 text-sm font-black uppercase text-accent">AI generators</p>
          <h2 className="text-4xl font-black tracking-normal md:text-5xl">
            Structured artifacts for every stage of MVP planning.
          </h2>
        </header>
        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
          {generators.map((generator, index) => (
            <article className="rounded-lg border border-border bg-card p-5" key={generator.slug}>
              <span className="text-sm font-black text-accent">{String(index + 1).padStart(2, "0")}</span>
              <h3 className="mt-4 text-xl font-black">{generator.title}</h3>
              <p className="mt-3 min-h-20 text-sm leading-6 text-muted">
                {generator.description}
              </p>
              <Link href={`/generators/${generator.slug}`}>
                <Button className="mt-5 w-full" variant="secondary">
                  Configure generator
                </Button>
              </Link>
            </article>
          ))}
        </section>
      </section>
    </main>
  );
}
