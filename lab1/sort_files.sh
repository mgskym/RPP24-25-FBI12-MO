if [ -d "$1" ]; then
    ls -lt
else
    echo "Ошибка. Директория не существует или не указана"
fi
