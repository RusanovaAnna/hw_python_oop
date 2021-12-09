from typing import Union, List


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(
            self,
            training_type: str,
            duration: float,
            distance: float,
            speed: float,
            calories: float,
    ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        return(f"Тип тренировки: {self.training_type}; "
               f"Длительность: {self.duration:.3f} ч.; "
               f"Дистанция: {self.distance:.3f} км; "
               f"Ср. скорость: {self.speed:.3f} км/ч; "
               f"Потрачено ккал: {self.calories:.3f}.")


class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000
    min = 60

    def __init__(
            self,
            action: int,
            duration: float,
            weight: float,
    ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        message = InfoMessage(self.__class__.__name__,
                              self.duration,
                              self.get_distance(),
                              self.get_mean_speed(),
                              self.get_spent_calories())
        return message


class Running(Training):
    """Тренировка: бег."""
    const_c_r_1 = 18
    const_c_r_2 = 20

    def get_spent_calories(self) -> float:
        cal_r = ((self.const_c_r_1 * self.get_mean_speed()
                 - self.const_c_r_2) * self.weight
                 / self.M_IN_KM) * (self.duration * self.min)
        return cal_r


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    const_c_w_1 = 0.035
    const_c_w_2 = 2
    const_c_w_3 = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        cal_w = (self.const_c_w_1 * self.weight
                 + (self.get_mean_speed() ** self.const_c_w_2 // self.height)
                 * self.const_c_w_3 * self.weight) * (self.duration * self.min)
        return cal_w


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    const_c_s_1 = 1.1
    const_c_s_2 = 2

    def get_distance(self) -> float:
        """Получить дистанцию в км."""

        return self.action * self.LEN_STEP / self.M_IN_KM

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return ((self.length_pool
                 * self.count_pool) / self.M_IN_KM) / self.duration

    def get_spent_calories(self) -> float:
        cal_s = (self.get_mean_speed()
                 + self.const_c_s_1) * self.const_c_s_2 * self.weight
        return cal_s


def read_package(workout_type: str, data: List[Union[int, float]]) -> Training:
    """Прочитать данные полученные от датчиков."""
    work = {"SWM": Swimming,
            "RUN": Running,
            "WLK": SportsWalking}
    if workout_type not in work.keys():
        raise ValueError("Неизвестный тип тренировки")
    training = work[workout_type](*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == "__main__":
    packages = [
        ("SWM", [720, 1, 80, 25, 40]),
        ("RUN", [15000, 1, 75]),
        ("WLK", [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
