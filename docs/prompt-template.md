---
name: prompt-template
description: Template and best practices for writing effective MCP prompts
---

# Prompt Template & Best Practices

This document provides a structured template for creating effective prompts in the MCP Prompt Server, following Claude's prompt engineering best practices.

---

## Template Structure

Use the following structure when creating prompts. Sections marked **(optional)** can be omitted for simple prompts.

### 1. Context

**Purpose:** Provide background information, role definition, and situational context that Claude needs to understand the task.

**Guidelines:**
- Be clear and direct about what Claude needs to know
- Define Claude's role or perspective (e.g., "You are an expert software architect")
- Include relevant domain knowledge or constraints
- Place critical context at the beginning and end (primacy and recency effects)

**Example:**
```markdown
## Context

You are a senior Python developer with expertise in secure API design. You are reviewing code for a financial services application that handles sensitive customer data. Security and data privacy are top priorities.
```

---

### 2. Variables **(optional)**

**Purpose:** Define dynamic inputs that will be filled in when the prompt is used. Useful for reusable prompt templates.

**Guidelines:**
- Use clear, descriptive variable names
- Specify expected format or type
- Provide defaults if applicable
- Use markdown formatting for variable placeholders

**Example:**
```markdown
## Variables

- **Input File Path**: `path/to/source/code.py`
- **Security Level**: `high`
- **Output Format**: `markdown`
```

---

### 3. Instructions

**Purpose:** Clear, actionable directives that specify exactly what Claude should do.

**Guidelines:**
- Use imperative language ("Analyze", "Generate", "Review")
- Be specific and unambiguous
- Break down complex instructions into numbered steps
- Order instructions sequentially
- Use markdown lists and formatting for clarity

**Example:**
```markdown
## Instructions

1. Analyze the provided code for security vulnerabilities
2. Identify any instances of hardcoded credentials or secrets
3. Check for proper input validation and sanitization
4. Evaluate error handling and logging practices
5. Assess authentication and authorization mechanisms
```

---

### 4. Constraints **(optional)**

**Purpose:** Define boundaries, limitations, or requirements that must be respected in the output.

**Guidelines:**
- Specify what Claude should NOT do
- Define output length or format restrictions
- Set quality or compliance requirements
- Use clear, enforceable statements

**Example:**
```markdown
## Constraints

- Do not suggest solutions that require external dependencies beyond the Python standard library
- Limit recommendations to a maximum of 10 items
- All suggestions must be compatible with Python 3.11+
- Do not include opinionated style preferences unless they affect security
```

---

### 5. Workflow

**Purpose:** Define the sequential steps or logical flow for processing the task. Essential for complex, multi-step operations.

**Guidelines:**
- Use numbered steps for sequential processes
- Use XML tags **only** for conditional branches or emphasis
- Clearly define decision points
- Specify what happens at each stage
- Include validation or checkpoint steps

**Example:**
```markdown
## Workflow

1. Parse the input file and extract all function definitions

2. For each function, perform security analysis:
   - Check for SQL injection vulnerabilities
   - Verify input sanitization
   - Assess authentication requirements
   - Assign severity rating (critical, high, medium, low)
   - Document the specific vulnerability

3. <conditional>
   IF critical vulnerabilities found:
     - Flag for immediate review
     - Generate detailed remediation steps
   ELSE:
     - Proceed with standard reporting
   </conditional>

4. Compile findings into structured report
```

---

### 6. Process **(optional)**

**Purpose:** Describe the thinking methodology or approach Claude should use. Different from workflow—this is about *how* to think, not *what* to do.

**Guidelines:**
- Encourage chain-of-thought reasoning
- Define evaluation criteria
- Specify thinking techniques (e.g., "think step-by-step")
- Use markdown for structure; XML only for emphasis

**Example:**
```markdown
## Process

### Reasoning Approach

Use chain-of-thought reasoning for each code section:

1. State what the code is attempting to do
2. Identify potential security risks
3. Consider attack vectors
4. Evaluate severity and likelihood
5. Propose mitigation strategies

### Evaluation Criteria

- **Severity**: Impact if exploited (data loss, unauthorized access, system compromise)
- **Exploitability**: How easy is it to exploit this vulnerability?
- **Context**: Does the deployment environment increase or decrease risk?
```

---

### 7. Reporting **(optional)**

**Purpose:** Specify the exact format, structure, and content of Claude's output.

**Guidelines:**
- Define output structure clearly
- Provide examples of expected format
- Specify required sections
- Use markdown formatting for output structure
- Consider using prefill techniques for consistent formatting

**Example:**
```markdown
## Reporting

Format your response as follows:

# Security Analysis Report

## Executive Summary
[Brief overview of findings, 2-3 sentences]

## Critical Findings
[List any critical vulnerabilities]

## Detailed Analysis

### Finding 1: [Title]
- **Severity**: [Critical/High/Medium/Low]
- **Location**: [File:Line]
- **Description**: [Detailed explanation]
- **Recommendation**: [Specific fix]
- **Code Example**: [Proposed solution]

[Repeat for each finding]

## Summary Statistics
- Total issues found: [N]
- Critical: [N] | High: [N] | Medium: [N] | Low: [N]
```

