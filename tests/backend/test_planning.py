from app.models.entities import GeneratorType
from app.services.planning import StartupPlanningEngine, render_markdown


def test_full_plan_contains_required_sections() -> None:
    engine = StartupPlanningEngine()
    plan = engine.build_full_plan("Uber for pet care", "pet care")

    assert "startup_overview" in plan
    assert "database_schema" in plan
    assert "pitch_deck_outline" in plan
    assert "risk_analysis" in plan


def test_generator_plan_is_scoped() -> None:
    engine = StartupPlanningEngine()
    plan = engine.build_generator_plan(
        idea="AI receptionist for clinics",
        generator_type=GeneratorType.API,
        industry="healthcare",
    )

    assert set(plan.keys()) == {"rest_api_design", "authentication_flow"}


def test_markdown_renderer_outputs_headings() -> None:
    markdown = render_markdown("Test Report", {"mvp_feature_list": ["Auth", "Dashboard"]})

    assert markdown.startswith("# Test Report")
    assert "## Mvp Feature List" in markdown
    assert "- Auth" in markdown

