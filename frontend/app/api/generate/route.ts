import { NextResponse } from "next/server";

import { getGeneratorBySlug } from "@/lib/generators";

interface GenerateRequest {
  slug: string;
  idea: string;
  industry: string;
  depth: string;
}

interface ModelSection {
  title: string;
  body: string;
  bullets: string[];
}

interface ModelReport {
  assumptionSummary: string;
  sections: ModelSection[];
}

const OPENAI_RESPONSES_URL = "https://api.openai.com/v1/responses";

function extractOutputText(payload: unknown): string {
  if (!payload || typeof payload !== "object") return "";
  const data = payload as { output_text?: string; output?: Array<{ content?: Array<{ text?: string }> }> };
  if (typeof data.output_text === "string") return data.output_text;
  return (
    data.output
      ?.flatMap((item) => item.content || [])
      .map((content) => content.text || "")
      .join("\n") || ""
  );
}

function parseModelJson(text: string): ModelReport {
  const cleanText = text
    .trim()
    .replace(/^```json\s*/i, "")
    .replace(/^```\s*/i, "")
    .replace(/```$/i, "")
    .trim();
  const parsed = JSON.parse(cleanText) as ModelReport;

  if (!parsed.assumptionSummary || !Array.isArray(parsed.sections)) {
    throw new Error("Model response did not match the expected report shape.");
  }

  return {
    assumptionSummary: parsed.assumptionSummary,
    sections: parsed.sections.map((section) => ({
      title: String(section.title || "Untitled section"),
      body: String(section.body || ""),
      bullets: Array.isArray(section.bullets) ? section.bullets.map(String) : []
    }))
  };
}

function buildPrompt(generatorTitle: string, payload: GenerateRequest) {
  return `Generate a serious, non-generic startup planning artifact.

Generator: ${generatorTitle}
Startup idea: ${payload.idea}
Industry/context: ${payload.industry || "Not specified"}
Depth: ${payload.depth}

Rules:
- Analyze the idea before producing output.
- Do not add random AI, ML, blockchain, big data, or marketplace features unless the idea actually needs them.
- Make architecture sections technically specific: services, data flow, scaling, security, queues, database, observability.
- Make roadmap sections practical: MVP boundary, sprint sequencing, dependencies, risks, post-MVP only when justified.
- Make investor readiness sections evidence-based: score rationale, validation gaps, metrics, fundraising blockers.
- For marketplace ideas, cover demand side, supply side, trust, payments, fulfillment, cancellation, and liquidity.
- For SaaS ideas, cover tenants, roles, data model, workflows, billing, audit logs, integrations, and support.
- Return only valid JSON. No markdown fences.

JSON shape:
{
  "assumptionSummary": "One short paragraph explaining how you interpreted the idea.",
  "sections": [
    {
      "title": "Section title",
      "body": "A specific paragraph with analysis.",
      "bullets": ["Specific bullet", "Specific bullet"]
    }
  ]
}`;
}

export async function POST(request: Request) {
  const apiKey = process.env.OPENAI_API_KEY;
  const model = process.env.OPENAI_MODEL || "gpt-5.5";

  if (!apiKey) {
    return NextResponse.json(
      {
        error:
          "OPENAI_API_KEY is not configured. Add it to startup-pilot-ai/frontend/.env.local and restart npm run dev."
      },
      { status: 503 }
    );
  }

  const payload = (await request.json()) as GenerateRequest;
  const generator = getGeneratorBySlug(payload.slug);

  if (!generator || !payload.idea?.trim()) {
    return NextResponse.json({ error: "Generator slug and startup idea are required." }, { status: 400 });
  }

  const response = await fetch(OPENAI_RESPONSES_URL, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${apiKey}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      model,
      input: [
        {
          role: "system",
          content:
            "You are StartupPilot AI, a senior startup strategist, staff software engineer, AI architect, and investor-readiness advisor. Produce concrete, idea-specific SaaS planning outputs."
        },
        {
          role: "user",
          content: buildPrompt(generator.title, payload)
        }
      ],
      max_output_tokens: 3200
    })
  });

  const data = await response.json();

  if (!response.ok) {
    return NextResponse.json(
      { error: data?.error?.message || "OpenAI generation failed." },
      { status: response.status }
    );
  }

  try {
    return NextResponse.json(parseModelJson(extractOutputText(data)));
  } catch (error) {
    return NextResponse.json(
      {
        error:
          error instanceof Error
            ? `Model returned an invalid structured report: ${error.message}`
            : "Model returned an invalid structured report."
      },
      { status: 502 }
    );
  }
}
