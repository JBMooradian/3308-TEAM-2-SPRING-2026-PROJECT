# 3308-TEAM-2-SPRING-2026-PROJECT

# Cawler ID

**Team #:** 2  
**Team/Product Name:** Team Cawl / Cawler ID

---

## Team Members

| Name | GitHub Username | Email |
|------|----------------|-------|
| Peyton Cunningham | peytoncunningham720 | GrokCO303@gmail.com |
| Bri Martinez | bmartinez-web | briannarosemartinez@gmail.com |
| Stephen Enriquez | latencies | sten8791@colorado.edu |
| Jake Mooradian | JBMooradian | jbmooradian@gmail.com |

---

## Weekly Meeting

Mondays or Wednesdays at 7pm Mountain Time via Zoom — 30 minutes

---

## Vision Statement

Web application that acts as an ornithology tool, identifying the birds around you via a user-uploaded recording of a bird call. 

---

## Motivation

Driven by the challenge of integrating complex signal processing with full-stack engineering, our team is using Cawler ID as a technical proving ground for modern software collaboration. While similar tools exist, our focus is mastering the synchronization of a Python-based machine learning pipeline with a high-performance React frontend. Ultimately, we aim to refine our collective skills in Scrum methodology, database architecture, and machine learning development.


---

## Risks and Mitigation Strategies

_Risk_: New Technology Stack. Limited experience with audio processing libraries (e.g., Librosa) and ML frameworks. \
_Strategy_: Team members have background knowledge that can fill gaps, and class material will provide structure. Dedicate Sprint 0 to "Spikes" (research tasks) and building a simple audio uploader.

_Risk_: Data Scarcity. Difficulty finding high-quality, labeled bird call datasets.\
_Strategy_: Utilize the Xeno-canto API and Kaggle datasets to ensure a diverse training set.

_Risk_: Scope Creep. Attempting to identify too many species in one semester.\
_Strategy_: Limit initial MVP to the most common North American backyard birds.

---

## Development Method

We will utilize an Agile Scrum framework to ensure iterative progress and transparency. \
    -Sprints: Weekly iterations focusing on specific functional increments. \
    -Sprint Planning: Primary use of weekly meeting time, where we select items from the Product Backlog for the upcoming Sprint. \
    -Asynchronous Stand-ups: Conducted via Discord on non-meeting days to report: \
        a. What did I do yesterday? \
        b. What am I doing today? \
        c. Are there any blockers? \
    -Sprint Review & Retrospective: Occurs at the end of each Sprint to discuss internal process improvements. \
    -Tools: We will use GitHub Projects for our Kanban board and issue tracking. 


---

## Development Steps
1. Identify a suitable open-source database from our list of candidates, and isolate a sample data set
2. Define user stories to identify minimum viable features
3. Design backend software and machine learning mechanisms that correctly and reliably identify a series of test inputs
4. Design a frontend interface that accepts user input, displays output, and clearly explains intended use
5. Polish frontend interface and visuals, expand output bird profiles to include more detail

---

## Technology Stack
Frontend: React.js\
    -efficient for handling the "state" of an audio upload (e.g., showing a loading spinner while the model processes). \
Backend: FastAPI (Python) \
    -built for high-speed asynchronous tasks. Processing audio files and running a Neural Network is "blocking" work; FastAPI handles this better than Flask or Node.js. \
Database: PostgreSQL \
    -for structured data: User accounts, bird species names, scientific descriptions, and "History" of previous identifications. 




## Project Tracking

This shared GitHub repository and our weekly standups
