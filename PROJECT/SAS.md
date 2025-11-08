### Software Architecture Specification (SAS) 

## Projekt 4: Semantic Wikibase

Based on IEEE 1471-2000 – Recommended Practice for Architectural Description of Software-Intensive
Systems

Author: Colin Dietschmann
Institution: DHBW Stuttgart

| Version | DATE       | AUTHOR            | KOMMENT |
|-|-|-|-|
| 0.1     | 29.10.2025 | Colin Dietschmann | First draft |
|1.0|08.011.2025|Colin Dietschmann|First Version|
### 1. Overview

# 1.1 Scope:
This Software Archtecture Specification (SAS) describes the architecture of the Semantic Wikibase platform integrated with the existing AAS Cinnect Backend Service.
The combined sysem offers:
- A production/development AAS repository (AAS Connect Backend Service) that exposes REST (OpenAPI) and GraphQL endpoints and also stores AAS artifacts in Neo4j.
- A Semantic Wikibase instance which works as the registry of Concept Descriptions (CDs) using the IEC 61360 inspired data model.
- Integration layers that link AAS submodel elements with resolvable semantic URIs from semantic Wikibase. Mapping and synchronization between Neo4j based AAS data an Wikibase RDF entites.
- Web and programmatic interfaces for AAS clients to retrive language aware IEC61360 JSON representations via a REST facade.


#1.2 Purpose:
The purpose is to define the architectural structure, rationale and components of the semantic Wikibase
pplatform, ensuring reusability and interoperability across AAS systems.

The purpose is to provide a concrete architectural blueprint showing how to adapt the existing AAS Connect repository to:
- Using the Wikibase as the caninical semantix registry for Concept Descriptions (CDs).
- Provide a REST API that returns IEC61360 responses 
- Keep the AAS repository functionality intact and extend it with the semantic referencing and solution.
- Support operational deployment using the provided docker-compose.yml as a baseline.




# 1.3 Intended Users
This specification is intended for:
- **System archtiects** working on the semantic infrastructures and deploying Dockerized services.
- **Developers implementing** working on the AAS Connect Backendand Semantic Wikibase integration.
- **Community contributors** defining or maintianing concept definitons.

# 1.4 Conformance 
This SAS conforms to the IEEE-1471 by providing: AD identification, stakeholders and concerns, selected viewpoints, one or more views per viewpointm rationale and known inconsistencies.

### 2. References
- foprs/aas-connect-repository — GitHub repository (README, docker-compose, Neo4j config).
- IEEE Std 1471-2000.
- IEC 61360 Data Specification (CDD / IEC Common Data Dictionary).
- AAS OpenAPI Specification (IDTA).
- Semantic MediaWiki / Wikibase documentation (Pretty URIs, SPARQL).
- Wikidata / Wikibase REST API docs.
- Catena-X Semantic Hub user guide (for optional federation).


# 3 Definitons

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


# 4 onceptual Framework
### 4.1 System Context
The integrated system has two principal subsystems:
1. AAS Repository Subsystem and AAS Connect Backend Service:
- Neo4j graph database
- Backend service exposing OpenAPI/REST and GraphQL endpoints.
- BaSyx Web UI integrated 
- Docker Compose depolyment (docker-compose.yml from repo)

2. Semantic Registry Subsystem
- Wikibase instance or standalone Wikibase
- REST facade delivering IEC61360 formatted response per concept
- Admin UI for community editing and governance. 

Integration Layers:
- API Gateway, provides Get /semantic/{id}?lang=de returning IEC61360 JSON. Handels rewrite rules for pretty URIs and proxies request to Wikibase SPARQL or RDF store.
- Sync/Mapping Services, background jobs or API endpoints for mapping external IEC/ECLASS entries into Wiki itemns and for periodic synchronization from AAS repository to Wikibase.

External system: AASX Explorer, third-party IEC/ECLASS sources.


### 4.2 Identification of Stakeholders and Concerns

