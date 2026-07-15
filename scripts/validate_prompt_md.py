#!/usr/bin/env python3
"""Validate a single-scene render prompt or an optional Cookbook style spec."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


FILE_RE = re.compile(r"^.+_v(?P<version>\d+\.\d+\.\d+)(?P<compressed>_1000字符)?\.md$")
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
PLACEHOLDER_RE = re.compile(r"\{([A-Z0-9_]+)\}")
ASCII_TERM_RE = re.compile(r"[A-Za-z]")
VERSION_DEPENDENCY_PATTERNS = (
    re.compile(r"上一(?:个)?版本|上一版|上个版本"),
    re.compile(r"前一(?:个)?版本|前一版|旧版本|旧版"),
    re.compile(r"原版本|原(?:\s*)?(?:prompt|提示词)", re.IGNORECASE),
    re.compile(r"其余(?:内容|部分)?(?:保持)?不变|其他(?:内容|部分)?(?:保持)?不变"),
    re.compile(r"未提及(?:的)?部分(?:保持)?不变|同前|同上(?:版|版本)?"),
    re.compile(r"之前(?:的)?(?:\s*)?(?:prompt|提示词|版本)", re.IGNORECASE),
)

STYLE_REQUIRED_FIELDS = {
    "style_name", "style_slug", "style_version", "style_summary",
    "environment_variables", "style_fidelity_anchors", "source_content_to_avoid",
    "visual_deconstruction", "composition", "typography", "color_palette",
    "design_rules", "do", "avoid", "prompt_template", "negative_prompt", "examples",
}
STYLE_ALLOWED_FIELDS = STYLE_REQUIRED_FIELDS | {"image_treatment", "photographic_direction"}
STYLE_REQUIRED_ENV = {
    "SUBJECT", "SUBJECT_ACTION", "PRODUCT_OR_PROP", "LOCATION",
    "BACKGROUND_ELEMENTS", "MAIN_TEXT", "SECONDARY_TEXT", "ACCENT_SYMBOL",
    "WARDROBE_STYLE", "ASPECT_RATIO",
}

RENDER_REQUIRED_FIELDS = {
    "prompt_name", "prompt_version", "format", "creative_direction", "style_direction",
    "scene", "visual_hierarchy", "composition", "typography", "color_lighting_material",
    "reference_images", "hard_constraints", "negative_prompt",
}
FORMAT_FIELDS = {"type", "aspect_ratio", "use_case"}
CREATIVE_FIELDS = {
    "visual_thesis", "dominant_move", "supporting_moves", "deliberate_sacrifice", "anti_generic",
}
STYLE_DIRECTION_FIELDS = {"style_formula", "primary_style", "secondary_influences", "coherence_rule"}
INFLUENCE_FIELDS = {"english_terms", "role", "visible_effect"}
SCENE_FIELDS = {"subject", "action", "environment", "product_or_props", "spatial_relationship"}
HIERARCHY_FIELDS = {"first_glance", "second_read", "detail_reward"}
COMPOSITION_FIELDS = {
    "camera_and_perspective", "mass_and_scale", "negative_space", "crop_and_edges",
    "depth_and_visual_flow",
}
TYPOGRAPHY_FIELDS = {"exact_text", "type_direction", "placement_and_behavior"}
COLOR_FIELDS = {"color_system", "lighting", "material_behavior", "production_finish"}
REFERENCE_FIELDS = {"reference", "priority", "role", "learn", "preserve", "do_not_copy"}


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def non_empty_string(value: Any) -> bool:
    return isinstance(value, str) and bool(value.strip())


def validate_exact_object(
    value: Any,
    fields: set[str],
    label: str,
    errors: list[str],
    *,
    strings: bool = True,
) -> None:
    require(isinstance(value, dict), f"{label} must be an object", errors)
    if not isinstance(value, dict):
        return
    require(set(value) == fields, f"{label} must contain exactly: {sorted(fields)}", errors)
    if strings:
        require(all(non_empty_string(item) for item in value.values()),
                f"all {label} values must be non-empty strings", errors)


def validate_string_list(
    value: Any,
    label: str,
    errors: list[str],
    *,
    minimum: int = 0,
    maximum: int | None = None,
) -> None:
    valid = isinstance(value, list) and all(non_empty_string(item) for item in value)
    require(valid, f"{label} must be an array of non-empty strings", errors)
    if not isinstance(value, list):
        return
    require(len(value) >= minimum, f"{label} must contain at least {minimum} item(s)", errors)
    if maximum is not None:
        require(len(value) <= maximum, f"{label} must contain at most {maximum} item(s)", errors)


def validate_influence(value: Any, label: str, errors: list[str]) -> None:
    validate_exact_object(value, INFLUENCE_FIELDS, label, errors, strings=False)
    if not isinstance(value, dict):
        return
    validate_string_list(value.get("english_terms"), f"{label}.english_terms", errors, minimum=1)
    terms = value.get("english_terms")
    if isinstance(terms, list):
        require(all(ASCII_TERM_RE.search(term) for term in terms if isinstance(term, str)),
                f"{label}.english_terms must use model-sensitive English terms", errors)
    require(non_empty_string(value.get("role")), f"{label}.role must be non-empty", errors)
    require(non_empty_string(value.get("visible_effect")),
            f"{label}.visible_effect must be non-empty", errors)


def validate_render_prompt(data: dict[str, Any], version: str, errors: list[str]) -> None:
    keys = set(data)
    require(not (RENDER_REQUIRED_FIELDS - keys),
            f"missing render-prompt fields: {sorted(RENDER_REQUIRED_FIELDS - keys)}", errors)
    require(not (keys - RENDER_REQUIRED_FIELDS),
            f"unexpected render-prompt fields: {sorted(keys - RENDER_REQUIRED_FIELDS)}", errors)
    require(data.get("prompt_version") == version, "prompt_version does not match filename", errors)
    require(non_empty_string(data.get("prompt_name")), "prompt_name must be non-empty", errors)

    validate_exact_object(data.get("format"), FORMAT_FIELDS, "format", errors)
    validate_exact_object(data.get("creative_direction"), CREATIVE_FIELDS,
                          "creative_direction", errors, strings=False)
    creative = data.get("creative_direction")
    if isinstance(creative, dict):
        for key in ("visual_thesis", "dominant_move", "deliberate_sacrifice"):
            require(non_empty_string(creative.get(key)),
                    f"creative_direction.{key} must be non-empty", errors)
        validate_string_list(creative.get("supporting_moves"),
                             "creative_direction.supporting_moves", errors, minimum=1, maximum=2)
        validate_string_list(creative.get("anti_generic"),
                             "creative_direction.anti_generic", errors, minimum=1, maximum=3)

    validate_exact_object(data.get("style_direction"), STYLE_DIRECTION_FIELDS,
                          "style_direction", errors, strings=False)
    style = data.get("style_direction")
    if isinstance(style, dict):
        formula = style.get("style_formula")
        require(non_empty_string(formula) and bool(ASCII_TERM_RE.search(formula)),
                "style_direction.style_formula must contain English style terms", errors)
        validate_influence(style.get("primary_style"), "style_direction.primary_style", errors)
        secondary = style.get("secondary_influences")
        require(isinstance(secondary, list), "style_direction.secondary_influences must be an array", errors)
        if isinstance(secondary, list):
            require(len(secondary) <= 2, "style_direction.secondary_influences must contain at most 2 items", errors)
            for index, influence in enumerate(secondary):
                validate_influence(influence, f"style_direction.secondary_influences[{index}]", errors)
        require(non_empty_string(style.get("coherence_rule")),
                "style_direction.coherence_rule must be non-empty", errors)

    validate_exact_object(data.get("scene"), SCENE_FIELDS, "scene", errors)
    validate_exact_object(data.get("visual_hierarchy"), HIERARCHY_FIELDS,
                          "visual_hierarchy", errors)
    validate_exact_object(data.get("composition"), COMPOSITION_FIELDS, "composition", errors)
    validate_exact_object(data.get("typography"), TYPOGRAPHY_FIELDS,
                          "typography", errors, strings=False)
    typography = data.get("typography")
    if isinstance(typography, dict):
        exact_text = typography.get("exact_text")
        require(isinstance(exact_text, dict), "typography.exact_text must be an object", errors)
        if isinstance(exact_text, dict):
            require(all(non_empty_string(value) for value in exact_text.values()),
                    "typography.exact_text values must be non-empty strings", errors)
        require(non_empty_string(typography.get("type_direction")),
                "typography.type_direction must be non-empty", errors)
        require(non_empty_string(typography.get("placement_and_behavior")),
                "typography.placement_and_behavior must be non-empty", errors)
    validate_exact_object(data.get("color_lighting_material"), COLOR_FIELDS,
                          "color_lighting_material", errors)

    references = data.get("reference_images")
    require(isinstance(references, list), "reference_images must be an array", errors)
    if isinstance(references, list):
        for index, reference in enumerate(references):
            validate_exact_object(reference, REFERENCE_FIELDS,
                                  f"reference_images[{index}]", errors)
            if isinstance(reference, dict):
                require(reference.get("priority") in {"high", "medium", "low"},
                        f"reference_images[{index}].priority must be high, medium, or low", errors)

    validate_string_list(data.get("hard_constraints"), "hard_constraints", errors)
    require(isinstance(data.get("negative_prompt"), str), "negative_prompt must be a string", errors)


def validate_style_spec(data: dict[str, Any], version: str, errors: list[str]) -> None:
    keys = set(data)
    require(not (STYLE_REQUIRED_FIELDS - keys),
            f"missing style-spec fields: {sorted(STYLE_REQUIRED_FIELDS - keys)}", errors)
    require(not (keys - STYLE_ALLOWED_FIELDS),
            f"unexpected style-spec fields: {sorted(keys - STYLE_ALLOWED_FIELDS)}", errors)
    require("image_treatment" in data or "photographic_direction" in data,
            "style-spec needs image_treatment or photographic_direction", errors)
    require(data.get("style_version") == version, "style_version does not match filename", errors)
    require(isinstance(data.get("style_slug"), str) and bool(SLUG_RE.fullmatch(data["style_slug"])),
            "style_slug must be lowercase kebab-case", errors)

    env = data.get("environment_variables")
    require(isinstance(env, dict), "environment_variables must be an object", errors)
    if isinstance(env, dict):
        require(not (STYLE_REQUIRED_ENV - set(env)),
                f"missing environment variables: {sorted(STYLE_REQUIRED_ENV - set(env))}", errors)
        require(all(non_empty_string(value) for value in env.values()),
                "all environment variable descriptions must be non-empty strings", errors)
        template = data.get("prompt_template")
        require(non_empty_string(template), "prompt_template must be non-empty", errors)
        if isinstance(template, str):
            undefined = set(PLACEHOLDER_RE.findall(template)) - set(env)
            require(not undefined, f"undefined prompt_template variables: {sorted(undefined)}", errors)

    for field, minimum in (("style_fidelity_anchors", 6), ("source_content_to_avoid", 4),
                           ("design_rules", 4), ("do", 3), ("avoid", 3)):
        validate_string_list(data.get(field), field, errors, minimum=minimum)

    examples = data.get("examples")
    require(isinstance(examples, list) and len(examples) >= 3,
            "style-spec examples must contain at least 3 cases", errors)
    if isinstance(examples, list):
        for index, case in enumerate(examples):
            require(isinstance(case, dict) and set(case) == {"case_name", "values"},
                    f"examples[{index}] must contain only case_name and values", errors)
            if not isinstance(case, dict):
                continue
            require(non_empty_string(case.get("case_name")),
                    f"examples[{index}].case_name must be non-empty", errors)
            values = case.get("values")
            require(isinstance(values, dict) and len(values) >= 5,
                    f"examples[{index}].values must contain at least 5 entries", errors)
            if isinstance(values, dict):
                require("ASPECT_RATIO" not in values,
                        f"examples[{index}] must not define ASPECT_RATIO", errors)
                if isinstance(env, dict):
                    require(not (set(values) - set(env)),
                            f"examples[{index}] uses undeclared variables: {sorted(set(values) - set(env))}", errors)
                require(all(non_empty_string(value) for value in values.values()),
                        f"examples[{index}] values must be non-empty strings", errors)


def detect_mode(data: dict[str, Any], errors: list[str]) -> str | None:
    has_prompt = "prompt_version" in data
    has_style = "style_version" in data
    require(has_prompt != has_style,
            "JSON must contain exactly one version field: prompt_version or style_version", errors)
    if has_prompt and not has_style:
        return "render-prompt"
    if has_style and not has_prompt:
        return "style-spec"
    return None


def validate_document(data: dict[str, Any], version: str, errors: list[str]) -> str | None:
    mode = detect_mode(data, errors)
    if mode == "render-prompt":
        validate_render_prompt(data, version, errors)
    elif mode == "style-spec":
        validate_style_spec(data, version, errors)
    return mode


def validate_json(data: dict[str, Any], version: str, errors: list[str]) -> None:
    """Backward-compatible wrapper used by older local tooling."""
    validate_document(data, version, errors)


def compact_warnings(data: dict[str, Any], text: str) -> list[str]:
    warnings: list[str] = []
    if "prompt_version" in data and len(text.strip()) > 12000:
        warnings.append(
            f"render-prompt has {len(text.strip())} Unicode characters; it is usually at most 12000"
        )
    if "style_version" in data and len(text.strip()) > 16000:
        warnings.append(
            f"style-spec has {len(text.strip())} Unicode characters; review it for repetition"
        )
    template = data.get("prompt_template")
    if isinstance(template, str) and len(template) > 3000:
        warnings.append(
            f"prompt_template has {len(template)} characters; keep it focused on variable assembly and core relations"
        )
    return warnings


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("file", type=Path)
    args = parser.parse_args()
    path = args.file.expanduser().resolve()
    errors: list[str] = []

    match = FILE_RE.match(path.name)
    require(
        match is not None,
        "filename must match <中文项目名>_vX.Y.Z.md or <中文项目名>_vX.Y.Z_1000字符.md",
        errors,
    )
    if not path.is_file():
        raise SystemExit(f"file not found: {path}")
    text = path.read_text(encoding="utf-8")
    stripped = text.strip()
    for pattern in VERSION_DEPENDENCY_PATTERNS:
        dependency = pattern.search(text)
        if dependency:
            errors.append(
                "prompt must be self-contained; expand cross-version dependency instead of using: "
                f"{dependency.group(0)!r}"
            )

    if match and match.group("compressed"):
        require(bool(stripped), "compressed prompt must not be empty", errors)
        require(len(stripped) <= 1000, "compressed prompt must not exceed 1000 Unicode characters", errors)
        require("```" not in text, "compressed prompt must not use Markdown code fences", errors)
        if errors:
            for error in errors:
                print(f"FAIL: {error}")
            raise SystemExit(1)
        print(f"PASS: {path}")
        return

    require(stripped.startswith("{") and stripped.endswith("}"),
            "file must contain only one raw JSON object with no frontmatter, headings, or code fences", errors)

    version = match.group("version") if match else ""
    data: Any = None
    mode: str | None = None
    try:
        data = json.loads(text)
        require(isinstance(data, dict), "prompt JSON must be an object", errors)
        if isinstance(data, dict):
            mode = validate_document(data, version, errors)
    except json.JSONDecodeError as exc:
        errors.append(f"invalid prompt JSON: {exc}")

    if errors:
        for error in errors:
            print(f"FAIL: {error}")
        raise SystemExit(1)
    if isinstance(data, dict):
        for warning in compact_warnings(data, text):
            print(f"WARN: {warning}")
    print(f"PASS: {path} ({mode})")


if __name__ == "__main__":
    main()
