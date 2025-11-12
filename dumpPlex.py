import json
from plexapi.server import PlexServer

# --- CONFIGURATION ---
PLEX_HOST = "http://localhost:32400"
# !!! REPLACE WITH YOUR ACTUAL PLEX TOKEN !!!
PLEX_TOKEN = ""
OUTPUT_FILE = "plex_media_dump.json"
# ---------------------


def dump_plex_library_to_json():
    """
    Connects to Plex, fetches Movie and TV Show metadata, and dumps it to a JSON file.
    Only includes Movie and TV Show (Series) level data, excluding individual episodes.
    """
    try:
        # 1. Connect to the Plex Server
        print(f"Connecting to Plex at {PLEX_HOST}...")
        plex = PlexServer(PLEX_HOST, PLEX_TOKEN)
        print("Connection successful.")

        all_media_data = {"movies": [], "tv_shows": []}

        # 2. Iterate through all library sections
        for section in plex.library.sections():
            print(f"\nProcessing section: **{section.title}** (Type: {section.type})")

            # --- Handle Movies ---
            if section.type == "movie":
                for movie in section.all():
                    # The `Movie` object represents the film; this is what we want.
                    movie_data = {
                        "type": "movie",
                        "title": movie.title,
                        "year": movie.year,
                        "summary": movie.summary,
                        "rating": movie.rating,
                        "content_rating": movie.contentRating,
                        "studio": movie.studio,
                        "tags_genre": [g.tag for g in movie.genres],
                        "tags_collection": [c.tag for c in movie.collections],
                        # You can add more attributes from the 'movie' object as needed
                    }
                    all_media_data["movies"].append(movie_data)
                print(f"-> Found {len(all_media_data['movies'])} movies.")

            # --- Handle TV Shows (Series Level) ---
            elif section.type == "show":
                for show in section.all():
                    # The `Show` object represents the series itself, not the episodes.
                    # Getting the total number of seasons and episodes can be useful.
                    show_data = {
                        "type": "show",
                        "title": show.title,
                        "year": show.year,
                        "summary": show.summary,
                        "rating": show.rating,
                        "content_rating": show.contentRating,
                        "tags_genre": [g.tag for g in show.genres],
                        "num_seasons": show.leafCount // show.childCount
                        if show.childCount
                        else 0,  # Approximation
                        "total_episodes": show.leafCount,
                        # You can add more attributes from the 'show' object as needed
                    }
                    all_media_data["tv_shows"].append(show_data)
                print(
                    f"-> Found {len(all_media_data['tv_shows'])} TV shows (series level)."
                )

        # 3. Write data to JSON file
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(all_media_data, f, indent=4, ensure_ascii=False)

        print(f"\n✅ Successfully dumped data to **{OUTPUT_FILE}**")

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")
        print(
            "Please ensure your PLEX_TOKEN is correct and the server is running at the specified host."
        )


if __name__ == "__main__":
    dump_plex_library_to_json()
