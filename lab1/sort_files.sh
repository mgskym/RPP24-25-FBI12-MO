if [ -d "$1" ]; then
    cd "$1"
    ls -l | grep "^-"
else
    echo "Ошибка. Директория не существует или не указана"
fi