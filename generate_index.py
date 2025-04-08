import os
import re
import yaml  # Using PyYAML for robust frontmatter parsing

# --- Configuration ---
CONTENT_DIR = "./content"  # Relative path to your content directory
INDEX_FILE = os.path.join(CONTENT_DIR, "index.md")
EXCLUDE_DIRS_TOP = {"assets", "private", ".obsidian", ".git"}  # Exclude at top level
EXCLUDE_DIRS_SUB = {"assets", ".obsidian", ".git"}  # Exclude within subfolders
# Define placeholder comments
START_MARKER = "<!-- AUTO-INDEX-START -->"
END_MARKER = "<!-- AUTO-INDEX-END -->"
# Define default page number for sorting if 'page' is missing or invalid
# Use float('inf') to ensure items without 'page' sort last
DEFAULT_PAGE_NUMBER = float("inf")
# --- End Configuration ---


def parse_frontmatter(filepath):
    """Parses YAML frontmatter from a Markdown file."""
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        if not content.startswith("---"):
            return None

        parts = content.split("---", 2)
        if len(parts) < 3:
            return None

        frontmatter_text = parts[1]
        frontmatter_data = yaml.safe_load(frontmatter_text)
        # Ensure it returns a dictionary even if YAML is just a value
        if not isinstance(frontmatter_data, dict):
            print(
                f"Warning: Frontmatter in {filepath} is not a dictionary. Treating as empty."
            )
            return {}
        return frontmatter_data
    except FileNotFoundError:
        return None
    except yaml.YAMLError as e:
        print(f"Warning: Error parsing YAML frontmatter in {filepath}: {e}")
        return None
    except Exception as e:
        print(f"Warning: Could not read or parse frontmatter for {filepath}: {e}")
        return None


def get_folder_metadata(folder_path):
    """
    Gets metadata (draft status, page number) from a folder's index.md or folder-name.md.
    Returns a dictionary: {'name': str, 'path': str, 'is_draft': bool, 'page': float}
    """
    folder_name = os.path.basename(folder_path)
    potential_index_files = [
        os.path.join(folder_path, "index.md"),
        os.path.join(folder_path, f"{folder_name}.md"),
    ]

    frontmatter = None
    found_file = None
    for index_path in potential_index_files:
        if os.path.exists(index_path):
            frontmatter = parse_frontmatter(index_path)
            if frontmatter is not None:  # Found valid frontmatter
                found_file = index_path
                break

    is_draft = False
    page_number = DEFAULT_PAGE_NUMBER

    if frontmatter:  # Frontmatter was successfully parsed from found_file
        # Check draft status
        draft_value = frontmatter.get("draft", False)
        if isinstance(draft_value, bool):
            is_draft = draft_value
        elif isinstance(draft_value, str):
            is_draft = draft_value.lower() == "true"

        # Check page number
        page_value = frontmatter.get("page")
        if page_value is not None:
            try:
                # Attempt to convert to float first for flexibility, then int if needed
                page_number = float(page_value)
            except (ValueError, TypeError):
                print(
                    f"Warning: Invalid 'page' value '{page_value}' in {found_file}. Using default sort order."
                )
                page_number = DEFAULT_PAGE_NUMBER

    return {
        "name": folder_name,
        "path": folder_path,
        "is_draft": is_draft,
        "page": page_number,
    }


def get_subfolders(parent_folder_path):
    """Gets relevant, non-draft subfolders within a given parent folder, sorted by 'page' property."""
    subfolder_metadata_list = []
    try:
        for item in os.listdir(parent_folder_path):
            item_path = os.path.join(parent_folder_path, item)
            # Check if it's a directory, not excluded, and not hidden
            if (
                os.path.isdir(item_path)
                and item not in EXCLUDE_DIRS_SUB
                and not item.startswith(".")
            ):
                # Get metadata including draft status and page number
                metadata = get_folder_metadata(item_path)

                if not metadata["is_draft"]:
                    subfolder_metadata_list.append(metadata)
                else:
                    print(
                        f"  Skipping draft subfolder: {os.path.join(os.path.basename(parent_folder_path), item)}"
                    )

        # Sort the list of dictionaries based on the 'page' number
        subfolder_metadata_list.sort(key=lambda x: x["page"])

    except FileNotFoundError:
        print(
            f"Warning: Parent folder not found for subfolder scan: {parent_folder_path}"
        )

    return subfolder_metadata_list  # Return list of metadata dicts


def get_main_folders(content_dir):
    """Gets relevant, non-draft top-level folders, sorted by 'page' property."""
    folder_metadata_list = []
    for item in os.listdir(content_dir):
        item_path = os.path.join(content_dir, item)
        # Check if it's a directory, not excluded (top level), and not hidden
        if (
            os.path.isdir(item_path)
            and item not in EXCLUDE_DIRS_TOP
            and not item.startswith(".")
        ):
            # Get metadata including draft status and page number
            metadata = get_folder_metadata(item_path)

            if not metadata["is_draft"]:
                folder_metadata_list.append(metadata)
            else:
                print(f"Skipping draft top-level folder: {item}")

    # Sort the list of dictionaries based on the 'page' number
    folder_metadata_list.sort(key=lambda x: x["page"])

    return folder_metadata_list  # Return list of metadata dicts


