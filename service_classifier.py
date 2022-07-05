''' На вход принимает str, на выходе dict вида {service_class: int, ‘service_name’: str}
Возвращаемый dict формировать путём рандомного выбора пары ключ-значение из этого словаря
{1: ‘консультация’, 2: ‘лечение’, 3: ‘стационар’, 4: ‘диагностика’, 5: ‘лаборатория’},
где ключ это service_class, а значение это ‘service_name’.'''

import random


def service_classifier(string):
    service = {1: 'консультация', 2: 'лечение', 3: 'стационар', 4: 'диагностика', 5: 'лаборатория'}
    n = random.choice(list(service))
    return {n: service[n]}
