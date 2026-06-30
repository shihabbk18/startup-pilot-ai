import type { GeneratorType } from "@/types/api";

export interface GeneratorDefinition {
  slug: string;
  type: GeneratorType;
  title: string;
  shortTitle: string;
  description: string;
  sections: string[];
  sampleOutput: string[];
}

export const generators: GeneratorDefinition[] = [
  {
    slug: "business-plan",
    type: "business_plan",
    title: "Business Plan Generator",
    shortTitle: "Business Plan",
    description: "Create a complete business plan with positioning, market, revenue, risks, and execution priorities.",
    sections: ["Startup overview", "Problem", "Market analysis", "Revenue model", "Risk analysis"],
    sampleOutput: ["Executive summary", "Target segment", "Business model", "90-day validation plan"]
  },
  {
    slug: "lean-canvas",
    type: "lean_canvas",
    title: "Lean Canvas Generator",
    shortTitle: "Lean Canvas",
    description: "Turn an idea into a concise Lean Canvas with problem, solution, metrics, channels, and unfair advantage.",
    sections: ["Problem", "Solution", "Key metrics", "Channels", "Cost and revenue"],
    sampleOutput: ["Top 3 problems", "MVP solution", "Unique value proposition", "Early adopter segment"]
  },
  {
    slug: "marketing-plan",
    type: "marketing_plan",
    title: "Marketing Plan Generator",
    shortTitle: "Marketing Plan",
    description: "Generate positioning, acquisition channels, launch campaigns, lifecycle messaging, and growth experiments.",
    sections: ["Positioning", "Acquisition", "Launch plan", "Lifecycle", "Growth loops"],
    sampleOutput: ["ICP messaging", "Channel strategy", "Launch calendar", "Campaign experiments"]
  },
  {
    slug: "roadmap",
    type: "roadmap",
    title: "Roadmap Generator",
    shortTitle: "Roadmap",
    description: "Plan MVP scope, sprint sequence, later roadmap phases, and measurable product milestones.",
    sections: ["MVP scope", "Sprint plan", "Milestones", "Nice-to-have features", "Release risks"],
    sampleOutput: ["MVP feature list", "Sprint breakdown", "Release criteria", "Post-MVP roadmap"]
  },
  {
    slug: "pitch-deck",
    type: "pitch_deck",
    title: "Pitch Deck Generator",
    shortTitle: "Pitch Deck",
    description: "Create an investor-ready pitch structure with narrative, traction assumptions, and slide-by-slide outline.",
    sections: ["Narrative", "Problem", "Solution", "Market", "Ask"],
    sampleOutput: ["Investor pitch", "Slide outline", "Funding ask", "Traction proof points"]
  },
  {
    slug: "database",
    type: "database",
    title: "Database Generator",
    shortTitle: "Database",
    description: "Design production entities, relationships, indexes, and ER diagrams for the MVP backend.",
    sections: ["Entities", "Relationships", "Indexes", "ER diagram", "Data risks"],
    sampleOutput: ["PostgreSQL tables", "Relationship map", "Index strategy", "Mermaid ERD"]
  },
  {
    slug: "api",
    type: "api",
    title: "API Generator",
    shortTitle: "API",
    description: "Generate REST resources, endpoint contracts, auth rules, validation, and error patterns.",
    sections: ["Resources", "Endpoints", "Auth", "Validation", "Errors"],
    sampleOutput: ["REST endpoint list", "Request/response DTOs", "RBAC rules", "Error model"]
  },
  {
    slug: "architecture",
    type: "architecture",
    title: "Architecture Generator",
    shortTitle: "Architecture",
    description: "Produce system architecture, cloud deployment plan, scaling strategy, and security boundaries.",
    sections: ["Components", "Data flow", "Deployment", "Scaling", "Security"],
    sampleOutput: ["System diagram", "Cloud topology", "Scaling plan", "Security recommendations"]
  },
  {
    slug: "tech-stack",
    type: "tech_stack",
    title: "Tech Stack Generator",
    shortTitle: "Tech Stack",
    description: "Recommend frontend, backend, database, AI, storage, deployment, and observability choices.",
    sections: ["Frontend", "Backend", "Database", "AI", "Infrastructure"],
    sampleOutput: ["Recommended stack", "Build-vs-buy notes", "Cost estimate", "Hiring implications"]
  },
  {
    slug: "investor-readiness",
    type: "investor_readiness",
    title: "Investor Readiness Score",
    shortTitle: "Investor Readiness",
    description: "Score the idea against market, product, moat, traction, financial, and risk readiness dimensions.",
    sections: ["Score", "Strengths", "Gaps", "Risks", "Next actions"],
    sampleOutput: ["Readiness score", "Investor gaps", "Risk mitigation", "Fundraising checklist"]
  }
];

export function getGeneratorBySlug(slug: string) {
  return generators.find((generator) => generator.slug === slug);
}