def get_file_metadata(file_path):
    """Gets metadata (draft status) from a Markdown file."""
    frontmatter = parse_frontmatter(file_path)
    is_draft = False

    if frontmatter:
        # Check draft status
        draft_value = frontmatter.get("draft", False)
        if isinstance(draft_value, bool):
            is_draft = draft_value
        elif isinstance(draft_value, str):
            is_draft = draft_value.lower() == "true"
        page_value = frontmatter.get("page")
        if page_value is not None:
            try:
                # Attempt to convert to float first for flexibility, then int if needed
                page_number = float(page_value)
            except (ValueError, TypeError):
                print(
                    f"Warning: Invalid 'page' value '{page_value}' in {file_path}. Using default sort order."
                )
                page_number = DEFAULT_PAGE_NUMBER

    return {
        "is_draft": is_draft,
        "page": page_number,
    }


def format_folder_list_md(top_level_folders_metadata):
    """Formats the list of folders and their subfolders into Markdown, using sorted metadata."""
    md_lines = []
    # Iterate through the already sorted list of top-level folder metadata
    for folder_meta in top_level_folders_metadata:
        folder_name = folder_meta["name"]
        top_level_folder_path = folder_meta["path"]

        # --- Format Top-Level Folder Heading ---
        display_name = folder_name
        if re.match(r"^\d+-", display_name):
            display_name = re.sub(r"^\d+-", "", display_name).strip()

        display_name = display_name.replace("-", " ")  # Basic cleaning for display
        top_level_wikilink = f"[[{folder_name}|{display_name}]]"
        md_lines.append(f"### {top_level_wikilink}")

        # --- Get and Format Subfolders (they are already sorted by page) ---
        subfolders_metadata = get_subfolders(top_level_folder_path)

        if subfolders_metadata:
            # Iterate through the already sorted list of subfolder metadata
            for subfolder_meta in subfolders_metadata:
                subfolder_name = subfolder_meta["name"]
                sub_display_name = subfolder_name.replace(
                    "-", " "
                )  # Basic cleaning for display

                # Create wikilink: [[TopFolder/SubFolder|Sub Display Name]]
                subfolder_wikilink = (
                    f"[[{folder_name}/{subfolder_name}|{sub_display_name}]]"
                )
                md_lines.append(f"*   {subfolder_wikilink}")
        else:
            # md_lines.append(f"*   *(No sub-topics listed yet)*")
            # find any .md files other than index.md in the top-level folder
            files = list(
                filter(
                    lambda x: os.path.isfile(os.path.join(top_level_folder_path, x))
                    and x.endswith(".md")
                    and x != "index.md",
                    os.listdir(top_level_folder_path),
                )
            )
            # sort the files by page number
            files.sort(
                key=lambda x: get_file_metadata(os.path.join(top_level_folder_path, x))[
                    "page"
                ]
            )
            if files:
                # print(f"  Found files in {folder_name} (not subfolders): {files}")
                for file in files:
                    file_path = os.path.join(top_level_folder_path, file)
                    metadata = get_file_metadata(file_path)
                    if not metadata["is_draft"]:
                        sub_display_name = file.replace("-", " ").replace(".md", "")
                        subfolder_wikilink = (
                            f"[[{folder_name}/{file}|{sub_display_name}]]"
                        )
                        md_lines.append(f"*   {subfolder_wikilink}")
                    else:
                        print(
                            f"  Skipping draft file: {os.path.join(folder_name, file)}"
                        )
            # for item in os.listdir(top_level_folder_path):
            #     item_path = os.path.join(top_level_folder_path, item)
            #     if (
            #         os.path.isfile(item_path)
            #         and item.endswith(".md")
            #         and item != "index.md"
            #     ):
            #         # Get metadata including draft status and page number
            #         metadata = get_file_metadata(item_path)
            #         print(f"  Found file: {os.path.join(folder_name, item)}")
            #         print(metadata, type(metadata["is_draft"]))
            #         if metadata["is_draft"]:
            #             sub_display_name = item.replace("-", " ").replace(".md", "")
            #             subfolder_wikilink = (
            #                 f"[[{folder_name}/{item}|{sub_display_name}]]"
            #             )
            #             md_lines.append(f"*   {subfolder_wikilink}")
            #         else:
            #             print(
            #                 f"  Skipping draft file: {os.path.join(folder_name, item)}"
            #             )

        md_lines.append("")  # Add a blank line for spacing after each top-level section

    # Remove the last blank line if it exists
    if md_lines and md_lines[-1] == "":
        md_lines.pop()

    return "\n".join(md_lines)


def update_index_file(index_path, new_content):
    """Reads the index file and replaces content between markers."""
    try:
        with open(index_path, "r", encoding="utf-8") as f:
            original_content = f.read()

        pattern = re.compile(
            f"({re.escape(START_MARKER)})(.*?)({re.escape(END_MARKER)})", re.DOTALL
        )

        if not pattern.search(original_content):
            print(
                f"Error: Markers {START_MARKER} or {END_MARKER} not found in {index_path}. No update performed."
            )
            return

        replacement_content = f"\\1\n{new_content}\n\\3"
        updated_content = pattern.sub(replacement_content, original_content, count=1)

        if updated_content != original_content:
            with open(index_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"Successfully updated index: {index_path}")
        else:
            print(f"Index content unchanged: {index_path}")

    except FileNotFoundError:
        print(f"Error: Index file not found at {index_path}")
    except Exception as e:
        print(f"An error occurred: {e}")


# --- Main Execution ---
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate index for Markdown files.")
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        default=CONTENT_DIR,
        help="Path to the content directory (default: ./content)",
    )
    args = parser.parse_args()

    # Get main folders metadata, already sorted by 'page'
    main_folders_metadata = get_main_folders(args.input)

    if main_folders_metadata:
        markdown_list = format_folder_list_md(main_folders_metadata)
        update_index_file(INDEX_FILE, markdown_list)
    else:
        print("No non-draft main folders found to generate index.")
