# Deep Research Prompt

**Generated:** 2025-10-24
**Created by:** Alex
**Target Platform:** Multiple platforms (Gemini, Claude, Perplexity)

---

## Research Prompt (Ready to Use)

### Research Question

Integrated open-source reading infrastructure: Evaluate and recommend compatible solutions for KOReader statistics backup, library file cloud backup (epubs/audiobooks), self-hosted library management server, audiobook player with Hardcover.app integration, unified database platform, secure remote access, and cross-device file synchronization - optimized for a single-user personal reading system with iOS and Boox Palma 2 devices.

### Research Goal and Context

**Objective:** Technical architecture decision

**Context:**
{{research_persona}}

### Scope and Boundaries

**Temporal Scope:** Last 2 years (2023-2025) - focus on current stable versions and recent developments in this rapidly evolving tech space

**Geographic Scope:** Global

**Thematic Focus:**

**Focus on:**
- Tool compatibility and integration between components (CRITICAL)
- Free/open-source solutions (zero ongoing cost requirement)
- iOS and Boox Palma 2 device compatibility
- Hardcover.app API integration capabilities
- Self-hosted solutions and deployment complexity
- Community support and documentation quality
- Ease of setup and maintenance for solo user
- Data backup reliability and restore procedures

**Exclude:**
- Commercial/paid enterprise solutions requiring subscription
- Managed cloud services with ongoing costs
- Android-only or Windows-only solutions
- Deprecated or unmaintained projects
- Solutions requiring teams/multi-user infrastructure

### Information Requirements

**Types of Information Needed:**
- Technical specifications and capabilities
- Comparative analysis (tool vs tool trade-offs)
- Qualitative insights and expert opinions (community feedback, user experiences)
- Trends and patterns (tool maturity, adoption, active development)

**Preferred Sources:**
- Official project documentation and wikis
- GitHub repositories (commit activity, release notes, active development status)
- GitHub issues: Evaluate critically - verify if issues are edge cases or already resolved in recent versions; do not over-weight unresolved edge-case issues
- Community forums and discussions (Reddit r/selfhosted, r/homelab, project-specific Discord/forums)
- Technical blogs and setup guides from real users (actual implementation experiences)
- Stack Overflow and technical Q&A sites
- KOReader forums, Calibre forums, Hardcover community discussions
- YouTube tutorials and walkthroughs showing real-world deployments

### Output Structure

**Format:** Executive Summary + Detailed Sections with Comparative Analysis

**Required Sections:**

1. Executive Summary (top recommendations, critical compatibility considerations, overall architecture)
2. KOReader Statistics Backup Strategy (cloud sync options, alternatives, reliability)
3. Library File Cloud Backup for Epubs/Audiobooks (separate from statistics backup)
4. Self-Hosted Library Management Server (Calibre-Web-Automated vs alternatives, metadata automation, OPDS, audiobook support)
5. Audiobook Player & Hardcover Integration (BookPlayer vs audiobookshelf vs shelfbridge, sync reliability, iOS compatibility)
6. Unified Database Platform (Supabase vs self-hosted PostgreSQL, schema design, API access)
7. Secure Remote Access Solution (Tailscale vs Cloudflare Tunnel vs alternatives, setup complexity)
8. Syncthing Configuration for Multi-Device Library (iOS options, conflict resolution, folder structure)
9. Integration & Compatibility Assessment (how components work together, integration challenges, data flow)
10. Implementation Roadmap (suggested order, dependencies between components)

**Depth Level:** Exhaustive - deep dive with all available data, real-world examples, edge cases, and comprehensive trade-off analysis

### Research Methodology

**Keywords and Technical Terms:**
KOReader, statistics.sqlite3, cloud sync, Calibre-Web-Automated, Calibre, OPDS, BookPlayer, audiobookshelf, shelfbridge, Hardcover.app, Hardcover GraphQL API, Supabase, PostgreSQL, PostgREST, Syncthing, iOS sync, Boox Palma 2, Google Drive, iCloud, Koofr, WebDAV, Tailscale, Cloudflare Tunnel, VPN, zero-trust networking, Readest, epub, audiobook, self-hosted, open-source, free-tier

**Research Persona:**
Act as a technical architect evaluating infrastructure for a personal reading system. Prioritize practical implementation considerations, compatibility between components, and ease of maintenance for a solo developer. Focus on solutions that actually work together in real-world deployments.

**Special Requirements:**
- Include specific version numbers and release dates for recommended tools
- Prioritize sources from 2023-2025 for current best practices
- Distinguish between theoretical compatibility and proven real-world integrations
- Note setup complexity and time investment for each component
- Highlight breaking changes or known issues between component versions
- For each recommendation, provide evidence from actual user implementations
- Consider total system cost (must be $0 ongoing, free-tier only)

