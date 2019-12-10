.. _api:

Developer Interface
===================

.. module:: libpurecool.dyson
.. module:: libpurecool.dyson_device
.. module:: libpurecool.dyson_360_eye
.. module:: libpurecool.dyson_pure_cool
.. module:: libpurecool.dyson_pure_cool_link
.. module:: libpurecool.dyson_pure_hotcool_link
.. module:: libpurecool.dyson_pure_hotcool
.. module:: libpurecool.dyson_pure_state
.. module:: libpurecool.dyson_pure_state_v2

This part of the documentation covers all the interfaces of libpurecool.


Classes
-------

Common
~~~~~~

DysonAccount
############

.. autoclass:: libpurecool.dyson.DysonAccount
    :members:

NetworkDevice
#############

.. autoclass:: libpurecool.dyson_device.NetworkDevice
    :members:

Fan/Purifier devices
~~~~~~~~~~~~~~~~~~~~

DysonPureCool
#################

.. autoclass:: libpurecool.dyson_pure_cool.DysonPureCool
    :members:
    :inherited-members:

DysonPureCoolLink
#################

.. autoclass:: libpurecool.dyson_pure_cool_link.DysonPureCoolLink
    :members:
    :inherited-members:

DysonPureHotCoolLink
####################

.. autoclass:: libpurecool.dyson_pure_hotcool_link.DysonPureHotCoolLink
    :members:
    :inherited-members:

DysonPureCoolState
##################

.. autoclass:: libpurecool.dyson_pure_state.DysonPureCoolState
    :members:

DysonEnvironmentalSensorState
#############################

.. autoclass:: libpurecool.dyson_pure_state.DysonEnvironmentalSensorState
    :members:

DysonPureHotCoolState
#####################

.. autoclass:: libpurecool.dyson_pure_state.DysonPureHotCoolState
    :members:
    :inherited-members:

Eye 360 robot vacuum device
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Dyson360Eye
###########

.. autoclass:: libpurecool.dyson_360_eye.Dyson360Eye
    :members:
    :inherited-members:

Dyson360EyeState
################

.. autoclass:: libpurecool.dyson_360_eye.Dyson360EyeState
    :members:

Dyson360EyeTelemetryData
########################

.. autoclass:: libpurecool.dyson_360_eye.Dyson360EyeTelemetryData
    :members:

Dyson360EyeMapData
##################

.. autoclass:: libpurecool.dyson_360_eye.Dyson360EyeMapData
    :members:

Dyson360EyeMapGrid
##################

.. autoclass:: libpurecool.dyson_360_eye.Dyson360EyeMapGrid
    :members:

Dyson360EyeMapGlobal
####################

.. autoclass:: libpurecool.dyson_360_eye.Dyson360EyeMapGlobal
    :members:

Exceptions
----------

DysonNotLoggedException
~~~~~~~~~~~~~~~~~~~~~~~

.. autoexception:: libpurecool.exceptions.DysonNotLoggedException

DysonInvalidTargetTemperatureException
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. autoexception:: libpurecool.exceptions.DysonInvalidTargetTemperatureException
