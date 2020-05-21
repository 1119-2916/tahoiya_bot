import sys
import random
from typing import List
from enum import Enum
from collections import OrderedDict
from functools import total_ordering
from copy import deepcopy


class User:

    def __init__(self, id:int, name:str):
        self.__id = id
        self.name = name

    @property
    def id(self):
        return self.__id

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return NotImplemented
        return self.__id == other.__id

    def __hash__(self):
        return hash(self.__id)


class ExplanationText:

    def __init__(self, text:str, writer:User, correct:bool = False):
        self.__text = text
        self.__writer = writer
        self.__correct = correct
        self.__voted = {}

    @property
    def text(self):
        return self.__text

    @property
    def writer(self):
        return self.__writer

    @property
    def is_correct(self):
        return self.__correct

    @property
    def voted(self):
        return deepcopy(self.__voted)

    def set_correct(self):
        self.__correct = True

    def set_wrong(self):
        self.__correct = False

    def add_voted(self, usr:User, point:int):
        if self.__writer != usr:
            self.__voted[usr] = point


class TahoiyaMaster:

    class State(Enum):
        NEUTRAL = 0
        WAITING_EXP_TEXTS = 1
        WAITING_VOTES = 2
        FINISH = 3

    def __init__(self):
        self.__users = {}
        self.neutral()

    def neutral(self):
        self.__prob = None
        self.__explanations = {}
        self.__state = self.State.NEUTRAL

    @property
    def state(self):
        return self.__state

    @property
    def problem(self):
        return self.__prob

    @property
    def users(self):
        return deepcopy(self.__users)

    @property
    def explanations(self):
        return deepcopy(self.__explanations)

    def add_user(self, usr:User, point:int = 10):
        self.__users[usr] = point

    def set_problem(self, prob:str):
        if self.__state == self.State.NEUTRAL:
            self.__prob = prob
            self.__state = self.State.WAITING_EXP_TEXTS

    # 状態 2 なら説明文を追加できる
    def add_wrong_explanation(self, text:ExplanationText):
        if self.__state == self.State.WAITING_EXP_TEXTS:
            text.set_wrong()
            self.__explanations[text.writer] = text

    def add_correct_explanation(self, text:ExplanationText):
        if self.__state == self.State.WAITING_EXP_TEXTS:
            text.set_correct()
            self.__explanations[text.writer] = text

    def finish_exp_step(self):
        is_correct = lambda exp: exp.is_correct
        # 説明文が1より多く、説明文の中にたった1つの正しい説明文が存在する
        if (self.__state == self.State.WAITING_EXP_TEXTS 
                and len(self.__explanations) > 1
                and len(filter(is_correct, self.__explanations)) == 1):
            # 問題文のシャッフルはここで
            random.shuffle(self.__explanations)
            self.__state = self.State.WAITING_VOTES
            return True
        else:
            return False

    def add_vote(self, usr:User, index:int, point:int):
        if self.__state == self.State.WAITING_VOTES:
            self.__explanations[index].add_voted(usr, point)

    def get_voted(self):
        let = []
        for exp in self.__explanations:
            let.extend(list(exp.voted.keys()))
        return let

    def finish_vote(self):
        if self.__state == self.State.WAITING_VOTES:
            self.__state = self.State.FINISH
            result = self.get_result()
            for u, v in result.items():
                self.__users[u] += v

    def get_result(self):
        if self.__state == self.State.FINISH:
            ret = {}
            for exp in self.__explanations:
                if exp.is_correct:
                    for u, v in exp.voted.items():
                        ret[u] += v
                        ret[exp.writer] -= v
                else:
                    for u, v in exp.voted.items():
                        ret[u] -= v + 1
                        ret[exp.writer] += v
            return let
        else:
            return None
    

# test
if __name__ == '__main__':
    master = TahoiyaMaster()
    print('state = ', master.state)

    ikeda = User(1, 'ikeda')
    nikeda = User(2, 'nikeda')
    sankeda = User(3, 'sankeda')
    paka = User(4, 'iko')
    pika = User(5, 'niko')
    puka = User(6, 'iko')
    peka = User(7, 'niko')
    poka1 = User(8, 'noko')
    poka2 = User(8, 'nonoko')
    
    master.add_user(ikeda)
    master.add_user(nikeda)
    master.add_user(sankeda)
    master.add_user(paka)
    master.add_user(pika)
    master.add_user(puka)
    master.add_user(peka)
    master.add_user(peka)
    master.add_user(poka1)
    master.add_user(poka2)

    for u, v in master.users.items():
        print(u.name, v)
    
    master.set_problem("たほいや")

    print('state = ', master.state)
    print("問題　：　", master.problem)

    exp1 = ExplanationText("犬", ikeda)
    exp2 = ExplanationText("猫", nikeda)
    exp3 = ExplanationText("猫", sankeda)
    exp4 = ExplanationText("亀", paka)
    exp5 = ExplanationText("桃", pika)
    exp6 = ExplanationText("やらい小屋", puka)
    exp7 = ExplanationText("やおい小屋", peka)
    exp8 = ExplanationText("hogehuga", poka2)
    master.add_wrong_explanation(exp1)
    master.add_wrong_explanation(exp2)
    master.add_wrong_explanation(exp3)
    master.add_wrong_explanation(exp4)
    master.add_wrong_explanation(exp5)
    master.add_correct_explanation(exp6)
    master.add_wrong_explanation(exp7)
    master.add_wrong_explanation(exp8)

    for u, e in master.explanations.items():
        print(u.name, e.text, e.writer.name)

    



