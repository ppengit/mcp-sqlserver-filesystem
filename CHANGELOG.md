# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2025-08-26

### Added
- Database reconnection mechanism with `database_reconnect` tool
- Database status checking with `database_status` tool
- Graceful database connection failure handling
- Dynamic tool availability based on database connection status

### Changed
- **BREAKING**: Database connection failures no longer crash the MCP server
- MCP server now starts successfully even when database is unavailable
- Database tools are dynamically hidden when database is not available
- Improved error messages for database connection issues

### Removed
- All UI-related code and parameters (`show_ui`, `confirm_ui`, etc.)
- UI references in tool descriptions
- Unused UI confirmation dialogs

### Fixed
- MCP server startup failure when SQL Server is unavailable
- Database connection error handling
- Tool availability logic

## [1.0.2] - 2025-08-25

### Added
- Enhanced database connection parameters
- Improved error handling and logging
- Cross-platform compatibility improvements

### Changed
- Updated database connection string format
- Improved security configurations

## [1.0.1] - 2025-08-24

### Added
- Initial release
- SQL Server database operations
- Filesystem operations
- Security features
- Environment variable configuration

### Features
- SQL query execution (SELECT, INSERT, UPDATE, DELETE)
- Table schema inspection
- File read/write operations
- Directory listing
- SQL injection protection
- Filesystem access control
