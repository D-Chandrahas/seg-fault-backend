Push-Location
cd $PSScriptRoot
cd "../database management"
sqlite3 "../database/cqadb.sqlite" ".read 'reset_db.sql'"
Pop-Location