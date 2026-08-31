#!/usr/bin/env python3
"""Validate, query, resolve, and render the architecture-poster token catalog."""

from __future__ import annotations

import argparse
import html
import json
import sys
from pathlib import Path
from typing import Any


CATALOG_PATH = Path(__file__).resolve().parents[1] / "references" / "design-tokens.json"
TOKEN_FIELDS = {
    "id",
    "tier",
    "category",
    "label",
    "intent",
    "value",
    "tags",
    "requires",
    "compatible",
    "conflicts",
    "constraints",
    "prompt",
    "visual",
    "sources",
}
TIERS = {"primitive", "semantic", "component"}


def load_catalog(path: Path = CATALOG_PATH) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def token_map(catalog: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {token["id"]: token for token in catalog["tokens"]}


def resolve_requires(token_ids: list[str], tokens: dict[str, dict[str, Any]]) -> list[str]:
    resolved: list[str] = []
    active: set[str] = set()
    done: set[str] = set()

    def visit(token_id: str) -> None:
        if token_id in done:
            return
        if token_id in active:
            raise ValueError(f"dependency cycle at {token_id}")
        active.add(token_id)
        for dependency in tokens[token_id].get("requires", []):
            visit(dependency)
        active.remove(token_id)
        done.add(token_id)
        resolved.append(token_id)

    for item in token_ids:
        visit(item)
    return resolved


def selection_errors(
    token_ids: list[str], catalog: dict[str, Any], tokens: dict[str, dict[str, Any]]
) -> list[str]:
    selected = set(token_ids)
    errors: list[str] = []
    conflict_pairs: set[tuple[str, str]] = set()
    for token_id in token_ids:
        for conflict in tokens[token_id].get("conflicts", []):
            if conflict in selected:
                conflict_pairs.add(tuple(sorted((token_id, conflict))))
    for left, right in sorted(conflict_pairs):
        errors.append(f"conflict: {left} <> {right}")

    for group in catalog.get("mutex_groups", []):
        hits = [item for item in group["members"] if item in selected]
        if len(hits) > group["max"]:
            errors.append(
                f"mutex {group['id']} allows {group['max']}, got {len(hits)}: "
                + ", ".join(hits)
            )
    return errors


def validate_catalog(catalog: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    items = catalog.get("tokens")
    if not isinstance(items, list) or not items:
        return ["tokens must be a non-empty list"]

    ids = [item.get("id") for item in items]
    duplicate_ids = sorted({item for item in ids if ids.count(item) > 1})
    if duplicate_ids:
        errors.append("duplicate token ids: " + ", ".join(duplicate_ids))

    tokens = token_map(catalog)
    known = set(tokens)
    for index, token in enumerate(items):
        missing = sorted(TOKEN_FIELDS - set(token))
        token_id = token.get("id", f"tokens[{index}]")
        if missing:
            errors.append(f"{token_id}: missing fields {', '.join(missing)}")
        if not str(token_id).startswith("cap."):
            errors.append(f"{token_id}: id must start with cap.")
        if token.get("tier") not in TIERS:
            errors.append(f"{token_id}: unknown tier {token.get('tier')!r}")
        if not token.get("tags"):
            errors.append(f"{token_id}: at least one search tag is required")
        if not token.get("constraints"):
            errors.append(f"{token_id}: at least one checkable constraint is required")
        if not token.get("sources"):
            errors.append(f"{token_id}: at least one source is required")
        for field in ("requires", "compatible", "conflicts"):
            for reference in token.get(field, []):
                if reference not in known:
                    errors.append(f"{token_id}: unknown {field} reference {reference}")

    for group in catalog.get("mutex_groups", []):
        if not group.get("id") or group.get("max", 0) < 1:
            errors.append(f"invalid mutex group: {group}")
        for member in group.get("members", []):
            if member not in known:
                errors.append(f"{group.get('id')}: unknown member {member}")

    recipe_ids: set[str] = set()
    for recipe in catalog.get("recipes", []):
        recipe_id = recipe.get("id", "<recipe>")
        if recipe_id in recipe_ids:
            errors.append(f"duplicate recipe id: {recipe_id}")
        recipe_ids.add(recipe_id)
        all_refs = recipe.get("tokens", []) + recipe.get("optional", []) + recipe.get("forbidden", [])
        for reference in all_refs:
            if reference not in known:
                errors.append(f"{recipe_id}: unknown token {reference}")
        if any(reference not in known for reference in recipe.get("tokens", [])):
            continue
        try:
            resolved = resolve_requires(recipe.get("tokens", []), tokens)
        except ValueError as exc:
            errors.append(f"{recipe_id}: {exc}")
            continue
        for issue in selection_errors(resolved, catalog, tokens):
            errors.append(f"{recipe_id}: {issue}")
        forbidden = set(recipe.get("forbidden", []))
        overlap = forbidden.intersection(resolved)
        if overlap:
            errors.append(f"{recipe_id}: required and forbidden: {', '.join(sorted(overlap))}")
        if not recipe.get("invariants"):
            errors.append(f"{recipe_id}: at least one invariant is required")

    return errors


def searchable_text(token: dict[str, Any]) -> str:
    fields = [
        token["id"],
        token["label"],
        token["intent"],
        " ".join(token.get("tags", [])),
        " ".join(token.get("constraints", [])),
    ]
    return " ".join(fields).lower()


def query_tokens(
    catalog: dict[str, Any],
    category: str | None,
    tier: str | None,
    tag: str | None,
    search: str | None,
    compatible_with: str | None,
) -> list[dict[str, Any]]:
    tokens = token_map(catalog)
    candidates = list(catalog["tokens"])
    if category:
        candidates = [item for item in candidates if item["category"] == category]
    if tier:
        candidates = [item for item in candidates if item["tier"] == tier]
    if tag:
        needle = tag.lower()
        candidates = [item for item in candidates if any(needle in value.lower() for value in item["tags"])]
    if search:
        needle = search.lower()
        candidates = [item for item in candidates if needle in searchable_text(item)]
    if compatible_with:
        if compatible_with not in tokens:
            raise KeyError(f"unknown token: {compatible_with}")
        peer = tokens[compatible_with]
        candidates = [
            item
            for item in candidates
            if item["id"] != compatible_with
            and (
                item["id"] in peer.get("compatible", [])
                or compatible_with in item.get("compatible", [])
            )
            and item["id"] not in peer.get("conflicts", [])
            and compatible_with not in item.get("conflicts", [])
        ]
    return sorted(candidates, key=lambda item: (item["category"], item["tier"], item["id"]))


def print_tokens(items: list[dict[str, Any]], as_json: bool) -> None:
    if as_json:
        print(json.dumps(items, ensure_ascii=False, indent=2))
        return
    if not items:
        print("No matching tokens.")
        return
    width = max(len(item["id"]) for item in items)
    for item in items:
        print(f"{item['id']:<{width}}  {item['label']}  [{', '.join(item['tags'])}]")


def recipe_payload(catalog: dict[str, Any], recipe_id: str) -> dict[str, Any]:
    recipes = {item["id"]: item for item in catalog.get("recipes", [])}
    if recipe_id not in recipes:
        raise KeyError(f"unknown recipe: {recipe_id}")
    tokens = token_map(catalog)
    recipe = recipes[recipe_id]
    resolved_ids = resolve_requires(recipe["tokens"], tokens)
    return {
        "id": recipe["id"],
        "label": recipe["label"],
        "tags": recipe["tags"],
        "resolved_tokens": [tokens[item] for item in resolved_ids],
        "optional": recipe["optional"],
        "forbidden": recipe["forbidden"],
        "invariants": recipe["invariants"],
        "errors": selection_errors(resolved_ids, catalog, tokens),
    }


def badges(values: list[str], css_class: str = "") -> str:
    return "".join(
        f'<span class="badge {css_class}">{html.escape(value)}</span>' for value in values
    )


def render_catalog(catalog: dict[str, Any]) -> str:
    categories = sorted({item["category"] for item in catalog["tokens"]})
    tiers = ["primitive", "semantic", "component"]
    cards: list[str] = []
    for item in sorted(catalog["tokens"], key=lambda value: (value["category"], value["tier"], value["id"])):
        search_blob = searchable_text(item)
        swatch = html.escape(item.get("visual", {}).get("swatch", "#ddd"), quote=True)
        glyph = html.escape(item.get("visual", {}).get("glyph", ""))
        relations = []
        if item.get("requires"):
            relations.append(f'<div><b>依赖</b>{badges(item["requires"], "requires")}</div>')
        if item.get("compatible"):
            relations.append(f'<div><b>兼容</b>{badges(item["compatible"], "compatible")}</div>')
        if item.get("conflicts"):
            relations.append(f'<div><b>冲突</b>{badges(item["conflicts"], "conflicts")}</div>')
        constraint_list = "".join(f"<li>{html.escape(value)}</li>" for value in item["constraints"])
        cards.append(
            f'''<article class="card" data-category="{html.escape(item['category'])}" data-tier="{html.escape(item['tier'])}" data-search="{html.escape(search_blob, quote=True)}">
  <div class="swatch" style="background:{swatch}"><span>{glyph}</span></div>
  <div class="card-body">
    <div class="eyebrow">{html.escape(item['tier'])} · {html.escape(item['category'])}</div>
    <h2>{html.escape(item['label'])}</h2>
    <code>{html.escape(item['id'])}</code>
    <p>{html.escape(item['intent'])}</p>
    <div class="tags">{badges(item['tags'])}</div>
    <details><summary>参数与约束</summary><pre>{html.escape(json.dumps(item['value'], ensure_ascii=False, indent=2))}</pre><ul>{constraint_list}</ul></details>
    <details><summary>关系</summary>{''.join(relations) or '<p>无显式关系</p>'}</details>
  </div>
</article>'''
        )

    recipe_cards: list[str] = []
    for recipe in catalog.get("recipes", []):
        recipe_cards.append(
            f'''<article class="recipe" data-search="{html.escape((' '.join(recipe['tags']) + ' ' + recipe['label']).lower(), quote=True)}">
  <div class="eyebrow">recipe</div><h2>{html.escape(recipe['label'])}</h2><code>{html.escape(recipe['id'])}</code>
  <div class="tags">{badges(recipe['tags'])}</div>
  <p><b>必选</b>{badges(recipe['tokens'], 'requires')}</p>
  <p><b>可选</b>{badges(recipe['optional'], 'compatible')}</p>
  <p><b>禁用</b>{badges(recipe['forbidden'], 'conflicts')}</p>
  <ul>{''.join(f'<li>{html.escape(value)}</li>' for value in recipe['invariants'])}</ul>
</article>'''
        )

    category_options = "".join(f'<option value="{html.escape(value)}">{html.escape(value)}</option>' for value in categories)
    tier_options = "".join(f'<option value="{value}">{value}</option>' for value in tiers)
    return f'''<!doctype html>
<html lang="zh-CN">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Chinese Architecture Poster · Token Catalog</title>
<style>
:root{{--paper:#eee8dd;--ink:#24211e;--muted:#766f67;--red:#a33b32;--green:#3d6b5f;--line:#cbc1b4}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font-family:Inter,"Noto Sans SC",system-ui,sans-serif}}
header{{position:sticky;top:0;z-index:5;background:rgba(238,232,221,.94);backdrop-filter:blur(12px);border-bottom:1px solid var(--line);padding:22px clamp(20px,5vw,72px)}}
h1{{margin:0 0 6px;font:700 clamp(26px,4vw,54px)/1.05 Georgia,"Noto Serif SC",serif}}header p{{margin:0;color:var(--muted)}}
.controls{{display:grid;grid-template-columns:minmax(180px,1fr) repeat(2,minmax(130px,220px));gap:10px;margin-top:18px}}input,select{{width:100%;border:1px solid var(--line);background:#f7f3eb;padding:12px 14px;color:var(--ink);font:inherit}}
main{{padding:32px clamp(20px,5vw,72px) 80px}}.section-title{{display:flex;align-items:baseline;gap:14px;margin:40px 0 18px}}.section-title h2{{font:700 30px Georgia,"Noto Serif SC",serif;margin:0}}.count{{color:var(--muted)}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(285px,1fr));gap:16px}}.card,.recipe{{background:#f7f3eb;border:1px solid var(--line);min-width:0}}.swatch{{height:116px;display:grid;place-items:center;border-bottom:1px solid var(--line)}}.swatch span{{font:700 38px Georgia,"Noto Serif SC",serif;white-space:pre-line;text-align:center;color:#fff;mix-blend-mode:difference}}.card-body,.recipe{{padding:18px}}.eyebrow{{font-size:11px;letter-spacing:.14em;text-transform:uppercase;color:var(--muted)}}h2{{margin:5px 0 7px;font-size:21px}}code{{font-size:11px;overflow-wrap:anywhere;color:#5d554d}}p{{line-height:1.55}}.badge{{display:inline-block;margin:3px 4px 3px 0;padding:3px 6px;border:1px solid var(--line);font-size:10px;overflow-wrap:anywhere}}.requires{{border-color:#8c7962}}.compatible{{border-color:var(--green);color:var(--green)}}.conflicts{{border-color:var(--red);color:var(--red)}}details{{border-top:1px solid #ded6ca;margin-top:12px;padding-top:10px}}summary{{cursor:pointer;font-weight:650}}pre{{white-space:pre-wrap;font-size:11px}}li{{margin:5px 0;line-height:1.4}}.recipe-grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(360px,1fr));gap:16px}}.hidden{{display:none!important}}
@media(max-width:720px){{.controls{{grid-template-columns:1fr}}.recipe-grid{{grid-template-columns:1fr}}}}
</style>
</head>
<body>
<header><h1>建筑海报 Token Catalog</h1><p>{len(catalog['tokens'])} tokens · {len(catalog.get('recipes', []))} recipes · v{html.escape(catalog['version'])}</p>
<div class="controls"><input id="q" placeholder="检索：塔、中轴、纹样、夜景、Xerox…"><select id="category"><option value="">全部类别</option>{category_options}</select><select id="tier"><option value="">全部层级</option>{tier_options}</select></div></header>
<main><div class="section-title"><h2>Tokens</h2><span class="count" id="tokenCount"></span></div><section class="grid" id="tokenGrid">{''.join(cards)}</section>
<div class="section-title"><h2>Recipes</h2><span class="count" id="recipeCount"></span></div><section class="recipe-grid" id="recipeGrid">{''.join(recipe_cards)}</section></main>
<script>
const q=document.querySelector('#q'),cat=document.querySelector('#category'),tier=document.querySelector('#tier');
function apply(){{const n=q.value.trim().toLowerCase();let tc=0,rc=0;document.querySelectorAll('.card').forEach(el=>{{const ok=(!n||el.dataset.search.includes(n))&&(!cat.value||el.dataset.category===cat.value)&&(!tier.value||el.dataset.tier===tier.value);el.classList.toggle('hidden',!ok);if(ok)tc++}});document.querySelectorAll('.recipe').forEach(el=>{{const ok=(!n||el.dataset.search.includes(n))&&!cat.value&&!tier.value;el.classList.toggle('hidden',!ok);if(ok)rc++}});document.querySelector('#tokenCount').textContent=tc+' results';document.querySelector('#recipeCount').textContent=rc+' results'}}
[q,cat,tier].forEach(el=>el.addEventListener('input',apply));apply();
</script></body></html>'''


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--catalog", type=Path, default=CATALOG_PATH)
    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("validate", help="validate token references, recipes and mutex groups")

    query = subparsers.add_parser("query", help="query tokens")
    query.add_argument("--category")
    query.add_argument("--tier", choices=sorted(TIERS))
    query.add_argument("--tag")
    query.add_argument("--search")
    query.add_argument("--compatible-with")
    query.add_argument("--json", action="store_true")

    recipe = subparsers.add_parser("recipe", help="resolve one recipe and its dependencies")
    recipe.add_argument("recipe_id")
    recipe.add_argument("--json", action="store_true")

    render = subparsers.add_parser("render", help="render a standalone searchable HTML catalog")
    render.add_argument("--output", type=Path, required=True)
    return parser


def main() -> int:
    args = build_parser().parse_args()
    try:
        catalog = load_catalog(args.catalog)
        errors = validate_catalog(catalog)
        if errors:
            for error in errors:
                print(f"ERROR: {error}", file=sys.stderr)
            return 1

        if args.command == "validate":
            print(
                f"Valid: {len(catalog['tokens'])} tokens, "
                f"{len(catalog.get('recipes', []))} recipes, "
                f"{len(catalog.get('mutex_groups', []))} mutex groups."
            )
        elif args.command == "query":
            results = query_tokens(
                catalog,
                args.category,
                args.tier,
                args.tag,
                args.search,
                args.compatible_with,
            )
            print_tokens(results, args.json)
        elif args.command == "recipe":
            payload = recipe_payload(catalog, args.recipe_id)
            if args.json:
                print(json.dumps(payload, ensure_ascii=False, indent=2))
            else:
                print(f"{payload['id']}  {payload['label']}")
                print("resolved:")
                for item in payload["resolved_tokens"]:
                    print(f"  {item['id']}  {item['label']}")
                print("optional:", ", ".join(payload["optional"]) or "none")
                print("forbidden:", ", ".join(payload["forbidden"]) or "none")
                for invariant in payload["invariants"]:
                    print("invariant:", invariant)
                if payload["errors"]:
                    for error in payload["errors"]:
                        print("ERROR:", error)
                    return 1
        elif args.command == "render":
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(render_catalog(catalog), encoding="utf-8")
            print(args.output.resolve())
        return 0
    except (OSError, json.JSONDecodeError, KeyError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
