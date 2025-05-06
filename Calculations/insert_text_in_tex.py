def insert_text_in_tex(file_path: str, insertion_keyword: str, text) -> bool:
    """
    Inserts `text` (string or list of strings) into a .tex file,
    replacing everything between the markers:

      % BEGIN <insertion_keyword>
          (old lines here)
      % END   <insertion_keyword>

    Returns True on success, False if markers aren't found.
    """
    # Build the exact marker lines
    start_tag = f"% BEGIN {insertion_keyword}"
    end_tag   = f"% END {insertion_keyword}"

    # Normalize `text` to a list of lines (each ending in `\n`)
    if isinstance(text, str):
        lines_to_insert = [text.rstrip("\n") + "\n"]
    elif isinstance(text, list):
        lines_to_insert = [str(t).rstrip("\n") + "\n" for t in text]
    else:
        raise TypeError("`text` must be a str or a list of str")

    # Read the file
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    # Find the markers
    start_idx = next((i for i, L in enumerate(lines) if L.strip() == start_tag), None)
    end_idx   = next((i for i, L in enumerate(lines) if L.strip() == end_tag),   None)

    if start_idx is None or end_idx is None or end_idx <= start_idx:
        return False

    # Replace everything *between* the markers by slice assignment
    # (this preserves the lines at start_idx and end_idx)
    lines[start_idx+1 : end_idx] = lines_to_insert

    # Write it back
    with open(file_path, "w", encoding="utf-8") as f:
        f.writelines(lines)

    return True



