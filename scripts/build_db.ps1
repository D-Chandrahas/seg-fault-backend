Push-Location $PSScriptRoot
(sqlite3 "..\database\cqadb.sqlite" ".read 'reset_db.sql'") *> $null
Pop-Location