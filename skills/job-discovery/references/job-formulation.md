# Job Formulation

A Job is the progress a person is trying to make in a situation — not the feature they asked for, not the product they imagine.

## The formulation template

Forbid "User needs X." Use:

> When **[situation]**, I want to **[motivation / progress]**, so I can **[desired outcome]**.

Example:

> When an autonomous agent is running a long task,
> I want to know when meaningful human intervention is required,
> so I can avoid continuously monitoring the execution while maintaining
> confidence in the outcome.

## Job classes

### Primary Functional Job
The core task the person is trying to accomplish. One per analysis, though you may be uncertain which of two candidates is primary — say so.

### Related Functional Jobs
Sub-jobs required to complete the primary Job. Often the real unmet need hides here.

### Emotional Job
How the person wants to feel: confidence, control, reduced anxiety, trust. Only list what the source supports.

### Social Job
How the person wants to be seen by others. Only when the source supports it — never invent one.

## One complaint ≠ one Job

The same complaint can map to multiple Jobs. "我一直要盯着 Agent" could be:

- Primary: know whether the agent is in an abnormal state
- Related: reduce the cost of human supervision
- Related: intervene before a failure happens
- Emotional: maintain a sense of control over an autonomous system

Generate all hypotheses the evidence supports. Do not collapse to a single answer when the evidence is ambiguous.

## Rules

- Every Job statement must be traceable to Evidence IDs.
- A Job is about progress, not about the tool. "Use a monitoring dashboard" is not a Job; "know when to intervene" is.
- Write Jobs in solution-free language. If a Job statement names a product or a feature, it's still a solution in disguise — rewrite it.
