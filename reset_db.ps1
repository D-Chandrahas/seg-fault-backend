Push-Location $PSScriptRoot
(sqlite3 .\database\cqadb.sqlite ".read 'database management/reset_db.sql'") *> $null
Pop-Location