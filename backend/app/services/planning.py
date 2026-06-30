from app.models.entities import GeneratorType


PLAN_SECTIONS: dict[str, str] = {
    "startup_overview": "Summarize the startup concept, core value proposition, and why now.",
    "problem_statement": "Define the painful problem and current alternatives.",
    "target_audience": "Describe the primary buyer, user, and early adopter segments.",
    "user_personas": "Create realistic founder-facing personas with goals and objections.",
    "market_analysis": "Analyze market size, trends, timing, and category dynamics.",
    "competitor_analysis": "Compare direct, indirect, and substitute competitors.",
    "swot_analysis": "List strengths, weaknesses, opportunities, and threats.",
    "business_model_canvas": "Fill key partners, activities, resources, value propositions, channels, customer relationships, segments, costs, and revenues.",
    "lean_canvas": "Fill problem, solution, metrics, unfair advantage, channels, costs, and revenue.",
    "revenue_model": "Recommend revenue streams and monetization assumptions.",
    "pricing_strategy": "Recommend packages, price anchors, and experiments.",
    "customer_acquisition_strategy": "Recommend repeatable acquisition loops.",
    "marketing_strategy": "Recommend positioning, messaging, and launch campaigns.",
    "product_roadmap": "Create phased roadmap from MVP to scale.",
    "mvp_feature_list": "Prioritize must-have MVP features.",
    "nice_to_have_features": "List valuable features deferred from MVP.",
    "database_schema": "Design core entities and relationships.",
    "rest_api_design": "Design REST resources and endpoint boundaries.",
    "authentication_flow": "Describe auth, onboarding, password, OAuth, and RBAC flow.",
    "system_architecture": "Recommend architecture components and data flow.",
    "er_diagram": "Provide Mermaid ER diagram.",
    "frontend_page_structure": "List frontend pages and responsibilities.",
    "wireframes": "Provide Mermaid wireframe-level layout diagrams.",
    "user_flow_diagrams": "Provide Mermaid user flow diagrams.",
    "recommended_technology_stack": "Recommend frontend, backend, database, AI, infra, and observability.",
    "cloud_deployment_plan": "Describe deployment topology and environments.",
    "cost_estimation": "Estimate monthly tools, infra, and AI costs.",
    "scaling_strategy": "Recommend scaling patterns and bottleneck mitigation.",
    "security_recommendations": "Recommend product, app, infra, and AI security controls.",
    "ai_feature_recommendations": "Identify AI features and guardrails.",
    "development_timeline": "Estimate phases and milestones.",
    "sprint_planning": "Break MVP into two-week sprints.",
    "investor_pitch": "Draft a concise investor pitch.",
    "pitch_deck_outline": "Outline a 10-12 slide deck.",
    "risk_analysis": "Identify risks and mitigation plans.",
}


GENERATOR_SECTION_MAP: dict[GeneratorType, list[str]] = {
    GeneratorType.BUSINESS_PLAN: [
        "startup_overview",
        "problem_statement",
        "target_audience",
        "market_analysis",
        "revenue_model",
        "pricing_strategy",
        "risk_analysis",
    ],
    GeneratorType.LEAN_CANVAS: ["lean_canvas"],
    GeneratorType.MARKETING_PLAN: [
        "customer_acquisition_strategy",
        "marketing_strategy",
        "pricing_strategy",
    ],
    GeneratorType.ROADMAP: ["product_roadmap", "mvp_feature_list", "nice_to_have_features"],
    GeneratorType.PITCH_DECK: ["investor_pitch", "pitch_deck_outline"],
    GeneratorType.DATABASE: ["database_schema", "er_diagram"],
    GeneratorType.API: ["rest_api_design", "authentication_flow"],
    GeneratorType.ARCHITECTURE: ["system_architecture", "cloud_deployment_plan", "scaling_strategy"],
    GeneratorType.TECH_STACK: ["recommended_technology_stack", "cost_estimation"],
    GeneratorType.INVESTOR_READINESS: ["investor_pitch", "risk_analysis", "swot_analysis"],
}


