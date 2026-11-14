# Icons used in the skill badges

- **Source**: [Simple Icons](https://simpleicons.org) v16.37.0 (npm package `simple-icons`), licensed
  **CC0 1.0 Universal** (public domain dedication).
- **Trademark note**: the logos shown belong to their respective owners. They are used only to identify the
  technology that a skill refers to; their use does not imply endorsement.
- **Generic glyphs**: `migrations` ("Schema migrations") and `fetch` ("openapi-fetch") have no brand logo; they are
  original simple shapes drawn for this repository.
- **How they are used**: `scripts/icons.json` holds only the 22 path definitions needed. `scripts/cards.py`
  draws them inside the generated card images in one neutral colour. Nothing is fetched when the page loads.

## Regenerate `icons.json`

1. In a new empty directory, run `npm pack simple-icons@16.37.0` and extract the tarball without running
   anything from it (for example with `python3 -I` and `tarfile.extractall(..., filter="data")`).
2. Run `python3 scripts/fetch_icons.py <extracted package directory>`.
3. Run `python3 scripts/cards.py` and review the generated images.
