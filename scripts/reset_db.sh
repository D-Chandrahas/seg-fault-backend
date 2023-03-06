workingdir=$PWD
cd $( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )
cd "../database management"
sqlite3 "../database/cqadb.sqlite" ".read 'reset_db.sql'"
cd $workingdir