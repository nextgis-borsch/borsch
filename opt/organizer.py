#!/usr/bin/env python3
"""organizer — copy / sync helper between two directory trees.

Usage examples::

    # map mode using default mapping file (opt/mapping.yaml or folders.csv)
    organizer map --upstream /path/to/upstream

    # migrate legacy folders.csv to mapping.yaml
    organizer migrate --upstream /path/to/upstream

The script supports two mapping‑file formats:

* New YAML format (mapping.yaml) — see project docs.
* Legacy CSV format (folders.csv) kept for backward compatibility.

All user-facing messages use colour helpers (compatible with Windows terminals).
"""

import argparse
import csv
import filecmp
import os
import shutil
import subprocess
import sys
import textwrap
from dataclasses import dataclass, replace
from enum import StrEnum
from fnmatch import fnmatch
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Sequence, Set, Tuple
from enum import Enum, auto
from collections import defaultdict

try:
    import yaml  # type: ignore
except ModuleNotFoundError:
    print("PyYAML is required. Install with `pip install pyyaml`.", file=sys.stderr)
    sys.exit(1)


# ---------------------------------------------------------------------------
# Helper classes & utilities
# ---------------------------------------------------------------------------


class AnsiColor(StrEnum):
    """Basic ANSI 8‑color escape sequences (normal intensity)."""

    BLACK = "\033[0;90m"
    RED = "\033[0;91m"
    GREEN = "\033[0;92m"
    YELLOW = "\033[0;93m"
    BLUE = "\033[0;94m"
    PURPLE = "\033[0;95m"
    CYAN = "\033[0;96m"
    WHITE = "\033[0;97m"


def color_print(
    text: str,
    *,
    bold: bool = False,
    color: Optional[AnsiColor] = None,
    endl: bool = True,
) -> None:
    """Print text with optional ANSI color and bold formatting.

    :param text: Text to print
    :param bold: Print bold text
    :param color: ANSI color code
    :param endl: Print newline at end
    """
    if sys.platform == "win32" or (not bold and color is None):
        print(text, end="\n" if endl else "")
        return

    prefix = ""
    if bold:
        prefix += str(color).replace("[0", "[1") if color else "\033[1m"
    else:
        prefix += str(color) if color else ""

    suffix = "\033[0m"
    print(f"{prefix}{text}{suffix}", end="\n" if endl else "")


def mark_success(text: str) -> None:
    """Print success message with green color.

    :param text: Message text
    """
    color_print("✓", color=AnsiColor.GREEN, endl=False)
    color_print(f" {text}")


def mark_semi_success(text: str) -> None:
    """Print semi-success message with yellow color.

    :param text: Message text
    """
    color_print(f"✓ {text}", color=AnsiColor.YELLOW)


def mark_failure(text: str) -> None:
    """Print failure message with red color.

    :param text: Message text
    """
    color_print(f"✗ {text}", color=AnsiColor.RED)


def mark_warning(text: str) -> None:
    """Print warning message with yellow color.

    :param text: Message text
    """
    color_print(f"! {text}", color=AnsiColor.YELLOW)


def mark_info(text: str) -> None:
    """Print info message with purple color.

    :param text: Message text
    """
    color_print(f"ℹ {text}", color=AnsiColor.PURPLE)


def prompt(
    question: str, possible_values: Sequence[str], *, default: Optional[str] = None
) -> str:
    """
    Prompt user for input and validate against possible values.

    :param question: Question to display
    :param possible_values: Allowed values
    :param default: Default value if input is empty
    :returns: User's validated answer
    """

    def format_options(options: Sequence[str], default: Optional[str]) -> str:
        formatted = []
        for option in options:
            if option == default:
                formatted.append(option.upper())
            else:
                formatted.append(option.lower())
        return f"({'/'.join(formatted)})"

    options_str = format_options(possible_values, default)
    while True:
        try:
            value = input(f"{question} {options_str}: ").strip().lower()
        except EOFError:
            value = ""

        if value == "" and default is not None:
            value = default

        if value in possible_values:
            return value

        mark_warning(f"Please enter one of: {', '.join(possible_values)}")


# ---------------------------------------------------------------------------
# Parsing & CLI
# ---------------------------------------------------------------------------


