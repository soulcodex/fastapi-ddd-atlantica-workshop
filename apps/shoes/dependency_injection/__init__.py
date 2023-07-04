from pyxdi import PyxDI
from apps.shoes.dependency_injection.shoes_di import ShoesDi
from apps.shoes.dependency_injection.common_di import CommonDi

# Bootstrap di container
di = PyxDI()

# Modules
di.register_module(CommonDi)
di.register_module(ShoesDi)
