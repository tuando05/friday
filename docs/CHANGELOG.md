# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- New `audio` module for better separation of concerns.

### Changed
- Extracted voice listener and speaker functionality from `core` into `audio` package.
- Renamed `core/voice.py` to `audio/listener.py`.
- Renamed `core/speaker.py` to `audio/speaker.py`.

### Planned
- Web interface
- Multi-user support
- Advanced memory management
- Additional skills and abilities

## [0.2.0] - 2026-05-03

### Added
- Special command handling (exit, clear memory, help, etc)
- Enhanced command parser
- Command documentation

## [0.1.0] - 2026-05-01

### Added
- Initial project setup with modular architecture
- Core modules: brain, config, guard, memory, commands, services
- Conversation history persistence with JSON storage
- Ollama integration for local LLMs
- Vietnamese language support in UI and prompts
- System command handling (exit, clear memory, etc)
- File vault system for file management
- Complete documentation (README, DEVELOPMENT, CHANGELOG)
- Environment variable configuration via .env
- Comprehensive .gitignore
- Local AI conversation functionality
