# README Disclosure Review — Private Notes

Do **not** push this file if you want the review itself to remain private.

## Overall assessment

The original README was excellent for credibility, but it disclosed more of the candidate contribution than is necessary at this stage.

The main issue was not the generic idea of robot reflexes. Prior art already covers tactile sensing, reflexive robot behavior, learned policies, and distributed control. The potentially valuable part of this project is the particular way persistent-agent context, identity, semantic events, and bounded local reflexes are composed.

The original README described that composition in unusually explicit detail.

## Material I would reduce in the public README

### 1. The exact extension question

Original disclosure:
- identical physical touch
- different person identity
- conversational context
- different equally safe responses
- perceived intentionality / relationship-specific responsiveness

Why reduce it:
This is close to a research claim and future product behavior specification. Keep the public version at “higher-level interaction context may influence social responses while safety remains invariant.”

### 2. The exact three-layer candidate contribution

Original disclosure:
- deterministic safety layer
- local semantic reflex layer
- persistent-agent policy layer
- identity + compact conversation context
- bounded response request path

Why reduce it:
The broad layering is fine to publish, but the original wording effectively spelled out the proposed interface architecture. The revised README keeps the three layers but removes the detailed identity/context routing.

### 3. The exact semantic event vocabulary

Original disclosure included:
`PROXIMITY`, `CONTACT_START`, `LIGHT_CONTACT`, `PRESS`, `RAPID_HIGH_FORCE_CONTACT`, `SUSTAINED_HOLD`, `RELEASE`, `CONTACT_END`

Why reduce it:
The labels are not individually valuable, but publishing the full vocabulary plus the response vocabulary and the mappings creates a much more complete reproduction recipe than necessary.

Recommendation:
Keep the vocabulary in the private engineering notebook for now. Publish labels later if they become part of a paper or reproducibility package.

### 4. The exact response vocabulary

Original disclosure included:
`NO_RESPONSE`, `ORIENT_TOWARD`, `YIELD`, `WITHDRAW`, `HOLD_POSITION`, `WARM_SLOW`, `MAINTAIN_WARMTH`, `RETURN_TO_BASELINE`

Why reduce it:
Again, the labels are not inherently novel, but the paired event→response interface may become more important than any one hardware component.

### 5. Exact BOM and component models

Original disclosure named specific sensors and parts.

Why reduce it:
This is probably low IP risk by itself, but it adds implementation detail without giving much extra strategic value before the rig exists.

Recommendation:
Public README uses hardware categories. Exact BOM can stay private until procurement/testing, then selectively publish what is needed for reproducibility.

### 6. Exact experimental mappings

Original:
- gentle contact → orient toward
- rapid/high-force → withdraw
- sustained gentle contact → thermal response

Why reduce it:
These mappings are part of the experiment logic. Keep the high-level experiment stages public, but withhold exact thresholds, timings, mappings, and tuning until an IP decision is made.

### 7. MolmoAct 2 positioning

This is safe to keep high-level.

The useful public signal is:
- awareness of Ai2's ecosystem
- intention to evaluate open embodied models later
- refusal to put a learned model into the V0 safety loop

Do not publish a detailed future integration plan until the architecture has been reviewed.

## Material that is valuable to keep public

- broad research question
- safety-first layered architecture
- prior-art acknowledgement
- high-level experiment stages
- public data schema
- sanitized results
- negative results
- high-level hardware categories
- explicit statement that learned models do not bypass local safety
- public timestamps and progress history

## Recommended operating rule

Before each public commit, ask:

> Does this commit prove progress, or does it reveal a mechanism?

If it mostly proves progress, publish it.
If it reveals a mechanism that might become differentiating IP, keep it private until reviewed.

## Important legal note

This is an engineering/IP-risk review, not legal advice. Patentability and the consequences of public disclosure vary by jurisdiction. If patent protection may matter, consult a patent attorney before publishing implementation details that could be considered an enabling disclosure.