**Validation Criteria:**
- Cross-reference recommendations across multiple community sources
- Verify compatibility claims with actual integration examples or documentation
- Identify conflicting information and explain discrepancies
- Distinguish between facts, community consensus, and individual opinions
- Highlight confidence levels for each recommendation (high/medium/low based on evidence)
- Flag areas where research is inconclusive or requires hands-on testing

### Follow-up Strategy

**If data/evidence is unclear:**
- If KOReader backup reliability is uncertain, create separate deep-dive into sync failure modes and recovery procedures
- If library server solutions show similar capabilities, create detailed comparison matrix with setup time, maintenance burden, and community support metrics
- If Hardcover.app API integration is poorly documented, search for actual implementation examples or GitHub code samples
- If database platform choice is ambiguous, analyze specific schema requirements and query patterns for the unified database

**If compatibility questions arise:**
- If iOS Syncthing integration seems problematic, explore alternative sync solutions for iOS-to-server file synchronization
- If audiobook players lack Hardcover sync, investigate manual export/import workflows or API-based custom solutions
- If component version mismatches are found, identify the most stable combination of versions across all tools

**If cost concerns emerge:**
- If free-tier limitations appear restrictive, calculate realistic storage/bandwidth needs and identify potential workarounds

---

## Complete Research Prompt (Copy and Paste)

