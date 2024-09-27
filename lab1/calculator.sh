if [ "$2" -eq "+" ]; then
    result=$(("$1" + "$3"))
if [ "$2" -eq "-" ]; then
    result=$(("$1" - "$3"))
else
    echo "Ошибка. Неверное выражение"
fi

echo "Результат: $result"