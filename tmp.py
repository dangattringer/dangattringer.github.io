import re


def extract_variables(style_content, dark=False):
    if dark:
        root_blocks = re.findall(
            r"@media \(prefers-color-scheme: dark\)\s*{[^}]*:root\s*{([^}]*)}",
            style_content,
            flags=re.DOTALL,
        )
    else:
        root_blocks = re.findall(r":root\s*{([^}]*)}", style_content, flags=re.DOTALL)

    if len(root_blocks) > 1:
        root_blocks = [root_blocks[0]]
    variables = {}
    for block in root_blocks:
        for line in block.split(";"):
            if ":" in line:
                key, value = line.split(":", 1)
                key = key.strip()
                value = value.strip()
                if key.startswith("--"):
                    variables[key] = value
    return variables


def replace_vars(style_content, variables):
    def replacer(match):
        var_name = match.group(1)
        return variables.get(var_name, match.group(0))

    replaced_content = re.sub(r"var\((--[^)]+)\)", replacer, style_content)
    return replaced_content


def remove_root_blocks(style_content):
    # Remove normal :root { ... }
    style_content = re.sub(r":root\s*{[^}]*}", "", style_content, flags=re.DOTALL)
    # Remove dark mode @media (prefers-color-scheme: dark) { ... }
    style_content = re.sub(
        r"@media\s*\(prefers-color-scheme:\s*dark\)\s*{[^}]*:root\s*{[^}]*}[^}]*}",
        "",
        style_content,
        flags=re.DOTALL,
    )
    return style_content


def resolve_svg_style(svg_content):
    style_match = re.search(r"<style[^>]*>(.*?)<\/style>", svg_content, flags=re.DOTALL)
    if not style_match:
        raise ValueError("No <style> block found in SVG.")

    style_content = style_match.group(1)

    light_vars = extract_variables(style_content, dark=False)
    dark_vars = extract_variables(style_content, dark=True)

    # Remove the root variable blocks BEFORE replacing
    style_content_no_vars = remove_root_blocks(style_content)

    # Create fully resolved versions
    light_style = replace_vars(style_content_no_vars, light_vars)
    dark_style = replace_vars(style_content_no_vars, dark_vars)

    # Replace the original <style> content
    svg_light = svg_content.replace(style_content, light_style)
    svg_dark = svg_content.replace(style_content, dark_style)

    return svg_light, svg_dark


# Example Usage
# with open("test1.svg", "r", encoding="utf-8") as f:
#     svg_content = f.read()

# svg_light, svg_dark = resolve_svg_style(svg_content)

# with open("output_light.svg", "w", encoding="utf-8") as f:
#     f.write(svg_light)

# with open("output_dark.svg", "w", encoding="utf-8") as f:
#     f.write(svg_dark)

if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser(
        description="Resolve SVG styles with CSS variables."
    )
    parser.add_argument("input_svg", type=Path, help="Input SVG file path.")
    parser.parse_args()
    args = parser.parse_args()
    with open(args.input_svg, "r", encoding="utf-8") as f:
        svg_content = f.read()
    svg_light, svg_dark = resolve_svg_style(svg_content)
    light_path = args.input_svg.with_name(args.input_svg.stem + "_light.svg")
    dark_path = args.input_svg.with_name(args.input_svg.stem + "_dark.svg")
    with open(light_path, "w", encoding="utf-8") as f:
        f.write(svg_light)
    with open(dark_path, "w", encoding="utf-8") as f:
        f.write(svg_dark)
