# Changelog

## Legal services

### 0.1 (draft), 2026-10-20

First public draft. Namespace `https://w3id.org/servicefacts/legal#`, prefix `legal:`.

- 16 properties: `actsFor`, `feeArrangement`, `disputeProcess`, `forum`, `governingLegislation`, `hasTimeLimit`, `appliesToStep`, `timeAllowed`, `countedFrom`, `legalSource`, `consequenceIfMissed`, `typicalDuration`, `matterValueRange`, `dateAdmitted`, `contractForm`, `projectType`.
- 1 class: `TimeLimit`.
- 5 value lists: PartyRoles (8), FeeArrangements (6), DisputeProcesses (8), ProjectTypes (4), PracticeAreas (6).
- Guidance for 58 standard schema.org properties, with a priority for each.
- Built for Australian building and construction law. Other practice areas come next.

Known gaps:

- The method terms (`priority`, `module`, `answersQuestion`, `visibleTextRequired`, `priorityEvidence`, `dualPublishAs`, `propertyIndex`) sit in the legal namespace. They move to a shared `profile#` namespace before 1.0.
- Priorities are hypotheses. They will be re-scored from AI prompt tracking.
