import re
from typing import Set, Dict

class LinkParser:
    @staticmethod
    def parse(links: Set[str]) -> Dict[str, Dict[str, list]]:
        categorized_links = {}

        for link in links:
            # Extract filename from the URL
            try:
                filename = link.split('/')[-1].split('?')[0]
            except IndexError:
                continue

            # Default values
            season = "Season 1"
            quality = "Unknown"
            episode = "N/A"
            file_type = "MKV"

            # Improved regex to find season/part information
            season_match = re.search(r'\[(.*?)\]', filename)
            if season_match:
                season_text = season_match.group(1)
                # More robust season detection
                if "season" in season_text.lower() or re.match(r'S\d+', season_text):
                    season = season_text
                elif re.search(r'II|III|IV|V', season_text): # Roman numerals for seasons
                    season = f"Season {season_text.count('I') + season_text.count('V')*4}"
                # Add other keywords that could indicate a new season or part
                elif any(s in season_text for s in ["Part", "Cour", "Book"]):
                    season = season_text


            # Regex to find quality
            quality_match = re.search(r'(\d{3,4}p)', filename)
            if quality_match:
                quality = quality_match.group(1)
            elif "BD" in filename:
                quality = "BD"

            # Regex for episode number
            episode_match = re.search(r' (\d{2,3}) ', filename)
            if episode_match:
                episode = episode_match.group(1)
            elif "NCOP" in filename:
                episode = "NCOP"
            elif "NCED" in filename:
                episode = "NCED"


            # Determine file type
            if ".torrent" in filename:
                file_type = "Torrent"

            # Build nested dictionary
            if season not in categorized_links:
                categorized_links[season] = {}
            if quality not in categorized_links[season]:
                categorized_links[season][quality] = []

            categorized_links[season][quality].append({
                "episode": episode,
                "file_type": file_type,
                "link": link
            })

        # Sort episodes within each quality
        for season in categorized_links.values():
            for quality_links in season.values():
                quality_links.sort(key=lambda x: x["episode"])

        return categorized_links