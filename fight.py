from abc import abstractmethod, ABCMeta
import random
import time


class Monster(metaclass=ABCMeta):
    """
    凶兽的基类，为抽象类
    """
    def __init__(self, name):
        """初始化凶兽的名称，血量"""
        self._name = name
        self._HP = 400

    @property
    def HP(self):
        return self._HP

    @HP.setter
    def HP(self, HP):
        self._HP = HP 

    @property
    def name(self):
        return self._name

    @abstractmethod
    def attack(self):
        """抽象的方法"""
        pass 

    def alive(self):
        return self._HP > 0 


class HolyBeast(metaclass=ABCMeta):
    def __init__(self, name):
        """初始化圣兽的名称，血量"""
        self._name = name 
        self._HP = 400
    
    @property
    def HP(self):
        return self._HP

    @HP.setter
    def HP(self, HP):
        self._HP = HP

    @property
    def name(self):
        return self._name

    @abstractmethod
    def attack(self):
        pass

    def resume(self):
        """自我恢复，使用随机模块来判定几率大小"""
        rand = random.random()
        if rand > 0.95:
            self._HP += int(0.02*self._HP)
        else:
            self.HP += 10

    def alive(self):
        return self._HP > 0


class TaoTie(Monster):
    def __init__(self, name):
        """调用父类的初始化方法"""
        super().__init__(name)

    def attack(self):
        """实现攻击时所攻击的血量，其余功能由beat实现"""
        rand = random.random()
        if rand > 0.85:
            kill_blood = 90 
        elif rand > 0.55:
            kill_blood = 35
        else:
            kill_blood = 20
        return kill_blood

    def beat(self, other):
        kill_blood = self.attack()
        print("凶兽{} 击杀 圣兽{} {} HP".format(self.name, other.name, kill_blood))
        other.HP -= kill_blood


class QingLong(HolyBeast):
    def __init__(self, name):
        super().__init__(name)

    def attack(self):
        rand = random.random()
        if rand > 0.9:
            kill_blood = 100
        elif rand > 0.6:
            kill_blood = 40 
        else:
            kill_blood = 10 
        return kill_blood

    def beat(self, other):
        kill_blood = self.attack()
        print("圣兽{} 击杀 凶兽{} {} HP".format(self.name, other.name, kill_blood))
        other.HP -= kill_blood
        self.resume()


def main():
    ql = QingLong("青龙")
    tt = TaoTie("饕餮")
    num = 0
    while ql.alive() and tt.alive():
        ql.beat(tt)
        tt.beat(ql)
        if ql.alive() and tt.alive():
            print("-----------回合{}------------".format(num))
            print("{}血量为:{},{}血量为:{}".format(ql.name, ql.HP, tt.name, tt.HP))
            time.sleep(0.5)
        else:
            print("")
            if ql.alive():
                print("{}血量为:{},{}血量为:0".format(ql.name, ql.HP, tt.name))
                print(">{}< 胜利".format(ql.name))
            else:
                print("{}血量为:0,{}血量为:{}".format(ql.name, tt.name, tt.HP))
                print(">{}< 胜利".format(tt.name))
        num += 1


if __name__ == '__main__':
    main()