```
# Comprehensive Technical Research: Integrated Open-Source Reading Infrastructure

## Research Objective
Evaluate and recommend compatible solutions for building an integrated open-source reading infrastructure optimized for a single-user personal reading system with iOS and Boox Palma 2 devices.

## Context & Persona
Act as a technical architect evaluating infrastructure for a personal reading system. Prioritize practical implementation considerations, compatibility between components, and ease of maintenance for a solo developer. Focus on solutions that actually work together in real-world deployments.

## Scope
- **Temporal**: Last 2 years (2023-2025) - focus on current stable versions and recent developments
- **Geographic**: Global
- **Cost Constraint**: $0 ongoing costs - free/open-source tools and free-tier cloud services only
- **Devices**: iOS (iPhone with Readest ebook reader) + Boox Palma 2 (KOReader)
- **Critical Requirement**: Tool compatibility and integration between ALL components

## Research Areas (Exhaustive Analysis Required)

### 1. KOReader Statistics Backup Strategy
**Question**: What is the most reliable approach for backing up KOReader's statistics.sqlite3 file?
- Evaluate KOReader native cloud sync (Google Drive, iCloud, WebDAV via Koofr)
- Alternative backup approaches (custom sync solutions, direct replication)
- Reliability assessment: sync failure modes, data corruption risks, recovery procedures
- Setup complexity and maintenance burden
- Real-world user experiences with each approach
**Deliverable**: Specific recommendation with version numbers, setup steps, and known issues

### 2. Library File Cloud Backup (Separate from Statistics)
**Question**: What solution should be used for backing up the actual epub and audiobook library files?
- This is SEPARATE from the KOReader statistics backup
- Evaluate free-tier cloud storage options (Google Drive, iCloud, Koofr, etc.)
- Integration considerations with library management system
- Sync reliability and restore procedures
- Storage capacity limits and file size constraints
**Deliverable**: Recommended cloud backup solution with integration approach

### 3. Self-Hosted Library Management Server
**Question**: Which self-hosted library server provides the best metadata automation and device compatibility?
- Deep evaluation of Calibre-Web-Automated (primary candidate)
- Alternative solutions: Kavita, Komga, custom Calibre CLI-based approaches
- Metadata automation capabilities (Hardcover.app API integration potential)
- OPDS protocol support for device access (Readest iOS, KOReader)
- Audiobook support and management
- Remote access configuration complexity
- Setup time, maintenance burden, community support quality
**Deliverable**: Detailed comparison matrix + specific recommendation with setup guidance

### 4. Audiobook Player & Hardcover.app Integration
**Question**: Which audiobook player provides reliable Hardcover.app sync and statistics export?
- Compare BookPlayer (current), audiobookshelf (self-hosted), shelfbridge
- Hardcover.app sync reliability and actual integration quality
- Statistics export capabilities (listening time, progress, completion data)
- iOS compatibility and user experience
- Ability to integrate with unified database
- Real-world user feedback on Hardcover sync quality
**Deliverable**: Recommendation with Hardcover integration assessment

### 5. Unified Database Platform
**Question**: Should the unified reading database use Supabase or self-hosted PostgreSQL?
- Supabase free tier: limitations, reliability, migration paths, API capabilities
- Self-hosted PostgreSQL: hosting options, backup strategies, API layer (PostgREST?)
- Schema design considerations for unified ebook + audiobook statistics
- Real-time sync capabilities between KOReader device and cloud database
- Query performance for analytics use cases
**Deliverable**: Database architecture recommendation with schema considerations

### 6. Secure Remote Access Solution
**Question**: What is the best approach for secure remote access to the library server?
- Tailscale (mesh VPN) evaluation
- Cloudflare Tunnel evaluation
- Alternative approaches (dynamic DNS, traditional VPN, etc.)
- Setup complexity, performance characteristics, reliability
- Device compatibility (especially iOS)
- Free-tier limitations if applicable
**Deliverable**: Remote access recommendation with setup complexity assessment

### 7. Syncthing Configuration for Multi-Device Library
**Question**: How should Syncthing be configured for reliable multi-device library synchronization?
- iOS Syncthing client options and limitations (this is a known pain point)
- Alternative iOS-to-server file sync solutions if Syncthing doesn't work well
- Conflict resolution strategies for simultaneous changes
- Optimal folder structure for ebooks, audiobooks, and metadata
- FAT filesystem considerations for e-readers
- Configuration best practices from real users
**Deliverable**: Syncthing configuration guide OR alternative sync approach if iOS issues are severe

### 8. Integration & Compatibility Analysis (CRITICAL)
**Question**: How do all the recommended components integrate with each other?
- Data flow diagram/description across the entire system
- Integration points and potential challenges
- Known version compatibility issues between components
- Proven real-world integration examples (links to user setups, GitHub repos, blog posts)
- Areas where custom glue code may be needed
**Deliverable**: Complete integration architecture with compatibility assessment

### 9. Implementation Roadmap
**Question**: In what order should these components be implemented?
- Dependency analysis (what must be set up first)
- Suggested phased implementation approach
- Estimated time investment for each phase
- Testing and validation checkpoints
**Deliverable**: Prioritized implementation plan

## Information Requirements
- Technical specifications and capabilities
- Comparative analysis with trade-off matrices
- Real-world user experiences and community consensus
- Tool maturity indicators (active development, community size, recent releases)
- Actual setup guides and documentation quality assessment

## Source Guidance
**Prioritize**:
- Official project documentation and wikis
- GitHub repositories (commit activity, release notes, actual code)
- GitHub issues: Evaluate critically - verify if issues are edge cases or already resolved; do not over-weight unresolved edge-case issues
- Community forums (Reddit r/selfhosted, r/homelab, project Discord/forums)
- Real user implementation blogs and setup guides
- KOReader forums, Calibre forums, Hardcover community
- YouTube walkthroughs showing actual deployments

**Critical Technical Terms to Include**:
KOReader, statistics.sqlite3, cloud sync, Calibre-Web-Automated, Calibre, OPDS, BookPlayer, audiobookshelf, shelfbridge, Hardcover.app, Hardcover GraphQL API, Supabase, PostgreSQL, PostgREST, Syncthing, Boox Palma 2, Google Drive, iCloud, Koofr, WebDAV, Tailscale, Cloudflare Tunnel, Readest, epub, audiobook, self-hosted, free-tier

## Output Format
**Executive Summary**:
- Top recommendation for each of the 7 components
- Critical compatibility/integration warnings
- Overall recommended architecture diagram/description

**Detailed Sections** (one per research area above):
- Current state analysis
- Comparative evaluation of alternatives
- Pros/cons with evidence
- **Specific recommendation with rationale**
- Version numbers and release recency
- Setup complexity estimate
- Known issues and limitations
- Confidence level (high/medium/low) with reasoning

**Final Recommendations**:
- Complete system architecture
- Implementation roadmap
- Total estimated setup time
- Maintenance expectations

## Validation Requirements
- Cross-reference all major claims with multiple sources
- Verify compatibility claims with actual integration examples or official docs
- Identify and explain any conflicting information found
- Distinguish between facts, community consensus, and individual opinions
- Assign confidence levels to each recommendation based on evidence quality
- Flag areas where hands-on testing is required due to insufficient documentation

## Success Criteria
Research is complete when:
1. Each of the 7 technical areas has a clear recommendation with rationale
2. Integration compatibility between ALL components is assessed
3. Real-world implementation evidence supports recommendations
4. Setup complexity and time investment is estimated
5. Known issues and limitations are documented
6. Alternative approaches are identified for high-risk areas
7. Total system cost is confirmed to be $0 ongoing

## Follow-up Questions
If any area lacks sufficient evidence, drill deeper:
- If KOReader backup reliability unclear → investigate sync failure modes and recovery
- If library servers appear similar → create detailed setup/maintenance comparison
- If Hardcover API integration unclear → find actual code examples
- If iOS Syncthing problematic → explore alternative iOS sync solutions
- If component versions conflict → identify most stable version combinations
```

