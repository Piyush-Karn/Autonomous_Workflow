# 🚀 Future Roadmap: From Research to Strategy

This document outlines the strategic evolution of the **Autonomous Workflow** platform. The goal is to transition from a "Data Discovery" tool to a "Decision Intelligence" ecosystem.

## 🎯 Phase 1: The Strategic Engine (Short Term)

### 1. Automated SWOT Analysis 
Implement a logic layer within the `Analyst` agent that maps NLP patterns to a SWOT framework:
- **Strengths**: Co-occurrence of high-sentiment entities and market leaders.
- **Weaknesses**: Themes linked to "risk", "conflict", or "decline" keywords.
- **Opportunities**: Divergent entities with rising volume but low institutional coverage.
- **Threats**: Rapidly accelerating negative sentiment clusters or competitive disruptors.

### 2. Decision Matrix Generation
Transform "Insights" into "Actions":
- **Immediate Action**: Trends with >80% confidence and high growth.
- **Monitor closely**: High-divergence topics (wide expert disagreement).
- **Discard/Low Priority**: Saturated themes with declining sentiment.

## 🧠 Phase 2: Conversational Intelligence (Mid Term)

### 3. "Chat with your Report" (RAG)
Leverage `langchain` and `faiss` (already in requirements) to create a local vector database of all scraped research.
- **User Story**: "I've generated a 20-page report on EVs. Now I want to ask: 'What did the specific expert from the UIUC professor's article say about battery solid-state longevity?'"
- **Tech**: Recursive character splitting, FAISS indexing, and retrieval-based QA.

## 📈 Phase 3: Competitive Edge (Long Term)

### 4. Cross-Topic Comparison
Allow the user to load two different research cycles and generate a "Gap Analysis."
- **Use Case**: Compare "Company A Strategy" vs "Company B Strategy" to find where Company B is winning the discourse battle.

### 5. Automated "Flash Alerts"
Integration with Slack/Discord to send alerts when:
- A specific entity's sentiment drops below a threshold.
- A new "Divergent Theme" is detected in a recurring research topic.

---
*Roadmap curated for Piyush Kumar @ Autonomous Workflow.*
