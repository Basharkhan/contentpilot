# ContentPilot issue drafts

These issues are ordered by dependency. Implement and verify one milestone at a time.

## 01 — Set up the MySQL database and verify foundation startup

**Milestone:** 1 — Project foundation

**Scope:** Create the `content_pilot` database and a dedicated application user in the existing MySQL 8 Docker container. Complete the dependency switch from PostgreSQL to MySQL and verify the app against the host port `3307`.

**Acceptance criteria:**
- Database uses `utf8mb4`; credentials remain outside Git.
- Flyway initializes successfully and Hibernate remains set to `validate`.
- The app starts with MySQL; `/` renders and `/actuator/health` returns `UP`.
- `mvn test` passes, and the MySQL connection check is recorded.

## 02 — Complete foundation configuration and Thymeleaf layout

**Milestone:** 1 — Project foundation

**Depends on:** 01

**Scope:** Add a small reusable page layout and document local configuration and profiles. Keep the package structure focused on existing features.

**Acceptance criteria:**
- The homepage uses a reusable Thymeleaf layout or fragments.
- Development and test configuration are documented without committing secrets.
- A clean checkout can run the documented setup and tests.
- Foundation changes are committed and pushed to `main`.

## 03 — Integrate a Boot 4 compatible Gemini model through Spring AI

**Milestone:** 2 — Gemini integration

**Depends on:** 02

**Scope:** Choose a Spring AI release compatible with Spring Boot 4.1.2, update the project guidance, add the Gemini model starter, and configure `ChatClient` with an environment-provided API key.

**Acceptance criteria:**
- No API key is committed or logged.
- A service can send a manual topic to Gemini and receive a response.
- Prompts live outside controller and business logic.
- Configuration and failure behavior are covered by focused tests.

## 04 — Generate and validate a Bangla Facebook draft from a manual topic

**Milestone:** 2 — Gemini integration

**Depends on:** 03

**Scope:** Add a simple form for a manual topic and generate a Bangla draft. Keep generation separate from publication.

**Acceptance criteria:**
- The user can enter a topic and see a Bangla draft.
- Empty or malformed model output is rejected with a useful message.
- The prompt asks for appropriate length and style, but does not treat model-generated facts or citations as verified.
- Generation errors do not publish or discard an existing saved draft.

## 05 — Create the content schema with Flyway and JPA

**Milestone:** 3 — Content management

**Depends on:** 04

**Scope:** Add only the data needed for topics, posts, and source references. Use Flyway for schema changes and JPA for persistence.

**Acceptance criteria:**
- Flyway creates `Topic`, `Post`, and `PostSource` tables with appropriate keys and timestamps.
- A post can store body text, hashtags, status, creation time, and source URLs.
- Hibernate validation passes against a newly migrated MySQL database.
- Repository and service tests cover persistence behavior.

## 06 — Save generated drafts and list them in the dashboard

**Milestone:** 3 — Content management

**Depends on:** 05

**Scope:** Persist generated drafts and show them in Thymeleaf pages with their topics and source references.

**Acceptance criteria:**
- Generated drafts survive application restart.
- Dashboard list and detail pages show post text, status, timestamps, and source links.
- The app stores the model/provider used for generation where available.
- Duplicate form submission does not create unintended duplicate drafts.

## 07 — Add editing, revision history, approval, and rejection

**Milestone:** 4 — Approval dashboard

**Depends on:** 06

**Scope:** Let the Page owner edit and review drafts. Preserve previous text when a draft is revised.

**Acceptance criteria:**
- A draft can be edited or rejected from the dashboard.
- Revisions retain the previous text and edit time.
- Approval records the exact reviewed version and the approving action.
- Rejected or unapproved posts cannot enter the publishing path.

## 08 — Collect candidate topics from RSS sources

**Milestone:** 5 — Topic discovery

**Depends on:** 06

**Scope:** Read Google Trends Trending Now RSS and a configurable set of news RSS feeds. Start with science, politics, and viral topics relevant to the Page.

**Acceptance criteria:**
- Each candidate stores its title, source URL, retrieval time, and category.
- Feed failures are isolated and visible without stopping other feeds.
- Duplicate or stale entries are filtered before generation.
- No feed item is presented as a verified fact solely because it is trending.

## 09 — Generate up to five morning drafts by 8 a.m. Dhaka time

**Milestone:** 5 — Topic discovery

**Depends on:** 08, 04, 06

**Scope:** Rank suitable distinct topics and run discovery and generation early enough for drafts to be ready by 8:00 a.m. `Asia/Dhaka`.

**Acceptance criteria:**
- A daily run creates up to five Bangla drafts with source links; unsuitable topics are skipped rather than used as filler.
- The dashboard shows run progress, partial results, and errors.
- Re-running a day does not create duplicate drafts for the same topics.
- A manual run is available for testing and recovery.

## 10 — Approve a post with a scheduled publication time

**Milestone:** 6 — Scheduling

**Depends on:** 07

**Scope:** Add a schedule time to the approval action and persist the approved version for later publication.

**Acceptance criteria:**
- The owner explicitly chooses a valid future publication time in `Asia/Dhaka`.
- Only the approved version is scheduled; later edits require a new review before publication.
- Scheduled posts can be viewed and canceled before publication.
- State transitions and invalid scheduling requests have business-logic tests.

## 11 — Verify Meta Page access and Graph API configuration

**Milestone:** 7 — Meta Graph API

**Depends on:** 02

**Scope:** Configure the Meta app, Page identity, access token storage, and required permissions. Verify access without creating a public post.

**Acceptance criteria:**
- Page identity and token are configured outside source control.
- A read-only connection check confirms the selected Page and usable permissions.
- Token expiry and permission failures produce actionable diagnostics.
- Current Meta requirements are checked against official documentation before implementation.

## 12 — Publish due approved posts through the Graph API

**Milestone:** 7 — Meta Graph API

**Depends on:** 10, 11

**Scope:** A background worker finds due scheduled posts and publishes their approved text to the Facebook Page.

**Acceptance criteria:**
- No post is sent without explicit prior approval and a due schedule.
- Successful publication stores the Meta post ID and time.
- Failures store the response and permit safe investigation or retry.
- Concurrent or repeated worker runs do not knowingly create duplicate posts; uncertain outcomes are reconciled before retry.
- Publisher behavior is tested with a stubbed Graph API response.

## 13 — Add focused security, observability, and integration checks

**Milestone:** 8 — Testing and deployment

**Depends on:** 12

**Scope:** Protect the owner dashboard, validate requests, and make generation and publishing failures diagnosable.

**Acceptance criteria:**
- Unauthenticated users cannot edit, approve, schedule, or publish posts.
- Logs omit API keys, Page tokens, and database passwords.
- Tests cover the full draft-to-scheduled-to-published path and failure cases.
- Health and application logs identify failed daily runs and publishing attempts.

## 14 — Deploy a continuously running MVP

**Milestone:** 8 — Testing and deployment

**Depends on:** 13

**Scope:** Package ContentPilot for an always-running host with MySQL, environment-based secrets, and repeatable startup.

**Acceptance criteria:**
- Deployment instructions cover build, configuration, database migrations, startup, and rollback.
- The daily job runs on the deployed host and meets the 8 a.m. draft target.
- Scheduled approved posts publish at their chosen time.
- A backup and restore procedure covers the content database.
