import os
import sys
import logging
from datetime import datetime, timedelta
from plexapi.server import PlexServer

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

# --- Config (env-friendly) ---
BASEURL = os.getenv('PLEX_BASEURL', '[URL here]')  # must include http:// or https://
TOKEN = os.getenv('PLEX_TOKEN', '[Token Here]')  # long-lived X-Plex-Token (no 2FA required)
LABEL_48H = os.getenv('LABEL_48H', 'HOTFOR48H')
LABEL_1MO = os.getenv('LABEL_1MO', 'ADDED1MONTHAGO')

# Dates for addedAt edits (local time format Plex accepts)
ADDED_IN_48H = (datetime.now() + timedelta(hours=48)).strftime("%Y-%m-%d %H:%M:%S")
ADDED_1MO_AGO = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d %H:%M:%S")


def connect_to_plex(baseurl: str, token: str) -> PlexServer:
    if not token:
        logging.error("Missing PLEX_TOKEN. Set a long-lived token in your environment and rerun.")
        sys.exit(1)

    if not (baseurl.startswith("http://") or baseurl.startswith("https://")):
        baseurl = "http://" + baseurl  # minimal safety net
        logging.warning(f"BASEURL missing scheme. Using: {baseurl}")

    try:
        plex = PlexServer(baseurl, token)
        # Fail early if URL/token is wrong
        _ = plex.library.sections()
        logging.info(f"Connected to Plex at {baseurl}.")
        return plex
    except Exception as e:
        logging.error(f"Failed to connect to Plex at {baseurl}: {e}")
        sys.exit(1)


def update_items_with_label(library, label: str, new_added_at: str):
    """Finds items by label, sets addedAt, then removes the label."""
    try:
        items = library.search(label=label)
    except Exception as e:
        logging.error(f"[{library.title}] Search failed for label '{label}': {e}")
        return

    if not items:
        logging.info(f"[{library.title}] No items with label '{label}'.")
        return

    updates = {"addedAt.value": new_added_at}

    for item in items:
        try:
            item.edit(**updates)
            item.reload()  # reflect server-side changes in this object
            logging.info(f"[{library.title}] Updated '{item.title}' -> {updates}")

            item.removeLabel(label)
            logging.info(f"[{library.title}] Removed label '{label}' from '{item.title}'")
        except Exception as e:
            logging.error(f"[{library.title}] Failed on '{item.title}': {e}")


def main():
    plex = connect_to_plex(BASEURL, TOKEN)

    for section in plex.library.sections():
        # Skip non-video libraries (music/photos)
        if getattr(section, "type", None) not in {"movie", "show"}:
            continue

        update_items_with_label(section, LABEL_48H, ADDED_IN_48H)
        update_items_with_label(section, LABEL_1MO, ADDED_1MO_AGO)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.info("Interrupted by user.")
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        sys.exit(1)
