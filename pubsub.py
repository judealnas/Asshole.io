from __future__ import annotations
import abc


class Observer(abc.ABC):
    @abc.abstractmethod
    def update(self, observable: Observable, *args, **kwargs):
        pass


class Observable(abc.ABC):
    @abc.abstractmethod
    def add_observer(self, observer: Observer):
        pass
