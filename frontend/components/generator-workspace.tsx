"use client";

import { useMemo, useState } from "react";
import { CheckCircle2, Copy, Download, Loader2, Sparkles } from "lucide-react";

import { Button } from "@/components/ui/button";
import type { GeneratorDefinition } from "@/lib/generators";

interface GeneratedSection {
  title: string;
  body: string;
  bullets: string[];
}

interface GeneratedReport {
  assumptionSummary: string;
  sections: GeneratedSection[];
}

function renderMarkdown(generator: GeneratorDefinition, report: GeneratedReport) {
  return [
    `# ${generator.title}`,
    "",
    `_${report.assumptionSummary}_`,
    "",
    ...report.sections.flatMap((section) => [
      `## ${section.title}`,
      section.body,
      "",
      ...section.bullets.map((bullet) => `- ${bullet}`),
      ""
    ])
  ].join("\n");
}

export function GeneratorWorkspace({ generator }: { generator: GeneratorDefinition }) {
  const [idea, setIdea] = useState("I want to build Uber for pet care.");
  const [industry, setIndustry] = useState("Pet care marketplace");
  const [depth, setDepth] = useState("Investor-ready");
  const [isGenerating, setIsGenerating] = useState(false);
  const [report, setReport] = useState<GeneratedReport | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const markdown = useMemo(
    () => (report ? renderMarkdown(generator, report) : ""),
    [generator, report]
  );

  async function generate() {
    if (!idea.trim()) {
      setError("Add a startup idea before generating.");
      return;
    }

    setIsGenerating(true);
    setError(null);
    setReport(null);

    try {
      const response = await fetch("/api/generate", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          slug: generator.slug,
          idea,
          industry,
          depth
        })
      });
      const data = (await response.json()) as GeneratedReport & { error?: string };

      if (!response.ok) {
        throw new Error(data.error || "Generation failed.");
      }

      setReport({
        assumptionSummary: data.assumptionSummary,
        sections: data.sections
      });
      setCopied(false);
    } catch (caughtError) {
      setError(caughtError instanceof Error ? caughtError.message : "Generation failed.");
    } finally {
      setIsGenerating(false);
    }
  }

  async function copyMarkdown() {
    if (!markdown) return;
    await navigator.clipboard.writeText(markdown);
    setCopied(true);
  }

  function downloadMarkdown() {
    if (!markdown) return;
    const blob = new Blob([markdown], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = `${generator.slug}-startup-plan.md`;
    link.click();
    URL.revokeObjectURL(url);
  }

  return (
    <section className="grid gap-4 xl:grid-cols-[0.9fr_1.1fr]">
      <article className="rounded-lg border border-border bg-card p-5">
        <div className="mb-5 flex items-center gap-3">
          <Sparkles className="h-5 w-5 text-accent" />
          <div>
            <p className="text-xs font-black uppercase text-accent">Input</p>
            <h3 className="text-2xl font-black">Startup idea</h3>
          </div>
        </div>
        <form className="grid gap-4" onSubmit={(event) => event.preventDefault()}>
          <label className="grid gap-2 text-sm font-bold">
            Idea
            <textarea
              className="min-h-36 rounded-lg border border-border bg-background p-3 text-sm leading-6 outline-none focus:border-primary"
              onChange={(event) => setIdea(event.target.value)}
              value={idea}
            />
          </label>
          <label className="grid gap-2 text-sm font-bold">
            Industry
            <input
              className="min-h-11 rounded-lg border border-border bg-background px-3 text-sm outline-none focus:border-primary"
              onChange={(event) => setIndustry(event.target.value)}
              value={industry}
            />
          </label>
          <label className="grid gap-2 text-sm font-bold">
            Output depth
            <select
              className="min-h-11 rounded-lg border border-border bg-background px-3 text-sm outline-none focus:border-primary"
              onChange={(event) => setDepth(event.target.value)}
              value={depth}
            >
              <option>Investor-ready</option>
              <option>MVP execution</option>
              <option>Technical architecture</option>
            </select>
          </label>
          <Button disabled={isGenerating} onClick={generate} type="button" className="w-full">
            {isGenerating ? (
              <span className="inline-flex items-center gap-2">
                <Loader2 className="h-4 w-4 animate-spin" />
                Generating with model...
              </span>
            ) : (
              `Generate ${generator.shortTitle}`
            )}
          </Button>
          {error ? (
            <div className="rounded-lg border border-red-500/40 bg-red-500/10 p-3 text-sm font-bold text-red-200">
              {error}
            </div>
          ) : null}
        </form>
      </article>

      <article className="rounded-lg border border-border bg-card p-5">
        <div className="flex flex-col gap-4 md:flex-row md:items-start md:justify-between">
          <div>
            <p className="text-xs font-black uppercase text-accent">Generated output</p>
            <h3 className="mt-1 text-2xl font-black">
              {report ? `${generator.shortTitle} result` : "Ready to generate"}
            </h3>
          </div>
          <div className="flex flex-wrap gap-2">
            <Button disabled={!report} onClick={copyMarkdown} type="button" variant="secondary">
              <Copy className="mr-2 h-4 w-4" />
              {copied ? "Copied" : "Copy"}
            </Button>
            <Button disabled={!report} onClick={downloadMarkdown} type="button" variant="secondary">
              <Download className="mr-2 h-4 w-4" />
              Markdown
            </Button>
          </div>
        </div>

        {report ? (
          <div className="mt-5 grid gap-3">
            <div className="rounded-lg border border-border bg-background p-4 text-sm font-bold text-muted">
              {report.assumptionSummary}
            </div>
            {report.sections.map((section) => (
              <div className="rounded-lg border border-border bg-background p-4" key={section.title}>
                <div className="mb-3 flex items-center gap-2">
                  <CheckCircle2 className="h-4 w-4 text-accent" />
                  <strong>{section.title}</strong>
                </div>
                <p className="text-sm leading-6 text-muted">{section.body}</p>
                <ul className="mt-3 grid gap-2 text-sm leading-6 text-muted">
                  {section.bullets.map((bullet) => (
                    <li key={bullet}>- {bullet}</li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        ) : (
          <div className="mt-5 grid gap-3">
            {generator.sampleOutput.map((item) => (
              <div className="rounded-lg border border-border bg-background p-4" key={item}>
                <strong>{item}</strong>
                <p className="mt-2 text-sm leading-6 text-muted">
                  Click Generate to call the configured OpenAI model and create a specific,
                  workflow-aware output.
                </p>
              </div>
            ))}
          </div>
        )}
      </article>
    </section>
  );
}
