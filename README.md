# Dendron Compiler

A simple python tool to compile dendron vault to static html files.

Supported

- Markmap

## How to use it

```bash
python3 src/compile.py <dendron-repository>
```

If you want to enable markmap compilation, add special meta to your dendron note.

```text
---
gramma: markmap
---
```

Then, the tool will compile the dendron note to mindmap html file.

## Why

I try to use visual studio code plugin 'Dendron' and 'Markmap' together. But it is not a happy journey.

- When I tried to publish dendron vault, some problems were encounterd and hard to be solved.
- The offical publish mechanism is not flexible enough to be used with other tools.

So I try to build a simple tool to compile dendron vault to static html files.

## Plan

I will explore the workflow of dendron, and try to find more useful features.

- [ ] Support more meta tags in dendron notes, such as `tag`, etc.
- [ ] Support Mermaid, etc.

## Others

This repository is still in **WIP** status for the reason that I am not a deep user of dendron. So I don't have a clear idea about the final goal.

Any suggestions and contributions are welcome.

Feel free to open an issue or pull request.
