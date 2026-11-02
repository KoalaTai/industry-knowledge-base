# Your own notes

Drop any Markdown file in this folder (for example `ancient_metallurgy.md`,
`week3_roman_engineering.md`) and run `python minecraft/generate.py` again.
Each file becomes an in-game function, `/function ac:notes/<file_name>`,
that prints the note to your chat, and it is listed by `/function ac:index`.

`#` headings are shown in yellow, everything else in white, wrapped at 90
characters. Keep lines short; Minecraft chat shows about 100 lines of
history.

If a note belongs with one of the technology records, add it to
`knowledge/premodern_technology.json` instead (a new record or a new
`sources` entry) so it also appears in the catalogue and in the chat text of
the matching `/function ac:tech/<model>`.

This README is skipped by the generator.
