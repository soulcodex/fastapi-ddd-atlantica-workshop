from injector import Injector
from apps.shoes.container.common_di import CommonDi
from apps.shoes.container.shoes_di import ShoesDi

di_container = Injector([CommonDi(), ShoesDi()])
