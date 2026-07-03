#!/usr/bin/env python3
from __future__ import annotations
import json, re, sys, tomllib
from pathlib import Path
import yaml

root = Path(__file__).resolve().parents[1]
project = root.parent
errors = []
names = {}
for skill in sorted((root / 'skills').iterdir()):
    if not skill.is_dir():
        continue
    md = skill / 'SKILL.md'
    if not md.exists():
        errors.append(f'{skill.name}: missing SKILL.md')
        continue
    text = md.read_text('utf-8', errors='replace')
    m = re.match(r'^---\n(.*?)\n---', text, re.S)
    if not m:
        errors.append(f'{skill.name}: invalid frontmatter envelope')
        continue
    try:
        fm = yaml.safe_load(m.group(1))
    except Exception as e:
        errors.append(f'{skill.name}: YAML: {e}')
        continue
    if not isinstance(fm, dict):
        errors.append(f'{skill.name}: frontmatter is not mapping')
        continue
    name = fm.get('name')
    desc = fm.get('description')
    if not isinstance(name, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name or '') or len(name) > 64:
        errors.append(f'{skill.name}: invalid name {name!r}')
    if name != skill.name:
        errors.append(f'{skill.name}: folder/name mismatch {name!r}')
    if name in names:
        errors.append(f'{skill.name}: duplicate name with {names[name]}')
    names[name] = skill.name
    if not isinstance(desc, str) or not desc.strip() or len(desc) > 1024 or '<' in desc or '>' in desc:
        errors.append(f'{skill.name}: invalid description')
    openai = skill / 'agents' / 'openai.yaml'
    if not openai.exists():
        errors.append(f'{skill.name}: missing agents/openai.yaml')
    else:
        try:
            cfg = yaml.safe_load(openai.read_text('utf-8'))
            if not isinstance(cfg, dict) or not isinstance(cfg.get('interface'), dict):
                errors.append(f'{skill.name}: invalid agents/openai.yaml')
        except Exception as e:
            errors.append(f'{skill.name}: openai.yaml YAML: {e}')

index = json.loads((root / 'SKILLS_INDEX.json').read_text('utf-8'))
index_names = [r.get('name') for r in index]
if len(index_names) != len(set(index_names)):
    errors.append('index contains duplicate names')
if set(index_names) != set(names):
    errors.append(f'index membership mismatch: missing={sorted(set(names)-set(index_names))}, extra={sorted(set(index_names)-set(names))}')

# Validate the consolidated design workflows and the boundaries that keep them
# from regressing into overlapping global skills.
design_skills = {
    'huashu-design': (
        'references/runtime-codex.md',
        'references/design-styles.md',
        'scripts/verify.py',
        'assets/design_canvas.jsx',
        'LICENSE.source.txt',
    ),
    'impeccable': (
        'reference/audit.md',
        'reference/codex.md',
        'scripts/detect.mjs',
        'scripts/live-copy-edit-agent.mjs',
        'LICENSE.source.txt',
    ),
    'design-taste-frontend': (
        'references/core-upstream.md',
        'references/image-to-code.md',
        'references/imagegen-web.md',
        'references/imagegen-mobile.md',
        'references/brandkit.md',
        'LICENSE.source.txt',
    ),
}
for skill_name, required in design_skills.items():
    skill_root = root / 'skills' / skill_name
    for rel in required:
        if not (skill_root / rel).exists():
            errors.append(f'{skill_name}: missing {rel}')

for excluded in ('design-taste-frontend-v1', 'full-output-enforcement'):
    if excluded in names or excluded in index_names:
        errors.append(f'{excluded}: excluded Taste skill must not be registered')

huashu_root = root / 'skills' / 'huashu-design'
if any(huashu_root.rglob('*.mp3')):
    errors.append('huashu-design: bundled MP3 files must remain excluded')

runner = root / 'skills' / 'impeccable' / 'scripts' / 'live-copy-edit-agent.mjs'
if runner.exists():
    runner_text = runner.read_text('utf-8', errors='replace')
    for forbidden in (
        '--dangerously-bypass-approvals-and-sandbox',
        "authCheck('claude')",
        "provider === 'claude'",
    ):
        if forbidden in runner_text:
            errors.append(f'impeccable: forbidden live-runner behavior remains: {forbidden}')

for agent_name in ('impeccable_asset_producer.toml', 'impeccable_manual_edit_applier.toml'):
    if not (project / '.codex' / 'agents' / agent_name).exists():
        errors.append(f'impeccable: missing project agent {agent_name}')

# Validate optional Caveman helper assets when present.
setup_dir = root / 'skills' / 'caveman-setup'
if setup_dir.exists():
    for rel in ('scripts/caveman_hook.py', 'scripts/install_hooks.py', 'references/hooks-template.json'):
        if not (setup_dir / rel).exists():
            errors.append(f'caveman-setup: missing {rel}')
    try:
        json.loads((setup_dir / 'references' / 'hooks-template.json').read_text('utf-8'))
    except Exception as e:
        errors.append(f'caveman-setup: hooks template JSON: {e}')

agent_dir = project / '.codex' / 'agents'
agent_count = 0
if agent_dir.exists():
    for path in sorted(agent_dir.glob('*.toml')):
        agent_count += 1
        try:
            data = tomllib.loads(path.read_text('utf-8'))
        except Exception as e:
            errors.append(f'{path.name}: TOML: {e}')
            continue
        for key in ('name','description','developer_instructions'):
            if not isinstance(data.get(key), str) or not data[key].strip():
                errors.append(f'{path.name}: missing {key}')
        if data.get('sandbox_mode') not in (None, 'read-only', 'workspace-write', 'danger-full-access'):
            errors.append(f'{path.name}: invalid sandbox_mode')


# Validate the 2026-07-03 marketing/SEO/content integration.
expected_new = {
    'bilingual-transcreator', 'humanizer', 'humanizer-ru', 'ru-text',
    'seo', 'seo-audit', 'seo-technical', 'seo-content', 'seo-schema',
    'marketing-seo-audit', 'content', 'content-editorial-strategy',
    'product-marketing', 'copywriting', 'copy-editing',
}
missing_expected = sorted(expected_new - set(names))
if missing_expected:
    errors.append(f'integration: missing expected skills {missing_expected}')

for rel in (
    'vendor/claude-seo/scripts',
    'vendor/marketingskills/tools/REGISTRY.md',
    'vendor/content-skills',
    'brand/README.md',
):
    if not (root / rel).exists():
        errors.append(f'integration: missing .agents/{rel}')

for agent_name in (
    'seo_technical.toml', 'seo_content.toml', 'seo_schema.toml',
    'content_writer.toml', 'content_strategist.toml', 'content_brand_guardian.toml',
):
    if not (project / '.codex' / 'agents' / agent_name).exists():
        errors.append(f'integration: missing project agent {agent_name}')

for forbidden in ('/content setup', '/humanizer-ru', '/bilingual-transcreator'):
    for skill_name in ('content', 'humanizer-ru', 'bilingual-transcreator'):
        text = (root / 'skills' / skill_name / 'SKILL.md').read_text('utf-8', errors='replace')
        if forbidden in text:
            errors.append(f'{skill_name}: legacy invocation remains: {forbidden}')

# Exact registration count is intentional for this pack release.
if len(names) != 252:
    errors.append(f'integration: expected 252 skills, found {len(names)}')

if errors:
    print('\n'.join('ERROR: ' + e for e in errors))
    sys.exit(1)
print(f'OK: {len(names)} skills and {agent_count} custom agents validated')
