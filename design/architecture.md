# Advanced RAG Application Architecture

## System Overview

This document outlines the simplified, async-first architecture for our RAG application using FastAPI, React, and Qdrant Cloud.

## Component Architecture

```mermaid
graph TB
    subgraph Frontend
        R[React UI]
        PDF[PDF Upload Component]
        Chat[Chat Interface]
        WS[WebSocket Client]
    end
    
    subgraph Backend
        API[FastAPI Server]
        WH[WebSocket Handler]
        BT[Background Tasks]
        Cache[(Redis Cache)]
        
        subgraph Core Services
            PS[PDF Service]
            VS[Vector Service]
            CS[Chat Service]
            US[User Service]
        end
    end
    
    subgraph External Services
        QC[(Qdrant Cloud)]
        OAI[OpenAI API]
        SQLITE[(SQLite)]
    end
    
    R --> |HTTP| API
    R --> |WebSocket| WH
    PDF --> |Upload| API
    Chat --> |Query| API
    
    API --> Cache
    API --> BT
    BT --> PS
    PS --> VS
    VS --> CS
    
    PS --> |Store| SQLITE
    VS --> |Search/Store| QC
    CS --> |Embed/Complete| OAI
    CS --> |Retrieve| QC
    CS --> |Session| SQLITE
    US --> |Auth| SQLITE
```

## Sequence Diagrams

### PDF Upload and Processing Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as FastAPI
    participant WS as WebSocket
    participant BT as Background Task
    participant DB as SQLite
    participant E as OpenAI
    participant Q as Qdrant Cloud
    
    U->>F: Upload PDF
    F->>DB: Create Document Record
    F->>BT: Schedule Processing
    F-->>U: Upload Accepted
    
    BT->>BT: Extract Text
    BT->>WS: Update Progress
    BT->>BT: Create Chunks
    BT->>WS: Update Progress
    BT->>E: Generate Embeddings
    BT->>WS: Update Progress
    BT->>Q: Store Vectors
    BT->>DB: Update Status
    BT->>WS: Processing Complete
```

### Chat Query Flow

```mermaid
sequenceDiagram
    participant U as User
    participant F as FastAPI
    participant C as Cache
    participant DB as SQLite
    participant E as OpenAI
    participant Q as Qdrant Cloud
    
    U->>F: Send Query
    F->>C: Check Cache
    alt Cache Hit
        C-->>F: Return Cached Response
        F-->>U: Return Response
    else Cache Miss
        F->>DB: Log Query
        F->>E: Generate Query Embedding
        F->>Q: Semantic Search
        Q-->>F: Similar Chunks
        F->>E: Generate Response
        F->>DB: Store Response
        F->>C: Cache Response
        F-->>U: Return Response
    end
```

## Data Model

```mermaid
erDiagram
    User ||--o{ Document : owns
    User ||--o{ ChatSession : owns
    Document ||--o{ Chunk : contains
    User {
        string id PK
        string email
        string hashed_password
        timestamp created_at
        timestamp updated_at
        boolean is_active
    }
    Document {
        string id PK
        string user_id FK
        string filename
        string status
        timestamp created_at
        timestamp updated_at
        timestamp deleted_at
        index idx_user_docs
    }
    Chunk {
        string id PK
        string document_id FK
        string content
        int position
        string vector_id
        index idx_doc_chunks
    }
    ChatSession ||--o{ Message : contains
    ChatSession {
        string id PK
        string user_id FK
        timestamp created_at
        string status
        index idx_user_sessions
    }
    Message {
        string id PK
        string session_id FK
        string role
        string content
        timestamp created_at
        json sources
        index idx_session_msgs
    }
```

## Project Structure

```mermaid
graph TD
    subgraph Project Root
        B[backend]
        F[frontend]
        D[docker]
        DOC[docs]
    end
    
    subgraph Backend Structure
        B --> BA[app]
        B --> BT[tests]
        B --> BS[scripts]
        B --> BM[migrations]
        
        BA --> BC[core]
        BA --> BR[api]
        BA --> BSV[services]
        BA --> BMD[models]
        BA --> BU[utils]
        
        BC --> BCC[config.py]
        BC --> BCL[logger.py]
        BC --> BCA[auth.py]
        BC --> BCH[health.py]
        
        BR --> BRD[documents.py]
        BR --> BRC[chat.py]
        BR --> BRU[users.py]
        BR --> BRH[health.py]
        
        BSV --> BSVP[pdf.py]
        BSV --> BSVV[vector.py]
        BSV --> BSVC[chat.py]
        BSV --> BSVU[user.py]
        
        BMD --> BMDB[base.py]
        BMD --> BMDD[document.py]
        BMD --> BMDC[chat.py]
        BMD --> BMDU[user.py]
    end
    
    subgraph Frontend Structure
        F --> FS[src]
        FS --> FC[components]
        FS --> FP[pages]
        FS --> FH[hooks]
        FS --> FU[utils]
        
        FC --> FCC[Chat]
        FC --> FCP[PDFUpload]
        FC --> FCU[UserAuth]
        
        FP --> FPH[Home]
        FP --> FPC[Chat]
        FP --> FPL[Login]
        
        FH --> FHA[useChat]
        FH --> FHU[useUpload]
        FH --> FHW[useWebSocket]
        
        FU --> FUF[fetcher.ts]
        FU --> FUA[auth.ts]
        FU --> FUW[ws.ts]
    end
    
    subgraph Documentation
        DOC --> DA[api]
        DOC --> DE[examples]
        DOC --> DD[deployment]
    end
``` 