---

## Platform-Specific Usage Tips

### Gemini Deep Research
- Paste the complete prompt above into Gemini
- Gemini will generate a multi-point research plan - **review and modify it before execution**
- Be specific and clear in the initial prompt (already done above)
- You can add follow-up questions to drill deeper or expand specific sections
- Available in 45+ languages globally
- Expected research time: 5-15 minutes depending on depth

### Claude (Projects or Artifacts)
- Use Claude Projects for best results - add your Product Brief as context
- Break into focused sub-prompts if needed (can use the 9 research areas as separate queries)
- Use Chain of Thought prompting by asking Claude to "think step-by-step"
- Provide explicit examples if Claude's first attempt misses the mark
- Can iterate and refine - Claude excels at conversational refinement
- Consider using Artifacts for structured output

### Perplexity (Pro Search)
- Paste the prompt into Perplexity Pro Search
- Perplexity excels at finding recent sources and providing citations
- Use the "Focus" feature if available (Academic, Writing, etc.)
- Review citations carefully - Perplexity provides source links
- Can ask follow-up questions to drill into specific areas
- Particularly good for finding real-world implementation examples and recent community discussions

---

## Research Execution Checklist

### Before Running Research
- [ ] Prompt clearly states the research question and all 9 technical areas
- [ ] Scope and boundaries are well-defined (timeframe, cost constraints, devices)
- [ ] Output format and structure specified (Executive Summary + 9 detailed sections)
- [ ] Keywords and technical terms included
- [ ] Source guidance provided with GitHub issue caveat
- [ ] Validation criteria clear (confidence levels, evidence requirements)

### During Research (Platform-Specific)

**Gemini:**
- [ ] Review the multi-point research plan before Gemini starts searching
- [ ] Modify the plan if any areas are missing or incorrectly scoped
- [ ] Monitor progress if visible

**Claude:**
- [ ] Add Product Brief document to Claude Project for context
- [ ] Consider breaking into focused sub-prompts per research area if initial output is too broad
- [ ] Use follow-up questions to drill deeper into specific components

**Perplexity:**
- [ ] Use Pro Search mode for comprehensive results
- [ ] Check citations as research progresses
- [ ] Note any areas with limited sources for follow-up

### After Research Completion
- [ ] Verify key technical claims from multiple sources
- [ ] Check if GitHub issues mentioned are actually resolved or edge cases
- [ ] Confirm compatibility claims have real-world evidence (user blogs, GitHub examples)
- [ ] Identify conflicting recommendations and understand why
- [ ] Note confidence levels for each recommendation (based on evidence quality)
- [ ] Flag areas requiring hands-on testing due to insufficient documentation
- [ ] Cross-reference recommendations across multiple platforms if running on more than one
- [ ] Export/save research results before moving on

### Integration Validation
- [ ] Verify that recommended components actually work together
- [ ] Check for version compatibility issues between recommended tools
- [ ] Identify any missing "glue code" or custom integration needs
- [ ] Confirm total system cost is $0 ongoing (no hidden subscription requirements)

### Follow-up Actions
- [ ] Create list of components requiring hands-on POC testing
- [ ] Identify areas where additional focused research is needed
- [ ] Document any assumptions that need validation during implementation
- [ ] Save all research outputs to project documentation folder

---

## Metadata

**Workflow:** BMad Research Workflow - Deep Research Prompt Generator v2.0
**Generated:** 2025-10-24
**Created by:** Alex
**Research Type:** Technical/Architecture Research (Deep Research Prompt)
**Target Platforms:** Gemini Deep Research, Claude Projects, Perplexity Pro Search
**Project:** BookHelper - Integrated Open-Source Reading Infrastructure

**Research Areas Covered:**
1. KOReader Statistics Backup Strategy
2. Library File Cloud Backup (Epubs/Audiobooks)
3. Self-Hosted Library Management Server
4. Audiobook Player & Hardcover.app Integration
5. Unified Database Platform
6. Secure Remote Access Solution
7. Syncthing Multi-Device Configuration
8. Integration & Compatibility Analysis
9. Implementation Roadmap

---

_This research prompt was generated using the BMad Method Research Workflow, incorporating best practices from Gemini Deep Research, Claude Projects, and Perplexity Pro Search (2025)._
