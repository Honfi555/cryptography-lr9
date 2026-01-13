from random import randint


class DiffieHellman:
	def __init__(self, g: int, secret_key: int = None, p: int = None) -> None:
		self.g = g  # base
		self.secret_key = secret_key  # Secret key
		self.p = p  # big prime number

		self.s = None # Shared secret key

	def generate_public_key(self) -> int:
		return pow(self.g, self.secret_key, self.p)

	def calculate_shared_secret(self, public_key: int) -> None:
		self.s = pow(public_key, self.secret_key, self.p)
		print("Shared secret is:", self.s)

def main() -> None:
	"""Точка запуска файла."""

	dh_a = DiffieHellman(5, 6, 23)
	print(public_key_a := dh_a.generate_public_key())

	dh_b = DiffieHellman(5, 9, 23)
	print(public_key_b := dh_b.generate_public_key())

	dh_a.calculate_shared_secret(public_key_b)
	dh_b.calculate_shared_secret(public_key_a)

	return None


def cryptographically_strong_example() -> None:
	"""Точка запуска файла."""
	p: int = 956317513020534262615100203184617734758327

	secret_key_a: int = randint(2, p-2)
	secret_key_b: int = randint(2, p-2)
	print("secret_key_a =", secret_key_a, "\nsecret_key_b =", secret_key_b)

	dh_a = DiffieHellman(2, secret_key_a, p)
	dh_b = DiffieHellman(2, secret_key_b, p)

	print(public_key_a := dh_a.generate_public_key())
	print(public_key_b := dh_b.generate_public_key())

	dh_a.calculate_shared_secret(public_key_b)
	dh_b.calculate_shared_secret(public_key_a)

	return None


if __name__ == "__main__":
	# main()
	cryptographically_strong_example()
