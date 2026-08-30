# Research Principles

This document defines the public research and engineering principles for the Embodied AI Reflex Layer project.

These principles are intended to keep the work safe, interpretable, portable across model ecosystems, and useful as an experimental platform.

## 1. Safety remains local and invariant

Safety-critical behavior must not depend on model identity, conversational context, relationship context, or cloud connectivity.

The local system owns physical limits such as:

- maximum temperature;
- maximum force or torque where applicable;
- maximum speed and travel;
- current and power limits;
- timeout behavior;
- fault handling;
- safe-stop behavior.

Higher-level AI systems may request bounded behavior, but they do not override local safety constraints.

## 2. Recognition is not authorization

The system may estimate who is interacting using multiple signals, but confidence about identity does not automatically grant privileges.

A nearby phone, watch, credential, face, voice, touch pattern, or other signal should be treated as evidence rather than unquestioned proof.

Low-risk personalization may be allowed at a lower confidence threshold than sensitive actions. Private context, configuration changes, account actions, and other privileged functions require stronger authentication.

## 3. The embodiment interface is model-agnostic

The physical system should be defined in terms of:

**observations out → policy or logic → bounded actions in**

The embodiment must remain usable with:

- deterministic control;
- different learned policies;
- different model providers;
- future robotics frameworks.

LeRobot is currently an interoperability target, not a required internal architecture. MolmoAct 2 is one candidate policy, not a dependency.

Model-specific adapters belong outside the core device API.

## 4. Preserve original experimental data

Raw and canonical experiment records should not be discarded simply to satisfy a downstream machine-learning format.

The project should preserve:

- episode and frame structure;
- timestamps;
- sensor observations;
- requested behavior;
- executed behavior;
- safety interventions;
- experimental condition;
- protocol and hardware version information.

Exporters may convert this data into LeRobotDataset v3 or other formats later.

## 5. Requested behavior and executed behavior are different things

When a higher-level policy requests a response, the record should preserve both:

1. what was requested; and
2. what the local safety-constrained system actually executed.

Any clamp, substitution, rejection, timeout, or safe-state transition should be visible in the data.

This distinction is necessary for both safety auditing and later policy evaluation.

## 6. Do not infer social or emotional meaning from physical signals alone

Physical measurements should be described as physical measurements.

For example:

- high force is not automatically aggression;
- sustained touch is not automatically affection;
- physiological data is not automatically emotional state.

Higher-level interpretation may be studied separately, but raw sensor signals should not be labeled with unsupported social meaning.

## 7. Context should be semantic and minimal

Low-level embedded systems should not receive raw private conversation logs.

When conversational or relational context is needed for an experiment, it should be represented as a compact, sanitized semantic state sufficient for the task.

Public datasets should not contain intimate conversation, identifying private context, or unnecessary personal information.

## 8. Public work should prove progress without automatically disclosing every mechanism

The public repository should document:

- research questions;
- safety boundaries;
- high-level architecture;
- protocols;
- sanitized schemas;
- results;
- negative results;
- interoperability decisions.

Implementation details that may affect future IP strategy, security, privacy, or unpublished experimental methods may remain private until there is a deliberate reason to disclose them.

Before publishing, ask:

> Does this commit primarily prove progress, or does it reveal a differentiating mechanism?

## 9. Reproducibility requires versioning

Every experiment should eventually identify the versions that could affect its outcome, including:

- firmware version;
- hardware revision;
- schema version;
- experiment protocol version;
- sensor configuration;
- relevant model or policy version;
- adapter/exporter version where applicable.

A result without enough provenance to reconstruct its setup should not be treated as a strong result.

## 10. Negative results are results

Failed hypotheses, noisy sensors, poor classifiers, unstable thermal behavior, confusing interaction mappings, and safety interventions should be recorded rather than hidden.

The goal is not to produce a sequence of polished demonstrations. The goal is to reduce uncertainty and learn which embodiment mechanisms are actually useful.

## 11. Claims should remain narrower than the evidence

The project may describe:

- persistent agents;
- context-sensitive behavior;
- identity-aware interaction;
- agent-selected or policy-selected responses;
- learned or deterministic control;
- perceived intentionality or responsiveness when measured.

The project should not present consciousness, subjective feeling, personhood, or autonomous consent as engineering facts unless there is evidence that supports those claims.

## 12. Human testing should be deliberate

Human-contact experiments should use explicit procedures and stopping conditions.

As the work progresses, protocols should address:

- informed participation;
- anonymization;
- thermal and mechanical stopping rules;
- exclusion criteria where relevant;
- incident logging;
- whether formal ethics or institutional review is appropriate for the intended study or publication context.

## 13. Security-sensitive identity data stays separate

Biometric templates, wearable identifiers, credentials, authentication secrets, and private recognition data should not be placed in ordinary public logs.

Identity research data should be minimized, pseudonymized where possible, and separated from authorization credentials.

## 14. The prototype should remain smaller than the thesis

V0 exists to test one narrow embodiment question at a time.

A successful small experiment is more valuable than prematurely building a complex humanoid system whose failures cannot be interpreted.

The current objective is to establish measurable, bounded, context-sensitive embodied behavior and a clean interface for future policy integration.
