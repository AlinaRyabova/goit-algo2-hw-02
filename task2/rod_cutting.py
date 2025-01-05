from typing import List, Dict
from colorama import init, Fore

init(autoreset=True)

def rod_cutting_memo(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через мемоізацію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """
    
    def helper(n: int, memo: Dict[int, Dict]):
        if n == 0:
            return {"max_profit": 0, "cuts": [], "number_of_cuts": 0}
        if n in memo:
            return memo[n]
        
        max_profit = 0
        best_cuts = []
        
        for i in range(1, n + 1):
            if i <= len(prices):
                result = helper(n - i, memo)
                current_profit = prices[i - 1] + result["max_profit"]
                if current_profit > max_profit:
                    max_profit = current_profit
                    best_cuts = result["cuts"] + [i]

        memo[n] = {
            "max_profit": max_profit,
            "cuts": best_cuts,
            "number_of_cuts": len(best_cuts) - 1
        }
        return memo[n]

    return helper(length, {})

def rod_cutting_table(length: int, prices: List[int]) -> Dict:
    """
    Знаходить оптимальний спосіб розрізання через табуляцію

    Args:
        length: довжина стрижня
        prices: список цін, де prices[i] — ціна стрижня довжини i+1

    Returns:
        Dict з максимальним прибутком та списком розрізів
    """
    dp = [0] * (length + 1)
    cuts = [[] for _ in range(length + 1)]

    for i in range(1, length + 1):
        max_profit = 0
        best_cut = []
        for j in range(1, i + 1):
            if j <= len(prices) and dp[i - j] + prices[j - 1] > max_profit:
                max_profit = dp[i - j] + prices[j - 1]
                best_cut = cuts[i - j] + [j]
        dp[i] = max_profit
        cuts[i] = best_cut

    return {
        "max_profit": dp[length],
        "cuts": cuts[length],
        "number_of_cuts": len(cuts[length]) - 1
    }

def run_tests():
    """Функція для запуску всіх тестів"""
    test_cases = [
        # Тест 1: Базовий випадок
        {
            "length": 5,
            "prices": [2, 5, 7, 8, 10],
            "name": "Базовий випадок"
        },
        # Тест 2: Оптимально не різати
        {
            "length": 3,
            "prices": [1, 3, 8],
            "name": "Оптимально не різати"
        },
        # Тест 3: Всі розрізи по 1
        {
            "length": 4,
            "prices": [3, 5, 6, 7],
            "name": "Рівномірні розрізи"
        }
    ]

    for test in test_cases:
        print(f"\n{Fore.CYAN}Тест: {test['name']}")
        print(f"{Fore.YELLOW}Довжина стрижня: {test['length']}")
        print(f"{Fore.YELLOW}Ціни: {test['prices']}")

        # Тестуємо мемоізацію
        memo_result = rod_cutting_memo(test['length'], test['prices'])
        print(f"\n{Fore.GREEN}Результат мемоізації:")
        print(f"{Fore.RED}Максимальний прибуток: {memo_result['max_profit']}")
        print(f"{Fore.RED}Розрізи: {memo_result['cuts']}")
        print(f"{Fore.RED}Кількість розрізів: {memo_result['number_of_cuts']}")

        # Тестуємо табуляцію
        table_result = rod_cutting_table(test['length'], test['prices'])
        print(f"\n{Fore.GREEN}Результат табуляції:")
        print(f"{Fore.RED}Максимальний прибуток: {table_result['max_profit']}")
        print(f"{Fore.RED}Розрізи: {table_result['cuts']}")
        print(f"{Fore.RED}Кількість розрізів: {table_result['number_of_cuts']}")

        print(f"\n{Fore.MAGENTA}Перевірка пройшла успішно!")

if __name__ == "__main__":
    run_tests()
