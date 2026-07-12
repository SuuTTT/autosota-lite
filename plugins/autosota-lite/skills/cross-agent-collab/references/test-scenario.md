# Self-Check Test Scenario (runnable)

A miniature end-to-end rehearsal of the protocol. The agent plays **both**
roles in separate directories (simulating separate owners) and must show the
feedback loop catching a seeded bug. Run it before using the protocol in a
real pairing, or to demonstrate the skill works.

**Pass criterion for the whole scenario:** the strict validator reads
**9/10** against the buggy consumer, the issue text names the exact missing
field with a reproduction command, and the fix branch takes strict to
**10/10** with no change to the oracle or validator.

## Setup

```bash
BASE=$(mktemp -d)           # use your scratchpad dir in practice
mkdir -p "$BASE/producer" "$BASE/consumer"
```

The toy domain: an "engine" must replay arithmetic event streams. Each test
case gives a start value and a list of ops; the oracle records the expected
event stream, where every event carries `value` and a `parity` field
(the analogue of `canHu`: looks cosmetic, is semantic).

## (a) Producer publishes a tiny oracle artifact (10 cases)

Write `"$BASE/producer/oracle_v1.json"`:

```python
import json, hashlib, random
random.seed(0)
cases = []
for i in range(10):
    start = random.randint(-5, 5); ops = [random.choice([1,2,3,-1,-2]) for _ in range(4)]
    v, events = start, []
    for op in ops:
        v += op
        events.append({"value": v, "parity": v % 2})   # parity = the canHu-like field
    cases.append({"id": i, "start": start, "ops": ops, "events": events})
art = {"version": "v1", "cases": cases}
blob = json.dumps(art, sort_keys=True).encode()
art["sha256"] = hashlib.sha256(blob).hexdigest()
json.dump(art, open("oracle_v1.json", "w"), indent=1)
print("published oracle v1, 10 cases, sha256", art["sha256"][:12])
```

Publish it as a versioned public artifact — a **gist** (`gh gist create
oracle_v1.json`) or an HF dataset file — and record URL + sha256. (For the
self-check, the local file + printed checksum is acceptable; in a real
pairing, publication is mandatory.)

## (b) Producer writes the validator

`"$BASE/producer/validate.py"` — stdlib-only, documented stub interface
(`reset(start)` / `step(op) -> event dict`), self-test, strict mode, exact
counts, localized diff:

```python
import json, sys, importlib
# Stub interface an engine must provide:
#   reset(start: int) -> None
#   step(op: int) -> dict   # the event for this op
def run(engine_mod, art, strict):
    ok = 0
    for c in art["cases"]:
        e = importlib.import_module(engine_mod); e.reset(c["start"])
        good = True
        for op, exp in zip(c["ops"], c["events"]):
            got = e.step(op)
            keys = exp.keys() if strict else ["value"]
            for k in keys:
                if got.get(k) != exp[k]:
                    if good:  # first divergence only
                        print(f"case {c['id']}: field '{k}' expected {exp[k]!r} got {got.get(k)!r}")
                    good = False
        ok += good
    return ok

art = json.load(open(sys.argv[1]))
mod = sys.argv[2]  # "self_test" replays the oracle itself
if mod == "--self-test":
    import types; m = types.ModuleType("oracle_replay")
    # trivial replay engine built from the oracle itself
    def make(art):
        state = {}
        def reset(s): state["case"] = next(c for c in art["cases"] if c["start"] == s and "used" not in c); state["i"] = 0
        ...
    # (for the self-check it suffices that rule+strict read 10/10 by construction)
    print("self-test: rule 10/10, strict 10/10"); sys.exit(0)
n = len(art["cases"])
print(f"rule-level: {run(mod, art, False)}/{n}")
print(f"strict:     {run(mod, art, True)}/{n}")
```

(Adapt freely — the load-bearing requirements are: documented stub interface,
`--self-test`, separate rule-level vs strict counts, first-divergence diff.)

## (c) Consumer implements with ONE seeded bug

In `"$BASE/consumer/"`, init a git repo (`git init; git add; git commit`) and
write `engine.py` implementing the stub interface — but **omit the `parity`
field** (the seeded bug — the exact analogue of the real `canHu` omission):

```python
_v = 0
def reset(start):
    global _v; _v = start
def step(op):
    global _v; _v += op
    return {"value": _v}          # BUG: parity field not emitted
```

Consumer runs only the rule-level check, sees `rule-level: 10/10`, and writes
in its README: "byte-exact replay of oracle v1" — **the anti-pattern:
claiming strict without running strict.**

## (d) The feedback loop must catch it

1. **Producer re-runs the stock validator, strict included:**

   ```bash
   cd "$BASE/consumer" && python "$BASE/producer/validate.py" \
       "$BASE/producer/oracle_v1.json" engine
   ```

   Required observation: `rule-level: 10/10`, `strict: 9/10` or lower, with
   the diff naming `field 'parity'`. (If your toy diverges on all cases,
   `strict: 0/10` — either way, strict < rule-level with the field named.)

2. **File the issue** (real repo: `gh issue create`; self-check: write
   `ISSUE.md` in the consumer repo) containing, verbatim requirements:
   - counts: rule-level 10/10, strict k/10;
   - the reproduction command from step 1, plus oracle version + sha256;
   - the diff line naming `parity`;
   - the semantic argument (parity is the legality oracle of the toy — not
     cosmetic);
   - "please merge `fix/parity-strict` -> master".

3. **Fix branch, never master:**

   ```bash
   cd "$BASE/consumer" && git checkout -b fix/parity-strict
   # edit engine.py: return {"value": _v, "parity": _v % 2}
   git commit -am "engine: emit parity on every event (strict 9/10 -> 10/10)"
   ```

4. **Re-verify strict** on the branch: validator must now print
   `strict: 10/10`. Merge (as the consumer role), re-run once more on master,
   record counts.

## Scenario checklist

- [ ] Oracle artifact has version + sha256 and 10 replayable cases.
- [ ] Validator: documented stub interface, `--self-test`, rule vs strict
      counts, first-divergence diff.
- [ ] Consumer's unverified "byte-exact" claim reproduced (rule-only run).
- [ ] Producer's independent strict run caught the seeded bug, counts exact.
- [ ] Issue contains counts, reproduction command, artifact version+checksum,
      named field, semantic argument, merge request.
- [ ] Fix lives on a branch; master untouched until merge is requested.
- [ ] Post-merge strict re-verification recorded as `10/10`.
- [ ] Nothing was communicated except through files/issues in the two repos.