class StartupPlanningEngine:
    """Deterministic planning engine used as fallback and output normalizer."""

    def build_full_plan(self, idea: str, industry: str | None = None) -> dict[str, str | list[str] | dict]:
        context = industry or "the target market"
        return {
            "startup_overview": f"{idea.strip()} is positioned as a focused SaaS-enabled venture for {context}, built around a sharp wedge, fast validation, and measurable customer outcomes.",
            "problem_statement": "Customers face fragmented workflows, low trust in existing options, and high switching friction. The MVP should prove one painful workflow can be solved end to end.",
            "target_audience": ["Early adopters with urgent need", "Budget owners seeking measurable ROI", "Operators currently stitching tools together"],
            "user_personas": [
                "Primary user: time-constrained operator who wants a faster workflow.",
                "Economic buyer: founder or manager who needs ROI and reporting.",
                "Admin: team lead responsible for access, billing, and compliance.",
            ],
            "market_analysis": f"Start with a beachhead in {context}, validate willingness to pay through concierge pilots, then expand into adjacent workflows once retention is proven.",
            "competitor_analysis": "Map competitors by workflow depth, price, AI capability, integrations, and trust. Win with speed, vertical specificity, and better onboarding.",
            "swot_analysis": {
                "strengths": ["Clear AI-assisted planning value", "Fast time to first artifact"],
                "weaknesses": ["Requires trust in AI output", "Needs strong export quality"],
                "opportunities": ["Founder education", "Accelerator partnerships", "Investor readiness tooling"],
                "threats": ["Generic AI tools", "Low-cost template products", "Model quality variance"],
            },
            "business_model_canvas": {
                "segments": ["Founders", "Accelerators", "Startup studios"],
                "value_propositions": ["Complete MVP plan in minutes", "Document-grounded AI assistant", "Export-ready investor artifacts"],
                "channels": ["SEO", "startup communities", "accelerator partnerships"],
                "revenue_streams": ["Subscription", "usage-based exports", "team plans"],
            },
            "lean_canvas": {
                "problem": "Founders struggle to convert raw ideas into complete execution plans.",
                "solution": "AI generators plus RAG over uploaded docs.",
                "key_metrics": ["Activation", "reports generated", "exports", "paid conversion"],
                "unfair_advantage": "Structured startup-specific generation pipeline.",
            },
            "revenue_model": "Subscription tiers with usage limits, team collaboration, premium export packs, and accelerator licensing.",
            "pricing_strategy": "Free trial, $19 solo, $49 pro, $149 team, and custom accelerator plans.",
            "customer_acquisition_strategy": "Use SEO templates, founder communities, Product Hunt launch, accelerator partnerships, and viral report sharing.",
            "marketing_strategy": "Position as the fastest path from idea to MVP plan. Lead with before/after examples and investor-ready outputs.",
            "product_roadmap": ["MVP generators", "Document RAG", "Exports", "Team workspaces", "Billing", "Advanced investor scoring"],
            "mvp_feature_list": ["Idea intake", "Full plan generator", "Saved reports", "Markdown/PDF export", "AI chat", "Document upload"],
            "nice_to_have_features": ["Collaborative comments", "Benchmark data", "Pitch rehearsal", "Financial model builder"],
            "database_schema": "Organizations, users, memberships, projects, generations, reports, documents, chunks, conversations, messages, exports, audit logs.",
            "rest_api_design": "Expose tenant-scoped resources under /api/v1 with JWT auth, typed request schemas, and async job endpoints.",
            "authentication_flow": "Email/password and Google OAuth issue JWT access tokens. Membership roles gate project, billing, and admin actions.",
            "system_architecture": "Next.js frontend, FastAPI backend, PostgreSQL, Redis, Supabase Storage, ChromaDB, OpenAI, worker processes, Vercel, Railway.",
            "er_diagram": "erDiagram\n  ORGANIZATIONS ||--o{ PROJECTS : owns\n  USERS ||--o{ MEMBERSHIPS : has\n  PROJECTS ||--o{ GENERATIONS : creates\n  PROJECTS ||--o{ REPORTS : stores\n  PROJECTS ||--o{ DOCUMENTS : indexes",
            "frontend_page_structure": ["Dashboard", "Projects", "Generators", "AI Chat", "Documents", "Exports", "Team", "Billing", "Settings"],
            "wireframes": "flowchart TD\n  Dashboard --> ProjectDetail\n  ProjectDetail --> Generators\n  ProjectDetail --> Reports\n  ProjectDetail --> Chat",
            "user_flow_diagrams": "flowchart LR\n  Idea --> GeneratePlan --> ReviewReport --> Export --> Share",
            "recommended_technology_stack": "Next.js, TypeScript, Tailwind, shadcn/ui, FastAPI, SQLAlchemy, PostgreSQL, Redis, Supabase Storage, OpenAI, LangChain, LlamaIndex, ChromaDB.",
            "cloud_deployment_plan": "Deploy frontend to Vercel, API and workers to Railway, managed PostgreSQL/Redis on Railway, Supabase for file storage.",
            "cost_estimation": "$150-$500/month early stage depending on AI usage, storage, database size, and team seats.",
            "scaling_strategy": "Queue long-running AI/export jobs, cache repeated reads, shard vector stores by tenant, add read replicas, and rate-limit generation endpoints.",
            "security_recommendations": "Tenant isolation, RBAC, audit logs, encrypted secrets, signed upload URLs, prompt-injection hardening, and export access controls.",
            "ai_feature_recommendations": ["RAG over founder docs", "Investor readiness scoring", "Prompt versioning", "Citation-backed chat", "Export formatting assistant"],
            "development_timeline": "8-10 weeks for production MVP with auth, projects, core generators, RAG, exports, billing, and deployment.",
            "sprint_planning": ["Sprint 1: auth/projects", "Sprint 2: generators/reports", "Sprint 3: RAG/documents", "Sprint 4: exports/billing", "Sprint 5: hardening"],
            "investor_pitch": f"StartupPilot AI turns a raw idea like '{idea.strip()}' into a complete execution and fundraising package in minutes.",
            "pitch_deck_outline": ["Problem", "Solution", "Market", "Product", "AI moat", "Business model", "Go-to-market", "Traction", "Team", "Ask"],
            "risk_analysis": "Risks include generic AI competition, hallucinated output, high AI costs, and low conversion. Mitigate with structured workflows, citations, usage controls, and high-quality exports.",
        }

    def build_generator_plan(
        self,
        idea: str,
        generator_type: GeneratorType,
        industry: str | None = None,
    ) -> dict[str, str | list[str] | dict]:
        full_plan = self.build_full_plan(idea=idea, industry=industry)
        section_keys = GENERATOR_SECTION_MAP[generator_type]
        return {key: full_plan[key] for key in section_keys}


def render_markdown(title: str, sections: dict[str, str | list[str] | dict]) -> str:
    """Render a structured report to Markdown."""
    lines = [f"# {title}", ""]
    for key, value in sections.items():
        heading = key.replace("_", " ").title()
        lines.append(f"## {heading}")
        if isinstance(value, list):
            lines.extend(f"- {item}" for item in value)
        elif isinstance(value, dict):
            lines.extend(f"- **{item_key.replace('_', ' ').title()}**: {item_value}" for item_key, item_value in value.items())
        else:
            lines.append(value)
        lines.append("")
    return "\n".join(lines).strip()

