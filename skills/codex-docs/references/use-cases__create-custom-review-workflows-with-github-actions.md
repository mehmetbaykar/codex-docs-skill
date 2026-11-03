---
title: "Create custom review workflows with GitHub Actions"
source: https://learn.chatgpt.com/use-cases/create-custom-review-workflows-with-github-actions
path: /use-cases/create-custom-review-workflows-with-github-actions
---

# Create custom review workflows with GitHub Actions

Run security checks on your own triggers and keep the results for review.

Make security reviews a repeatable part of your development process. Configure a GitHub Actions workflow that runs Codex Security on proposed changes and saves the results for your team to inspect.

## Recipe details

```yaml
name: Create custom review workflows with GitHub Actions
tagline: Run security checks on your own triggers and keep the results for review.
summary: Make security reviews a repeatable part of your development process.
  Configure a GitHub Actions workflow that runs Codex Security on proposed
  changes and saves the results for your team to inspect.
bestFor:
  - Platform and application security teams adding security checks to GitHub
    Actions.
  - Repository maintainers configuring custom review triggers and scan scope.
  - Teams that need repeatable reviews with saved findings, evidence, and
    coverage reports.
relatedLinks:
  - label: Run Codex Security in GitHub Actions
    url: https://learn.chatgpt.com/docs/security/cli/ci/github
  - label: Save reports and upload SARIF results
    url: https://learn.chatgpt.com/docs/security/cli/ci/github#save-reports-and-upload-sarif
  - label: Explore CI/CD integrations and enforcement options
    url: https://learn.chatgpt.com/docs/security/cli/ci
```

Instead of enforcing security reviews through Codex, it is also possible to create custom workflows that run the Codex Security CLI. We’ve packaged this workflow to easily be used as a GitHub Action.
```yaml
name: Codex Security review
on:
  workflow_dispatch:
  schedule:
    - cron: '23 7 * * 1' # Mondays at 07:23 UTC

permissions:
  contents: read

jobs:
  security:
    runs-on: ubuntu-24.04
    steps:
      - name: Set up the Ubuntu sandbox
        run: |
          sudo apt-get update
          sudo apt-get install --yes bubblewrap apparmor-profiles
          sudo apparmor_parser -r /usr/share/apparmor/extra-profiles/bwrap-userns-restrict

      - uses: actions/checkout@3d3c42e5aac5ba805825da76410c181273ba90b1 # v7.0.1
        with:
          persist-credentials: false
      - uses: openai/codex-security@3f61e5150981a5087c32e4395bbaa8ce5ce0c3e3 # action-v0.3.0
        with:
          model: gpt-5.6-sol
          effort: high
        env:
          OPENAI_API_KEY: ${{ secrets.CODEX_SECURITY_API_KEY }}
```

These workflows can also be applied to other source code management tools like GitLab, BitBucket, or Jenkins. Take a look at our documentation page to learn more: [Run Codex Security in CI](https://developers.openai.com/codex/security/cli/ci).
