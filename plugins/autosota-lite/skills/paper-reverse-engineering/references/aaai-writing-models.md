# AAAI contribution-family writing models

Use these models as rhetorical priors. Recompute surface statistics from the
selected three to five exemplars whenever feasible.

## Mechanism-first method

Narrative spine:

`observed failure -> missing mechanism -> proposed mechanism -> predicted effect -> controlled evidence`

Abstract moves: task/capability, concrete failure, cause in existing design,
method, mechanism, expected consequence, evaluation scope, bounded result.

Introduction paragraphs: stakes, failure evidence, assumption grouping prior work,
mechanistic answer, component-to-effect preview, experiment-to-claim map, at most
three core contribution bullets.

Experiments should answer: does it work under matched conditions; is the mechanism
responsible; where does it persist or fail; what cost is paid?

Illustrative four-paper AAAI-26 award corpus: mean sentence length about 26 words,
middle 50% about 13-36, short (<12) about 22%, long (>30) about 33%. These PDF-
derived values include extraction noise and are not acceptance thresholds.

## Diagnostic/evaluation

Narrative spine:

`accepted inference -> hidden confound -> controlled intervention -> revised conclusion -> decision consequence`

Abstract moves: decision stakes, current proxy/inference, confound, diagnostic
question, controlled design, headline result, boundary, practical implication.

Results paragraphs: inference under test, control/treatment, effect and uncertainty,
observation, alternative explanation, boundary, decision consequence. Null results
need intervals, sensitivity, power, or detectable-effect context.

Illustrative one-award/three-accepted AAAI corpus: mean sentence length about 32
words, middle 50% about 17-44, short about 17%, long about 48%. Do not lengthen a
clear sentence to match this syntactically dense family.

## Benchmark/resource

Narrative spine:

`real capability -> coverage failure -> resource design -> validity evidence -> baseline diagnosis -> reusable release`

Abstract moves: capability, current omission, resource/unit, construction, coverage,
protocol, baseline diagnosis, availability and intended scope.

The resource section must define provenance, task unit, fields, splits, allowed
information, annotations, adjudication, metrics, leakage/contamination safeguards,
evaluator reliability, and baseline protocol. Size supports coverage; it is not the
contribution by itself.

Illustrative four-paper accepted AAAI corpus: mean sentence length about 26 words,
middle 50% about 14-34, short about 20%, long about 31%.

## Controlled vocabulary profile

Measure function words, transitions, first-person forms, and stance/evidence verbs
per 1,000 words. Useful monitored classes include:

- contrast: `however`, `but`, `while`, `in contrast`;
- reference: `this`, `these`, `which`, `that`;
- author action: `we`, `our`;
- calibrated evidence: `show`, `indicate`, `suggest`, `may`, `can`.

Use the distribution to detect monotony or excess, not to force exact counts.
Preserve topic vocabulary from the author's project.
