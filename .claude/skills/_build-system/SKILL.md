# Build System Auto-Detection Skill

Automatically detects the project's build system and runs the appropriate commands.

## Detection Rules

| Detection File | Project Type | Build Command | Test Command | Run Command |
|----------------|-------------|---------------|-------------|-------------|
| `Makefile` | Make | `make` | `make test` | `make run` |
| `package.json` | Node.js | `npm run build` | `npm test` | `npm start` |
| `pyproject.toml` | Python (modern) | `pip install -e .` | `pytest` | `python -m <pkg>` |
| `requirements.txt` | Python (classic) | `pip install -r requirements.txt` | `pytest` | `python main.py` |
| `Cargo.toml` | Rust | `cargo build` | `cargo test` | `cargo run` |
| `go.mod` | Go | `go build ./...` | `go test ./...` | `go run .` |
| `*.csproj` | .NET | `dotnet build` | `dotnet test` | `dotnet run` |
| `*.sln` | .NET (solution) | `dotnet build` | `dotnet test` | `dotnet run` |
| `pom.xml` | Maven (Java) | `mvn compile` | `mvn test` | `mvn exec:java` |
| `build.gradle` | Gradle (Java) | `./gradlew build` | `./gradlew test` | `./gradlew run` |
| `build.gradle.kts` | Gradle (Kotlin DSL) | `./gradlew build` | `./gradlew test` | `./gradlew run` |
| `Dockerfile` | Docker | `docker build .` | - | `docker run` |
| `CMakeLists.txt` | CMake (C/C++) | `cmake --build build/` | `ctest --test-dir build/` | `./build/<binary>` |
| `*.dpr` | Delphi | `dcc32 *.dpr` | - | `./<binary>` |
| `Gemfile` | Ruby | `bundle install` | `bundle exec rspec` | `bundle exec ruby main.rb` |
| `mix.exs` | Elixir | `mix compile` | `mix test` | `mix run` |
| `build.zig` | Zig | `zig build` | `zig build test` | `zig build run` |
| `dub.json` / `dub.sdl` | D | `dub build` | `dub test` | `dub run` |

## Package Manager Detection

### Node.js

| Detection File | Package Manager | install | run |
|----------------|----------------|---------|-----|
| `pnpm-lock.yaml` | pnpm | `pnpm install` | `pnpm run` |
| `yarn.lock` | yarn | `yarn install` | `yarn` |
| `bun.lockb` | bun | `bun install` | `bun run` |
| `package-lock.json` | npm | `npm install` | `npm run` |
| (none) | npm (default) | `npm install` | `npm run` |

### Python

| Detection File | Package Manager | install |
|----------------|----------------|---------|
| `uv.lock` | uv | `uv sync` |
| `poetry.lock` | poetry | `poetry install` |
| `Pipfile.lock` | pipenv | `pipenv install` |
| `requirements.txt` | pip | `pip install -r requirements.txt` |
| `pyproject.toml` (default) | pip | `pip install -e .` |

## Lint Tool Detection

| Detection File/Config | Lint Tool | Run Command |
|-----------------------|-----------|-------------|
| `.eslintrc*` / `eslint.config.*` | ESLint | `npx eslint .` |
| `biome.json` | Biome | `npx biome check .` |
| `ruff.toml` / `pyproject.toml [tool.ruff]` | Ruff | `ruff check .` |
| `Cargo.toml` | Clippy | `cargo clippy` |
| `go.mod` | go vet | `go vet ./...` |
| `.golangci.yml` | golangci-lint | `golangci-lint run` |
| `Makefile` (lint target) | make lint | `make lint` |

## Multiple Build Systems

If the project has multiple build files, priority order:
1. `Makefile` (often used as top-level orchestrator)
2. Language-specific build files (package.json, Cargo.toml, etc.)
3. `Dockerfile` (container build)

## On Build Failure

1. Parse error message
2. Classify error type (compile/dependency/config/test)
3. Attempt auto-fix with `/_build-fix` command
4. Verify with rebuild after fix
