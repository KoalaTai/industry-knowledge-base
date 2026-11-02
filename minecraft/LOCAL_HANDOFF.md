# Handoff: finish the AC Worlds datapack setup on this Mac and drive Minecraft

You are Claude Code running locally on the user's Mac. A cloud session did the
repo work; you have what it lacked: this machine, the Minecraft install and the
running game. Finish the job end to end and report what you actually observed.

## Where things stand

- Repo: `~/industry-knowledge-base`, branch `claude/adoring-newton-2oc4eu`
  (already checked out). The datapack lives in `minecraft/datapack/ac_worlds/`
  and is zipped to `minecraft/datapack/ac_worlds.zip` by `minecraft/generate.py`.
- `python3 minecraft/install.py` already copied the zip to
  `~/Library/Application Support/minecraft/saves/Animus/datapacks/ac_worlds.zip`.
- An earlier zip was broken (`pack.mcmeta` nested in a subfolder, so Minecraft
  silently ignored it). That is fixed on this branch; the installed zip should
  now have `pack.mcmeta` at its root. Verify, do not assume.
- The pack needs Java Edition 1.21 or newer (`pack_format` 48, `function`
  folder, macro functions). Bedrock cannot load it.
- In game: `/function ac:hub` builds all 119 landmarks in rows north of the
  player. `/function ac:index` lists them. `/function ac:cancel` stops a run.
  On load the pack prints a gold "AC Worlds datapack loaded" line in chat.
- The user has not yet seen anything happen in game. Your job is to find out why
  and get the build running.

## Step 1: verify the installed pack from the terminal

```
unzip -l "$HOME/Library/Application Support/minecraft/saves/Animus/datapacks/ac_worlds.zip" | head
```

`pack.mcmeta` must be listed at the top level, not under `ac_worlds/`. If it is
nested, run `python3 minecraft/generate.py` then `python3 minecraft/install.py
--world Animus` and check again. Also run `python3 -m pytest minecraft/tests -q`
once so you know the generator is healthy.

## Step 2: find the game version and check the log

- Version the user actually launches: read
  `~/Library/Application Support/minecraft/launcher_profiles.json` (the
  `lastVersionId` of the most recently used profile) and the first lines of
  `~/Library/Application Support/minecraft/logs/latest.log`, which print the
  running version. If it is below 1.21, stop here and tell the user to pick
  "Latest release" in the launcher.
- After the user has opened Animus or typed `/reload`, grep the log:

```
grep -n -i "ac_worlds\|datapack\|pack.mcmeta\|ac:" "$HOME/Library/Application Support/minecraft/logs/latest.log" | tail -40
```

  A healthy load shows no errors mentioning `ac:`. Red function parse errors
  there point to a bug in the generated functions; copy the exact lines into
  your report and fix the generator if the cause is obvious.
- Confirm the world has the pack enabled: `level.dat` in the Animus save lists
  enabled packs. World-folder datapacks are enabled automatically, but if the
  user disabled it once, `/datapack enable "file/ac_worlds.zip"` turns it back
  on. You can read `level.dat` with a small Python NBT read if needed, but the
  in-game `/datapack list` is simpler.

## Step 3: drive the game

You can type commands into the running game for the user. Ask them first, once,
then proceed. Two options, in order of preference:

1. **The user types.** Tell them exactly what to type, one command at a time,
   and read the log after each to confirm it ran. Commands, in order:
   `/reload`, `/datapack list` (expect `[file/ac_worlds.zip]` under enabled),
   `/function ac:hub`. Each `/function` call and each `tellraw` from the pack
   lands in `latest.log`, so you can confirm progress without a screenshot.
2. **You type via AppleScript.** Only if they ask you to. Minecraft must be the
   frontmost window and the user must not be moving the mouse. Press `t` to open
   chat, type the command, press return:

   ```
   osascript -e 'tell application "System Events"
     tell process "java" to set frontmost to true
     delay 0.5
     keystroke "t"
     delay 0.3
     keystroke "/function ac:hub"
     delay 0.2
     key code 36
   end tell'
   ```

   The process name may be `java` or `Minecraft`; check with
   `osascript -e 'tell application "System Events" to get name of every process whose background only is false'`.
   The Terminal needs Accessibility permission in System Settings > Privacy &
   Security > Accessibility the first time. Never send keystrokes while the
   user is typing.

Prerequisites in game: cheats enabled for the world (Esc > Open to LAN > Allow
Cheats ON works for an existing world), Creative mode recommended, flat open
ground, player facing north. The hub run takes several minutes and prints
progress to chat and the log.

## Step 4: report

Tell the user plainly: the game version you found, whether the zip was valid,
whether the log shows the pack loading, and whether `/function ac:hub` started
building. If something failed, paste the exact log lines and what you changed.
If you changed files under `minecraft/`, run the tests, commit on this branch
with a clear message, and push with `git push -u origin claude/adoring-newton-2oc4eu`.

## Known local snag

This machine's Claude Code has a daily token quota hook that blocked the user
earlier ("Daily token quota exceeded ... Edit TOKEN_QUOTA_DAILY"). If it
blocks you, tell the user to raise `TOKEN_QUOTA_DAILY` in the hook's settings
or wait for the midnight reset; do not try to disable the hook yourself.
