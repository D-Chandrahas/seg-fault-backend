Push-Location $PSScriptRoot
(sqlite3 .\database\cqadb.db ".read 'database management/reset_db.sql'") *> $null
Pop-Location