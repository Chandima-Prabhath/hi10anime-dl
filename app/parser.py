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
                parts = decoded_link.split('/')
                
                filename = parts[-1].split('?')[0]
                
                season = "Unknown Series"
                quality = "Unknown"
                episode = "N/A"
                file_type = "MKV"

                # Detect if it's a Show or Torrent from path
                if "Shows" in parts:
                    show_index = parts.index("Shows")
                    if len(parts) > show_index + 1:
                        # Directory name usually contains (Group)_Title_(Quality)
                        # e.g., (Hi10)_Aharen_san_Hakarenai_(BD_720p)
                        dir_name = parts[show_index + 1]
                        
                        # Extract Quality from the last parentheses
                        quality_match = re.search(r'\(([^)]+)\)$', dir_name)
                        if quality_match:
                            quality = quality_match.group(1)
                            # Remove the quality part to get the Title/Season
                            # Also remove the leading group tag like (Hi10) if possible, 
                            # but user just asked for organized list, so the directory name minus quality is a good "Season" Key
                            season = dir_name.rsplit('(', 1)[0].strip('_ ').strip()
                        else:
                            season = dir_name
                
                elif "Torrents" in parts:
                    file_type = "Torrent"
                    # For torrents, the filename usually matches the directory structure of shows
                    # e.g. (Hi10)_Aharen_san_wa_Hakarenai_S2_(BD_720p).torrent
                    name_without_ext = filename.rsplit('.', 1)[0]
                    
                    quality_match = re.search(r'\(([^)]+)\)$', name_without_ext)
                    if quality_match:
                        quality = quality_match.group(1)
                        season = name_without_ext.rsplit('(', 1)[0].strip('_ ').strip()
                    else:
                        season = name_without_ext

                # Refine Episode Number from Filename
                # Look for patterns like " - 01 ", " - 01", "_01_", " 01 "
                # Specific check for OP/ED/NCOP/NCED
                
                # Refine Episode Number from Filename
                # Look for patterns like " - 01 ", " - 01", "_01_", " 01 "
                # Specific check for OP/ED/NCOP/NCED
                
                # Check for specials first
                if any(x in filename for x in ["NCOP", "NCED", "OP", "ED"]):
                    # Try to extract the full tag e.g. OP01
                    op_ed_match = re.search(r'[-_ ]((?:NC)?(?:OP|ED)\d{0,2})', filename, re.IGNORECASE)
                    if op_ed_match:
                        episode = op_ed_match.group(1).upper()
                    else:
                        episode = "Extras" 
                else:
                    # Standard episode number matching
                    # Priority 1: Look for explicit dash separator (common in scene releases)
                    # e.g. " - 01", "_-_01", " - 01 "
                    episode_match = re.search(r'[ _]-[ _](\d{2,3}(?:v\d)?)', filename)
                    
                    if not episode_match:
                        # Priority 2: Look for number strictly surrounded by _ or space or brackets
                        # e.g. "_01_", " 01 ", "[01]"
                        # We carefully exclude things like "720p" (followed by p) or "2022" (4 digits)
                        # We use (?<!\d) to ensure we don't match middle of number
                        # We use (?![pP]) to avoid resolution (p)
                        episode_match = re.search(r'(?:^|[ _\[\(-])(\d{2,3}(?:v\d)?)(?:[ _\]\)-]|$)(?![pP])', filename)
                    
                    if episode_match:
                        episode = episode_match.group(1)
                    else:
                        pass

                # Clean up extracted Season Name (remove leading (Hi10) if present for cleaner UI?)
                # user didn't explicitly ask to remove (Hi10) but "organized list" implies cleanliness.
                # Let's clean it up slightly if it starts with (Hi10)
                if season.startswith("(Hi10)"):
                    season = season.replace("(Hi10)", "").strip("_ ")
                
                # Build nested dictionary
                if season not in categorized_links:
                    categorized_links[season] = {}
                if quality not in categorized_links[season]:
                    categorized_links[season][quality] = []

                categorized_links[season][quality].append({
                    "episode": episode,
                    "file_type": file_type,
                    "link": link,
                    "filename": filename # useful for UI
                })

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
                    if item['file_type'] == 'Torrent':
                        return (2, str(ep)) # Torrents at bottom?
                    
                    if ep.isdigit():
                        return (0, int(ep))
                    
                    # Handle "01v2"
                    if re.match(r'^\d+v\d+$', ep):
                         main_ep, ver = ep.split('v')
                         return (0, int(main_ep), int(ver))
                    
                    return (1, ep)

                quality_links.sort(key=sort_key)

        return categorized_links