|Stakeholder-Role| Specific Project Role| Core Interest|
|-|-|-|
|User / Acquier (Client) | AAS Tool Users| Needs stable URIs and a compact, machine-readable API response (resolving JSON pain points) for Submodel Elements.|
|User(Operator)| Domain Experts| Requires correct, multilingual definitions and units to ensure data quality and semantic integrity.|
|Developer/User| System Integrators|Requires correct, multilingual definitions and units to ensure data quality and semantic integrity. |
|Acquier/Oversight| Lecturers|Expects a running demo system, conformance to academic standards (Documentation/SAS), and successful project execution. |
|Developer| Student Team| Desires a feasible project with clear requirements and a practical, implementable technical approach using Wikibase.|
|Oversight/Auditor|Data Protection/IT Security Officers| Demands strong access control, data security (especially for the custom REST-Gateway), and compliance with data governance rules.|
| Community/Governance |Community/Open Data Enthusiasts| Wants low barriers to entry for data access and defined governance rules (licensing, contribution guidelines).|

### 4.3 Concerns

- Global resolvability of semantic URIs (Pretty URIs, rewriting).
- API conformance to IEC61360-shaped output and AAS OpenAPI compatibility.
- Data consistency & provenance across Neo4j and Wikibase.
- Low entry barrier: easy UI to publish CDs.
- Scalable deployment using Docker compose and containerization.
- Governance & moderation for community contributions.

### 4.4 Mission 
The mission is to offer an open, community-driven, web-resolvable registriy of semantic Conceüt Descriptions that integrates with the existing AAS Connect repository and supports language-aware IEC61360 ouputs for AAS consumers.

