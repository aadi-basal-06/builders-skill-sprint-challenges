# Challenge 5 (Innovate): Build Your Own 🚀

## Goal
Now you know the pattern: **create something → break it → ask the agent → fix it.** For this challenge, **invent your own break** and show the agent solving it. Most creative one gets a **shoutout!** 🏆

## Rules
- Use your existing Agent Space (`bss-may-2026`).
- Make your **own** broken scenario — don't just repeat challenges 1–4.
- Show the agent investigating it and giving a root cause.

## Easy ways to make your own break
You don't need anything fancy. Pick one:

- 🧨 **Break a different service** — make an S3 bucket, DynamoDB table, or API Gateway, then misconfigure it (wrong permission, bad setting) and ask the agent.
- 🐌 **Different failure** — instead of CPU, make a Lambda **time out** (add `import time; time.sleep(60)` with the timeout set to 5 seconds), or run several `yes > /dev/null &` processes to spike CPU and ask about it.
- 💸 **Cost or config** — leave something misconfigured and ask the agent for prevention tips.
- 💬 **Connect a tool** — wire the agent to **Slack** and run an investigation from there.
- 📋 **Write a runbook (Skill)** — give the agent a short markdown "runbook" for your scenario and show it following your steps.

## What to Submit
Create a file **`FINDINGS.md`** in this folder (`challenge-5-build-your-own-agentic-sre/`) using this template:

```markdown
# Challenge 5 — Findings

## What I built and how I broke it
(describe your scenario)

## What the agent found
(the root cause it identified, in your own words)

## Fix applied
(what you changed to resolve it)

## Evidence
- [ ] Screenshot or short recording of the agent investigating your break
- [ ] Screenshot of recovery (if your scenario has a fix)
- [ ] Bonus: Slack integration / runbook / coding-assistant fix
```

Then submit it at [awsugmdu.in](https://www.awsugmdu.in/), with your screenshot or recording attached.

## Judging

| Criteria | Weight |
|----------|--------|
| **Creativity** — is the scenario original? | ⭐⭐⭐ |
| **It works** — did the agent actually investigate it? | ⭐⭐⭐ |
| **Clarity** — can we understand your break & fix? | ⭐⭐ |
| **Bonus** — Slack, a runbook, or a coding-assistant fix | ⭐ |

## Resources
- [About AWS DevOps Agent](https://docs.aws.amazon.com/devopsagent/latest/userguide/about-aws-devops-agent.html)
- [Kiro](https://kiro.dev/) — let a coding assistant write your fix

## ⚠️ Cleanup
Delete any stacks/resources you created (CloudFormation → **Delete**). See [COST-AND-CLEANUP.md](../COST-AND-CLEANUP.md).

**Surprise us! 🚀**
