# Eureka Personal Notes

Shareable, portable preferences for the **Notes** field in Eureka's profile settings. These are personal preferences, not a skill or an automatically loaded configuration.

## Files

| File | Purpose |
|------|---------|
| [common.md](common.md) | Shared communication, execution, coding, Git, tooling, and repo-bundled skill preferences. No private projects or machine-specific paths. |
| [windows.md](windows.md) | Windows-only shell preference. Do not include on macOS. |
| [local.example.md](local.example.md) | Public template for personal branch prefixes, tooling differences, project aliases, and repo-specific skill locations. |
| `local/notes.md` (not tracked) | Your filled-in notes for this machine. The entire `local/` directory is ignored by Git. |

## Set up a machine

1. Review [common.md](common.md). The `uv`, `nvm`, and `podman` choices are personal preferences, not installation instructions; adjust the applied notes if this machine uses different tools.
2. If needed, create `local/` here and copy [local.example.md](local.example.md) to `local/notes.md`. Fill in the values for this machine; remove unused sections and template comments. Omit the local file if you have no local additions.
3. In Eureka, open **Settings > System > Profile > Notes** and paste the applicable contents in this order:

   | Platform | Contents |
   |----------|----------|
   | Windows | `common.md` + `windows.md` + your local notes |
   | macOS | `common.md` + your local notes |

4. Resolve any conflicting preferences in the combined text before saving. Do not paste this README, unresolved placeholders, or Markdown code fences around the notes. Update the Notes field only; configure name, timezone, and language separately in the profile's basic fields.

There is no macOS overlay yet: the original macOS variant only removed the Windows shell preference and adjusted local project paths. Add a separate macOS file if a real macOS-only preference emerges; do not duplicate the common notes or assume a shell preference.

## Sharing and privacy

- Keep reusable preferences in the tracked files. Keep usernames in branch prefixes, absolute paths, private project names, internal skill inventories, and work-specific context in local notes or a private store outside this repo.
- The local template deliberately uses placeholders. It is not a ready-to-paste profile.
- `.gitignore` prevents accidental inclusion of untracked local files in normal Git adds; it is not encryption or a security boundary. Do not force-add local notes, and never store credentials or tokens in profile notes.
- Review `git diff --cached` and the staged file list before committing. Do not commit a combined profile export or screenshots containing private notes.
- Local files do not travel with a clone. Recreate them per machine or sync them through a separate private channel.

## Updating and migrating

- Edit shared preferences here, then manually reapply the appropriate notes in Eureka on each machine. Eureka does not automatically read or synchronize these files.
- Keep the old private work note unchanged until you have verified the new composition. Transfer only machine-local or private additions to your local notes; avoid maintaining a second copy of the shared preferences there.
- This repository contains only the reusable notes and a blank local template. It does not include the original work note, personal basic profile fields, private project mappings, or a filled-in local profile.
