from pathlib import Path
import re

ROOT = Path("docs/glider-components")
INDEX = ROOT / "index.md"

IGNORE = {
    "images",
    "__pycache__",
}

SITE_PREFIX = "/Glider-Operation-Best-Practices"


def pretty(name):
    return name.replace("-", " ").replace("_", " ").title()


def node_id(path):
    return (
        str(path)
        .replace("/", "_")
        .replace("-", "_")
        .replace(".", "_")
    )


lines = []
clicks = []

lines.append("flowchart LR")
lines.append("")

lines.append('GC["Glider Components"]')


for platform in sorted(ROOT.iterdir()):

    if not platform.is_dir():
        continue

    if platform.name in IGNORE:
        continue

    platform_id = node_id(platform)

    lines.append(f'{platform_id}["{pretty(platform.name)}"]')
    lines.append(f"GC --> {platform_id}")

    clicks.append(
        f'click {platform_id} "{SITE_PREFIX}/glider-components/{platform.name}/"'
    )

    for component in sorted(platform.iterdir()):

        if not component.is_dir():
            continue

        if component.name in IGNORE:
            continue

        component_id = node_id(component)

        lines.append(
            f'{component_id}["{pretty(component.name)}"]'
        )

        lines.append(
            f"{platform_id} --> {component_id}"
        )

        clicks.append(
            f'click {component_id} "{SITE_PREFIX}/glider-components/{platform.name}/{component.name}/"'
        )

        for child in sorted(component.iterdir()):

            if not child.is_dir():
                continue

            if child.name in IGNORE:
                continue

            child_id = node_id(child)

            lines.append(
                f'{child_id}["{pretty(child.name)}"]'
            )

            lines.append(
                f"{component_id} --> {child_id}"
            )

            if child.name in {"guides", "checklists"}:

                target = (
                    f"{SITE_PREFIX}/glider-components/"
                    f"{platform.name}/"
                    f"{component.name}/"
                )

                clicks.append(
                    f'click {child_id} "{target}"'
                )

lines.append("")
lines.extend(clicks)

mermaid = (
    "```mermaid\n"
    + "\n".join(lines)
    + "\n```"
)

text = INDEX.read_text()

pattern = re.compile(
    r"<!-- COMPONENT_MAP_START -->.*?<!-- COMPONENT_MAP_END -->",
    re.DOTALL,
)

replacement = (
    "<!-- COMPONENT_MAP_START -->\n\n"
    + mermaid
    + "\n\n<!-- COMPONENT_MAP_END -->"
)

updated = pattern.sub(replacement, text)

INDEX.write_text(updated)

print("Component map updated.")
