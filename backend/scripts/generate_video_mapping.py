"""
Script to help generate video mapping for Google Drive videos.

This script provides utilities to:
1. Generate a template for manual video mapping
2. Validate existing video mappings
3. Extract video IDs from VSL_DATA.json

Usage:
    python backend/scripts/generate_video_mapping.py --mode template
    python backend/scripts/generate_video_mapping.py --mode validate
    python backend/scripts/generate_video_mapping.py --mode extract-ids
"""

import argparse
import json
import sys
from pathlib import Path

# Add backend to path
backend_dir = Path(__file__).parent.parent
sys.path.insert(0, str(backend_dir.parent))


def generate_template(output_path: str = "data/video_mapping_template.json") -> None:
    """
    Generate a template for manual video mapping.

    Args:
        output_path: Path to save the template
    """
    template = {
        "_comment": "Video ID to Google Drive File ID mapping",
        "_instructions": [
            "1. Open your Google Drive folder: https://drive.google.com/drive/folders/1kGAzGKgO9Sc53D5bNoWQYjhQHiucG3sZ",
            "2. For each video, right-click → Share → Copy link",
            "3. Extract the file ID from the URL: https://drive.google.com/file/d/FILE_ID_HERE/view",
            "4. Replace 'YOUR_FILE_ID_HERE' with the actual file IDs",
            "5. Remove entries with '_comment' and '_instructions' keys",
            "6. Save as video_mapping.json"
        ],
        "_example_format": {
            "D0001B": "1abc123def456ghi789",
            "D0001N": "1xyz987wvu654tsr321"
        },
        "D0001B": "YOUR_FILE_ID_HERE",
        "D0001N": "YOUR_FILE_ID_HERE",
        "D0001T": "YOUR_FILE_ID_HERE",
        "D0002": "YOUR_FILE_ID_HERE",
        "D0003": "YOUR_FILE_ID_HERE",
    }

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with open(output, "w", encoding="utf-8") as f:
        json.dump(template, f, indent=2, ensure_ascii=False)

    print(f"✓ Template generated: {output}")
    print("\nNext steps:")
    print("1. Open your Google Drive folder")
    print("2. For each video, get the file ID from the shareable link")
    print("3. Fill in the template with actual file IDs")
    print("4. Save as data/video_mapping.json")


def validate_mapping(mapping_path: str = "data/video_mapping.json") -> bool:
    """
    Validate an existing video mapping file.

    Args:
        mapping_path: Path to the video mapping file

    Returns:
        True if valid, False otherwise
    """
    path = Path(mapping_path)

    if not path.exists():
        print(f"❌ Error: Mapping file not found: {path}")
        return False

    try:
        with open(path, "r", encoding="utf-8") as f:
            mapping = json.load(f)

        # Filter out comment keys
        video_mappings = {k: v for k, v in mapping.items() if not k.startswith("_")}

        if not video_mappings:
            print("❌ Error: No video mappings found in file")
            return False

        # Check for placeholder values
        placeholders = [k for k, v in video_mappings.items() if "PLACEHOLDER" in str(v) or "YOUR_FILE_ID" in str(v)]

        print(f"\n✓ Mapping file loaded: {path}")
        print(f"✓ Total mappings: {len(video_mappings)}")

        if placeholders:
            print(f"\n⚠️  Warning: {len(placeholders)} placeholder values found:")
            for video_id in placeholders[:5]:  # Show first 5
                print(f"   - {video_id}: {video_mappings[video_id]}")
            if len(placeholders) > 5:
                print(f"   ... and {len(placeholders) - 5} more")
            print("\nReplace these with actual Google Drive file IDs before using.")
            return False

        # Validate file ID format (basic check)
        invalid = []
        for video_id, file_id in video_mappings.items():
            if not isinstance(file_id, str) or len(file_id) < 10:
                invalid.append(video_id)

        if invalid:
            print(f"\n⚠️  Warning: {len(invalid)} potentially invalid file IDs:")
            for video_id in invalid[:5]:
                print(f"   - {video_id}: {video_mappings[video_id]}")
            if len(invalid) > 5:
                print(f"   ... and {len(invalid) - 5} more")

        print("\n✓ Validation complete!")
        print(f"✓ Valid mappings: {len(video_mappings) - len(invalid)}")

        return len(invalid) == 0

    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON format: {e}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def extract_video_ids(json_path: str = "data/VSL_DATA.json", output_path: str = "data/video_ids.txt") -> None:
    """
    Extract all unique video IDs from VSL_DATA.json.

    Args:
        json_path: Path to VSL_DATA.json
        output_path: Path to save the extracted IDs
    """
    path = Path(json_path)

    if not path.exists():
        print(f"❌ Error: Data file not found: {path}")
        return

    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)

        # Extract video IDs
        video_ids = set()
        for entry in data.get("data", []):
            video_id = entry.get("_id")
            if video_id:
                video_ids.add(video_id)

        # Sort video IDs
        sorted_ids = sorted(video_ids)

        # Save to file
        output = Path(output_path)
        output.parent.mkdir(parents=True, exist_ok=True)

        with open(output, "w", encoding="utf-8") as f:
            for video_id in sorted_ids:
                f.write(f"{video_id}\n")

        print(f"✓ Extracted {len(sorted_ids)} unique video IDs")
        print(f"✓ Saved to: {output}")

        # Generate mapping template with all IDs
        template_path = "data/video_mapping_all.json"
        mapping_template = {video_id: "YOUR_FILE_ID_HERE" for video_id in sorted_ids}

        with open(template_path, "w", encoding="utf-8") as f:
            json.dump(mapping_template, f, indent=2, ensure_ascii=False)

        print(f"✓ Full mapping template saved to: {template_path}")
        print("\nNext steps:")
        print("1. Use this template to fill in all Google Drive file IDs")
        print("2. You can do this gradually or use a script with Google Drive API")

    except json.JSONDecodeError as e:
        print(f"❌ Error: Invalid JSON format: {e}")
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Generate and validate video mapping for Google Drive videos"
    )
    parser.add_argument(
        "--mode",
        choices=["template", "validate", "extract-ids"],
        required=True,
        help="Mode: generate template, validate existing mapping, or extract video IDs"
    )
    parser.add_argument(
        "--mapping-path",
        default="data/video_mapping.json",
        help="Path to video mapping file (default: data/video_mapping.json)"
    )
    parser.add_argument(
        "--data-path",
        default="data/VSL_DATA.json",
        help="Path to VSL_DATA.json (default: data/VSL_DATA.json)"
    )

    args = parser.parse_args()

    print("=" * 60)
    print("Video Mapping Generator")
    print("=" * 60)
    print()

    if args.mode == "template":
        generate_template()
    elif args.mode == "validate":
        is_valid = validate_mapping(args.mapping_path)
        sys.exit(0 if is_valid else 1)
    elif args.mode == "extract-ids":
        extract_video_ids(args.data_path)


if __name__ == "__main__":
    main()
