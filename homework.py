from dataclasses import dataclass

@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: int
          
    def get_message(self) -> str:
        """Получить дистанцию в км."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')

@dataclass
class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000.0
    M_IN_HR = 60
    action: int
    duration: float
    weight: float
        

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        self.distance = self.action * self.LEN_STEP / self.M_IN_KM
        return self.distance

    def get_mean_speed(self) -> float:
        self.get_distance()
        self.mean_speed = self.distance / self.duration
        return self.mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())

@dataclass
class Running(Training):
    """Тренировка: бег."""
    run_calorie_1 = 18
    run_calorie_2 = 20
    action: int
    duration: float
    weight: float

    def get_spent_calories(self) -> float:
        self.get_mean_speed()
        return ((self.run_calorie_1 * self.get_mean_speed() - self.run_calorie_2)
                * self.weight / self.M_IN_KM * self.duration * self.M_IN_HR)

@dataclass
class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    sw_calorie_1 = 0.035
    sw_calorie_2 = 0.029
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        self.get_mean_speed()
        return ((self.sw_calorie_1 * self.weight + (self.get_mean_speed() ** 2
                // self.height) * self.sw_calorie_2 * self.weight)
                * self.duration * self.M_IN_HR)

@dataclass
class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    s_calorie_1 = 1.1
    s_calorie_2 = 2
    action: int
    duration: float
    weight: float
    length_pool: float
    count_pool: int
           
    def get_mean_speed(self) -> float:
        self.mean_speed = (self.length_pool * self.count_pool
                           / self.M_IN_KM / self.duration)
        return self.mean_speed

    def get_spent_calories(self) -> float:
        self.get_mean_speed()
        return ((self.get_mean_speed() + self.s_calorie_1)
                * self.s_calorie_2 * self.weight)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workout_type_dict: dict[str, Training] = {'SWM': Swimming,
                                              'RUN': Running,
                                              'WLK': SportsWalking}
    training = workout_type_dict[workout_type](*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)