# Future Prompts & Resources

This document contains planned prompts and resources for future implementation, focused on enhancing the development experience.

---

## 1. Project Planning & Documentation

### Prompts

- **prd-create** : Generate comprehensive Product Requirements Documents with user stories, acceptance criteria, and success metrics
- **tech-spec-draft** : Create technical specifications for features including architecture decisions, data models, and API contracts
- **context-updater** : Update project context files (CLAUDE.md, AGENTS.md) with new architectural decisions and guidelines
- **changelog-generate** : Generate structured changelog entries from git commits following conventional commits format
- **api-docs-generate** : Create API documentation from code with endpoint descriptions, parameters, and examples
- **readme-improve** : Enhance README files with better structure, examples, and onboarding instructions

### Resources

- **prd-template** : Template for Product Requirements Documents with sections and examples
- **tech-spec-template** : Technical specification template with architecture decision records
- **documentation-style-guide** : Guidelines for consistent technical documentation across the project

---

## 2. Development Workflow

### Prompts

- **implement-tasks** : Break down and implement tasks from issue trackers with TDD approach and progress tracking
- **feature-scaffold** : Generate boilerplate code structure for new features (files, tests, configs)
- **branch-strategy** : Recommend git branching strategy and naming conventions for different work types
- **dependency-update** : Guide through safe dependency updates with changelog review and testing plan
- **refactor-plan** : Create step-by-step refactoring plan with risk assessment and rollback strategy
- **code-migration** : Guide migration between frameworks, languages, or architectural patterns

### Resources

- **coding-standards** : Team coding conventions, patterns, and anti-patterns reference
- **git-workflow-guide** : Comprehensive git workflow guide with common scenarios and solutions
- **task-breakdown-examples** : Examples of well-broken-down tasks from epic to implementation

---

## 3. Code Quality & Review

### Prompts

- **code-review-checklist** : Perform systematic code review using team-specific checklist and standards
- **security-scan** : Review code for security vulnerabilities following OWASP guidelines
- **performance-audit** : Analyze code for performance bottlenecks and optimization opportunities
- **accessibility-check** : Review frontend code for WCAG compliance and accessibility best practices
- **tech-debt-assessment** : Identify and prioritize technical debt with effort/impact analysis
- **code-smell-detector** : Identify code smells and suggest refactoring patterns

### Resources

- **code-review-standards** : Code review guidelines with examples of good/bad patterns
- **security-checklist** : Security review checklist with common vulnerabilities and fixes
- **performance-patterns** : Common performance patterns and anti-patterns with benchmarks

---

## 4. Testing & Debugging

### Prompts

- **test-plan-create** : Generate comprehensive test plans with test cases, edge cases, and coverage goals
- **unit-test-generate** : Create unit tests for existing code with mocks and assertions
- **integration-test-design** : Design integration tests for APIs, databases, and external services
- **debug-assistant** : Guide through debugging process with hypothesis testing and root cause analysis
- **error-analyze** : Analyze error messages, stack traces, and logs to identify root causes
- **test-coverage-improve** : Identify gaps in test coverage and generate tests for untested code paths

### Resources

- **testing-strategies** : Testing pyramid, test types, and when to use each approach
- **debugging-checklist** : Systematic debugging approach with common pitfalls
- **test-examples** : Well-written test examples for different patterns (unit, integration, e2e)

---

## 5. API & Integration

### Prompts

- **api-design** : Design RESTful or GraphQL APIs with resource modeling and endpoint specifications
- **openapi-generate** : Generate OpenAPI/Swagger specifications from code or requirements
- **api-client-create** : Create API client libraries with error handling and retry logic
- **webhook-implement** : Implement webhook receivers with validation, security, and retry handling
- **integration-plan** : Plan third-party integrations with authentication, rate limiting, and error handling
- **graphql-schema-design** : Design GraphQL schemas with types, queries, mutations, and resolvers

### Resources

- **api-design-principles** : REST/GraphQL design principles and best practices
- **api-security-guide** : API authentication, authorization, and security patterns
- **integration-patterns** : Common integration patterns (pub/sub, polling, webhooks, etc.)

---

## 6. DevOps & Deployment

### Prompts

- **ci-cd-setup** : Configure CI/CD pipelines with testing, building, and deployment stages
- **docker-optimize** : Optimize Dockerfiles and docker-compose configurations for size and performance
- **deployment-checklist** : Pre-deployment verification checklist with rollback procedures
- **monitoring-setup** : Set up application monitoring, logging, and alerting infrastructure
- **infrastructure-as-code** : Generate Terraform/CloudFormation templates for infrastructure
- **release-notes-create** : Generate user-facing release notes from changelog and commits

### Resources

- **deployment-guide** : Step-by-step deployment procedures for different environments
- **monitoring-standards** : What to monitor, alert thresholds, and incident response
- **infrastructure-patterns** : Common infrastructure patterns (load balancing, caching, scaling)

---

## 7. Team Collaboration

### Prompts

- **onboarding-guide** : Generate onboarding documentation for new team members
- **issue-triage** : Triage and categorize issues with priority, effort, and assignment recommendations
- **sprint-planning-assistant** : Help plan sprints with capacity planning and story point estimation
- **postmortem-create** : Guide through creating postmortem documents after incidents
- **architecture-decision** : Document architecture decisions with context, options, and trade-offs
- **meeting-notes-structure** : Structure meeting notes with action items, decisions, and follow-ups

### Resources

- **onboarding-template** : Template for team onboarding with checklists and resources
- **sprint-planning-guide** : Sprint planning best practices and estimation techniques
- **adr-template** : Architecture Decision Record template (Lightweight ADR format)

---

## 8. Data & Database

### Prompts

- **database-schema-design** : Design database schemas with normalization, indexes, and constraints
- **migration-create** : Generate database migrations with rollback scripts
- **query-optimize** : Analyze and optimize SQL queries for performance
- **data-validation** : Create data validation schemas (JSON Schema, Pydantic, Zod)
- **etl-pipeline-design** : Design ETL/ELT pipelines for data processing

### Resources

- **database-patterns** : Common database patterns and when to use them
- **sql-optimization-guide** : SQL query optimization techniques with examples
- **data-modeling-guide** : Data modeling best practices and normalization rules

---

## Implementation Priority

When implementing these prompts and resources, consider prioritizing based on:

1. **Most Frequent Use Cases** - Start with prompts that will be used daily in development workflow
2. **Highest Impact** - Focus on prompts that save the most time or prevent critical issues
3. **Dependencies** - Implement resources before their corresponding prompts
4. **Team Needs** - Align with current team pain points and workflow gaps

## Contributing

When implementing prompts from this list:

1. Follow the prompt template in `resources/prompt-template.md`
2. Include appropriate YAML frontmatter (name, description, arguments)
3. Use markdown-first structure with XML only when necessary
4. Add corresponding resources to support complex prompts
5. Test prompts with real-world scenarios before committing
6. Update this document to mark completed items

---

**Note**: This is a living document. Add new ideas as they emerge and remove items as they're implemented.
