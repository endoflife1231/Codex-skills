# Offline Web Interface Review Checklist

Use this fallback only when the live Vercel guideline source cannot be opened.

## Accessibility
- All interactive controls are keyboard reachable and have visible focus states.
- Icon-only controls have accessible names.
- Form labels are programmatically associated with inputs; errors are announced and specific.
- Color is not the only carrier of meaning; contrast remains readable in all states.
- Dialogs trap focus, restore focus on close, and close predictably with Escape when appropriate.

## Interaction
- Buttons perform actions; links navigate.
- Disabled, loading, empty, success, and error states are explicit.
- Destructive actions require deliberate confirmation or provide undo.
- Hit targets are sufficiently large and do not overlap.
- Hover-only information has keyboard/focus equivalents.

## Layout and typography
- Information hierarchy is clear without relying on decorative effects.
- Text remains readable at browser zoom and within constrained panels.
- Long text, filenames, and user content wrap or truncate intentionally.
- Scroll areas are obvious and do not create accidental nested-scroll traps.

## Forms
- Preserve user input after recoverable errors.
- Use correct input types, autocomplete attributes, and sensible defaults.
- Validation runs at appropriate times and explains how to fix the problem.
- Primary action remains distinguishable from secondary and destructive actions.

## Performance
- Avoid unnecessary client components, re-renders, layout shifts, and oversized images.
- Reserve media dimensions and lazy-load non-critical assets.
- Keep frequently used actions responsive under realistic data volume.

## MythicTable-specific checks
- GM-only data never appears in player DOM, serialized props, network payloads, or client caches.
- Map controls are usable by keyboard where practical and have clear selected/locked states.
- Reconnection, stale state, and server rejection are visible to the user.
- Gameplay warnings do not block GM override unless the failure is authorization or integrity related.
