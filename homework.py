class InfoMessage:
    """Информационное сообщение о тренировке."""
    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: int,
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self) -> str:
        """Получить дистанцию в км."""
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')

class Training:
    """Базовый класс тренировки."""
    LEN_STEP = 0.65
    M_IN_KM = 1000.0
    M_IN_HR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

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


class Running(Training):
    """Тренировка: бег."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    M_IN_HR = 60
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        super().__init__(action, duration, weight)
  
    def get_spent_calories(self) -> float:
        self.get_mean_speed()
        run_calorie_1 = 18
        run_calorie_2 = 20
        return ((run_calorie_1 * self.get_mean_speed() - run_calorie_2) 
                 * self.weight / self.M_IN_KM * self.duration * self.M_IN_HR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    M_IN_KM = 1000
    M_IN_HR = 60
    LEN_STEP = 0.65
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height
        
    def get_spent_calories(self) -> float:
        self.get_mean_speed()
        sw_calorie_1 = 0.035
        sw_calorie_2 = 0.029
        return ((sw_calorie_1 * self.weight + (self.get_mean_speed() ** 2 
                 // self.height) * sw_calorie_2 * self.weight) 
                 * self.duration * self.M_IN_HR)
        

class Swimming(Training):
    """Тренировка: плавание."""
    M_IN_KM = 1000
    LEN_STEP = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        self.mean_speed = (self.length_pool * self.count_pool 
                           / self.M_IN_KM / self.duration)
        return self.mean_speed

    def get_spent_calories(self) -> float:
        self.get_mean_speed()
        s_calorie_1 = 1.1
        s_calorie_2 = 2
        return ((self.get_mean_speed() + s_calorie_1) 
                 * s_calorie_2 * self.weight)

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