def _build_parser() -> argparse.ArgumentParser:
    """Build and return CLI argument parser.

    :returns: ArgumentParser instance
    """
    parser = argparse.ArgumentParser(
        prog="organizer",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """\
            Copy/sync files between two directory trees using declarative rules.

            * map      — apply mapping file (mapping.yaml or folders.csv)
            * migrate  — convert legacy folders.csv to mapping.yaml
            """
        ),
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    def _add_common_options(subparser: argparse.ArgumentParser) -> None:
        subparser.add_argument(
            "--local",
            metavar="PATH",
            type=Path,
            default=find_git_root(),
            help="Local repository root (defaults to git root)",
        )
        subparser.add_argument(
            "--upstream",
            metavar="PATH",
            type=Path,
            required=True,
            help="Upstream (reference) directory tree",
        )
        subparser.add_argument(
            "--no-checks",
            action="store_true",
            help="Skip preflight checks",
        )

    map_parser = subparsers.add_parser("map", help="Apply mapping rules")
    _add_common_options(map_parser)
    map_parser.add_argument(
        "--mapping-file",
        metavar="FILE",
        type=Path,
        help="Path to mapping.yaml or folders.csv (defaults to <local>/opt/...)",
    )
    map_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Do not modify anything, just report what would be done",
    )
    map_parser.add_argument(
        "--verbose",
        action="store_true",
        help="Print detailed information about actions taken",
    )
    map_parser.add_argument(
        "--apply-patches",
        action="store_true",
        default=False,
        help="Apply patches to the files",
    )

    migrate_parser = subparsers.add_parser(
        "migrate", help="Convert folders.csv to mapping.yaml"
    )
    _add_common_options(migrate_parser)

    return parser


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Parse and return CLI arguments.

    :param argv: Optional sequence of arguments
    :returns: Parsed arguments namespace
    """
    return _build_parser().parse_args(argv)


# ---------------------------------------------------------------------------
# Data structures for mapping entries
# ---------------------------------------------------------------------------


@dataclass(slots=True, frozen=True)
class YamlRule:
    source: str
    destination: Optional[str] = None
    action: str = "sync"  # sync | copy
    include: Optional[Tuple[str, ...]] = None
    exclude: Optional[Tuple[str, ...]] = None

    def iter_include(self) -> List[str]:
        if self.include is None:
            return ["*"]
        if isinstance(self.include, str):
            return [self.include]
        return list(self.include)

    def iter_exclude(self) -> List[str]:
        if self.exclude is None:
            return []
        if isinstance(self.exclude, str):
            return [self.exclude]
        return list(self.exclude)


@dataclass(slots=True)
class CsvRow:
    old: str
    new: str
    action: str
    ext2keep: str


# ---------------------------------------------------------------------------
# Mapping file loaders
# ---------------------------------------------------------------------------


def read_mapping_yaml(yaml_file_path: Path) -> List[YamlRule]:
    """
    Read mapping rules from a YAML file.

    :param yaml_file_path: Path to the YAML mapping file
    :returns: List of YamlRule objects parsed from the file
    """
    with yaml_file_path.open("r", encoding="utf-8") as file_handle:
        content = yaml.safe_load(file_handle) or {}
    return [YamlRule(**entry) for entry in content.get("paths", [])]


def write_mapping_yaml(yaml_file_path: Path, yaml_rules: Sequence[YamlRule]) -> None:
    """
    Write mapping rules to a YAML file.

    :param yaml_file_path: Path to the YAML mapping file
    :param yaml_rules: Sequence of YamlRule objects to write
    """
    yaml_content: Dict[str, Any] = {"paths": []}

    for rule in yaml_rules:
        entry: Dict[str, Any] = {"source": rule.source}
        if rule.destination and rule.destination != rule.source:
            entry["destination"] = rule.destination
        if rule.action != "sync":
            entry["action"] = rule.action
        if rule.include and rule.include != "*" and rule.include != ("*",):
            entry["include"] = rule.include
        if rule.exclude:
            entry["exclude"] = rule.exclude
        yaml_content["paths"].append(entry)

    with yaml_file_path.open("w", encoding="utf-8") as file_handle:
        yaml.safe_dump(yaml_content, file_handle, sort_keys=False, allow_unicode=True)

    mark_success(f"Writed {len(yaml_rules)} rules into {yaml_file_path}")


def read_folders_csv(csv_file_path: Path) -> List[CsvRow]:
    """
    Read mapping rules from a legacy CSV file.

    :param csv_file_path: Path to the CSV mapping file
    :returns: List of CsvRow objects parsed from the file
    """
    rows = []
    with csv_file_path.open("r", newline="", encoding="utf-8") as file_handle:
        for line in csv.reader(file_handle):
            old, new, action, ext2keep = (column.strip() for column in line[:4])
            if not old:
                old = "."
            if not new:
                new = "."
            rows.append(CsvRow(old, new, action, ext2keep))
    return rows


# ---------------------------------------------------------------------------
# Git helpers
# ---------------------------------------------------------------------------


def find_git_root(start: Optional[Path] = None) -> Path:
    """
    Find the root directory of a Git repository.

    :param start: Starting directory (defaults to current working directory)
    :returns: Path to the Git root directory
    """
    current_path = (start or Path.cwd()).resolve()
    for directory in (current_path, *current_path.parents):
        if (directory / ".git").is_dir():
            return directory
    return Path.cwd().resolve()


def find_missing_upstream_file(
    repo_path: Path, relative_file_path: Path
) -> Optional[Literal["D", "R"]]:
    """
    Analyze the Git history of a file to determine whether it was deleted,
    renamed

    :param repo_path: Path to the Git repository root
    :param relative_file_path: File path relative to the repo root
    :return: One of "D", "R", or None if no info available
    """
    cmd = [
        "git",
        "-C",
        str(repo_path),
        "log",
        "--follow",
        "--find-renames",
        "--name-status",
        "--format=%H",
        "--",
        str(relative_file_path),
    ]

    try:
        output = subprocess.check_output(cmd, text=True)
    except subprocess.CalledProcessError:
        return None

    lines = output.strip().splitlines()

    seen_rename = False

    for line in lines:
        if not line or all(c in "0123456789abcdef" for c in line.strip()):
            continue  # commit hash line

        parts = line.split("\t")
        if parts[0].startswith("R"):
            seen_rename = True
        elif parts[0] == "D":
            return "D"

    if seen_rename:
        return "R"

    return None


def has_uncommitted_changes(repo_path: Path) -> bool:
    """
    Check if there are uncommitted changes in the repository.

    :param repo_path: Path to the Git repository root
    :returns: True if changes exist, False otherwise
    """
    try:
        output = subprocess.check_output(
            ["git", "-C", str(repo_path), "status", "--porcelain"],
            text=True,
        )
        return bool(output.strip())
    except subprocess.CalledProcessError:
        return False


def get_latest_tag(repo_path: Path) -> Optional[str]:
    """
    Get the latest tag in the repository.

    :param repo_path: Path to the Git repository root
    :returns: Latest tag string or None
    """
    try:
        tag = subprocess.check_output(
            ["git", "-C", str(repo_path), "describe", "--tags", "--abbrev=0"],
            text=True,
        ).strip()
        return tag
    except subprocess.CalledProcessError:
        return None


def confirm_continue(question: str, default: str = "n") -> bool:
    """
    Prompt user to confirm continuation.

    :param question: Question to display
    :param default: Default answer
    :returns: True if user confirms, False otherwise
    """
    answer = prompt(question, ["y", "n"], default=default)
    return answer == "y"


def preflight_checks(local_path: Path, upstream_path: Path) -> None:
    """
    Perform preflight checks before running main commands.

    :param repo_path: Path to local repository
    :param upstream_path: Path to upstream directory
    """
    if has_uncommitted_changes(local_path):
        if not confirm_continue(
            "There are uncommitted changes in fork repository. Continue?"
        ):
            mark_failure("Aborted by user due to uncommitted changes.")
            sys.exit(1)

    if has_uncommitted_changes(upstream_path):
        if not confirm_continue(
            "There are uncommitted changes in upstream repository. Continue?"
        ):
            mark_failure("Aborted by user due to uncommitted changes.")
            sys.exit(1)

    tag = get_latest_tag(upstream_path)
    if tag:
        if not confirm_continue(f"Upstream version is {tag}. Continue?"):
            mark_failure("Aborted by user due to upstream version confirmation.")
            sys.exit(1)
    else:
        mark_warning("Could not determine upstream version tag.")


# ---------------------------------------------------------------------------
# CSV → YAML conversion helpers
# ---------------------------------------------------------------------------


def expand_braced_range(token: str) -> List[str]:
    """Expand pattern like 'file[1-3]' → ['file1', 'file2', 'file3']."""

    if "[" not in token or "]" not in token:
        return [token]
    left_brace = token.index("[")
    right_brace = token.index("]", left_brace)
    start, finish = token[left_brace + 1 : right_brace].split("-")
    prefix = token[:left_brace]
    suffix = token[right_brace + 1 :]
    return [f"{prefix}{i}{suffix}" for i in range(int(start), int(finish) + 1)]


def is_extension(pattern: str) -> bool:
    EXTENSIONS = {
        "1",
        "api",
        "asn",
        "c",
        "cc",
        "cl",
        "cpp",
        "csv",
        "db",
        "frag",
        "geom",
        "gif",
        "gpl",
        "h",
        "hpp",
        "html",
        "ini",
        "jpg",
        "ll",
        "mm",
        "pap",
        "png",
        "py",
        "qrc",
        "rc",
        "sql",
        "svg",
        "ts",
        "txt",
        "ui",
        "vert",
        "xml",
        "xsd",
        "xcf",
        "yy",
    }

    result = pattern.lower().lstrip(".") in EXTENSIONS
    if not result and len(pattern) <= 4:
        raise RuntimeError("Possibly missed extension")
    return result


def collect_subdirs(root: Path) -> Dict[Path, Set[Path]]:
    all_directories: Dict[Path, Set[Path]] = {}
    all_directories[Path(".")] = set()

    ignored_directories = {root / ".git", root / "build"}
    for parent in root.rglob("*"):
        if not parent.is_dir() or any(
            parent.is_relative_to(ignored_directory)
            for ignored_directory in ignored_directories
        ):
            continue

        relative_parent = parent.relative_to(root)

        if relative_parent not in all_directories:
            all_directories[relative_parent] = set()
        all_directories[relative_parent.parent].add(relative_parent)

    return all_directories


def convert_csv_to_yaml_rules(
    csv_rows: Sequence[CsvRow],
) -> Tuple[Sequence[YamlRule], Set[Path]]:
    result: Set[YamlRule] = set()
    skip_directories: Set[Path] = set()

    for row in csv_rows:
        if row.action == "skip" or not row.ext2keep:
            # behavior identical to previous tool
            skip_directories.add(Path(row.old))
            continue

        include_patterns = None
        if row.ext2keep == "*":
            include_patterns = ["*"]

        elif row.ext2keep:
            expanded_tokens = []
            for token in row.ext2keep.split(","):
                expanded_tokens.extend(expand_braced_range(token.strip()))

            include_patterns = []
            for pattern in expanded_tokens:
                include_patterns.append(
                    f"*.{pattern.lstrip('.')}" if is_extension(pattern) else pattern
                )

            include_patterns.sort()

        result.add(
            YamlRule(
                source=row.old,
                destination=row.new or None,
                action="sync" if not row.action else row.action,
                include=tuple(include_patterns) if include_patterns else None,
            )
        )

    return list(result), set(skip_directories)


def find_missed_rules(
    local: Path,
    upstream: Path,
    local_subdirs: Dict[Path, Set[Path]],
    upstream_subdirs: Dict[Path, Set[Path]],
    rules_dict: Dict[Path, YamlRule],
    skip_paths: Set[Path],
) -> List[YamlRule]:
    """
    Find directories that are missing corresponding rules.
    """
    # Create sets for easy lookup
    local_subdirs_set = set(local_subdirs.keys())
    upstream_subdirs_set = set(upstream_subdirs.keys())
    rules_dirs_set = set(rules_dict.keys())

    common_dirs = upstream_subdirs_set & local_subdirs_set
    not_listed = (common_dirs - rules_dirs_set) - skip_paths
    if not not_listed:
        return []

    missed_rules = []
    for subdir in not_listed:
        if subdir.name == "__pycache__":
            continue

        upstream_files = [
            file for file in (upstream / subdir).glob("*") if file.is_file()
        ]
        local_files = [file for file in (local / subdir).glob("*") if file.is_file()]
        if not local_files:
            continue

        upstream_exts = {
            file.suffix.lstrip(".").lower() for file in upstream_files if file.suffix
        }
        local_exts = {
            file.suffix.lstrip(".").lower() for file in local_files if file.suffix
        }

        if len(upstream_exts) > 0 and upstream_exts == local_exts:
            include_patterns = ["*"]
        else:
            include_patterns = [f"*.{ext}" for ext in sorted(local_exts) if ext]

        missed_rules.append(
            YamlRule(
                source=subdir.as_posix(),
                destination=None,
                action="sync",
                include=tuple(include_patterns),
            )
        )

    return missed_rules


class CollapseType(Enum):
    COLLAPSIBLE = auto()
    COLLAPSIBLE_WITH_EXCLUDE = auto()
    COLLAPSIBLE_WITH_SPLIT = auto()
    NOT_COLLAPSIBLE = auto()


def collapsibility(
    rule_path: Path,
    rule: YamlRule,
    subpaths: Set[Path],
    rules_dict: Dict[Path, YamlRule],
    suspicious_rules: Set[YamlRule],
) -> CollapseType:
    if rule_path == Path(".") or len(subpaths) == 0:
        return CollapseType.NOT_COLLAPSIBLE

    all_paths_has_rules = True
    all_paths_has_same_rules = True
    all_patterns_is_glob = all("*" in pattern for pattern in rule.iter_include())
    all_patterns_has_intersection = True
    is_relative_to_same_directory = True

    common_include = set(rule.iter_include())

    source_root = Path(rule.source)
    destination_root = Path(rule.destination or rule.source)

    for subpath in subpaths:
        if subpath not in rules_dict:
            all_paths_has_rules = False
            continue

        subpath_rule = rules_dict[subpath]
        subpath_source = Path(subpath_rule.source)
        subpath_destination = Path(subpath_rule.destination or subpath_rule.source)
        if subpath_source.relative_to(source_root) != subpath_destination.relative_to(
            destination_root
        ):
            suspicious_rules.add(subpath_rule)
            is_relative_to_same_directory = False
            # break

        if rules_dict[subpath].iter_include() != rule.iter_include():
            all_paths_has_same_rules = False

        common_include &= set(subpath_rule.iter_include())

    all_patterns_has_intersection = bool(common_include)

    if not is_relative_to_same_directory:
        return CollapseType.NOT_COLLAPSIBLE

    if all_paths_has_same_rules:
        if all_paths_has_rules:
            return CollapseType.COLLAPSIBLE
        if all_patterns_is_glob:
            return CollapseType.COLLAPSIBLE_WITH_EXCLUDE
    elif all_patterns_has_intersection and all_paths_has_rules:
        return CollapseType.COLLAPSIBLE_WITH_SPLIT

    return CollapseType.NOT_COLLAPSIBLE


def combine_nested_subdirs(
    path: Path,
    all_subdirs: Dict[Path, Set[Path]],
) -> Set[Path]:
    result = set()
    stack = [path]
    while stack:
        current = stack.pop()
        children = all_subdirs.get(current, set())
        result.update(children)
        stack.extend(children)
    return result


def collapse_glob_dirs(
    source: Path,
    glob_dirs: List[Path],
    all_subdirs: Dict[Path, Set[Path]],
) -> Tuple[str]:
    """
    Collapse exclude patterns: if all subdirs of a parent are covered, use recursive.

    :param all_subdirs: Optional dict of all subdirs for coverage check
    :param patterns: List of Path objects (relative)
    :return: Tuple of collapsed patterns as strings
    """
    if not glob_dirs:
        return tuple()

    # Create a mapping of parent directories to their subdirectoriesa like all_subdirs
    glob_subdirs = defaultdict(set)
    for glob_dir in glob_dirs:
        glob_subdirs[glob_dir]
        if glob_dir.parent in glob_dirs:
            glob_subdirs[glob_dir.parent].add(glob_dir)

    processed = set()
    collapsed = set()
    for parent, children in sorted(glob_subdirs.items()):
        if parent in processed:
            continue

        processed.add(parent)

        if not children:
            collapsed.add(f"{parent.relative_to(source)}/*")
            continue

        all_filesystem_subdirs = combine_nested_subdirs(parent, all_subdirs)
        all_pattern_subdirs = combine_nested_subdirs(parent, glob_subdirs)
        if all_filesystem_subdirs == all_pattern_subdirs:
            collapsed.add(f"{parent.relative_to(source)}/**/*")
            processed.update(all_pattern_subdirs)
        else:
            collapsed.add(f"{parent.relative_to(source)}/*")

    return tuple(sorted(collapsed))


def collapse_rule_for_path(
    rule_path: Path,
    rule: YamlRule,
    rules_dict: Dict[Path, YamlRule],
    upstream_subdirs: Dict[Path, Set[Path]],
    added_rules: Set[YamlRule],
    suspicious_rules: Set[YamlRule],
) -> List[YamlRule]:
    """
    Collapse rules for a given path if possible.

    :param rule_path: Path of the rule
    :param rule: YamlRule instance
    :param rules_dict: All rules dict
    :param upstream_subdirs: Upstream subdirectories
    :param added_rules: Set of already added rules
    :return: List of collapsed or original rules
    """

    if rule in added_rules:
        return []

    rule_subdirs = combine_nested_subdirs(rule_path, upstream_subdirs)
    collapse_type = collapsibility(
        rule_path, rule, rule_subdirs, rules_dict, suspicious_rules
    )
    if collapse_type == CollapseType.NOT_COLLAPSIBLE:
        added_rules.add(rule)
        return [rule]

    if collapse_type == CollapseType.COLLAPSIBLE_WITH_SPLIT:
        # Find common include patterns among all subpaths
        common_include = set(rule.iter_include())
        for subpath in rule_subdirs:
            if subpath in rules_dict:
                common_include &= set(rules_dict[subpath].iter_include())

        parent_include = list(set(rule.iter_include()) - common_include)
        parent_include.extend(f"**/{pattern}" for pattern in sorted(common_include))
        parent_include.sort()

        # Create a parent rule with common patterns
        parent_rule = replace(
            rule,
            include=tuple(parent_include),
            exclude=None,
        )
        added_rules.add(parent_rule)

        # For each subpath, remove common patterns from its include
        child_rules = []
        for subpath in rule_subdirs:
            if subpath not in rules_dict:
                continue

            sub_rule = rules_dict[subpath]
            added_rules.add(sub_rule)

            sub_include = set(sub_rule.iter_include()) - common_include
            if not sub_include:
                continue

            child_rules.append(
                replace(
                    sub_rule,
                    include=tuple(sorted(sub_include)),
                    exclude=None,
                )
            )

        return [parent_rule] + child_rules

    include = tuple(f"**/{pattern}" for pattern in rule.iter_include())
    exclude = None
    if collapse_type == CollapseType.COLLAPSIBLE_WITH_EXCLUDE:
        exclude_patterns = list(
            sorted(subpath for subpath in rule_subdirs if subpath not in rules_dict)
        )
        exclude = collapse_glob_dirs(rule_path, exclude_patterns, upstream_subdirs)

    added_rules.add(rule)
    added_rules.update(
        rules_dict[subpath] for subpath in rule_subdirs if subpath in rules_dict
    )
    return [replace(rule, include=include, exclude=exclude)]


def collapse_rules(
    rules_dict: Dict[Path, YamlRule],
    upstream_subdirs: Dict[Path, Set[Path]],
) -> List[YamlRule]:
    """
    Collapse rules in the rules_dict using upstream_subdirs structure.

    :param rules_dict: All rules dict
    :param upstream_subdirs: Upstream subdirectories
    :return: List of collapsed rules
    """
    added_rules = set()
    filtered_yaml_rules = []
    suspicious_rules = set()

    for rule_path, rule in sorted(rules_dict.items(), key=lambda item: item[0]):
        collapsed = collapse_rule_for_path(
            rule_path, rule, rules_dict, upstream_subdirs, added_rules, suspicious_rules
        )
        filtered_yaml_rules.extend(collapsed)

    for suspicious_rule in suspicious_rules:
        mark_warning(
            f"Suspicious rule: {suspicious_rule.source} → {suspicious_rule.destination}"
        )

    return filtered_yaml_rules


def process_outdated_rules(
    local: Path, upstream: Path, rules_dict: Dict[Path, YamlRule]
) -> None:
    missing_dirs = set(
        rule.source
        for rule in rules_dict.values()
        if not (upstream / rule.source).exists()
    )
    if not missing_dirs:
        return

    # Remove rules for directories missing in both upstream and local
    missing_in_both = set(
        dir_path for dir_path in missing_dirs if not (local / dir_path).exists()
    )
    for dir_path in missing_in_both:
        del rules_dict[Path(dir_path)]

    missing_only_in_upstream = list(missing_dirs - missing_in_both)
    missing_only_in_upstream.sort()

    mark_warning(
        f"Directories missing in upstream: \n- {'\n- '.join(missing_only_in_upstream)}"
    )


def postprocess_rules(
    local: Path,
    upstream: Path,
    rules: Sequence[YamlRule],
    skip_directories: Set[Path],
) -> Sequence[YamlRule]:
    # Combine rules with upstream path
    rules_dict: Dict[Path, YamlRule] = {}
    for rule in sorted(rules, key=lambda rule: rule.source):
        rules_dict[Path(rule.source)] = rule

    # Collect all dirs and its nested dirs
    local_subdirs = collect_subdirs(local)
    upstream_subdirs = collect_subdirs(upstream)

    # Find directories that are not listed in rules_dict but exist both in local and upstream
    not_existed_rules: List[YamlRule] = find_missed_rules(
        local, upstream, local_subdirs, upstream_subdirs, rules_dict, skip_directories
    )
    for not_existed_rule in not_existed_rules:
        rules_dict[Path(not_existed_rule.source)] = not_existed_rule

    mark_info(f"Added {len(not_existed_rules)} not listed rules")

    process_outdated_rules(local, upstream, rules_dict)

    # if len(not_existed_rules) > 0:
    #     mark_warning(
    #         f"Found {len(not_existed_rules)} not existed rules ({len(upstream_subdirs)} total)"
    #     )

    #     # Print all not_existed_rules under upstream / src/core/
    #     core_dir = upstream / "tests/testdata/control_images/composer_mapoverview"
    #     core_rules = [p for p in not_existed_rules if p.is_relative_to(core_dir)]
    #     if core_rules:
    #         mark_info(f"Not existed rules under {core_dir}:")
    #         for p in core_rules:
    #             print(p)

    # sys.exit(1)

    # Delete obsolete directories
    # wrong_dirs = set(rules_dict.keys()) - set(all_directories.keys())

    # if len(wrong_dirs) > 0:
    #     mark_warning(f"{len(wrong_dirs)} obsolete rules")
    #     for obsolete_dir in wrong_dirs:
    # dir_status = _find_missing_upstream_file(upstream, obsolete_dir)
    # mark_warning(f"{None} {obsolete_dir}")
    # for obsolete_dir in obsolete_dirs:
    #     del rules_dict[obsolete_dir]

    # Collapse rules
    collapsed_yaml_rules = collapse_rules(rules_dict, upstream_subdirs)
    mark_info(f"Collapsed to {len(collapsed_yaml_rules)} rules")

    result = list(sorted(collapsed_yaml_rules, key=lambda rule: rule.source))
    return result


# ---------------------------------------------------------------------------
# File operations (map)
# ---------------------------------------------------------------------------


def copy_file(
    source_path: Path, destination_path: Path, verbose: bool, dry_run: bool
) -> None:
    if destination_path.exists() and filecmp.cmp(
        source_path, destination_path, shallow=False
    ):
        if verbose or dry_run:
            mark_info(
                f"Unchanged: {destination_path.relative_to(destination_path.anchor)}"
            )
        return

    if dry_run:
        mark_semi_success(f"Would copy {source_path} → {destination_path}")
        return

    destination_path.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_path, destination_path)

    mark_success(
        "Copied {} → {}".format(
            source_path.relative_to(source_path.anchor),
            destination_path.relative_to(destination_path.anchor),
        )
    )


def delete_file(path: Path, dry_run: bool) -> None:
    if dry_run:
        mark_semi_success(f"Would delete {path}")
        return

    try:
        path.unlink()
        mark_warning(f"Deleted {path.relative_to(path.anchor)}")
    except OSError as error:
        mark_failure(f"Cannot delete {path}: {error}")


# ---------------------------------------------------------------------------
# Rule mapping
# ---------------------------------------------------------------------------


def map_rule(
    rule: YamlRule, upstream_root: Path, local_root: Path, verbose: bool, dry_run: bool
) -> None:
    source_path = upstream_root / rule.source
    destination_path = local_root / (rule.destination or rule.source)

    if not source_path.exists():
        # TODO investigate
        mark_warning(f"Source {source_path} missing; skipping")
        return

    if source_path.is_file():
        copy_file(source_path, destination_path, verbose, dry_run)
        return

    include_patterns = rule.iter_include()
    exclude_patterns = rule.iter_exclude()

    excluded_files = set()
    for exclude_pattern in exclude_patterns:
        excluded_files.update(source_path.glob(exclude_pattern))
        excluded_files.update(destination_path.glob(exclude_pattern))

    for include_pattern in include_patterns:
        for file_path in source_path.glob(include_pattern):
            if not file_path.is_file() or file_path in excluded_files:
                continue

            relative_path = file_path.relative_to(source_path).as_posix()
            copy_file(file_path, destination_path / relative_path, verbose, dry_run)

    # for file_path in source_path.rglob("*"):
    #     if not file_path.is_file():
    #         continue

    #     relative_path = file_path.relative_to(source_path).as_posix()

    #     if not matches_any(relative_path, include_patterns):
    #         continue
    #     if exclude_patterns and matches_any(relative_path, exclude_patterns):
    #         continue

    #     copy_file(
    #         file_path, destination_path / relative_path, verbose, dry_run
    #     )

    # if rule.action == "sync":
    #     for file_path in destination_path.rglob("*"):
    #         if not file_path.is_file():
    #             continue
    #         relative_path = file_path.relative_to(destination_path).as_posix()
    #         if not matches_any(relative_path, include_patterns):
    #             continue
    #         if exclude_patterns and matches_any(relative_path, exclude_patterns):
    #             continue
    #         if not (source_path / relative_path).exists():
    #             delete_file(file_path, dry_run)


# ---------------------------------------------------------------------------
# map command
# ---------------------------------------------------------------------------


def run_map(args: argparse.Namespace) -> None:
    local_root = Path(args.local).resolve()
    upstream_root = Path(args.upstream).resolve()

    if args.mapping_file:
        mapping_file = Path(args.mapping_file)
    else:
        mapping_file = local_root / "opt" / "mapping.yaml"
        if not mapping_file.exists():
            mapping_file = local_root / "opt" / "folders.csv"

    if not mapping_file.exists():
        mark_failure(f"Mapping file not found in {mapping_file.parent}")
        sys.exit(1)

    if mapping_file.suffix in {".yaml", ".yml"}:
        rules = read_mapping_yaml(mapping_file)
    else:
        mark_warning("Using legacy folders.csv — consider migrating")
        sys.exit(1)

    mark_info(f"Read {len(rules)} rules from {mapping_file}")

    for rule in rules:
        map_rule(rule, upstream_root, local_root, args.verbose, args.dry_run)

    mark_success(f"Mapping completed. {len(rules)} rules applied")

    if args.dry_run:
        return

    patcher = local_root / "scripts" / "patcher.py"
    if not patcher.exists() or (
        not args.apply_patches and not confirm_continue("Apply patches using patcher.py?")
    ):
        return

    subprocess.run(
        [
            sys.executable,
            str(patcher),
            "apply",
            "--upstream",
            str(upstream_root),
            "--local",
            str(local_root),
        ],
        check=True,
    )


# ---------------------------------------------------------------------------
# migrate command — CONVERTS CSV to YAML
# ---------------------------------------------------------------------------


def run_migrate(args: argparse.Namespace) -> None:
    """
    Execute the 'migrate' command: convert legacy folders.csv to mapping.yaml.

    :param args: Parsed command-line arguments
    """
    local_root = Path(args.local).resolve()
    upstream_root = Path(args.upstream).resolve()

    # Step 1: read legacy CSV mapping file
    csv_file_path = local_root / "opt" / "folders.csv"
    if not csv_file_path.exists():
        mark_failure(f"Legacy file {csv_file_path} not found")
        sys.exit(1)

    rows = read_folders_csv(csv_file_path)
    mark_info(f"Read {len(rows)} rows from {csv_file_path}")

    # Step 2: convert CSV rules to YAML rules and postprocess
    yaml_rules, skip_directories = convert_csv_to_yaml_rules(rows)
    yaml_rules = postprocess_rules(
        local_root, upstream_root, yaml_rules, skip_directories
    )

    # Step 3: write YAML mapping file
    yaml_file_path = local_root / "opt" / "mapping.yaml"
    write_mapping_yaml(yaml_file_path, yaml_rules)

    # Step 4: offer to delete old CSV mapping file
    if confirm_continue("Remove legacy folders.csv?"):
        try:
            csv_file_path.unlink()
            mark_success("Deleted folders.csv")
        except OSError as error:
            mark_failure(f"Cannot delete {csv_file_path}: {error}")
            sys.exit(1)

    mark_success("Migration completed. Please check the new mapping.yaml file.")


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------


def main() -> None:
    arguments = parse_args()

    local_root = Path(arguments.local).resolve()
    upstream_root = Path(arguments.upstream).resolve()
    if not getattr(arguments, "no_checks", False):
        preflight_checks(local_root, upstream_root)

    if arguments.command == "map":
        run_map(arguments)
    elif arguments.command == "migrate":
        run_migrate(arguments)
    else:
        mark_failure(f"Unknown command: {arguments.command}")
        sys.exit(2)


if __name__ == "__main__":
    main()
