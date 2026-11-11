# ContentPilot

## Local database

ContentPilot uses MySQL and reads its connection settings from environment variables. The database must exist, and the application user needs permission to create and change tables for Flyway migrations.

When running the app on the host machine against the Docker container exposed on port `3307`, set:

```bash
export DB_URL=jdbc:mysql://127.0.0.1:3307/content_pilot
export DB_USERNAME=your_mysql_user
read -rs -p 'MySQL password: ' DB_PASSWORD; echo
export DB_PASSWORD
mvn spring-boot:run
```

Replace the database name and user with those configured in your MySQL container. Keep passwords out of project files and Git. If ContentPilot later runs in a container on the same Docker network, use the MySQL service name and its internal port `3306` in `DB_URL`.

Open `http://localhost:8080/` for the homepage and `http://localhost:8080/actuator/health` for the health check.

Run `mvn test` for the automated tests. They use an in-memory H2 database and do not need a running MySQL container.