# 5 Architectural Description Practices
## 5.1 Architectural View
### 5.1.1 Structural View (Comonents and Interfaces Componentes)
- AAS Connect Backend (existing)
    - Exposes: REST OpenAPI (/api/v1//*), GraphQL (/graphql/), Swagger UI (/docs/), BaSyx GUI (/gui)
    - Presists to: Neo4j.

- Semantic Wikibase (new)
    - MediaWiki + Wikibase extension
    - Provides SPARQL endpoint and MediaWiki API
    - Stores concept items with unique QIDs (or custom URIs)

- SemanticFacade/API Gateway (new)
    - REST endpoint "GET /semantic/{sid}?lang={lang}" -> returns IEC61360 JSON
    - Translates between Wikibase RDF and IEC61360 JSON template
    - Handles üretty URI rewriting (for example, "https://semantic.example.org/id/Q21"-> internal item).

- Mapping and Sync Service (new)
    - Jobs to: import mappings from IEC/ECLASS where allowed, export AAS submodel references to Wikibase, create/update link entries.

- Authentication/Authorization
    - OAuth2/API tokens for programmatic clients, UI-based login for editors (BaSyx UI credentrials/MediaWiki accounts).
- Presitent Starage
    - Neo4j (AAS data) is existing
    - RDF triple store / Blazegraph (optional) or Wikibase internal storage for semantic triples.

Interfaces:

![interface](interface.jpg)

### 5.1.2 Behavioral View

1. Concept Resolution in AAS path
- AAS client request submodel that references sid (Semantic URI)
- AAS Backend that sees semantic reference, calls SemanticFacade "semantics/{sid}?lang=de"
- SemanticFacade queries Wikibase SPARQL or item API and consturcts IEC61360 JSON
- Backend responds to client with a submodel + resolved semantic definition.

2. Create/Edit Concept
- User who uses Wikibase UI to create a item with properties aligned to IEC61360 fields 
- Admin/curation workflow approves
- Mapping Service optionally syncs approced items into AAS Connect systems as registry entries.

3. Deploy/Start
- Start with docker compose up -d (existing repo), extend docker-compose.yml to include Wikibase, Blazegraph/triplestore and SemanticFacade service.


### 5.1.3 Information View and Data Model (IEC61360)
Primary entity: ConceptDescription with fields:

- id (SID URI) — e.g. https://semantic.example.org/id/Q21
- prefLabel / preferredName {lang-tagged}
- definition {lang-tagged}
- unit (linked to unit concept, optional QID)
- valueFormat (dataType / format)
- sourceReferences (links to IEC/ ECLASS entries, with provenance)
- version (history)
- createdBy, createdAt, approvedBy, approvedAt
- externalIdentifiers (for example, IEC CDD property ID, ECLASS code)

Representation outputs:

- IEC61360 JSON (for API): matches template (preferredName, shortName, definition, dataType, unit, valueList, source).
- RDF/Turtle (for SPARQL and linked data).

### 5.1.4 Deployment View: Containers & Topology Baseline (from repo)
- aas-backend container (existing)
- neo4j container (presistent volumes: neo4j/data, neo4j/logs)
- basyx-gui (integrated)

Added components: 
- wikibase container (MediaWiki + Wikibase)
- semantic-facade container (Node.js/Python Flask) for IEC61360 JSON translation.
- sync-service container
- nginx reverse proxy for Pretty URIs and SSL termination (rewrite rules to map /id/Qxxx -> SemanticFacade)

Env configuration: .env (extend .env.sample), new variables for Wikibase DB, SPARQL endpoint, facade configs, admin credentials.

### 5.2

- The structural view defines a SemanticFacade interface that the behavioral flows expect (translation to IEC61360). The information view provides the schema the facade must implement. The deployment view maps each logical component to a container defined in docker-compose.yml extension.

- Known inconsistency: The existing AAS Connect backend may embed semantic references as simple IRDIs or strings; a migration adapter is required to map those to full HTTP SIDs. This adapter is specified in Mapping Service.

### 5.3 Architectural Rationale
- Resuse: Keeping the exiting forprs/aas-connect-repository stack unchanged wherever possible to minimize the risk.
- Seperation of concerns: Put the translation and URI resolution into the SemanticFacade. Keeps the AAS backend simpler and allows diffrent Wikibase implementations.
- Deployment: Docker compose keeps consistent deployment experience.
- Governance and Provenance: Wikibase gives edit history and moderation features.

# 6 Quality Attributes & Requirements
Functional Requierments:
- FR1: Provide GET /semantic/{sid}?lang={lang} returning IEC61360 JSON.
- FR2: POST/PUT/PATCH via Wikibase UI/API for concept creation
- FR3: Provide mapping endpoints to import/export mappings between AAS Backend and Wikibase
- FR4: Expose SPARQL for advanced queries.

Non-Functional Requirments:

- NFR1: API latency < 300ms for cached responses
- NFR2: Persistent storage durability (Neo4j + Wikibase DB volumes).
- NFR3: Scalability via container orchestration (initially docker compose)
- NFR4: Security via OAuth2 for programmatic endpoints and role-based access for edits.

# 7 Implementation Notes (practical steps)

1. Fork & clone foprs/aas-connect-repository. Start the existing stack via docker compose up -d to verify baseline.

2. Extend docker-compose.yml to include wikibase, blazegraph, semantic-facade, and sync-service containers. Use separate networks to allow controlled access.

3. implement SemanticFacade:

- Language: Node.js (Express) or Python (FastAPI/Flask).
- Endpoints: GET /semantics/{sid} (lang param), admin endpoints for sync.
- Connectors: call Wikibase SPARQL or MediaWiki REST API.
- Output: IEC61360 JSON (example mapping provided in code).

4. Wikibase configuration:
- Create properties for IEC61360 fields (preferred name, definition, unit, value format, IRDI, external IDs).
- Configure pretty URIs and allow rewriting, e.g. https://semantic.example.org/id/Q{item}.

5. Mapping & Sync:
- Script to import AAS submodel templates into Wikibase items (with provenance), and to export Wikibase SIDs into Neo4j as SemanticReference nodes/edges.

6. Testing:
Test with AASX Explorer and BaSyx UI by creating a submodel that references a SID and verifying resolved IEC61360 JSON via the AAS backend.



# 8 Compliance / Acceptance Criteria

SAS is accepted if:
GET /semantics/{sid}?lang={lang} works for sample SID and returns IEC61360 JSON.
AAS Connect Backend can be started unmodified and used together with the added Wikibase stack in docker-compose.
Basic CRUD of concepts through Wikibase UI + created SIDs can be resolved from AAS clients.
Basic mapping script can import at least one submodel template into Wikibase.

# 9 Conclusion

This SAS specifies how to adapt the existing foprs/aas-connect-repository to host and consume semantic ConceptDescriptions via a Semantic Wikibase. The approach minimizes changes to the existing AAS Connect backend while adding a separate, decoupled semantic registry (Wikibase) with a small translation façade and mapping/synchronization components.