---

## Best Practices

### 1. Clarity and Precision
- Use clear, unambiguous language
- Avoid jargon unless necessary for the domain
- Be specific about expectations
- Define technical terms if they have multiple meanings

### 2. Prefer Markdown Over XML

**Use Markdown by default** for structure and formatting:
- Headings (`##`, `###`)
- Lists (`-`, `1.`)
- Code blocks (` ``` `)
- Tables
- Bold/italic text

**Use XML tags only when:**
- Emphasizing critical information that must not be missed
- Defining conditional logic or branching workflows
- Separating distinct data structures that need parsing
- Creating nested hierarchies that markdown can't express well

**Good Example (Markdown-first):**
```markdown
## Instructions

1. Review the code for security issues
2. For each issue found:
   - Document the severity
   - Provide a fix
   - Include code examples
```

**XML Usage (When needed for emphasis):**
```markdown
## Instructions

1. Review the code for security issues
2. For each issue found:
   - Document the severity
   - Provide a fix
   - Include code examples

<critical>
IMPORTANT: If you find any hardcoded passwords or API keys, flag them immediately as CRITICAL priority regardless of other severity criteria.
</critical>
```

### 3. Examples (Multishot Prompting)
- Provide examples of desired input/output when possible
- Include both good and bad examples if relevant
- Show edge cases
- Use markdown code blocks for examples

**Example:**
```markdown
## Examples

### Good Example
```python
user_input = request.form.get('username')
sanitized = sanitize_input(user_input)
query = db.execute("SELECT * FROM users WHERE username = ?", (sanitized,))
```
**Status**: Properly sanitized with parameterized query

### Bad Example
```python
user_input = request.form.get('username')
query = db.execute(f"SELECT * FROM users WHERE username = '{user_input}'")
```
**Issue**: SQL injection vulnerability - no sanitization, string interpolation
**Fix**: Use parameterized queries
```

### 4. Context Placement
- Put critical information at the **beginning** and **end** of prompts
- Long context should be placed early
- Final instructions should reinforce key requirements
- Use "**Important:**" or "**Note:**" for emphasis in markdown

### 5. Chain of Thought
- For complex reasoning, explicitly ask Claude to think step-by-step
- Use phrases like:
  - "Let's approach this step-by-step"
  - "First, consider... then..."
  - "Before providing recommendations, analyze..."

### 6. Output Prefilling
- Use system prompts to prefill the start of Claude's response
- Ensures consistent formatting
- Guides the structure of the output

**Example:**
```
User: [Your prompt]
Assistant: # Security Analysis Report

I'll analyze the code systematically for security vulnerabilities.

## Executive Summary
```

---

## Simple Prompt Example

For straightforward tasks, you can use a minimal structure:

```yaml
---
name: code-review-simple
description: Basic code review for Python scripts
---

# Code Review Prompt

## Context

You are a Python code reviewer focusing on code quality and best practices.

## Instructions

1. Review the provided Python code
2. Identify potential bugs or anti-patterns
3. Suggest improvements for readability and maintainability
4. Provide specific code examples for your suggestions

## Reporting

Format your response with:
- Issue description
- Location in code
- Suggested fix with code example
```

---

## Complex Prompt Example

For sophisticated multi-step tasks:

```yaml
---
name: security-audit-comprehensive
description: Comprehensive security audit for Python web applications
---

# Comprehensive Security Audit

## Context

You are a senior security engineer conducting a security audit for a Python web application handling financial transactions. The application must comply with PCI DSS standards and protect sensitive customer data.

## Variables

- **Codebase Path**: `./src`
- **Compliance Standard**: PCI DSS 4.0
- **Risk Tolerance**: Low

## Instructions

Perform a comprehensive security audit of the provided codebase:

### Phase 1: Static Analysis
1. Static code analysis for common vulnerabilities
2. Review authentication and authorization mechanisms
3. Analyze data handling and storage practices
4. Evaluate API security and input validation

### Phase 2: Compliance & Monitoring
5. Assess logging and monitoring implementation
6. Review error handling and information disclosure
7. Check for secure dependency management
8. Evaluate cryptographic implementations

## Constraints

- Focus on vulnerabilities that could lead to data breaches
- Consider OWASP Top 10 categories
- Prioritize findings by severity and exploitability
- Provide actionable remediation steps
- Do not report false positives without verification

## Workflow

1. **Discovery Phase**
   - Scan all Python files in the codebase
   - Identify entry points and data flows
   - Map authentication boundaries

2. **Analysis Phase**

   For each identified component:
   - Apply security checks from OWASP guidelines
   - Cross-reference against known CVEs
   - Evaluate against PCI DSS requirements

   <conditional>
   IF vulnerability detected:
     - Document with severity rating
     - Identify affected code locations
     - Research exploitation scenarios
   </conditional>

3. **Validation Phase**
   - Verify each finding to minimize false positives
   - Test edge cases where applicable
   - Consider deployment context

4. **Reporting Phase**
   - Compile all findings
   - Sort by severity (critical → low)
   - Generate remediation roadmap

## Process

### Thinking Approach

Use systematic reasoning for each potential vulnerability:

1. **Identification**: What is the potential issue?
2. **Context**: Where does it occur and why does it exist?
3. **Impact**: What could an attacker achieve?
4. **Likelihood**: How easy is it to exploit?
5. **Mitigation**: What specific code changes fix this?

### Severity Matrix

- **Critical**: Direct path to data breach or system compromise
- **High**: Requires minimal effort to exploit, significant impact
- **Medium**: Requires specific conditions, moderate impact
- **Low**: Difficult to exploit or minimal impact

<critical>
IMPORTANT: Any vulnerability that allows direct access to customer financial data or PII must be classified as CRITICAL, regardless of exploitability difficulty.
</critical>

## Reporting

Structure your output as follows:

# Security Audit Report

## Executive Summary
[2-3 paragraphs: overall security posture, critical findings, key recommendations]

## Compliance Status
- **PCI DSS 4.0 Compliance**: [Pass/Fail with justification]
- **Critical compliance gaps**: [List]

## Vulnerability Summary

| Severity | Count | Status |
|----------|-------|--------|
| Critical | N     | Action Required |
| High     | N     | Action Required |
| Medium   | N     | Review Recommended |
| Low      | N     | Monitor |

## Detailed Findings

### [Finding ID]: [Vulnerability Title]

**Severity**: Critical/High/Medium/Low
**CWE**: [CWE Number and Name]
**OWASP Category**: [OWASP Top 10 Category]
**PCI DSS Requirement**: [Relevant requirement number]

**Location**:
- File: `path/to/file.py`
- Lines: XX-YY
- Function: `function_name()`

**Description**:
[Detailed technical explanation of the vulnerability]

**Proof of Concept**:
```python
# Example of how this could be exploited
```

**Impact**:
[What an attacker could achieve by exploiting this]

**Recommendation**:
[Specific, actionable steps to fix]

**Remediation Code**:
```python
# Secure implementation
```

**Effort**: Low/Medium/High
**Priority**: P0/P1/P2/P3

---

## Remediation Roadmap

### Immediate Actions (P0 - Critical)
1. [Action item with file reference]
2. [Action item with file reference]

### Short-term (P1 - Within 30 days)
[List prioritized actions]

### Medium-term (P2 - Within 90 days)
[List recommended improvements]

### Long-term (P3 - Ongoing)
[List best practice enhancements]

## Positive Security Practices Observed
[List things done well - encourages good practices]

## Testing Recommendations
[Suggested security testing approaches post-remediation]
```

---

## When to Use XML Tags

XML tags should be used sparingly and strategically:

### ✅ Good Use Cases

1. **Conditional Logic**
```markdown
<conditional>
IF critical_vulnerabilities > 0:
  - Halt deployment
  - Notify security team
ELSE:
  - Proceed with review
</conditional>
```

2. **Critical Warnings**
```markdown
<critical>
STOP: If you detect remote code execution vulnerabilities, flag immediately and stop analysis.
</critical>
```

3. **Data Structures for Parsing**
```markdown
<input>
  <file_path>src/main.py</file_path>
  <scan_type>full</scan_type>
</input>
```

4. **Nested Hierarchies**
```markdown
<workflow>
  <phase name="discovery">
    <step>Scan files</step>
    <step>Identify patterns</step>
  </phase>
</workflow>
```

### ❌ Avoid XML for Simple Structure

**Don't do this:**
```xml
<instructions>
  <step1>Review the code</step1>
  <step2>Find bugs</step2>
</instructions>
```

**Do this instead (markdown):**
```markdown
## Instructions

1. Review the code
2. Find bugs
```

---

## Prompt Checklist

Before publishing a prompt, verify:

- [ ] **Context is clear**: Does Claude understand its role and the task?
- [ ] **Instructions are specific**: Are the steps actionable and unambiguous?
- [ ] **Markdown is primary**: Is XML only used where truly needed for emphasis?
- [ ] **Examples included**: Are there examples for complex or ambiguous tasks?
- [ ] **Output format defined**: Is the expected response structure clear?
- [ ] **Constraints specified**: Are limitations and requirements explicit?
- [ ] **Variables documented**: Are all dynamic inputs clearly defined?
- [ ] **Workflow is logical**: Do the steps follow a sensible sequence?
- [ ] **Success criteria defined**: How will output quality be evaluated?
- [ ] **Edge cases considered**: Does the prompt handle unusual inputs?

---

## Resources

- [Claude Prompt Engineering Overview](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/overview)
- [Using XML Tags](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/use-xml-tags)
- [Chain Prompts](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/chain-prompts)
- [Multishot Prompting](https://docs.claude.com/en/docs/build-with-claude/prompt-engineering/multishot-prompting)

---

## Version History

- **v1.0** - Initial template structure with markdown-first approach
