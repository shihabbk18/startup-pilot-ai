import Link from "next/link";
import { notFound } from "next/navigation";
import { ArrowLeft, CheckCircle2 } from "lucide-react";

import { Sidebar } from "@/components/sidebar";
import { GeneratorWorkspace } from "@/components/generator-workspace";
import { generators, getGeneratorBySlug } from "@/lib/generators";

interface GeneratorDetailPageProps {
  params: {
    slug: string;
  };
}

export function generateStaticParams() {
  return generators.map((generator) => ({ slug: generator.slug }));
}

export default function GeneratorDetailPage({ params }: GeneratorDetailPageProps) {
  const generator = getGeneratorBySlug(params.slug);

  if (!generator) {
    notFound();
  }

  return (
    <main className="grid min-h-screen grid-cols-1 bg-background xl:grid-cols-[280px_1fr]">
      <Sidebar />
      <section className="p-5 md:p-8">
        <Link
          className="mb-5 inline-flex items-center gap-2 text-sm font-bold text-muted transition hover:text-foreground"
          href="/generators"
        >
          <ArrowLeft className="h-4 w-4" />
          All generators
        </Link>

        <header className="mb-6 grid gap-5 xl:grid-cols-[1.1fr_0.9fr]">
          <div>
            <p className="mb-2 text-sm font-black uppercase text-accent">Configure generator</p>
            <h2 className="text-4xl font-black tracking-normal md:text-5xl">{generator.title}</h2>
            <p className="mt-4 max-w-3xl text-base leading-7 text-muted">{generator.description}</p>
          </div>
          <article className="rounded-lg border border-border bg-card p-5">
            <p className="text-xs font-black uppercase text-accent">What this produces</p>
            <div className="mt-4 grid gap-3">
              {generator.sections.map((section) => (
                <div className="flex items-center gap-3 text-sm font-bold text-muted" key={section}>
                  <CheckCircle2 className="h-4 w-4 text-accent" />
                  {section}
                </div>
              ))}
            </div>
          </article>
        </header>

        <GeneratorWorkspace generator={generator} />
      </section>
    </main>
  );
}
