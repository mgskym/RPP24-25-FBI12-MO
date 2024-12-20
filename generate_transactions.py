import asyncio
import json
import random
from datetime import datetime
import sys

categories_list = ["Appliances and electronics", "Food and Cafe", "Clothes and shoes", "Transport"]

category_limits = {
    "Appliances and electronics": 20000,
    "Food and Cafe": 10000,
    "Clothes and shoes": 15000,
    "Transport": 8000,
}

def generate_transaction():
    amount_min = 100
    amount_max = 10000
    transaction = {
        "timestamp": datetime.now().timestamp(),
        "category": random.choice(categories_list),
        "amount": round(random.uniform(amount_min, amount_max), 2),
    }
    return transaction

async def generate_transactions_group(group_size, transactions_count):
    for i in range(0, transactions_count, group_size):
        group = []
        for j in range(min(group_size, transactions_count - i)):
            group.append(generate_transaction())
        yield group

async def cost_analysis(filename):
    category_sums = {}

    with open(filename, "r") as file:
        transactions = json.load(file)

    for transaction in transactions:
        category = transaction["category"]
        amount = transaction["amount"]

        if category not in category_sums:
            category_sums[category] = 0.0
        category_sums[category] += amount

        limit = category_limits.get(category, float("inf"))
        if category_sums[category] > limit:
            print(f"Лимит расходов по '{category}' превышен на {round(category_sums[category] - limit, 2)}. Итоговая сумма по категории: {round(category_sums[category], 2)}")

    print('=' * 40)
    print("Сумма расходов по каждой категории:")
    print('-' * 40)
    for category, total in category_sums.items():
        print(f"{category}: {round(total, 2)}")
    print('=' * 40)

async def main(transactions_count):
    group_size = 10
    group_number = 1

    async for group in generate_transactions_group(group_size, transactions_count):
        filename = f"transaction_group_{group_number}.json"
        with open(filename, "w") as file:
            file.write(json.dumps(group, indent=4))
        print(f"Группа транзакций {group_number} успешно сохранена!")

        await cost_analysis(filename)

        group_number += 1

if __name__ == "__main__":
    asyncio.run(main(int(sys.argv[1])))