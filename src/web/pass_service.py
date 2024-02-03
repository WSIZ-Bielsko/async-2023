from argon2 import PasswordHasher


class PasswordService:

    def __init__(self):
        self.ph = PasswordHasher()

    def get_hash(self, password: str):
        return self.ph.hash(password)

    def check_password(self, correct_hash: str, password: str) -> bool:
        """

        :param correct_hash:
        :param password:
        :return: Raises VerifyMismatchError if password incorrect.
        """
        return self.ph.verify(correct_hash, password)


if __name__ == '__main__':
    ps = PasswordService()
    h = ps.get_hash('Kadabra')
    print(ps.check_password(h, 'Kadabra!'))
