#!/usr/bin/env python3
"""
WorkflowX Cross-Platform Sync Script
=====================================
Generates platform-specific agent/skill files from canonical src/ definitions.

Usage:
    python script/sync.py                  # Sync all platforms
    python script/sync.py --platform copilot  # Sync specific platform
    python script/sync.py --dry-run           # Preview without writing
    python script/sync.py --verify            # Verify consistency only
"""

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

# ============================================================================
# Constants
# ============================================================================

ROOT = Path(__file__).resolve().parent.parent
SRC_AGENTS = ROOT / "src" / "agents"
SRC_SKILLS = ROOT / "src" / "skills"
SRC_PROMPTS = ROOT / "src" / "prompts"
CONFIG_PATH = ROOT / "script" / "sync_config.json"

PLACEHOLDER = "{{PLATFORM_SKILLS}}"

# ============================================================================
# Platform Definitions
# ============================================================================

@dataclass
class PlatformConfig:
    name: str
    skills_path: str
    agents_path: str
    agent_suffix: str
    prompts_path: str  # Path for prompt/command files (empty = skip)
    prompt_suffix: str  # File extension for prompt files
    # Whether to validate tool/handoff metadata exists in config
    needs_metadata: bool = True

PLATFORMS = {
    "copilot": PlatformConfig(
        name="copilot",
        skills_path=".github/skills",
        agents_path=".github/agents",
        agent_suffix=".agent.md",
        prompts_path=".github/prompts",
        prompt_suffix=".prompt.md",
    ),
    "codex": PlatformConfig(
        name="codex",
        skills_path=".codex/skills",
        agents_path=".codex/agents",
        agent_suffix=".toml",
        prompts_path="",  # Codex has no prompt file mechanism
        prompt_suffix="",
    ),
    "claude": PlatformConfig(
        name="claude",
        skills_path=".claude/skills",
        agents_path=".claude/agents",
        agent_suffix=".md",
        prompts_path=".claude/commands",
        prompt_suffix=".md",
    ),
}

# ============================================================================
# Sync Config (loaded from sync_config.json)
# ============================================================================

def load_config() -> dict:
    if not CONFIG_PATH.exists():
        print(f"[ERROR] Config not found: {CONFIG_PATH}")
        sys.exit(1)
    with open(CONFIG_PATH, "r", encoding="utf-8-sig") as f:
        return json.load(f)

# ============================================================================
# Source Parsing
# ============================================================================

@dataclass
class AgentSource:
    """Parsed src/agents/*.md file."""
    name: str
    description: str
    argument_hint: Optional[str]
    body: str  # Everything after the frontmatter
    file_path: Path

