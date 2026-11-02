# Controlling a live Minecraft Java Edition game from Claude / Claude Code (macOS, 26.x releases)

Research date: 2026-11-02. User context: Java Edition on macOS, singleplayer Creative world "Animus" with cheats on, currently on the 2026 year-versioned line ("Minecraft 26.3"). Goal: replace AppleScript keystroke-typing of chat commands with a programmatic control channel, ideally one Claude Code can call as an MCP tool.

## Version context: what "26.3" is and why it matters for every tool below

### Takeaway
Mojang switched Java Edition to year.drop.hotfix numbering in 2026: 1.21.11 was followed directly by 26.1 (March 2026), then 26.2 (June) and 26.3 (September). Almost every community bot/MCP project still advertises "1.21.x" support, so "last updated before March 2026" means "predates the entire 26.x line" and must be treated as unverified for the user's game.

### Cited Findings
- Java versions since 26.1 follow year.drop.hotfix; the game went from 1.21.11 straight to 26.1, so there is no 1.22 — [packsmc.com](https://packsmc.com/articles/minecraft-version-numbering-explained); [mc-node.net](https://mc-node.net/blog/en/minecraft-versions-2026-explained/)
- Release dates reported: 26.1 "Tiny Takeover" 24 March 2026, 26.2 "Chaos Cubed" 16 June 2026, 26.3 "Wilderness Bound" 15 September 2026; a 26.4-snapshot-3 existed by 6 October 2026 — [minecrafthub.io](https://minecrafthub.io/articles/minecraft-version-history); [crafty.gg](https://crafty.gg/articles/minecraft-26-update)
- Network protocol numbers: 26.1 = 775, 26.2 = 776, 26.3 = 777 — [VitaminMCP issue #4](https://github.com/Backas03/VitaminMCP/issues/4)
- 26.1 and later require Java 25 (PaperMC requirements table) — [PaperMC getting started](https://docs.papermc.io/paper/getting-started/)
- Fabric lists 26.3 as stable (Fabric Loader 0.19.5+ tested); NeoForge 26.3 builds exist but are all labelled beta (e.g. 26.3.0.48-beta) — [minecrafthub.io](https://minecrafthub.io/articles/minecraft-26-3-mods-shaders-packs)
- Caveat: version-naming/date sources are fan blogs and hosting-provider wikis rather than Mojang announcements — [gameserverkings.com](https://www.gameserverkings.com/knowledge-base/minecraft/updating-your-server-version/)

### Inferences
- Any project whose README says "supports up to 1.21.11" has not been validated on 26.x; protocol 775/776/777 are all different from 1.21.11, so bot-style (fake-player) tools will refuse to connect unless explicitly updated.
- Command-based tools (RCON, server console) are far less version-sensitive because the RCON wire protocol has not changed; only the command syntax inside the payload evolves.

### Gaps
- I did not find the official Mojang changelog page confirming the exact 26.3 release date; dates above are from secondary sources that agree with each other.

## Key Question 1: RCON — enabling it for a singleplayer world, libraries, limits, and feedback

### Takeaway
RCON is a dedicated-server feature (`server.properties`), and no current mod adds RCON to the singleplayer client; the practical route is running a local dedicated server (Paper/Fabric/vanilla 26.3, Java 25 via Homebrew) that hosts a copy of Animus. RCON does return command output in the response payload, but many commands return nothing (and failures often return empty strings), outbound commands are capped at ~1446 bytes, and long responses are fragmented into 4096-byte packets with no fully reliable end-of-response marker.

### Cited Findings
**Enabling and protocol facts**
- RCON is Java Edition only. Enable via `server.properties`: `enable-rcon=true`, `rcon.password=...`, `rcon.port=...` (default 25575), `broadcast-rcon-to-ops=false` — [Minecraft Wiki: RCON](https://minecraft.wiki/w/RCON)
- Packet layout: int32 length, request ID, type (3 = login, 2 = command, 0 = response), null-terminated payload, null pad; integers are little-endian (unlike the game protocol) — [Minecraft Wiki: RCON](https://minecraft.wiki/w/RCON)
- Client-to-server payload max is listed as 1446 bytes (1460 total packet), flagged on the wiki as "possibly outdated"; server-to-client payload max is 4096 bytes (4110 total) — [Minecraft Wiki: RCON](https://minecraft.wiki/w/RCON); [wiki.vg RCON mirror](https://c4k3.github.io/wiki.vg/RCON.html)
- Command output IS returned in the response payload, "but many commands return nothing", and the protocol cannot reliably tell when a command is unknown — [Minecraft Wiki: RCON](https://minecraft.wiki/w/RCON)
- Long output is split into packets of up to 4096 bytes; there is no fully reliable last-packet marker. Documented workarounds: treat a <4096 payload as last (unreliable), wait a fixed time, or send a second dummy packet (e.g. type 200) and read until the server replies "Unknown request c8" — [Minecraft Wiki: RCON](https://minecraft.wiki/w/RCON)
- RCON is unencrypted and must never be exposed beyond localhost; the password grants full console access — [Minecraft Wiki: RCON](https://minecraft.wiki/w/RCON); [xgamingserver RCON guide](https://xgamingserver.com/docs/minecraft/setup-rcon)
- Server responses may contain legacy color codes (0xA7); clients may need ISO-8859-1 decoding or to strip them — [Minecraft Wiki: RCON](https://minecraft.wiki/w/RCON)
- Practitioner gotcha from a Claude-Code-over-RCON project: "Failed commands often return empty strings over RCON"; the recommended pattern is to verify with `execute if entity ...` rather than parse error text — [adrianwedd/clawdcraft](https://github.com/adrianwedd/clawdcraft)
- A build-automation project had to keep each generated command below the 1446-byte RCON limit because oversize commands stopped the game — [Larspolo/aoe2mc PR #1662](https://github.com/Larspolo/aoe2mc/pull/1662)
- mciwb (RCON-driven Python world builder) merged a change to "handle RCON size-limit errors in its survey script" — [gilesknap/mciwb PR #162](https://github.com/gilesknap/mciwb/pull/162)

**Singleplayer / Open to LAN**
- Open to LAN picks a random port by default; since 22w45a (1.19.3) the port can be chosen in the LAN screen or via `/publish [<allowCommands>] [<gamemode>] [<port>]`; chat reports "Local game hosted on port NNNN". The wiki does not mention RCON or server.properties applying to LAN worlds at all — [Minecraft Wiki: Setting up a LAN world](https://minecraft.wiki/w/Tutorial:Setting_up_a_LAN_world)
- Searches for a singleplayer/client-side RCON mod found none. The closest items: "Rcon Output Newline" (only reformats RCON output, 1.18.1-1.20.4), ConsoleMC (chat-to-console, 1.17.1-1.21.5), and LCon, a client-only WebSocket command server (see KQ4), none of which add true RCON to the client — [Modrinth: Rcon Output Newline](https://modrinth.com/mod/rconoutputnewline); [Modrinth: ConsoleMC](https://modrinth.com/mod/consolemc); [Modrinth: LCon](https://modrinth.com/mod/lcon-local-console-access)
- CraftControl RCON (Fabric) is server-side only and "does nothing on the client" — [CurseForge: CraftControl RCON](https://www.curseforge.com/minecraft/mc-mods/craftcontrol-rcon)
- A Fabric server image documents the standard route: set `enable-rcon=true`, connect with any RCON client on 25575 — [Docker Hub xblaxk/minecraft_fabric](https://hub.docker.com/r/xblaxk/minecraft_fabric)

**Local dedicated server on macOS**
- Paper requires at least Java 25 for 26.1+; official docs recommend `brew install openjdk@25` on macOS and warn against headless JDK variants — [PaperMC getting started](https://docs.papermc.io/paper/getting-started/); [PaperMC Java install](https://docs.papermc.io/misc/java-install/)
- A third-party tracker listed Paper 26.3 build 237 published 1 Nov 2026 (unverified against the official downloads page) — [mcreference.com](https://mcreference.com/server-software/paper)
- Upgrade caveat: switch to Java 25 before first start on 26.3 or the server stops immediately — [space-node.net](https://space-node.net/blog/minecraft-26-3-server-update-guide-2026)

**Libraries**
- Python `mcrcon` (PyPI): latest 0.7.0, July 30 2021; Snyk rates it inactive — [libraries.io mcrcon](https://libraries.io/pypi/mcrcon); [Snyk mcrcon](https://snyk.io/advisor/python/mcrcon)
- Python `rconx` (PyPI): version 0.3.0 published 21 Oct 2026 with GitHub-Actions attestation; generic Source-RCON packet library — [PyPI rconx](https://pypi.org/project/rconx/)
- Python `mctools` (Minecraft-Connection-Tools 1.4.1, Sep 2025): enforces the 1446-byte outbound limit (can be disabled, with warnings) and handles inbound fragmentation by sending a junk packet and reading until the server echoes it — [mctools RCON docs](https://mctools.readthedocs.io/en/master/rcon.html)
- Python `mcipc` is the RCON client used by mciwb — [gilesknap/mciwb](https://github.com/gilesknap/mciwb)
- Async Python options: `py-aio-mcrcon` ("support for fragmented responses"), aio-mc-rcon, async-mcrcon — [libraries.io py-aio-mcrcon](https://libraries.io/pypi/py-aio-mcrcon); [wiki.vg RCON](https://c4k3.github.io/wiki.vg/RCON.html)
- Node `rcon-client` (npm): latest 4.2.5, 4 Sep 2024; libraries.io warns it "has not been maintained for a while", Snyk rates it inactive — [npm rcon-client](https://www.npmjs.com/package/rcon-client); [libraries.io rcon-client](https://libraries.io/npm/rcon-client)
- Faneraiy14/minecraft-rcon-mcp implements the RCON protocol directly in Node with no dependency — [Faneraiy14/minecraft-rcon-mcp](https://github.com/Faneraiy14/minecraft-rcon-mcp)
- CLI: Tiiffi/mcrcon (C) is the classic command-line client — [Tiiffi/mcrcon releases](https://github.com/Tiiffi/mcrcon/releases)

### Inferences
- The RCON wire protocol is frozen (unchanged since Source RCON), so a 2021 `mcrcon` still works against a 26.3 server; the "inactive" ratings matter for packaging hygiene, not compatibility. For new code, `rconx` (Oct 2026) or `mctools` (handles both limits) are safer picks.
- Because singleplayer cannot run RCON and a world folder cannot be safely opened by the client and a dedicated server at the same time, the realistic workflow is: copy `saves/Animus` into the server's `world/` folder, let Claude build there over RCON, then copy it back (or just play on the local server by connecting to `localhost`). The world-import mechanics are covered by the sibling research notes in this folder.
- The 1446-byte limit means large builds must be chunked into many `/fill`, `/setblock`, `/clone` commands (or a datapack `/function`), not one giant command. A bridge should also always pair state-changing commands with an `execute if block`/`execute if entity` probe because empty responses are ambiguous.
- Running Paper (vs vanilla) costs nothing for singleplayer use and gives plugin options later; vanilla 26.3 `server.jar` works equally for RCON.

### Gaps
- I did not find a mod, for any 26.x loader, that adds RCON to the singleplayer integrated server. Treat "RCON on singleplayer" as not available.
- Exact vanilla `/fill` block-count cap per command on 26.3 was not retrieved in this research; the historical limit is 32,768 blocks, but I did not fetch a 26.x source confirming it is unchanged.
- The wiki itself flags the 1446-byte figure as possibly outdated; no 2026 measurement was found.

## Key Question 2: MCP servers for Minecraft (what exists, what they expose, maintenance, version support)

### Takeaway
There are three families: (a) Mineflayer "fake player" MCP servers (rich tools: move, place/dig blocks, chat, inventory, some with top-down screenshots) but gated by Mineflayer's protocol support, which stops at 26.1 as of mid-October 2026; (b) RCON MCP servers (run any command; thin, version-agnostic, need a dedicated server); (c) mod/plugin-backed world-API MCP servers (MairwunNx minecraft-mcp + WorldAPI, VitaminMCP) and Bedrock WebSocket ones (irrelevant for Java). Nothing official from Anthropic exists.

### Cited Findings
**Mineflayer-based (fake player joins the game)**
- yuniko-software/minecraft-mcp-server: the reference project; tools include get-position, move-to-position, look-at, jump, fly-to, list-inventory, equip-item, place-block, dig-block, get-block-info, find-blocks, smelt-item, find-entity, send-chat, read-chat, detect-gamemode; README says "Currently supports Minecraft version 1.21.11" and newer versions may not work; default setup is a singleplayer world opened to LAN on localhost:25565; run via `npx -y github:yuniko-software/minecraft-mcp-server --host --port --username`; Node 20.10+ — [yuniko-software/minecraft-mcp-server](https://github.com/yuniko-software/minecraft-mcp-server). Search metadata showed it last updated ~587 days before the search (i.e. roughly early 2025), predating the 26.x line.
- Forks of yuniko: KRIShark (remote HTTP transport, 73 tools), MrMirhan (Docker + Pterodactyl egg, connect-to-server at runtime), Trycky64 (npx, 1.21.11), AR2100 (adds collect-blocks), monkeorg/cavecrew-mcp — [KRIShark](https://github.com/KRIShark/minecraft-mcp-server); [MrMirhan](https://github.com/MrMirhan/minecraft-mcp-server); [AR2100](https://github.com/AR2100/minecraft-mcp-server)
- CDX-1/minecraft-client-mcp: ~20 tools including `minecraft_chat` (chat, whispers, slash commands), `minecraft_move` (A* pathfinding), `minecraft_look`, `minecraft_block` (inspect/activate/dig/place), `minecraft_attack`, inventory/containers, world snapshots, nearby block/entity queries, events, `minecraft_capture` (top-down PNG of nearby terrain), and a local dashboard on 127.0.0.1:3210; supports 26.1/26.1.1/26.1.2 and explicitly says 26.2 is not supported because "the current Mineflayer stack lacks complete 26.2 game data"; Node 22+; MIT; install into Claude Code with `claude mcp add minecraft --scope user -- npx -y github:CDX-1/minecraft-client-mcp` — [CDX-1/minecraft-client-mcp](https://github.com/CDX-1/minecraft-client-mcp)
- Backas03/VitaminMCP (v3.2.1): agent side "supports Minecraft 26.2 and 26.3, checked by hand on Paper 26.2-134 and 26.3-200" (loads, captures events/logs, answers state queries, runs commands) but "bots cannot join either yet" because its bundled Mineflayer runner only speaks protocol 775 — [VitaminMCP issue #4](https://github.com/Backas03/VitaminMCP/issues/4)

**RCON-based (console commands only)**
- Faneraiy14/minecraft-rcon-mcp (Node, zero-dependency RCON): list players, broadcast, teleport, weather/time, raw command; Docker setup; added to Claude Code with a single `claude mcp add` using host/port/password env vars; note that launching several MCP servers can hit Claude Code's 30-second startup timeout — [Faneraiy14/minecraft-rcon-mcp](https://github.com/Faneraiy14/minecraft-rcon-mcp)
- MinecraftCodeFoundary/Minecraft-MCP-Server: RCON command execution with automatic reconnection plus log tailing; configured via RCON host/port/password env vars — [MinecraftCodeFoundary/Minecraft-MCP-Server](https://github.com/MinecraftCodeFoundary/Minecraft-MCP-Server)
- Peterson047/Minecraft-MCP-Server: Python FastMCP server executing commands over RCON; works with Claude Desktop; server must be started before the client — [Peterson047/Minecraft-MCP-Server](https://github.com/Peterson047/Minecraft-MCP-Server)
- mjmorales/rcon-mcp-server (Go, generic Source RCON) and deemkeen/minecraft-rcon-mcp (Java/Spring AI) also exist — [mjmorales/rcon-mcp-server](https://github.com/mjmorales/rcon-mcp-server); [GitHub rcon topic](https://github.com/topics/rcon?l=java)
- A `rgbkrk/minecraft-rcon` listing shows 0 documented tools; a lobehub "minecraft-rcon-mcp" listing uses placeholder URLs — treat both as unfinished — [mcp-use listing](https://mcp-use.com/servers/rgbkrk-minecraft-rcon); [lobehub listing](https://lobehub.com/mcp/your_username-minecraft-rcon-mcp)

**World-API / plugin-backed**
- MairwunNx/minecraft-mcp (`@mairwunnx/minecraft-mcp` on npm): 51 tools covering server status, worlds, blocks, chests, entities, players, commands, leaderboards, recipes, configs, logs and Java scripts; viewer token exposes 19 read-only tools; features include undo for builds, live event alerts, chat relay to Discord/Slack/etc.; talks to the companion WorldAPI (REST + WebSocket) which "runs on Paper, Fabric, or NeoForge servers, and in singleplayer with the WorldAPI mod installed"; requires WorldAPI 4.2.0+; token created in-game via `/worldapi token create agent`; Claude Desktop install via `.mcpb` bundle; Claude Code via `claude mcp add minecraft -- npx -y @mairwunnx/minecraft-mcp` (URL/token optional for singleplayer) — [MairwunNx/minecraft-mcp](https://github.com/MairwunNx/minecraft-mcp)
- simonerecchia/minecraft-schematic-lab: MCP server for building, previewing and exporting WorldEdit Sponge `.schem` files (offline, no live game) — [minecraft-schematic-lab](https://github.com/simonerecchia/minecraft-schematic-lab)

**Bedrock WebSocket (not applicable to Java)**
- rice-awa/mc-mcp-server (Python, Bedrock `/wsserver`, archived) and Mming-Lab/minecraft-bedrock-education-mcp (TypeScript, needs Minecraft Education 1.26+) are the Bedrock MCP servers; Sandertv/mcwss, p0t4t0sandwich/minecraft-be-websocket-api, mcbe-ws-sdk are non-MCP WebSocket libraries; all rely on Bedrock's `/connect`/`/wsserver` command which requires cheats — [rice-awa/mc-mcp-server](https://github.com/rice-awa/mc-mcp-server); [Mming-Lab](https://github.com/Mming-Lab/minecraft-bedrock-education-mcp); [Sandertv/mcwss](https://github.com/Sandertv/mcwss)

**Claude-Code-specific glue (not MCP, but relevant)**
- adrianwedd/clawdcraft: Claude Code lives in a tmux session; a Node bridge tails `logs/latest.log` of a Paper server for chat lines, forwards them with `tmux send-keys`, and Claude acts via RCON scripts (`say.js`, `rcon.js`, `gift.js`, `memory.js` are the only pre-approved scripts); repo contains `UPGRADE-26x.md`; MIT — [adrianwedd/clawdcraft](https://github.com/adrianwedd/clawdcraft)
- lightningreflex/mcclaude: lets Claude read the console, run commands, and edit plugin files in real time — [lightningreflex/mcclaude](https://github.com/lightningreflex/mcclaude)
- gilesknap/mciwb: Python RCON world builder (via `mcipc`) with `.claude/skills/minecraft-build` and a CLAUDE.md; quick start uses a Minecraft 26.3 server in podman; skill walks an agent through survey-build-inspect-iterate; Apache-2.0 — [gilesknap/mciwb](https://github.com/gilesknap/mciwb); [mciwb PR #162](https://github.com/gilesknap/mciwb/pull/162)

### Inferences
- For a 26.3 game today, only the RCON family and the WorldAPI/VitaminMCP "server-side" family can actually talk to the game; every Mineflayer MCP server (yuniko and forks, CDX-1) is capped at 26.1 until PrismarineJS ships 776/777 support.
- CDX-1/minecraft-client-mcp is the best-maintained Mineflayer MCP option (26.1, Node 22, screenshots, explicit Claude Code install line); yuniko's original is effectively frozen at 1.21.11.
- MairwunNx/minecraft-mcp is the richest tool surface (51 tools, undo, logs) and is the only one claiming singleplayer support via a client mod, but its 26.x status is unverified (see Gaps).
- RCON MCP servers are near-interchangeable; pick on transport/language preference. A ~50-line custom FastMCP/`rconx` server is equally viable and avoids trusting a stranger's RCON password handling.

### Gaps
- Could not fetch the WorldAPI repository (404 at github.com/MairwunNx/WorldAPI and "Project not found" on modrinth.com/mod/worldapi), so WorldAPI's supported game versions, whether it has a 26.3 build, and the singleplayer mod's loader are unverified. The minecraft-mcp wiki/CHANGELOG should be checked before relying on it.
- GitHub README fetches do not expose last-commit dates; maintenance assessments above rely on README version claims and search metadata, not commit timestamps.
- No Anthropic-published Minecraft MCP server or official integration was found.

## Key Question 3: Bot/agent frameworks (Mineflayer, Baritone, Mindcraft, Voyager/MineDojo) and bulk block placement

### Takeaway
Mineflayer (the foundation for nearly all Node bots, Mindcraft, and most MCP servers) supports 1.8 through 26.1 (v4.39.0) but NOT 26.2/26.3 as of 18 Oct 2026, with upstream PRs still open. Baritone has official 26.1 and 26.2 releases (client mod for pathing, not an external API). Mindcraft is Mineflayer-bound (1.21.11) and Voyager/MineDojo are dormant research code. Only command channels (RCON/WorldAPI) place blocks at scale; Mineflayer/Baritone/Mindcraft place blocks one at a time as a player (unless the bot is opped and sends `/fill` via chat).

### Cited Findings
**Mineflayer / node-minecraft-protocol**
- Mineflayer docs list support for 1.8 through 26.1 — [Mineflayer site](http://prismarinejs.github.io/mineflayer/)
- As of 2026-10-17: mineflayer 4.39.0, minecraft-protocol 1.68.0, minecraft-data 3.117.0 do not support 26.2 or 26.3; minecraft-data lists 776/777 in its version table only, with no data; open PRs: minecraft-data #1219, node-minecraft-protocol #1496, mineflayer #3926/#4121 (26.2); minecraft-data #1301 (stacked on #1300) and mineflayer #4146 (26.3) — [VitaminMCP issue #4](https://github.com/Backas03/VitaminMCP/issues/4)
- mineflayer PR #4146 (26.3) opened 21 Sep 2026, still open as of 18 Oct 2026; a maintainer-side comment states "mineflayer does not support 26.3, neither does it support 26.2"; blocked on minecraft-data #1301; related PR #4130 (teleport_confirm for 26.3) also open — [mineflayer PR #4146](https://github.com/PrismarineJS/mineflayer/pull/4146)
- An unofficial community package `node-minecraft-protocol-26.2` (Complexity-ML) implements protocol 776 outside PrismarineJS — [Complexity-ML repo](https://github.com/Complexity-ML/node-minecraft-protocol-26.2)
- Documented workaround: install ViaVersion + ViaBackwards (5.12.0+ for 26.3) on a 26.2/26.3 server so a 26.1-protocol bot can join; the bot then sees 26.2/26.3 blocks/items as substitutes; a 14-step and a 5-step scenario passed in the experiment — [VitaminMCP issue #4](https://github.com/Backas03/VitaminMCP/issues/4)
- Earlier (April 2026) mineflayer issue #3893 reported 26.1.2 "unsupported protocol version", resolved by 4.39.0 — [mineflayer issue #3893](https://github.com/PrismarineJS/mineflayer/issues/3893)

**Baritone**
- Official cabaletta/baritone releases: v1.18.0 for 26.1 and v1.19.0 for 26.2, both with Fabric; the build dependency is unpinned — [cabaletta/baritone releases](https://github.com/cabaletta/baritone/releases); [baritone issue #5059](https://github.com/cabaletta/baritone/issues/5059)
- Community ports: XMRhapsody0807/NewBaritone (26.1 Fabric), dysnasia/baritone-26.2 (WIP, needs Fabric API), NullVoidDev/baritone-26.2 (beta), a "Baritone Bot" CurseForge jar for 26.2 uploaded 5 Oct 2026; aggregator baritonemc.net lists 26.1/26.2/26.3 jars — [NewBaritone](https://github.com/XMRhapsody0807/NewBaritone); [dysnasia release](https://github.com/dysnasia/baritone-26.3/releases/tag/26.2); [CurseForge Baritone Bot](https://www.curseforge.com/minecraft/mc-mods/baritone-bot/files/9065370); [baritonemc.net](https://baritonemc.net/download/)

**Mindcraft**
- mindcraft-bots/mindcraft: "supports Minecraft Java Edition up to v1.21.11, recommend v1.21.6"; connects to a LAN world (localhost:55916) or online server (Microsoft auth required); Anthropic supported via `ANTHROPIC_API_KEY` alongside OpenAI, Gemini, xAI, DeepSeek, Ollama, OpenRouter, etc.; suggests viaproxy for unsupported versions; Node 18/20 LTS recommended, v24+ "may cause issues with native dependencies"; LLM code-writing disabled by default (`allow_insecure_coding`), with warnings that the sandbox is still injection-vulnerable and Docker is strongly recommended; ~6.0k stars, 1,673 commits; 2025 arXiv paper — [mindcraft-bots/mindcraft](https://github.com/mindcraft-bots/mindcraft)
- mindcraft-ce fork: stable/develop/agent-system branches; agent-system adds function calling, RAG and tool prompting; routes through an OpenAI-compatible "Andy API" gateway — [mindcraft-ce](https://github.com/mindcraft-ce/mindcraft-ce)
- A third-party README copy notes the maintainers "are not very responsive to GitHub issues" — [Puzzlepart ACDC-26 copy](https://github.com/Puzzlepart/ACDC-26/blob/main/mindcraft/README.md)

**Voyager / MineDojo**
- MineDojo org page lists the Voyager repo as "Updated Apr 3, 2024" and MineDojo itself as last updated Mar 18, 2024; the newer MineDojo repo NitroGen shows Jan 25, 2026 — [MineDojo on GitHub](https://github.com/MineDojo)
- Voyager paper (arXiv 2305.16291, 2023), MIT-licensed; a 2026 write-up notes the code targets Azure OpenAI endpoints; aggregator "updated 1 month ago / Sept 2026" claims could not be verified — [arXiv](https://arxiv.org/abs/2305.16291); [starlog.is](https://starlog.is/articles/ai-agents/minedojo-voyager)

**Anthropic-related**
- No official Anthropic Minecraft agent or MCP server surfaced. Claude appears only as a supported provider (Mindcraft) or as the driver of community projects (clawdcraft, mcclaude, mciwb skill) — [mindcraft](https://github.com/mindcraft-bots/mindcraft); [clawdcraft](https://github.com/adrianwedd/clawdcraft)

**Block placement at scale**
- Mineflayer MCP tools expose per-block `place-block`/`dig-block` (yuniko) and `minecraft_block` place/dig against a reference block (CDX-1) — [yuniko README](https://github.com/yuniko-software/minecraft-mcp-server); [CDX-1 README](https://github.com/CDX-1/minecraft-client-mcp)
- Mineflayer-style chat tools can also send slash commands (CDX-1 `minecraft_chat` handles "chat, whispers, and slash commands") — [CDX-1 README](https://github.com/CDX-1/minecraft-client-mcp)
- mciwb builds castles/pagodas/villages via `world.set_block` and shape helpers over RCON — [gilesknap/mciwb](https://github.com/gilesknap/mciwb)
- MairwunNx/minecraft-mcp has block tools and "undo for builds" via WorldAPI — [MairwunNx/minecraft-mcp](https://github.com/MairwunNx/minecraft-mcp)

### Inferences
- For the user's 26.3 Animus world, no Mineflayer-based framework can join natively today. The only ways to use them are (a) run a 26.1 copy of the world, or (b) run a 26.3 server with ViaVersion+ViaBackwards and pin the bot to protocol 775 — workable but the bot's world model is lossy for 26.2/26.3 content.
- "Acts as a player" frameworks (Mineflayer, Baritone, Mindcraft, Voyager) are the wrong tool for "Claude builds things"; they are built for survival-style embodied play. Bulk construction belongs to `/fill`/`/setblock`/`/clone`/structure blocks via RCON, or WorldEdit-style APIs, where a single command moves thousands of blocks.
- Baritone is a client-side pathing mod with an in-game command/API surface; it has no external network endpoint and is only useful to Claude indirectly (e.g., `#goto` typed via a chat bridge).

### Gaps
- Whether PrismarineJS has shipped 26.2/26.3 support between 18 Oct and 2 Nov 2026 was not re-checked against npm; the latest confirmed state is "open PRs, unsupported".
- Baritone 26.3: only an aggregator (baritonemc.net) lists a 26.3 jar; no official cabaletta 26.3 release was confirmed.

## Key Question 4: Fabric/Forge/NeoForge mods exposing HTTP/WebSocket APIs or local command endpoints

### Takeaway
A handful of mods expose command endpoints, but the only ones with any sign of 26.x life are WorldAPI (REST+WS, Paper/Fabric/NeoForge + a singleplayer client mod, status unverified) and the HTTP-Request-Mod (server-side Fabric, 1.21.10, chat-to-coding-agent bridge). The one client-side, singleplayer-capable command WebSocket mod (LCon) is Forge-only for 1.19.2/1.20.1 and two years stale.

### Cited Findings
- LCon - Local Console Access: client-only mod adding a WebSocket server (default port 8115, config `enable_mod`/`port`); messages prefixed `[chat]`, `[message]`, `[system]`, `[client]`, `[server]`; replies carry status 200/201/400 and chat lines are echoed to connected clients; no auth mentioned; Minecraft 1.19.2 and 1.20.1, Forge only; last updated ~2 years ago; license ARR; source github.com/ZigTheHedge/lcon — [Modrinth: LCon](https://modrinth.com/mod/lcon-local-console-access)
- WorldAPI (companion to MairwunNx/minecraft-mcp): REST and WebSocket API on Paper, Fabric, or NeoForge servers, "and in singleplayer with the WorldAPI mod installed"; token-scoped permissions; version 4.2.0+ required by the MCP server — [MairwunNx/minecraft-mcp](https://github.com/MairwunNx/minecraft-mcp)
- cmoyates/HTTP-Request-Mod: server-side Fabric mod adding HTTP request commands and forwarding chat over WebSockets (`/websocket` set/connect/disconnect/status); targets 1.21.10; includes an opt-in bridge from chat to a live coding-agent session; README warns the agent then runs with the agent process's permissions — [cmoyates/HTTP-Request-Mod](https://github.com/cmoyates/HTTP-Request-Mod)
- WebSocket Commands (Modrinth): send commands to the server over WebSocket, built for Streamer.bot; listed for 1.21 and earlier; "works on servers and in single-player" — [Modrinth: WebSocket Commands](https://modrinth.com/mod/websocket-commands)
- WebConsole (Fabric, 1.18+): background WebSocket server for a web console that sends commands and receives the console log; page ~1,756 days old — [CurseForge: WebConsole](https://www.curseforge.com/minecraft/mc-mods/webconsole)
- HttpInfoServer: pushes in-game info to an external HTTP API (data collection only, no command execution) — [CurseForge: HttpInfoServer](https://www.curseforge.com/minecraft/mc-mods/httpinfoserver)
- server-management-mod-old: Fabric mod with WebSocket + HTTP REST, explicitly labelled old — [MinecraftPlayground repo](https://github.com/MinecraftPlayground/server-management-mod-old)
- Fabric dev note: a client-side mod can execute commands the same way it sends chat (ClientPlayerEntity `sendChatMessage`/command methods) — [FabricMC discussion #1489](https://github.com/orgs/FabricMC/discussions/1489)
- Loader status for 26.3: Fabric stable, NeoForge beta-only (see Version context) — [minecrafthub.io](https://minecrafthub.io/articles/minecraft-26-3-mods-shaders-packs)

### Inferences
- Writing a tiny Fabric client mod for 26.3 that opens a localhost WebSocket and calls the client command-send method (per the FabricMC discussion) is the only route that keeps Claude in the *singleplayer* Animus world without a server. It is feasible (Fabric is stable on 26.3) but it is custom code, and chat-sent commands return feedback only to the in-game chat/log, not to the socket, unless the mod also hooks chat/game messages (as LCon does with its echo).
- WorldAPI is the most promising off-the-shelf "mod with an API" if a 26.3 build exists; it should be verified first because it would give Claude both a singleplayer path and 51 MCP tools.

### Gaps
- WorldAPI's 26.x compatibility and loader list could not be verified (repo 404 / Modrinth slug not found).
- No Forge or NeoForge mod with a command endpoint and a 26.x build was found.
- WebSocket Commands' latest supported version beyond "1.21" was not checked.

## Key Question 5: Reading state back (client log, server log, RCON responses, screenshots)

### Takeaway
Reliable read-back exists only on the dedicated-server side: RCON response payloads (for commands that return text), the server's `logs/latest.log` (tailed by several Claude bridges), and query commands like `/data get`, `/execute if block`. For the singleplayer client, I found no source documenting the "stale latest.log on rotation" behaviour the user reports, but the log4j config is injectable via the launcher's `-Dlog4j.configurationFile` JVM argument, which is the sanctioned way to redirect/duplicate client logging to a stable file.

### Cited Findings
- RCON returns command output in the response payload; many commands return nothing; unknown commands are not reliably detectable; multi-packet responses have no reliable terminator — [Minecraft Wiki: RCON](https://minecraft.wiki/w/RCON)
- mctools' fragmentation strategy (junk packet, read until echoed) is the standard reliable terminator technique — [mctools RCON docs](https://mctools.readthedocs.io/en/master/rcon.html)
- clawdcraft reads chat by tailing the Paper server's `logs/latest.log`, and recommends verifying command effects with `execute if entity ...` because failures often return empty strings — [adrianwedd/clawdcraft](https://github.com/adrianwedd/clawdcraft)
- MinecraftCodeFoundary's RCON MCP server adds log tailing alongside command execution — [MinecraftCodeFoundary/Minecraft-MCP-Server](https://github.com/MinecraftCodeFoundary/Minecraft-MCP-Server)
- MairwunNx/minecraft-mcp exposes "logs" and "live event alerts" tools via WorldAPI — [MairwunNx/minecraft-mcp](https://github.com/MairwunNx/minecraft-mcp)
- VitaminMCP's agent "captures events and logs, answers state queries, and runs commands" on 26.2/26.3 servers — [VitaminMCP issue #4](https://github.com/Backas03/VitaminMCP/issues/4)
- Client log location is `.minecraft/logs/`; `latest.log` shows the current or last session; old logs are not deleted on restart — [Forge crash-report wiki](https://github.com/04Slash/Breaking-Down-Minecraft-Forge-Crash-Reports/wiki/Reading-a-Latest.log)
- The launcher's `client.json` carries a `logging` section whose JVM argument is `-Dlog4j.configurationFile=${path}`, pointing at the Log4j2 XML the version uses — [Minecraft Wiki: client.json](https://minecraft.wiki/w/Client.json)
- Apache's documented property name is `log4j2.configurationFile`; Minecraft's launcher uses the shorter `log4j.configurationFile` — [Log4j configuration docs](https://logging.apache.org/log4j/2.x/manual/configuration.html)
- A Fabric example shows adding a separate appender/logger with `additivity=false` so vanilla `latest.log` is untouched — [simple-developer120/client-custom-logs](https://github.com/simple-developer120/client-custom-logs)
- Typical `RollingRandomAccessFile` config writes `logs/latest.log` with a dated gzipped rollover pattern — [example log4j2.xml](https://github.com/mmachenry/on-demand-minecraft/blob/master/log4j2.xml)
- Screenshot-based verification: CDX-1's `minecraft_capture` returns a top-down PNG rendered from the bot's world data (not a game render) — [CDX-1/minecraft-client-mcp](https://github.com/CDX-1/minecraft-client-mcp); mciwb's Claude skill loop is "survey a site, build, inspect the rendered results, iterate" — [mciwb PR #162](https://github.com/gilesknap/mciwb/pull/162)
- LCon-style client mods echo chat messages to socket clients, giving command feedback without logs — [Modrinth: LCon](https://modrinth.com/mod/lcon-local-console-access)

### Inferences
- Cleanest state read-back for building: issue probe commands over RCON (`execute if block X Y Z minecraft:stone`, `data get block ...`, `execute if entity @e[...]`) and parse the response; these do return text, unlike `/fill` which may return only a count or nothing.
- If the user stays on the singleplayer client, the robust fix for stale `latest.log` is a custom log4j2 XML (passed via a launcher JVM argument or by editing the profile) that adds an extra non-rolling appender for chat/command feedback; this keeps vanilla logging intact and gives a file that never rotates mid-session.
- macOS screenshot verification is available from Claude Code's computer-use/screenshot tooling, but it is slow and pixel-based; prefer command probes for correctness and use screenshots only for aesthetics.

### Gaps
- No source was found documenting the client `latest.log` going stale when log4j rotates (the user's observation); the mechanism (likely size-based rollover creating a new file while a tail holds the old inode) is my inference, not cited.
- The launcher's exact UI for overriding `-Dlog4j.configurationFile` on macOS was not verified in this research.

## Key Question 6: Recommended simplest robust stack for "Claude builds things in my world"

### Takeaway
Run a local Paper (or vanilla) 26.3 dedicated server on the Mac with RCON on localhost, host a copy of Animus there, and give Claude Code either an existing RCON MCP server (Faneraiy14/minecraft-rcon-mcp) or a ~50-line Python FastMCP bridge using `rconx`/`mctools`, with command chunking under 1446 bytes and `execute if` probes for verification. Mineflayer-based MCP servers are not viable for 26.3 until PrismarineJS ships protocol 777.

### Cited Findings
- Prerequisite chain: `brew install openjdk@25`, download Paper 26.3 jar, set `enable-rcon=true`, `rcon.password`, `rcon.port=25575` — [PaperMC Java install](https://docs.papermc.io/misc/java-install/); [Minecraft Wiki: RCON](https://minecraft.wiki/w/RCON)
- Claude Code registration is one command: `claude mcp add ...` with RCON env vars (Faneraiy14) or `npx -y @mairwunnx/minecraft-mcp` (WorldAPI route) — [Faneraiy14/minecraft-rcon-mcp](https://github.com/Faneraiy14/minecraft-rcon-mcp); [MairwunNx/minecraft-mcp](https://github.com/MairwunNx/minecraft-mcp)
- A working precedent for exactly this workflow on 26.3: mciwb's quick start runs a Minecraft 26.3 server (podman) and drives it over RCON from Python with a Claude Code build skill — [gilesknap/mciwb](https://github.com/gilesknap/mciwb)
- A working precedent for Claude Code + Paper + RCON + log tailing: clawdcraft (tmux + RCON scripts, limited pre-approved script set) — [adrianwedd/clawdcraft](https://github.com/adrianwedd/clawdcraft)
- Mineflayer alternative is blocked at 26.1 — [VitaminMCP issue #4](https://github.com/Backas03/VitaminMCP/issues/4); [mineflayer PR #4146](https://github.com/PrismarineJS/mineflayer/pull/4146)
- Python RCON library choice: `rconx` 0.3.0 (Oct 2026) or `mctools` (limit + fragmentation handling); `mcrcon` 0.7.0 is 2021-era but protocol-compatible — [PyPI rconx](https://pypi.org/project/rconx/); [mctools docs](https://mctools.readthedocs.io/en/master/rcon.html); [libraries.io mcrcon](https://libraries.io/pypi/mcrcon)

### Inferences
- Recommended stack (ranked):
  1. **Local Paper 26.3 + RCON + thin MCP bridge** (free, version-proof, bulk `/fill`/`/clone`, text feedback, trivially sandboxed to 127.0.0.1). Play by connecting the normal client to `localhost` so the user watches Claude build live in the same world. Sync the world folder back to `saves/Animus` if singleplayer play must continue there.
  2. **WorldAPI + MairwunNx/minecraft-mcp** if a 26.3 build is confirmed: richest tools, undo, logs, and the only singleplayer-mod path; otherwise skip.
  3. **CDX-1/minecraft-client-mcp (Mineflayer)** only if the user is willing to run a 26.1 world or a ViaBackwards-translated server; good for "embodied" demos, poor for large builds.
  4. **Custom Fabric client mod with a localhost WebSocket** for true singleplayer control — feasible but bespoke; LCon is the (stale, Forge-only) design reference.
- Bridge design rules that fall out of the findings: keep each command under 1446 bytes; batch builds as many small commands or a datapack `function`; after every mutating command, send a verification probe; read responses with a junk-packet terminator; never put the RCON password in argv (mciwb's `ps` warning); bind RCON to localhost only.
- Datapack functions (`/function namespace:build`) let Claude write thousands of `setblock`/`fill` lines to disk and trigger them with one short RCON command, sidestepping the 1446-byte limit entirely; `/reload` picks up new function files without a restart.

### Gaps
- Whether Paper's 26.3 `/fill` has the historical 32,768-block cap, and the exact `max-chained-neighbor-updates`/`function-permission-level` defaults relevant to large RCON builds, were not verified against 26.3 documentation.
- No benchmark was found comparing RCON command throughput vs WorldAPI for very large builds.
