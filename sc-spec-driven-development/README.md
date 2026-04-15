# Spec-Driven Development Course

This repository contains the companion code for the DeepLearning.AI Spec-Driven Development course. Each lesson folder holds the complete project state you need to follow along with that lesson's video.

## How to use this repo

The simplest way to take this course is to start at Lesson 4 and follow along with each video, building the project as you go.

Each `Lesson_N` folder contains a snapshot of the AgentClinic project as it should look **at the start** of that lesson. You don't need to copy these folders each time -- they're here so you can jump into any lesson without having completed the previous ones. If you want to start fresh at a specific lesson, just copy that folder into your own working directory:

```bash
cp -r Lesson_05/ my-agentclinic/
cd my-agentclinic
npm install
```

## Lesson overview

| Folder | Lesson | What you're starting with |
|--------|--------|--------------------------|
| Lesson_04 | Creating the Constitution | Empty project scaffold (package.json, tsconfig.json, src/index.ts) |
| Lesson_05 | Feature Specification | Constitution in place (specs/mission.md, tech-stack.md, roadmap.md) |
| Lesson_06 | Feature Implementation | Constitution + Phase 1 feature spec (plan.md, requirements.md, validation.md) |
| Lesson_07 | Feature Validation | Phase 1 "Hello Hono" fully implemented with layout components |
| Lesson_08 | Project Replanning | Phase 1 merged to main, ready for replanning |
| Lesson_09 | 2nd Feature Phase | Replanning complete (testing, responsive design, changelog skill added) |
| Lesson_10 | MVP | Phase 2 "Agents & Ailments" merged, full app ready for MVP sprint |
| Lesson_11 | Legacy Support | MVP fully implemented, ready for legacy SDD introduction |
| Lesson_12 | Build Your Own Workflow | Rebuilt legacy constitution + Feedback Form feature implemented |
| Lesson_13 | Agent Replaceability | Feedback Form merged, feature-spec skill created, next feature spec drafted, backlog/ with research notes |

Lessons 1-3 (Introduction, Workflow Overview, and Setup) are conceptual and do not have starter code.

## Other directories

- **`skills/`** -- Reusable agent skills developed during the course (changelog, feature-spec).
- **`example_specs/`** -- Example specification documents referenced in the course.

## Prerequisites

- Node.js (v18+)
- Git
- A coding agent (the course uses Claude Code, but the workflow is agent-agnostic)
- An IDE or editor (the course uses [WebStorm](https://www.jetbrains.com/webstorm/download/))
