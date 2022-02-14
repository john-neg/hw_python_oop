from dataclasses import dataclass
from typing import List, ClassVar, Type, Dict


@dataclass(repr=False, eq=False)
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        message: str = (f"Тип тренировки: {self.training_type}; "
                        + f"Длительность: {self.duration:.3f} ч.; "
                        + f"Дистанция: {self.distance:.3f} км; Ср. "
                        + f"скорость: {self.speed:.3f} км/ч; "
                        + f"Потрачено ккал: {self.calories:.3f}.")
        return message


@dataclass(repr=False, eq=False)
class Training:
    """Базовый класс тренировки."""
    action: int
    duration: float
    weight: float
    LEN_STEP: ClassVar[float] = 0.65
    M_IN_KM: ClassVar[float] = 1000
    MIN_IN_HOUR: ClassVar[float] = 60

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        distance: float = self.action * self.LEN_STEP / self.M_IN_KM
        return distance

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = self.get_distance() / self.duration
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(
            f"Определите get_spent_calories в {self.__class__.__name__}")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        info: InfoMessage = InfoMessage(type(self).__name__,
                                        self.duration,
                                        self.get_distance(),
                                        self.get_mean_speed(),
                                        self.get_spent_calories())
        return info


@dataclass(repr=False, eq=False)
class Running(Training):
    """Тренировка: бег."""
    RUNNING_COEFF_1: ClassVar[float] = 18
    RUNNING_COEFF_2: ClassVar[float] = 20

    def get_spent_calories(self) -> float:
        calories: float = ((self.RUNNING_COEFF_1 * self.get_mean_speed()
                           - self.RUNNING_COEFF_2) * self.weight
                           / self.M_IN_KM * self.duration * self.MIN_IN_HOUR)
        return calories


@dataclass(repr=False, eq=False)
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    height: float
    WALKING_COEFF_1: ClassVar[float] = 0.035
    WALKING_COEFF_2: ClassVar[float] = 0.029

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories: float = ((self.WALKING_COEFF_1 * self.weight
                           + (self.get_mean_speed() ** 2 // self.height)
                           * self.WALKING_COEFF_2 * self.weight)
                           * self.duration * self.MIN_IN_HOUR)
        return calories


@dataclass(repr=False, eq=False)
class Swimming(Training):
    """Тренировка: плавание."""
    length_pool: int
    count_pool: int
    LEN_STEP: ClassVar[float] = 1.38
    SWIMMING_COEFF_1: ClassVar[float] = 1.1
    SWIMMING_COEFF_2: ClassVar[float] = 2

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        speed: float = (self.length_pool * self.count_pool
                        / self.M_IN_KM / self.duration)
        return speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        calories: float = ((self.get_mean_speed() + self.SWIMMING_COEFF_1)
                           * self.SWIMMING_COEFF_2 * self.weight)
        return calories


def read_package(workout_type: str, data: List[int]) -> Training:
    """Прочитать данные полученные от датчиков."""
    training_types: Dict[str, Type[Training]] = {
        "SWM": Swimming,
        "RUN": Running,
        "WLK": SportsWalking,
    }
    return training_types.get(workout_type)(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info: InfoMessage = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        try:
            training: Training = read_package(workout_type, data)
            main(training)
        except TypeError:
            print(f"Неверные данные {workout_type}, {data}")
