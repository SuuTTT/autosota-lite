# JAX Rewrite Guidance

Use this reference when rewriting a slow implementation in JAX.

## Rewrite Strategy

Start from a source-faithful implementation, then move performance-critical work into JAX:

1. Identify Python-loop bottlenecks, tiny tensor ops, data transfer points, and slow batch construction.
2. Define immutable train state with params, optimizer state, RNG, and step.
3. Write pure `loss_fn`, `train_step`, and `eval_step` functions.
4. Use `jax.jit` for steady-state train and eval steps.
5. Use `jax.vmap`, `lax.scan`, or batched environments to replace Python loops.
6. Keep host-side logging, checkpointing, and dataset IO outside compiled functions.
7. Report compile time separately from steady-state throughput.

## Preferred Libraries

- Use JAX plus Optax for optimizers.
- Use Flax or Equinox only when it reduces complexity for the target repo.
- Use Orbax or a simple structured checkpoint when the repo already has no checkpoint standard.
- Use framework-native data prefetching where available, but keep the batch contract explicit.

## RNG Rules

- Maintain a single explicit PRNG key in train state or run state.
- Split keys at the callsite where randomness is consumed.
- Log the seed and any per-device seed derivation.
- Avoid hidden global randomness.

## Compilation Rules

- Keep static arguments minimal and intentional.
- Avoid recompilation from changing shapes, Python objects, or data-dependent control flow.
- Warm up once before timing steady-state throughput.
- Track shape polymorphism or padding decisions in `porting_notes.md`.

## Parity Checks

Before trusting a JAX rewrite, compare against the source or PyTorch reference:

- Input preprocessing output on a tiny fixed batch.
- Model parameter count and major tensor shapes.
- Forward output shape and finite values.
- Loss value trend on a fixed tiny batch when exact equality is unrealistic.
- One optimizer update changes the expected parameter leaves.
- Eval metric direction and output format.

## Performance Report

Record:

- Hardware and accelerator type.
- JAX, jaxlib, CUDA, cuDNN, and Python versions when available.
- First-step compile time.
- Steady-state steps per second or samples per second.
- Peak memory.
- Batch size, precision, and parallelism settings.
- Any semantic differences from the canonical implementation.

## Common Traps

- Timing the compile step as steady-state training.
- Accidentally recompiling every step because a Python object changes.
- Moving dataset IO into `jit`.
- Hiding RNG in module state.
- Treating a speed approximation as the canonical reproduction.
- Reporting faster throughput without checking metric parity.
