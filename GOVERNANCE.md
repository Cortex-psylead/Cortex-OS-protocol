# 🏛️ Project Governance: Ethical Courts & Community Structure

This document defines how Cortex OS is governed as an open source project:
who makes decisions, how Ethical Courts operate, how contributions are
validated, and how user sovereignty is protected at every level.

For the foundational ethical principles that the system enforces at runtime,
see [GOVERNANCE-BASE.md](./GOVERNANCE-BASE.md).

---

## 🧭 Governance Philosophy

Cortex OS has no corporate owner. It has no profit motive.

Its governance model is built on three pillars:

1. **Community** — developers, researchers, and users who build and improve
   the protocol under GPL-3.0
2. **Ethical Courts** — independent university nodes that audit code and
   define safe-use protocols
3. **User Sovereignty** — the individual always holds final authority over
   their own device, as defined in GOVERNANCE-BASE.md

No single entity — including the project founder — can override a decision
validated by the full governance structure.

---

## 🏗️ Project Roles

### 🌱 Contributor
Anyone who submits a Pull Request, opens an Issue, or participates in
community discussion. No formal requirements — only adherence to the
[Code of Conduct](./CONTRIBUTING.md).

### 🔧 Maintainer
A contributor recognized by the community for sustained, high-quality
contributions. Maintainers can:
- Review and merge Pull Requests
- Triage Issues
- Propose changes to protocol documents

Maintainers are proposed by the community and confirmed by simple majority
of active maintainers.

### 🎓 Ethical Court Node
A university (public or private) formally affiliated with the project.
Court nodes are the only entities authorized to:
- Issue ethical certifications for capability modules
- Define or modify safety protocols in GOVERNANCE-BASE.md
- Veto contributions that violate core ethical principles

Court nodes have **no authority** over technical implementation decisions
outside their domain. A law faculty cannot block a DSP optimization.
An engineering faculty cannot override a clinical safety protocol.

### 🧭 Protocol Steward
The project founder role. Responsible for:
- Maintaining the vision and long-term direction
- Facilitating communication between maintainers and court nodes
- Breaking ties when governance processes deadlock

The Steward role is transitional — as the community and court structure
matures, governance authority transfers progressively to the collective.

---

## 🎓 Ethical Courts: Structure & Operation

### What they are
Independent university nodes — public or private — that provide scientific
and ethical oversight of the Cortex OS protocol. They are not employees,
not contractors, and not administrators of the project. They are
**independent auditors and protocol definers**.

### Three specialized roles per node

**🔩 Technical Audit (Engineering / Computer Science faculties)**
- Audit contributed code using Semgrep and SonarQube
- Verify that all hardware access paths respect the sovereignty principles
- Issue technical certification for new capability modules
- Tool: Public SonarQube dashboard (one per active court node)

**🧠 Ethical Protocol (Psychology / Bioethics / Neuroscience faculties)**
- Define safe-use parameters for each capability module
- Establish intervention level guidelines (see GOVERNANCE-BASE.md §3)
- Review and approve any module that interfaces with biometric data
- Reference frameworks: UNESCO AI Ethics (2021), IEEE CertifAIEd,
  Polyvagal Theory (Porges), Free Energy Principle (Friston)

**⚖️ Legal Compliance (Law faculties)**
- Validate protocol compliance with local data protection legislation
- Colombia: Ley 1581/2012 (data protection), Ley 1090/2006 (psychology)
- European contributors: GDPR
- Issue compliance declarations per jurisdiction

### How a node joins
1. A university representative opens a formal Issue tagged `[court-node-proposal]`
2. The proposal must include: institution name, faculty/department,
   designated role (technical / ethical / legal), and a brief statement
   of commitment
3. Active maintainers review and vote — simple majority confirms
4. The node is listed in this document and gains access to the
   audit pipeline

### How a node operates
- Each node publishes its audit findings publicly in the repository
  under `/courts/[node-name]/`
- Findings are dated, signed by the responsible academic, and linked
  to the specific commit or PR they evaluate
- Any community member can question a court finding by opening an Issue
  tagged `[court-challenge]`

### What courts cannot do
- Courts cannot block a contribution based on opinion — only on documented
  violation of GOVERNANCE-BASE.md principles or applicable law
- Courts cannot mandate commercial restrictions on the protocol
- Courts cannot override user sovereignty as defined in GOVERNANCE-BASE.md

---

## 🔄 Decision-Making Process

### Routine contributions (bug fixes, documentation, minor features)
1. Contributor opens a Pull Request
2. One maintainer reviews and approves
3. Merged after 48-hour review window with no objections

### Capability modules (new hardware features, new user profiles)
1. Contributor opens an Issue tagged `[capability-proposal]` with
   technical spec and use case
2. Community discussion — minimum 7 days
3. Technical Court node reviews code
4. Ethical Court node reviews safety parameters
5. Merged with approval from both relevant court roles

### Protocol changes (GOVERNANCE-BASE.md, ARCHITECTURE.md, core agent behavior)
1. Proposal opened as Issue tagged `[protocol-change]`
2. Minimum 30-day community discussion
3. Full court review — all three roles must issue findings
4. Requires consensus of active maintainers plus no veto from court nodes

### Emergency security patches
- Any maintainer can merge a security patch immediately
- Must be tagged `[security-patch]` and reviewed retroactively
  within 72 hours

---

## 🛡️ Anti-Capture Provisions

These rules exist to prevent the project from being captured by commercial,
governmental, or ideological interests:

1. **No corporate maintainers:** No single company may hold more than
   one maintainer seat. Employees of the same company count as one vote.

2. **No proprietary dependencies by default:** Any contribution that
   introduces a proprietary dependency must be explicitly opt-in and
   clearly documented. The core system must always run on fully open
   components.

3. **No hidden hardware locks:** Any code that limits user access to their
   own hardware — for any reason not explicitly defined in GOVERNANCE-BASE.md
   — is grounds for immediate revert.

4. **Fork right is absolute:** Any individual or community may fork this
   project under GPL-3.0 at any time, for any reason.

---

## 📋 Governance Review Cycle

The governance structure itself is reviewed annually by the community.
Any aspect of this document — including these anti-capture provisions —
can be modified through the Protocol Change process above.

The only unmodifiable rule: user sovereignty as defined in
GOVERNANCE-BASE.md §1 (Primacy of Will) cannot be weakened by any
governance process.

---

## 🌍 Current Status

| Role | Status |
|---|---|
| Protocol Steward | Active — project founder |
| Maintainers | Open — seeking first maintainers |
| Technical Court Nodes | Open — seeking university partners |
| Ethical Court Nodes | Open — seeking university partners |
| Legal Court Nodes | Open — seeking university partners |

To propose yourself as a maintainer or court node, open an Issue with
the appropriate tag.

---

> *"Governance is not control. It is the structure that prevents control
> from being taken by anyone who should not have it — including us."*
