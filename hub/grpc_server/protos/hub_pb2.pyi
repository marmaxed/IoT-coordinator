from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Iterable as _Iterable, Mapping as _Mapping, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor
HUMIDITY_SENSOR: SensorType
LIGHT_SENSOR: SensorType
TEMPERATURE_SENSOR: SensorType

class AllSensorsDataRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class AllSensorsDataResponse(_message.Message):
    __slots__ = ["sensors"]
    SENSORS_FIELD_NUMBER: _ClassVar[int]
    sensors: _containers.RepeatedCompositeFieldContainer[Sensor]
    def __init__(self, sensors: _Optional[_Iterable[_Union[Sensor, _Mapping]]] = ...) -> None: ...

class AllSensorsListRequest(_message.Message):
    __slots__ = []
    def __init__(self) -> None: ...

class AllSensorsListResponse(_message.Message):
    __slots__ = ["sensor_list"]
    class SensorListEntry(_message.Message):
        __slots__ = ["key", "value"]
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: int
        value: SensorType
        def __init__(self, key: _Optional[int] = ..., value: _Optional[_Union[SensorType, str]] = ...) -> None: ...
    SENSOR_LIST_FIELD_NUMBER: _ClassVar[int]
    sensor_list: _containers.ScalarMap[int, SensorType]
    def __init__(self, sensor_list: _Optional[_Mapping[int, SensorType]] = ...) -> None: ...

class Sensor(_message.Message):
    __slots__ = ["sensor_id", "sensor_name", "sensor_type", "timestamp", "value"]
    SENSOR_ID_FIELD_NUMBER: _ClassVar[int]
    SENSOR_NAME_FIELD_NUMBER: _ClassVar[int]
    SENSOR_TYPE_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    sensor_id: int
    sensor_name: str
    sensor_type: SensorType
    timestamp: int
    value: float
    def __init__(self, sensor_id: _Optional[int] = ..., sensor_type: _Optional[_Union[SensorType, str]] = ..., sensor_name: _Optional[str] = ..., value: _Optional[float] = ..., timestamp: _Optional[int] = ...) -> None: ...

class SensorDataRequest(_message.Message):
    __slots__ = ["sensor_id"]
    SENSOR_ID_FIELD_NUMBER: _ClassVar[int]
    sensor_id: int
    def __init__(self, sensor_id: _Optional[int] = ...) -> None: ...

class SensorDataResponse(_message.Message):
    __slots__ = ["sensor"]
    SENSOR_FIELD_NUMBER: _ClassVar[int]
    sensor: Sensor
    def __init__(self, sensor: _Optional[_Union[Sensor, _Mapping]] = ...) -> None: ...

class SensorsDataRequest(_message.Message):
    __slots__ = ["sensor_ids"]
    SENSOR_IDS_FIELD_NUMBER: _ClassVar[int]
    sensor_ids: _containers.RepeatedScalarFieldContainer[int]
    def __init__(self, sensor_ids: _Optional[_Iterable[int]] = ...) -> None: ...

class SensorsDataResponse(_message.Message):
    __slots__ = ["sensor_list"]
    SENSOR_LIST_FIELD_NUMBER: _ClassVar[int]
    sensor_list: _containers.RepeatedCompositeFieldContainer[Sensor]
    def __init__(self, sensor_list: _Optional[_Iterable[_Union[Sensor, _Mapping]]] = ...) -> None: ...

class TimeRequest(_message.Message):
    __slots__ = ["sensor_id", "since", "until"]
    SENSOR_ID_FIELD_NUMBER: _ClassVar[int]
    SINCE_FIELD_NUMBER: _ClassVar[int]
    UNTIL_FIELD_NUMBER: _ClassVar[int]
    sensor_id: int
    since: int
    until: int
    def __init__(self, sensor_id: _Optional[int] = ..., since: _Optional[int] = ..., until: _Optional[int] = ...) -> None: ...

class TimeResponse(_message.Message):
    __slots__ = ["time", "value"]
    TIME_FIELD_NUMBER: _ClassVar[int]
    VALUE_FIELD_NUMBER: _ClassVar[int]
    time: _containers.RepeatedScalarFieldContainer[int]
    value: _containers.RepeatedScalarFieldContainer[float]
    def __init__(self, time: _Optional[_Iterable[int]] = ..., value: _Optional[_Iterable[float]] = ...) -> None: ...

class SensorType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = []
