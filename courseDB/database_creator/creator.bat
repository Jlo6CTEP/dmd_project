IF EXIST ../courseDB (echo file exists) ELSE (
sqlite3 ./courseDB < ./commands.txt
move ./courseDB ..
)
cmd /k
