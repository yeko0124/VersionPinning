#!/usr/bin/env python
# -*- coding: utf-8 -*-

# author        : Seongcheol Jeon
# created date  : 2024.02.15
# modified date : 2024.02.15
# description   :

import typing


# 여기서 singleton을 관리해줌
class _SingletonWrapper:
    def __init__(self, cls):
        self.__wrapped = cls
        self.__instance = None

    def __call__(self, *args, **kwargs):
        if self.__instance is None:
            self.__instance = self.__wrapped(*args, **kwargs)
        return self.__instance


def singleton(cls):
    return _SingletonWrapper(cls)


class BitMask:
    def __init__(self):
        self.__field = 0b0000

    # def __str__(self) -> str:
    #     bits = list()
    #     digits = 8
    #     for i in range(digits):
    #         bits.append(str((self.__INSTANCE.FIELD >> (digits - 1 - i)) & 0x01))
    #         if ((i + 1) % 4) == 0:
    #             bits.append(' ')
    #     return ''.join(bits)

    def get_show_field(self):
        bits = list()
        digits = 8
        for i in range(digits):
            bits.append(str((self.__field >> (digits - 1 - i)) & 0x01))
            if ((i + 1) % 4) == 0:
                bits.append(' ')
        return ''.join(bits)

    @property
    def field(self):
        return self.__field

    def __activate(self, num: int) -> None:
        self.__field |= (0x01 << num)

    def __deactivate(self, num: int) -> None:
        self.__field &= (~(0x01 << num))

    def __toggle(self, num: int) -> None:
        self.__field ^= (0x01 << num)

    def __confirm(self, num: int) -> bool:
        return bool(self.__field & (0x01 << num))

    def activate(self, bitfield: int) -> None:
        self.__field |= bitfield

    def deactivate(self, bitfield: int) -> None:
        self.__field &= (~bitfield)

    def toggle(self, bitfield: int) -> None:
        self.__field ^= bitfield

    def confirm(self, bitfield: int) -> bool:
        return bool(self.__field & bitfield)

    def confirm_onebit(self, num: int) -> bool:
        return bool(self.__field & (0x01 << num))

    def empty(self) -> None:
        self.__field = 0

    def all(self) -> None:
        self.__field = -1


# 코드가 중복되지 않게 singleton 데코를 씌워줌
@singleton
class SingletonBitMask(BitMask): ...


class Stack:
    class Node:
        def __init__(self, data):
            self.data = data
            self.next = None

    def __init__(self):
        self.top = None

    def push(self, data) -> None:
        if self.top is None:
            self.top = Stack.Node(data)
        else:
            node = Stack.Node(data)
            node.next = self.top
            self.top = node

    def pop(self) -> typing.Any:
        if self.top is None:
            return None
        node = self.top
        self.top = self.top.next
        return node.data

    def peek(self) -> typing.Any:
        if self.top is None:
            return None
        return self.top.data

    def is_empty(self) -> bool:
        return self.top is None


if __name__ == '__main__':
    b1 = BitMask()
    b2 = BitMask()

    print(b1, b2)

    b1.empty()
    b2.empty()
    b1.activate(1)  # 0001
    b2.activate(2)  # 0010

    print(b1.get_show_field())
    print(b2.get_show_field())

    print('-----------------------------------------------')

    # 같은 객체를 공유하고 있음
    sb1 = SingletonBitMask()
    sb2 = SingletonBitMask()

    print(sb1, sb2)

    sb1.empty()
    sb2.empty()
    sb1.activate(1)  # 0001
    sb2.activate(2)  # 0010

    # 그러다보니 같은 FIELD를 공유하고 있음
    print(sb1.get_show_field())
    print(sb1.get_show_field())
