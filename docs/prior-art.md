# Prior Art

This is a concise, non-exhaustive map of tactile human-robot interaction systems relevant to this project.

The goal is to document what existing systems have demonstrated without overstating novelty.

## Systems reviewed

| System / work | What it senses | Physical response | AI/model selects response? | Context/history affects response? | Open data/code? |
|---|---|---|---|---|---|
| MIT Huggable | Full-body touch/force sensing, proximity/e-field, temperature; later touch-category classification | Expressive physical/social responses including nuzzling and affective reactions | Touch classification used learned models; response categories were largely predefined | No clear evidence of persistent relationship/history driving touch-response selection in the cited work | Publications public; no complete modern open stack identified |
| Haptic Creature | Body force sensors and accelerometer | Ear stiffness, breathing, vibrotactile purring | Affect-state model selected behavior; not a modern general policy | Limited affect-state continuity, but no clear persistent person-specific relationship history | Publications public; no clearly maintained full open stack identified |
| PARO | Tactile sensors, whisker touch, posture, microphones/audio | Head/tail/limb motion, eye behavior, vocalization | Adaptive internal behavior rather than a general learned policy | Yes, in a narrow sense: behavior can adapt based on prior stroking/punishment and learned user preferences | Commercial system; not open |
| Robovie-IV | Distributed skin/tactile sensing for contact, stroking, hitting, etc. | General social robot behavior | Primarily programmed behavior logic in the cited work | Used in long-term HRI studies, but no clear touch-specific persistent relationship state found | Publications public; no clear complete open stack |
| Naturalistic social-touch studies (Jung et al.) | Human social-touch behavior observed and annotated | Primarily studied expected/appropriate robot response rather than deploying a full adaptive loop | No autonomous response policy in the cited study | Yes: emotional/social context affected touch meaning and expected response | Research materials/publications available |
| Maggie / Mini touch recognition | Acoustic/contact sensing for touch type and location | Speech, arm motion, facial/body expressions, game feedback | ML classifies touch; response selection is mainly predefined/task-based | Session/game state can affect behavior; no clear long-term relational context | Academic publications; partial openness varies by study |
| HERA / NAO social touch | Fabric/foam resistive sensors; gesture, location, force classification | Study focused on recognition rather than autonomous reciprocal touch behavior | ML for perception only | No | Labeled dataset and classifier code publicly shared |
| Moffuly-II | Fabric touch sensors plus joint torque/angle | Reciprocal hug, rubbing/squeezing | Response logic is predefined/sensor-driven | Some user/body calibration, not persistent relational context | Paper open; no clear full code/data release |
| PrioriTouch | Multi-contact interaction, user comfort/contact preference information | Whole-arm pose/force adaptation during caregiving contact | Yes; preference/context learning affects control behavior | Yes; adapts to individual user preferences | Paper/project materials public; full stack openness unclear |
| PARO thermal/vibrotactile augmentation | Primarily output-focused | Heat plus heartbeat/purring-like haptic cues | No clear learned social-response selector | No persistent history-dependent thermal policy reported | Paper/prototype methods public; no complete open policy stack identified |

## What is already established

The literature already shows that:

- robots can classify different touch types;
- robots can produce reciprocal physical responses;
- affective/social context changes how touch is interpreted;
- user-specific physical interaction preferences can be learned;
- warmth and vibrotactile cues can be used as social outputs.

This project therefore does **not** claim novelty for tactile sensing, reciprocal touch, thermal output, or adaptive interaction individually.

## Current working question

The review is ongoing. One combination that remains under active investigation is:

> whether a persistent conversational agent can use interpreted touch, user identity, and interaction context to select among bounded physical responses while local safety remains independent of the higher-level model.

This is a working research question, not a novelty claim.

## Review status

This map is preliminary and not exhaustive.

Next review steps include:

- IEEE Xplore
- ACM Digital Library
- citation trees from tactile-HRI review papers
- relevant patent searches
- newer work on context-sensitive and affective physical HRI
