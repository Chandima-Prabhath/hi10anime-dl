import re
import urllib.parse
from typing import Set, Dict


class LinkParser:
    @staticmethod
    def parse(links: Set[str]) -> Dict[str, Dict[str, list]]:
        categorized_links = {}

        for link in links:
            try:
                # Decode URL to handle spaces and special chars
                decoded_link = urllib.parse.unquote(link)
                # Split path to segments
                # Example: .../Shows/(Hi10)_Title_(Quality)/filename
                parts = decoded_link.split("/")

                filename = parts[-1].split("?")[0]

                season = "Unknown Series"
                quality = "Unknown"
                episode = "N/A"
                file_type = "MKV"

                # Combine parts for easier parsing
                full_path_str = "/".join(parts)

                # Try to find quality in the full path
                quality_match = re.search(r"[\(\[]((?:\d{3,4}p|BD|DVD|EXTRAS|SPECIALS|ONA|OVA)[\w\s_.-]*)[\)\]]", full_path_str, re.IGNORECASE)
                if quality_match:
                    quality = quality_match.group(1)

                # Heuristic for season: Try to find a part of the path that looks like a season/show name
                # This is tricky because of the variability. Let's try to find the directory that contains the quality.
                season_match = re.search(r"/([^/]*?[\(\[]" + re.escape(quality) + r"[\)\]][^/]*)/", full_path_str, re.IGNORECASE)
                if season_match:
                    season = season_match.group(1)
                    season = re.sub(r"[\(\[]" + re.escape(quality) + r"[\)\]]", "", season, flags=re.IGNORECASE).strip("_ ").strip()

                if filename.endswith(".torrent"):
                    file_type = "Torrent"
                    season = filename.rsplit(".", 1)[0]
                    season = re.sub(r"[\(\[][^)\]]+[\)\]]$", "", season).strip("_ ").strip()

                # Refine Episode Number from Filename
                # Look for patterns like " - 01 ", " - 01", "_01_", " 01 "
                # Specific check for OP/ED/NCOP/NCED

                # Refine Episode Number from Filename
                # Look for patterns like " - 01 ", " - 01", "_01_", " 01 "
                # Specific check for OP/ED/NCOP/NCED

                # Check for specials first
                if any(x in filename for x in ["NCOP", "NCED", "OP", "ED"]):
                    # Try to extract the full tag e.g. OP01
                    op_ed_match = re.search(
                        r"[-_ ]((?:NC)?(?:OP|ED)\d{0,2})", filename, re.IGNORECASE
                    )
                    if op_ed_match:
                        episode = op_ed_match.group(1).upper()
                    else:
                        episode = "Extras"
                else:
                    # Standard episode number matching
                    # Priority 1: Look for explicit dash separator (common in scene releases)
                    # e.g. " - 01", "_-_01", " - 01 "
                    episode_match = re.search(r"[ _]-[ _](\d{2,3}(?:v\d)?)", filename)

                    if not episode_match:
                        # Priority 2: Look for number strictly surrounded by _ or space or brackets
                        # e.g. "_01_", " 01 ", "[01]"
                        # We carefully exclude things like "720p" (followed by p) or "2022" (4 digits)
                        # We use (?<!\d) to ensure we don't match middle of number
                        # We use (?![pP]) to avoid resolution (p)
                        episode_match = re.search(
                            r"(?:^|[ _\[\(-])(\d{2,3}(?:v\d)?)(?:[ _\]\)-]|$)(?![pP])",
                            filename,
                        )

                    if episode_match:
                        episode = episode_match.group(1)
                    else:
                        pass

                # Clean up extracted Season Name (remove leading (Hi10) or [Hi10] if present for cleaner UI?)
                # user didn't explicitly ask to remove it but "organized list" implies cleanliness.
                # Let's clean it up slightly if it starts with (Hi10) or [Hi10]
                if season.startswith("(Hi10)") or season.startswith("[Hi10]"):
                    season = season.replace("(Hi10)", "").replace("[Hi10]", "").strip("_ ")

                # Build nested dictionary
                if season not in categorized_links:
                    categorized_links[season] = {}
                if quality not in categorized_links[season]:
                    categorized_links[season][quality] = []

                categorized_links[season][quality].append(
                    {
                        "episode": episode,
                        "file_type": file_type,
                        "link": link,
                        "filename": filename,  # useful for UI
                    }
                )

            except Exception as e:
                print(f"Error parsing link {link}: {e}")
                continue

        # Sort episodes within each quality
        for season in categorized_links.values():
            for quality_links in season.values():
                # Sort: Torrents last? Or just by episode?
                # Let's try to sort by episode.
                # Helper to make '01' < '02' and handle 'OP' correctly.
                def sort_key(item):
                    ep = item["episode"]
                    # Sort logic:
                    # Digits first (numeric sort)
                    # Then strings (alphabetic)
                    # Torrents might have episode="N/A" -> put at top or bottom?
                    # User request: "Torrents are usually full batches".
                    if item["file_type"] == "Torrent":
                        return (2, str(ep))  # Torrents at bottom?

                    if ep.isdigit():
                        return (0, int(ep))

                    # Handle "01v2"
                    if re.match(r"^\d+v\d+$", ep):
                        main_ep, ver = ep.split("v")
                        return (0, int(main_ep), int(ver))

                    return (1, ep)

                quality_links.sort(key=sort_key)

        return categorized_links
