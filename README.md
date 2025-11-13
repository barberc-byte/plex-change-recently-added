### 📄 Script: `plex-change-recently-added`

### 🔍 What This Script Does

* Connects to Plex using a long-lived **X-Plex-Token**
* Scans all movie and TV show libraries
* Finds items with the labels:

  * `HOTFOR48H`
  * `ADDED1MONTHAGO`
* Updates their `addedAt` timestamp to:

  * **+48 hours** (pushes item to the top of "Recently Added")
  * **−30 days** (pushes item down the list)
  * (You can change these in the script)
* Removes the label after applying the change
* Does not touch music or photos

This makes it a completely non-destructive way to re-sort Plex without modifying any media files.

---

### 🛠 Requirements

* Python 3.8+
* `plexapi`

Install with:

```bash
pip install plexapi
```

You’ll also need a **long-lived Plex token**, which you can find how to do do [here](https://support.plex.tv/articles/204059436-finding-an-authentication-token-x-plex-token/)


### 🚀 Running the Script

```bash
python update_addedAt.py
```

You’ll see a clean log output showing:

* which items were found
* what their new timestamps are
* which labels were removed
* any errors (bad token, wrong URL, etc.)

---

### 🏷 Triggering Updates with Labels

To mark an item for update:

1. Open the movie/episode in Plex
2. Add the label:

   * `HOTFOR48H` → sets addedAt 48 hours in the future
   * `ADDED1MONTHAGO` → sets addedAt 30 days in the past

Run the script when you're ready, and it will process everything at once.

---

### 📌 Useful For

* Rebuilding Recently Added after migrating your libraries
* Fixing items Plex added out of order
* Pushing a show to the top without touching files
* Making older episodes “disappear” from the front page
* Metadata cleanup during reorganizations
