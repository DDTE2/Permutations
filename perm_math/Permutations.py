try:
    from math import lcm
except:
    from math import gcd

    lcm = lambda a, b: a * b // gcd(a, b)

class perms:
    def __init__(self, start={}, end=None): ## start - начальное состояние, end - конечное
        if isinstance(start, list) or isinstance(start, tuple):
            if isinstance(end, list) or isinstance(end, tuple):
                l = len(start)
                self.dict = {start[a]:end[a] for a in range(l)}
            else:
                try:
                    raise TypeError(f'Неизвестный тип {end}')
                except:
                    raise TypeError(f'Неизвестный тип переменной')
        elif isinstance(start, dict):
            if end == None:
                self.dict = start.copy()
            else:
                try:
                    raise TypeError(f'Неизвестный тип {end}')
                except:
                    raise TypeError(f'Неизвестный тип переменной')
        else:
            try:
                raise TypeError(f'Неизвестный тип {start},{end}')
            except:
                raise TypeError(f'Неизвестный тип переменной') ## Представление перестановки в виде словаря

        self.cycles = self.dict_to_cycles() ## Представление перестановки в произведения минимальных циклов
        self.order = self.order_calc() ## Порядок перестановки
        self.parity = self.parity_calc() ## Чётность перестановки. 0 - чётная, 1 - нечётная

    def dict_to_cycles(self): ## Функция разложения перестановки в произведение циклов
        res = []
        perm = self.dict.copy()

        while perm:
            m = min(perm)
            x = perm.pop(m)

            if m == x:
                self.dict.pop(m)
            else:
                res1 = [m]

                while x != m:
                    res1.append(x)
                    x = perm.pop(x)

                res.append(tuple(res1))
                res1.clear()

        return sorted(res)
    def order_calc(self): ## Вычисление порядка перестановки
        self.number_of_elements = 0 ##Число элементов перестановки
        order = 1

        for a in self.cycles:
            l = len(a)
            order = lcm(l, order)
            self.number_of_elements += l

        return order
    def parity_calc(self): ## Вычисление чётности перестановки
        res = 0

        for cycle in self.cycles:
            parity = (len(cycle) + 1) % 2
            res ^= parity

        return res

    def __str__(self): ## Строковое представление перестановки
        res = [str(a) for a in self.cycles]

        if res:
            return ''.join(res)
        else:
            return '()'
    def __repr__(self): ## Внутреннее представление перестановки в Python
        return str(self)
    def __hash__(self): ## Хэширование перестановки, как строки
        return str(self).__hash__()

    def __mul__(self, other): ## Вычисление композиции (произведения перстановок)
        if not isinstance(other, perms):
            try:
                raise TypeError(f'Неизвестный тип {perms}')
            except:
                raise TypeError(f'Неизвестный тип переменной')

        A = other.dict.copy()
        B = self.dict.copy()

        res = {}
        for a in A:
            x = A[a]

            if x in B:
                x = B.pop(x)

            if a != x:
                res[a] = x

        for a in B:
            x = B[a]

            if a != x:
                res[a] = x

        return perms(res)
    def __rmul__(self, other):
        if not isinstance(other, perms):
            try:
                raise TypeError(f'Неизвестный тип {perms}')
            except:
                raise TypeError(f'Неизвестный тип переменной')

        return other * self

    def __pow__(self, power, modulo=None): ## Возведение перестановки в степень
        if not isinstance(power, int):
            raise TypeError(f'{power} должно быть целым числом')

        res = {}
        for cycle in self.cycles:
            x = exponentiation_cycles(cycle, power)
            res.update(x)

        return perms(res)

    def __xor__(self, other): ## Возведение перестановки в степень, используя оператор ^
        return self ** other

    def __eq__(self, other):## Проверка, равны ли перестановки
        return str(self) == str(other)

    def __bool__(self): ## Проверка, является ли перестановка тождественной
        if self == '()':
            return False
        else:
            return True

    def copy(self): ## Копирование перестановки
        return perms(self.dict)

def exponentiation_cycles(cycle, power):
    order = len(cycle)
    power %= order

    if not power:
        return {}

    perm = {}
    for a in range(order):
        x = cycle[a]
        y = cycle[(a + power) % order]

        perm[x] = y

    return perm
