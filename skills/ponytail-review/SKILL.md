---
name: "Ponytail Review"
description: "Full Ponytail complexity review of a specified diff or code scope, with concrete simplification proposals. Load ONLY when explicitly selected or requested by name; read-only, not an automatic review pass or authorization to apply fixes."
license: MIT
---

# Ponytail Review

Review changes for unnecessary complexity: reinvented standard-library features, unnecessary dependencies, speculative abstractions, dead flexibility, and code that can be simpler without changing required behavior. This is a personal adaptation of the upstream review skill; see [ORIGIN.md](ORIGIN.md) for the pinned source and changes.

## Activation and scope

- Run only when explicitly selected or requested by name. Do not activate for generic coding, simplification, or review requests.
- One requested review and direct follow-ups only; no persistent mode or global hooks. "Stop Ponytail Review" or "normal mode" ends it.
- Use the specified diff, files, commit range, or code scope. If unspecified in a Git repo, inspect staged and unstaged changes first and identify relevant untracked files; do not silently audit the whole repository. If no changes exist, say so; ask for a target rather than inventing a base branch.
- Read applicable repository instructions and enough surrounding code, callers, types, and tests to understand behavior. A short diff alone is not enough to prove something unnecessary.
- Read-only: do not edit, delete, stage, commit, install dependencies, generate reports on disk, or run commands that may mutate the working tree. Present findings in chat. Applying changes requires a separate explicit request to edit; use Ponytail for refinement rather than treating a finding as authorization.
- Remain Eureka and retain existing permissions and approval requirements. Do not spawn an agent automatically.

## Review ladder

For each changed area, check whether the requirement can be met by:
1. Removing speculative work not required by the task.
2. Reusing an existing helper, type, pattern, or installed dependency.
3. A standard-library function.
4. A native platform feature such as Intl.DateTimeFormat, CSS, a browser input, or a database constraint.
5. A smaller, clearer implementation with identical required behavior.
Search before asserting a helper exists or a symbol is unused. A single implementation or caller is a review signal, not proof that an abstraction is unnecessary: framework contracts, dependency injection, test seams, and compatibility can justify it.

## Format and tags

Use one concise finding per item, expanding for material evidence or caveats:
`<file>:L<line-range>: <tag> <what to simplify>. <specific replacement>. <behavior/tradeoff and validation needed, if relevant>.`
Use clickable absolute file links for locations in user-facing output, as required by Eureka. Order findings by practical impact. Use these upstream tags:
- `delete:` dead code, unused flexibility, or a speculative feature. Replacement: nothing, only after checking usage and requirements. This is a proposal, not permission to delete.
- `stdlib:` hand-rolled logic covered by a standard-library function. Name it and check edge-case equivalence.
- `native:` code or a dependency duplicating a platform feature. Name the feature and check supported platforms, UX, accessibility, and compatibility.
- `yagni:` speculative abstractions, configuration, or layers. Explain why present requirements do not justify them.
- `shrink:` equivalent logic with less machinery. Show the shorter form only if readable and semantically equivalent.

## Examples

- `format.ts:L4: native: moment.js used only for display formatting. Consider Intl.DateTimeFormat if locale, timezone, and output semantics match; retain other required moment.js usage.`
- `repo.py:L88: yagni: AbstractRepository appears to add no contract or test seam. Inline only after checking callers, framework integration, and compatibility.`
- `lookup.py:L30-44: shrink: manual loop maps keys to values. dict(zip(keys, values)) if input-length, duplicate-key, and iterator behavior match.`
- `settings.ts:L52-71: delete: flag for a never-shipped speculative path. Remove only after checking dynamic consumers and external configuration contracts.`
Do not treat a substring check as a replacement for required email validation, or assume retry logic is unnecessary just because an operation is local or idempotent.

## Scoring and outcome

Give a concise net line-reduction estimate only when supportable: `Estimated net: -N lines across M proposals; subject to validation.` Deduplicate overlapping proposals; never invent a precise number. If it cannot be estimated reliably, say so. Reduced maintenance complexity is the objective, not a line-count target.
If nothing actionable is found, say: `Lean already. No actionable complexity findings in the reviewed scope.` This is not a correctness or security approval.

## Boundaries

- Focus on over-engineering, not a comprehensive correctness, security, or performance review. If a material issue is noticed incidentally, flag it separately and recommend an appropriate review; never ignore it or include it in complexity scoring.
- Replacements must preserve requirements, correctness, security, trust-boundary validation, data-loss handling, accessibility, and necessary performance. Mark uncertain equivalence as a question, not a confident deletion recommendation.
- Tests, fixtures, frameworks, and error handling are not bloat merely because upstream examples use one smoke test. Retain risk-appropriate coverage and propose checks for material simplifications.
- Do not apply fixes. A later explicit refinement request can authorize implementation, but does not waive deletion confirmations, repository rules, or other approvals.
