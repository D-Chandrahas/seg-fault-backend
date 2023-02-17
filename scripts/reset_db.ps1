Push-Location $PSScriptRoot
Push-Location "../database management"
(sqlite3 "../database/cqadb.sqlite" ".read 'reset_db.sql'")
Pop-Location
Pop-Location