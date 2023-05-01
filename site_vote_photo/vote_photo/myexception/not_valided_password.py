class UpdatePasswordExciption(Exception):
    def __init__(self, password, message):
        self.password = password
        self.message = message
        super().__init__(self.password)

    def __str__(self):
        return (
            f"Ваш пароль {self.password} не подходит под условия. Пароль должен быть:\n"
            f"1) Больше 8 символов.\n"
            f"2) Меньше 20 символов.\n"
            f"3) Не схож с username.\n"
            f"4) Не должен состоять из одних лишь цифр и букв.\n"
            f"В вашем случае: {self.message}."
        )
