---
name: create-jira
description: Generate well-structured Jira ticket descriptions in markdown format from user-provided information
---

# Create Jira Ticket

Generate a well-structured Jira ticket description in markdown format based on the information provided by the user. Your role is to structure the content, NOT to implement, investigate, research, or gather additional information beyond what the user provides.

## Instructions

1. **Use ONLY user-provided information**: Do not investigate, research files, run commands, or gather additional context. If information is missing, note it in the output with placeholder text like `[To be provided]`.

2. **Generate description immediately**: Based on what the user provides, create a structured markdown description following the template below.

3. **Output format**: Generate markdown format (NOT Jira markup). The user will convert it as needed.

## Markdown Template

```markdown
## Description
[Clear explanation of the task and its purpose]

## Why
**Business Value / Problem to Solve:**
[Why is this task important? What problem does it solve? What impact will it have?]

## What
**Task Details:**
[What needs to be done? Be specific and break down if necessary]

## How
**Resources & Context:**

**Documentation:**
- [Link to relevant specs/documents]
- [Link to design files]

**Contacts:**
- [Subject matter expert name/contact]
- [Stakeholder name/contact]

**Additional Context:**
- [Notes from planning/grooming]
- [Technical considerations]
- [Dependencies or blockers]

**Attachments:**
- [Screenshots]
- [Design mockups]
- [Reference materials]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]
- [ ] [Criterion 3]
- [ ] [Criterion 4]

## Definition of Done
- [ ] Code implemented and reviewed
- [ ] Tests written and passing
- [ ] Documentation updated
- [ ] Deployed to [environment]
- [ ] Stakeholders notified
```

## Guidelines
- **DO NOT implement** anything described by the user, your job is to create the jira description nothing else.
- **DO NOT investigate or research** - use only what the user provides
- **DO NOT run tools** to gather information
- Format output in clean markdown
- Keep descriptions clear and actionable
- Focus on structuring the information provided
- Use placeholders like `[To be provided]` for missing information
- Be concise but thorough with the provided details