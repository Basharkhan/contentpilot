
# Content Pilot

## Project
Build a content management and AI-assisted
publishing application for a Facebook Page
called Content Pilot.

## Technology
- Java 21
- Spring Boot 4.1.2
- Maven
- Spring AI 1.1.x
- Thymeleaf
- Bootstrap 5
- MySQL
- Spring Data JPA
- Flyway

## Architecture
- Use a modular monolith.
- Follow controller-service-repository separation.
- Keep business logic out of controllers.
- Use DTOs for request and response objects.
- Use constructor injection.
- Use clear domain boundaries.
- Avoid unnecessary abstractions.

## AI integration
- Use Spring AI ChatClient.
- Never hardcode API keys.
- Keep prompts separate from business logic.
- Validate AI-generated output.
- Never assume AI-generated facts are correct.
- Store source references when available.

## Development rules
- Do not implement multiple milestones at once.
- Explain important architectural decisions.
- Write tests for business logic.
- Run Maven tests after implementation.
- Do not introduce unnecessary dependencies.
- Do not modify unrelated files.
- Never publish content without explicit approval.
- Ask before introducing major architectural changes.
