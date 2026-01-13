"""
Данный фрагмент кода на Java реализует алгоритм генерации простых чисел,
используя метод многократного перемножения входного набора заведомо простых чисел.
Основная идея заключается в том, что на каждой итерации одно простое число перемножается с другим,
затем результат удваивается, и к нему прибавляется единица.
Полученное число проверяется на простоту с использованием функции addIfPrime,
которая осуществляет проверку на псевдопростоту и применяет аналог теста Ферма для детерминированной проверки простоты.

Алгоритм использует два списка: mod3_1 для хранения простых чисел с остатком 1 при делении на 3, и l для хранения чисел,
признанных простыми функцией addIfPrime.
В процессе работы алгоритма происходит перебор всех возможных пар простых чисел из входного списка, их перемножение,
проверка на простоту и добавление в соответствующий список.

Особенностью данного подхода является использование фильтрации по модулю 3 для исключения чисел, кратных трём,
что ускоряет процесс генерации и повышает эффективность проверки простоты.
Кроме того, алгоритм учитывает разрядность полученных простых чисел и ограничивает мощность генерации,
чтобы избежать избыточного количества промежуточных простых чисел.
"""
from typing import Generator, Optional


class PrimeGenerator:
	# Константы начальных простых чисел
	TWO: int = 2
	THREE: int = 3

	def __init__(self):
		self._primes: list[int] = []

	def get_primes(self) -> list[int]:
		return self._primes

	def generate_primes(self, input_primes: list[int]) -> Generator[int, None, None]:
		"""
		Генерация простых чисел путём многократного перемножения входного набора заведомо простых.
		На каждой итерации одно входное простое перемножается с другим, затем результат умножается на 2,
		после чего к результату прибавляется единица: probablyPrime=prime1*prime2*2+1
		Каждое потенциально простое далее проверяется на псевдопростоту в функции add_if_prime.
		Если псевдопростота исключена, то потенциально простое проверяется на простоту при помощи аналога
		теста Ферма, являющегося детерминированным для любых чисел, не являющихся псевдопростыми по основанию 2.
		"""
		# Список простых чисел с остатком при делении по модулю 3 = 1.
		mod3_1 = []
		# Список чисел, признанных простыми функцией add_if_prime()
		local_primes: list[int] = []

		# Цикл обработки простых чисел, данных в виде входящего параметра в процедуру.
		# В цикле для каждого входного простого вычисляется его произведение со всеми остальными простыми.
		# Если результат перемножения не равен единице по модулю 3, то такие числа игнорируются из-за
		# порождения при последующих перемножениях чисел, кратных трём.
		for k in range(len(input_primes) - 1):
			seed = input_primes[k]

			seed_doubled = seed << 1  # seed * 2

			result_0 = seed % self.THREE

			if result_0 == 1:
				mod3_1.append(seed)

			# Цикл по тем простым числам, с которыми данное число пока что не перемножалось
			for i in range(k + 1, len(input_primes)):
				result = input_primes[i] % self.THREE

				if result == result_0:
					# Пара обязательно будет делиться на 3, пропускаем
					continue
				else:
					# Если делимости на 3 нет, то проверяем на простоту
					self.add_if_prime(input_primes[i], seed, seed_doubled, local_primes)

		self._primes = local_primes

		# В этом цикле каждое ранее найденное простое перемножается с ранее отобранными простыми,
		# дающими по модулю 3 единицу. Результат перемножения проверяется на простоту функцией add_if_prime.
		while True:
			print(f"found {len(local_primes)}, bits={local_primes[0].bit_length() if local_primes else 0}")
			local_primes = []
			for k in range(len(self._primes)):
				seed = self._primes[k]

				seed_doubled = seed << 1  # seed * 2
				# Проходим по списку равных единице по модулю тройки чисел и перемножаем их на
				# ранее полученные простые результаты аналогичных перемножений
				for i in range(len(mod3_1)):
					self.add_if_prime(mod3_1[i], seed, seed_doubled, local_primes)

				# Проверяем разрядность полученных простых чисел, с целью ограничения мощности генерации
				if local_primes and local_primes[0].bit_length() < 700:
					n = 100 # максимально допустимое количество простых чисел на текущей итерации
				elif local_primes and local_primes[0].bit_length() < 800:
					n = 500
				elif local_primes and local_primes[0].bit_length() < 900:
					n = 2000
				else:
					n = 10_000
				if len(local_primes) > n:
					break  # Если количество полученных простых больше максимально допустимого, то выходим из данного цикла
			self._primes = local_primes

			for num in local_primes:
				yield num

			if len(local_primes) == 0:
				break

	def add_if_prime(self, a: int, b: int, b_doubled: int, local_primes: list[int]) -> None:
		a_doubled: int = a << 1  # alter: a * 2
		full_product: int = b * a_doubled  # a * b * 2
		new_potential_prime: int = full_product + 1

		result: Optional[int] = None

		if a_doubled < b:
			result = pow(self.TWO, a_doubled, new_potential_prime)
		elif a < b_doubled:
			result = pow(self.TWO, a, new_potential_prime)
		if result == 1:
			# Полученное число псевдослучайное
			return

		if b_doubled < a:
			result = pow(self.TWO, b_doubled, new_potential_prime)
		elif b < a_doubled:
			result = pow(self.TWO, b, new_potential_prime)
		if result == 1:
			# Полученное число псевдослучайное
			return

		result = pow(self.TWO, full_product >> 1, new_potential_prime)  # full_product == fp; 2^(fp/2) mod n
		if result != 1:
			# Полученное число составное
			return

		local_primes.append(new_potential_prime)


def main() -> None:
	"""Точка запуска файла."""

	# initial_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
	initial_primes = [
		2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71,
		73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151,
		157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233,
		239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311
	]
	pr = PrimeGenerator()
	generator = pr.generate_primes(initial_primes)

	with open("big_primes.txt", "w") as w_file:
		for i in generator:
			print(i)
			if i.bit_length() > 100:
				w_file.write(f"{i}\n")

	return None


if __name__ == "__main__":
	main()
	# a = 956317513020534262615100203184617734758327
	# print(a.bit_length())
