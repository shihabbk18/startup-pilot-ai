export type GeneratorType =
  | "business_plan"
  | "lean_canvas"
  | "marketing_plan"
  | "roadmap"
  | "pitch_deck"
  | "database"
  | "api"
  | "architecture"
  | "tech_stack"
  | "investor_readiness";

export interface Project {
  id: string;
  organization_id: string;
  owner_id: string;
  name: string;
  idea: string;
  industry?: string | null;
  stage: string;
  created_at: string;
  updated_at: string;
}

export interface FullPlanResponse {
  title: string;
  sections: Record<string, string | string[] | Record<string, unknown>>;
  markdown: string;
}