def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter delimited by --- markers."""
    if not content.startswith("---"):
        return {}, content
    
    end = content.find("---", 3)
    if end == -1:
        return {}, content
    
    fm_text = content[3:end].strip()
    body = content[end + 3:].strip()
    
    # Simple YAML parser (no external deps)
    fm = {}
    current_key = None
    current_value_lines = []
    
    for line in fm_text.split("\n"):
        match = re.match(r'^(\w[\w-]*):\s*(.*)', line)
        if match:
            if current_key:
                val = "\n".join(current_value_lines).strip()
                if val.startswith('"') and val.endswith('"'):
                    val = val[1:-1]
                fm[current_key] = val
            current_key = match.group(1)
            current_value_lines = [match.group(2)]
        elif current_key:
            current_value_lines.append(line)
    
    if current_key:
        val = "\n".join(current_value_lines).strip()
        if val.startswith('"') and val.endswith('"'):
            val = val[1:-1]
        fm[current_key] = val
    
    return fm, body

def load_agent_source(file_path: Path) -> AgentSource:
    content = file_path.read_text(encoding="utf-8-sig")
    fm, body = parse_frontmatter(content)
    
    name = fm.get("name", file_path.stem)
    description = fm.get("description", "")
    argument_hint = fm.get("argument-hint")
    
    return AgentSource(
        name=name,
        description=description,
        argument_hint=argument_hint,
        body=body,
        file_path=file_path,
    )

@dataclass
class PromptSource:
    """Parsed src/prompts/*.md file."""
    name: str
    description: str
    body: str  # Everything after the frontmatter
    file_path: Path

def load_prompt_source(file_path: Path) -> PromptSource:
    content = file_path.read_text(encoding="utf-8-sig")
    fm, body = parse_frontmatter(content)

    name = fm.get("name", file_path.stem)
    description = fm.get("description", "")

    return PromptSource(
        name=name,
        description=description,
        body=body,
        file_path=file_path,
    )

# ============================================================================
# Platform Generators
# ============================================================================

def replace_paths(body: str, platform: PlatformConfig) -> str:
    return body.replace(PLACEHOLDER, platform.skills_path)

def generate_copilot_agent(src: AgentSource, config: dict, platform: PlatformConfig) -> str:
    """Generate .github/agents/*.agent.md"""
    agent_meta = config.get("agents", {}).get(src.name, {}).get("copilot", {})
    
    lines = ["---"]
    lines.append(f"name: {src.name}")
    lines.append(f'description: {src.description}')
    
    if src.argument_hint:
        lines.append(f"argument-hint: {src.argument_hint}")
    
    tools = agent_meta.get("tools", [])
    if tools:
        lines.append(f"tools: [{', '.join(tools)}]")
    
    handoffs = agent_meta.get("handoffs", [])
    if handoffs:
        lines.append("handoffs:")
        for ho in handoffs:
            lines.append(f"  - label: {ho['label']}")
            lines.append(f"    agent: {ho['agent']}")
            lines.append(f"    prompt: >")
            prompt_lines = ho["prompt"].strip().split("\n")
            for pl in prompt_lines:
                lines.append(f"      {pl}")
            if "send" in ho:
                lines.append(f"    send: {str(ho['send']).lower()}")
    
    lines.append("---")
    lines.append("")
    lines.append(replace_paths(src.body, platform))
    
    return "\n".join(lines)

def generate_codex_agent(src: AgentSource, config: dict, platform: PlatformConfig) -> str:
    """Generate .codex/agents/*.toml"""
    name_for_toml = src.name
    # Codex doesn't use brackets in names
    name_for_toml = name_for_toml.replace("[zn]", "").replace("[", "").replace("]", "")
    
    lines = [f'name = "{name_for_toml}"']
    lines.append(f'description = "{src.description}"')
    lines.append("")
    lines.append('developer_instructions = """')
    
    body = replace_paths(src.body, platform)
    # For TOML, strip the leading markdown heading if it's just the agent name
    body_lines = body.split("\n")
    # Remove leading empty lines
    while body_lines and body_lines[0].strip() == "":
        body_lines.pop(0)
    # Remove the # agentName heading line
    if body_lines and body_lines[0].strip().startswith("# ") and src.name.replace("_zh", "").replace("[zn]", "") in body_lines[0]:
        body_lines.pop(0)
        while body_lines and body_lines[0].strip() == "":
            body_lines.pop(0)
    
    lines.extend(body_lines)
    lines.append('"""')
    
    return "\n".join(lines)

def generate_claude_agent(src: AgentSource, config: dict, platform: PlatformConfig) -> str:
    """Generate .claude/agents/*.md"""
    agent_meta = config.get("agents", {}).get(src.name, {}).get("claude", {})
    
    lines = ["---"]
    lines.append(f"name: {src.name}")
    lines.append(f'description: {src.description}')
    
    if src.argument_hint:
        lines.append(f"argument-hint: {src.argument_hint}")
    
    tools = agent_meta.get("tools", [])
    if tools:
        lines.append(f"tools: [{', '.join(tools)}]")
    
    lines.append("---")
    lines.append("")
    lines.append(replace_paths(src.body, platform))
    
    return "\n".join(lines)

GENERATORS = {
    "copilot": generate_copilot_agent,
    "codex": generate_codex_agent,
    "claude": generate_claude_agent,
}

# ============================================================================
# Prompt Generators
# ============================================================================

def generate_copilot_prompt(src: PromptSource, platform: PlatformConfig) -> str:
    """Generate .github/prompts/*.prompt.md"""
    lines = ["---"]
    lines.append(f"name: {src.name}")
    lines.append(f'description: {src.description}')
    lines.append("---")
    lines.append("")

    body = src.body.replace("$ARGUMENTS", "${input:args}")
    lines.append(body)

    return "\n".join(lines)

def generate_claude_prompt(src: PromptSource, platform: PlatformConfig) -> str:
    """Generate .claude/commands/*.md (plain body, no frontmatter)"""
    return src.body

PROMPT_GENERATORS = {
    "copilot": generate_copilot_prompt,
    "claude": generate_claude_prompt,
}

# ============================================================================
# Skill Sync
# ============================================================================

def sync_skills(platform: PlatformConfig, dry_run: bool = False) -> list[str]:
    """Copy skills from src/skills/ to platform skills dir with path replacement."""
    changes = []
    
    if not SRC_SKILLS.exists():
        return changes
    
    for skill_dir in sorted(SRC_SKILLS.iterdir()):
        if not skill_dir.is_dir():
            continue
        
        target_dir = ROOT / platform.skills_path / skill_dir.name
        target_dir.mkdir(parents=True, exist_ok=True)
        
        for file in sorted(skill_dir.rglob("*")):
            if not file.is_file():
                continue
            
            rel = file.relative_to(skill_dir)
            target_file = target_dir / rel
            
            content = file.read_text(encoding="utf-8-sig")
            content = content.replace(PLACEHOLDER, platform.skills_path)
            
            if target_file.exists():
                existing = target_file.read_text(encoding="utf-8-sig")
                if existing == content:
                    continue
            
            changes.append(str(target_file.relative_to(ROOT)))
            if not dry_run:
                target_file.parent.mkdir(parents=True, exist_ok=True)
                target_file.write_text(content, encoding="utf-8")
    
    return changes

# ============================================================================
# Prompt Sync
# ============================================================================

def sync_prompts(platform: PlatformConfig, dry_run: bool = False) -> list[str]:
    """Generate platform prompt files from src/prompts/."""
    changes = []

    if not platform.prompts_path or not SRC_PROMPTS.exists():
        return changes

    gen = PROMPT_GENERATORS.get(platform.name)
    if not gen:
        return changes

    target_dir = ROOT / platform.prompts_path
    target_dir.mkdir(parents=True, exist_ok=True)

    for src_file in sorted(SRC_PROMPTS.glob("*.md")):
        src = load_prompt_source(src_file)
        output = gen(src, platform)

        target_file = target_dir / f"{src.name}{platform.prompt_suffix}"

        if target_file.exists():
            existing = target_file.read_text(encoding="utf-8-sig")
            if existing == output:
                continue

        changes.append(str(target_file.relative_to(ROOT)))
        if not dry_run:
            target_file.write_text(output, encoding="utf-8")

    return changes

def sync_agents(platform: PlatformConfig, config: dict, dry_run: bool = False) -> list[str]:
    """Generate platform agent files from src/agents/."""
    changes = []
    gen = GENERATORS[platform.name]
    
    target_dir = ROOT / platform.agents_path
    target_dir.mkdir(parents=True, exist_ok=True)
    
    for src_file in sorted(SRC_AGENTS.glob("*.md")):
        src = load_agent_source(src_file)
        output = gen(src, config, platform)
        
        # Determine target filename
        # src: plannerX_zh.md → copilot: plannerX_zh.agent.md → codex: plannerX_zh.toml → claude: plannerX_zh.md
        stem = src_file.stem
        if platform.name == "codex":
            # Codex doesn't support brackets, uses underscores
            target_stem = stem
        else:
            target_stem = stem
        
        target_file = target_dir / f"{target_stem}{platform.agent_suffix}"
        
        if target_file.exists():
            existing = target_file.read_text(encoding="utf-8-sig")
            if existing == output:
                continue
        
        changes.append(str(target_file.relative_to(ROOT)))
        if not dry_run:
            target_file.write_text(output, encoding="utf-8")
    
    return changes

# ============================================================================
# Verify
# ============================================================================

def verify_platform(platform: PlatformConfig, config: dict) -> list[str]:
    """Verify that platform files match what sync would generate."""
    issues = []
    
    # Check agents
    if SRC_AGENTS.exists():
        gen = GENERATORS[platform.name]
        target_dir = ROOT / platform.agents_path
        
        for src_file in sorted(SRC_AGENTS.glob("*.md")):
            src = load_agent_source(src_file)
            expected = gen(src, config, platform)
            
            stem = src_file.stem
            target_file = target_dir / f"{stem}{platform.agent_suffix}"
            
            if not target_file.exists():
                issues.append(f"MISSING: {target_file.relative_to(ROOT)}")
            else:
                actual = target_file.read_text(encoding="utf-8")
                if actual != expected:
                    issues.append(f"OUTDATED: {target_file.relative_to(ROOT)}")
    
    # Check skills
    if SRC_SKILLS.exists():
        for skill_dir in sorted(SRC_SKILLS.iterdir()):
            if not skill_dir.is_dir():
                continue
            
            target_dir = ROOT / platform.skills_path / skill_dir.name
            
            for file in sorted(skill_dir.rglob("*")):
                if not file.is_file():
                    continue
                
                rel = file.relative_to(skill_dir)
                target_file = target_dir / rel
                
                expected = file.read_text(encoding="utf-8-sig").replace(PLACEHOLDER, platform.skills_path)
                
                if not target_file.exists():
                    issues.append(f"MISSING: {target_file.relative_to(ROOT)}")
                else:
                    actual = target_file.read_text(encoding="utf-8-sig")
                    if actual != expected:
                        issues.append(f"OUTDATED: {target_file.relative_to(ROOT)}")

    # Check prompts
    if platform.prompts_path and SRC_PROMPTS.exists():
        gen = PROMPT_GENERATORS.get(platform.name)
        if gen:
            target_dir = ROOT / platform.prompts_path

            for src_file in sorted(SRC_PROMPTS.glob("*.md")):
                src = load_prompt_source(src_file)
                expected = gen(src, platform)

                target_file = target_dir / f"{src.name}{platform.prompt_suffix}"

                if not target_file.exists():
                    issues.append(f"MISSING: {target_file.relative_to(ROOT)}")
                else:
                    actual = target_file.read_text(encoding="utf-8")
                    if actual != expected:
                        issues.append(f"OUTDATED: {target_file.relative_to(ROOT)}")

    return issues

# ============================================================================
# Main
# ============================================================================

def main():
    parser = argparse.ArgumentParser(description="WorkflowX Cross-Platform Sync")
    parser.add_argument("--platform", choices=list(PLATFORMS.keys()), help="Sync specific platform only")
    parser.add_argument("--dry-run", action="store_true", help="Preview changes without writing")
    parser.add_argument("--verify", action="store_true", help="Verify consistency only")
    parser.add_argument("--agents-only", action="store_true", help="Sync agents only")
    parser.add_argument("--skills-only", action="store_true", help="Sync skills only")
    parser.add_argument("--prompts-only", action="store_true", help="Sync prompts only")
    args = parser.parse_args()
    
    config = load_config()
    
    platforms = {args.platform: PLATFORMS[args.platform]} if args.platform else PLATFORMS
    
    if args.verify:
        all_ok = True
        for name, plat in platforms.items():
            issues = verify_platform(plat, config)
            if issues:
                all_ok = False
                print(f"\n[{name.upper()}] {len(issues)} issue(s):")
                for issue in issues:
                    print(f"  {issue}")
            else:
                print(f"[{name.upper()}] ✅ All files consistent")
        
        sys.exit(0 if all_ok else 1)
    
    for name, plat in platforms.items():
        print(f"\n{'='*50}")
        print(f"  Syncing: {name.upper()}")
        print(f"{'='*50}")
        
        total_changes = []
        
        if not args.skills_only and not args.prompts_only:
            agent_changes = sync_agents(plat, config, args.dry_run)
            total_changes.extend(agent_changes)
            if agent_changes:
                print(f"\n  Agents ({len(agent_changes)}):")
                for c in agent_changes:
                    print(f"    {'[DRY] ' if args.dry_run else ''}{c}")
            else:
                print(f"\n  Agents: ✅ up to date")

        if not args.agents_only and not args.prompts_only:
            skill_changes = sync_skills(plat, args.dry_run)
            total_changes.extend(skill_changes)
            if skill_changes:
                print(f"\n  Skills ({len(skill_changes)}):")
                for c in skill_changes:
                    print(f"    {'[DRY] ' if args.dry_run else ''}{c}")
            else:
                print(f"\n  Skills: ✅ up to date")

        if not args.agents_only and not args.skills_only:
            prompt_changes = sync_prompts(plat, args.dry_run)
            total_changes.extend(prompt_changes)
            if prompt_changes:
                print(f"\n  Prompts ({len(prompt_changes)}):")
                for c in prompt_changes:
                    print(f"    {'[DRY] ' if args.dry_run else ''}{c}")
            else:
                print(f"\n  Prompts: ✅ up to date")
        
        if not total_changes:
            print(f"\n  Result: ✅ No changes needed")
        else:
            print(f"\n  Result: {'[DRY RUN] ' if args.dry_run else ''}{len(total_changes)} file(s) {'would be' if args.dry_run else ''} updated")
    
    print()

if __name__ == "__main__":
    main()
