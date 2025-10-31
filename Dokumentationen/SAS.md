### Software Architecture Specification (SAS) 

## Projekt 4: Semantic Wikibase

Based on IEEE 1471-2000 – Recommended Practice for Architectural Description of Software-Intensive
Systems

Author: Colin Dietschmann
Institution: DHBW Stuttgart

| Version | DATE       | AUTHOR            | KOMMENT |
|-|-|-|-|
| 0.1     | 29.10.2025 | Colin Dietschmann | First draft |

### 1. Overview

# 1.1 Scope:
This Software Archtecture Specification (SAS) describes the architecture of the Semantic Wikibase
project, designed to provide a distributed, web-based Infrastructure for semantic concept definitions based
on Asset Administration Shell (AAS) Concept Description.

#1.2 Purpose:
The purpose is to define the architectural structure, rationale and components of the semantic Wikibase
pplatform, ensuring reusability and interoperability across AAS systems.

# 1.3 Intended Users
This specification is intended for:
- **System archtiects** developing semantic infrastructures for AAS ecosystems.
- **Developers implementing** REST APIs, web services and database schemas.
- **Groups** working with IEC, ECLASS and Catena-X SematicHub.
- **Community contributors** defining or maintianing concept definitons.
- **System integrators** connecting AAS environments with global semantic registries

# 1.4 Conformance 
An implementation conforms to this SAS if it includes:
- All major components as described in Section 4.
- REST API responeses structured according to the IEC 61360 Data Specification.
- URI resolution consistent with Semantic MediaWiki/Wikibase rules.
- Architectural viewpoints definded in Section 5.3.

### 2. References
- IEEE Srd 1471-2000: Recommended Pratice for Architectural Description of Software-Intensice Systems
- IEC 61360: Common Data Dictionary (CDD) Data Specification
- ECLASS REST API Documation (www.eclass.eu)
- Catena-X Sematic Hub: User Guid for Semantic Services
- Semantic MediaWiki Documentation: Pretty URIs, API usage
- Wikidata REST API Documentation
- AAS Specifications: admin-shell.io/aas-specs-metamodel

### 3 Definitons

|Term|Definition|
|-   |-         | 
|AAS (Asset Administration Shell)|A standardized digital representation of an asset.|
|Concept Description (CD)|A semantic definiton for submodel elements in a AAS.|
|Wikibase|A MediaWiki-based semantic knowledge base with linked data and versioned entities|
|Semantic Identifier(SID)|A globally resolvable URI that uniquely identifies a concept.|
|REST API|A web interface enabling HTTP-based interaction with system resources.|
|View/Viewpoint|Conceptual representations of system aspects according to IEEE 1471.|
|SemanticHub|Catena-X platform providing a federated semantic reference registry.|

References: IEEE Std 1471-2000 (Basis for this AD); AAS Specification Part 3a: Data Specification – IEC 61360; Wikibase Documentation; OpenAPI Specification.

### 1. Identification of Stakeholders and Concerns

|Stakeholder-Role| Specific Project Role| Core Interest|
|-|-|-|
|User / Acquier (Client) | AAS Tool Users| Needs stable URIs and a compact, machine-readable API response (resolving JSON pain points) for Submodel Elements.|
|User(Operator)| Domain Experts| Requires correct, multilingual definitions and units to ensure data quality and semantic integrity.|
|Developer/User| System Integrators|Requires correct, multilingual definitions and units to ensure data quality and semantic integrity. |
|Acquier/Oversight| Lecturers|Expects a running demo system, conformance to academic standards (Documentation/SAS), and successful project execution. |
|Developer| Student Team| Desires a feasible project with clear requirements and a practical, implementable technical approach using Wikibase.|
|Oversight/Auditor|Data Protection/IT Security Officers| Demands strong access control, data security (especially for the custom REST-Gateway), and compliance with data governance rules.|
| Community/Governance |Community/Open Data Enthusiasts| Wants low barriers to entry for data access and defined governance rules (licensing, contribution guidelines).|
