---
name: publish-finding
description: Publishes one completed finding to the Notion Findings Tracker database and creates a Notion page for it. Updates existing entries instead of creating duplicates.
---

When given a completed finding with: number, title, key statistic,
3-sentence interpretation, and priority (Alta/Media/Baja):

Use the Notion MCP to:

1. **Check if the entry already exists** — search the "Findings Tracker" database for a page
   whose Título matches the finding title exactly.

2a. **If it exists** — update the existing page:
    - Update the database entry fields: Estadística Clave, Alcance, Prioridad, Publicado
    - Replace the page body content with the new interpretation, callout, and Próximos pasos

2b. **If it does not exist** — create a new entry:
    - Create a new entry in the "Findings Tracker" database with fields:
      Título, Estadística Clave, Alcance (country or full sample), Prioridad, Publicado = true
    - Create a Notion page linked to that entry containing:
      - The key statistic in a callout block at the top
      - The 3-sentence interpretation as the page body
      - A "Próximos pasos" section with the programme recommendation

3. Confirm the Notion URL of the created or updated page.

Never create a duplicate entry. If in doubt, search first.
