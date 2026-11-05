---
title: "Administration"
source: https://learn.chatgpt.com/docs/administration
path: /docs/administration
---

# Administration

Set access and policy boundaries for ChatGPT, Codex developer tools, APIs, plugins, and connected systems.

Start with the rollout guide, then set up identity and access. Use Configuration for app installation, updates, and workspace policies. Use Advanced deployment for Amazon Bedrock, Bedrock in GovCloud, or an organization gateway. Browse the sections for feature controls, usage, and security.

[Start your rollout](https://learn.chatgpt.com/docs/enterprise/admin-setup)

## Getting started

Plan your rollout and explore tools for routine administration.

- [Admin rollout guide](https://learn.chatgpt.com/docs/enterprise/admin-setup): Plan access, assign owners, configure controls, and verify the rollout.
- [Admin plugin](https://learn.chatgpt.com/docs/enterprise/admin-plugin): Use the Admin plugin for permissions, approvals, and supported administrative workflows.

## Feature Configuration

Choose a setup task, then review its access and security requirements.

- [Configure dots permissions](https://learn.chatgpt.com/docs/enterprise/dots-admin-guide): Manage dots access, communication, computers, and custom rules.
- [Manage Space sharing and access](https://learn.chatgpt.com/docs/space/collaboration#for-workspace-admins): Control Library sharing permissions and help members share pages.
- [Sites administration](https://learn.chatgpt.com/docs/enterprise/sites): Enable sites, configure connections, and review hosting, access controls, and data responsibilities.
- [Set up teams and Team Tasks](https://learn.chatgpt.com/docs/enterprise/teams#for-workspace-admins): Set team permissions, connect shared accounts, and create recurring tasks.
- [Set up @ChatGPT in Slack or Teams](https://learn.chatgpt.com/docs/enterprise/chatgpt-slack-and-teams): Review administrator responsibilities and deployment prerequisites.
- [Set up a workspace connection](https://learn.chatgpt.com/docs/enterprise/shared-connections#set-up-a-connection): Prepare company-managed accounts and configure a workspace connection.
- [Local computer access for Work Cloud and dots](https://learn.chatgpt.com/docs/enterprise/cloud-local-access#how-to-set-up-local-computer-access): Review shared policies and compatibility, then enable local computer access separately for Work and dots.

## Identity and access

Manage sign-in, provisioning, roles, and credentials.

- [Authentication overview](https://learn.chatgpt.com/docs/auth): Compare sign-in methods, credential storage, and enforcement controls.
- [Groups and provisioning](https://learn.chatgpt.com/docs/enterprise/groups-and-provisioning): Compare membership sources and understand group permissions.
- [Dynamic groups](https://learn.chatgpt.com/docs/enterprise/dynamic-groups): Manage group membership with rules based on SCIM user attributes.
- [User lifecycle management](https://learn.chatgpt.com/docs/enterprise/user-lifecycle): Provision employees, update group access, and revoke departing users' credentials.
- [Roles and workspace permissions](https://learn.chatgpt.com/docs/enterprise/roles-and-workspace-permissions): Find workspace, runtime, API, plugin, and source-system controls.
- [Personal access tokens](https://learn.chatgpt.com/docs/enterprise/access-tokens): Create and manage tokens for programmatic access.
- [Service accounts](https://learn.chatgpt.com/docs/enterprise/service-accounts): Create and manage workspace identities for automated workflows.

## Configuration

Manage app installation, updates, runtime settings, remote connections, and workspace model availability.

- [Windows app and CLI deployment](https://learn.chatgpt.com/docs/enterprise/windows-deployment): Deploy the Windows app and Codex CLI on managed Windows devices.
- [Run Codex with an NFS home directory](https://learn.chatgpt.com/docs/environments/network-file-systems): Migrate a shared Linux home, verify cross-host resume, or keep independent jobs on local scratch.
- [Manage app updates](https://learn.chatgpt.com/docs/enterprise/manage-app-updates): Control desktop app updates and deploy approved versions through your device management platform.
- [Managed configuration](https://learn.chatgpt.com/docs/enterprise/managed-configuration): Review the global baseline in Agent Security, policy precedence for this feature, and supported runtime requirements.
- [Self-host Codex configuration for your team](https://learn.chatgpt.com/docs/enterprise/configuration-server): Serve Codex defaults and required settings from your own HTTPS endpoint.
- [Codex security cookbook](https://learn.chatgpt.com/docs/enterprise/security-cookbook): Configure and verify enterprise security controls, then combine them for common security goals.
- [Remote connections](https://learn.chatgpt.com/docs/remote-connections): Start and control work on connected computers.
- [Workspace model availability](https://learn.chatgpt.com/docs/enterprise/workspace-model-availability): Separate model access for ChatGPT, Codex in the ChatGPT desktop app, Codex CLI, the IDE extension, Codex cloud, and the Platform API.

## Advanced deployment

Connect directly to Amazon Bedrock, configure Bedrock in GovCloud, or deploy an organizational gateway that routes requests to your inference provider.

- [Amazon Bedrock](https://learn.chatgpt.com/docs/amazon-bedrock): Configure supported local clients to use models available through Bedrock.
- [GovCloud deployment](https://learn.chatgpt.com/docs/enterprise/govcloud-configuration): Configure local Codex workflows with Amazon Bedrock in AWS GovCloud.
- [Connect to a gateway](https://learn.chatgpt.com/docs/enterprise/connect-to-a-gateway): Connect to your organization's model gateway with or without ChatGPT sign-in.
- [Roll out a gateway](https://learn.chatgpt.com/docs/enterprise/roll-out-a-gateway): Configure model routes, issue credentials, and deploy Codex through your organization’s gateway.

## ChatGPT EDU

Compare education plans and configure access for your institution.

- [Education plans](https://learn.chatgpt.com/docs/enterprise/education-plans): Compare plans, help members get access, and manage multiple workspaces.
- [Higher education setup](https://learn.chatgpt.com/docs/enterprise/higher-education-roles-and-permissions): Choose campus roles, compare recommended permissions, and verify access.

## ChatGPT Work

Review the ChatGPT Work overview and administration reference.

- [Overview](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-overview): Understand local and cloud execution, Local computer access with Work Cloud, network controls, and data boundaries.
- [Cloud security](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-cloud-security): Review hosted execution, connected accounts, access controls, retention, and audit visibility.
- [Local security](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-local-security): Review local execution, device and browser access, managed policies, data handling, and audit limitations.
- [Usage and cost](https://learn.chatgpt.com/docs/enterprise/chatgpt-work-usage-and-cost): Understand shared credits, billing impact, spending controls, and adoption planning.
- [Admin FAQ](https://learn.chatgpt.com/docs/enterprise/work-admin-faq): Review access, data, governance, usage, and incident controls for ChatGPT Work.

## Collaboration and sharing

Manage GPT sharing and ownership.

- [GPTs and sharing](https://learn.chatgpt.com/docs/enterprise/gpts-and-sharing): Manage GPT sharing, ownership, connected apps, and third-party actions across your workspace.

## Plugins and connections

Control plugin installation, bundled skills, connector-backed capabilities, and connected-service access.

- [Plugin controls](https://learn.chatgpt.com/docs/enterprise/apps-and-connectors): Manage plugin availability, connector access and actions, and source-system permissions.
- [Import and sync plugins from GitHub](https://learn.chatgpt.com/docs/enterprise/plugin-management): Import and sync workspace plugins from GitHub.
- [Skill controls](https://learn.chatgpt.com/docs/enterprise/skills): Compare ChatGPT workspace, local filesystem, and plugin skill controls.
- [Migrate custom GPTs to plugins](https://learn.chatgpt.com/docs/migrate-custom-gpts): Plan your workspace transition, migrate individual GPTs or eligible batches, and test and share replacement plugins.

## Usage and analytics

Review workspace usage and adoption, and automate reporting.

- [Workspace analytics](https://learn.chatgpt.com/docs/enterprise/workspace-analytics): Review workspace-level ChatGPT adoption and Codex usage.
- [Usage Insights](https://learn.chatgpt.com/docs/enterprise/usage-insights): Explore usage across ChatGPT Work and Codex and assess workflow results with your team.
- [Analytics API](https://learn.chatgpt.com/docs/enterprise/analytics-api): Automate developer activity and code review reporting with the Codex Analytics API.

## Security and compliance

Review workspace security policies, governance, and audit controls.

- [Governance](https://learn.chatgpt.com/docs/enterprise/governance): Choose the right analytics, spend, and audit surface for each question.
- [Agent security](https://learn.chatgpt.com/docs/enterprise/agent-security): Manage the Global policy baseline and supported Local and Codex Cloud environment settings.
- [Safety and security in dots](https://learn.chatgpt.com/docs/enterprise/dots-security): Review dots security controls, data handling, and audit and offboarding considerations.
- [Prisma AIRS](https://learn.chatgpt.com/docs/enterprise/prisma-airs): Apply workspace-wide security policies to Codex prompts.
- [HIPAA configuration](https://learn.chatgpt.com/docs/hipaa-configuration): Configure local runtime safeguards for workflows that may handle protected health information.
- [Compliance API and audit events](https://learn.chatgpt.com/docs/enterprise/compliance-api): Export activity records for audit and investigation workflows.
