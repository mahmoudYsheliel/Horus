from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class LogLevel(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    DEBUG: _ClassVar[LogLevel]
    INFO: _ClassVar[LogLevel]
    WARNING: _ClassVar[LogLevel]
    ERROR: _ClassVar[LogLevel]
    CRITICAL: _ClassVar[LogLevel]

class ServiceStatus(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    OFFLINE: _ClassVar[ServiceStatus]
    ONLINE: _ClassVar[ServiceStatus]

class MonitorServiceRequest(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
    __slots__ = ()
    LOGS_HISTORY: _ClassVar[MonitorServiceRequest]
    SERVICES_STATUS: _ClassVar[MonitorServiceRequest]
    FILTER_CONFIG: _ClassVar[MonitorServiceRequest]
    SETTINGS_CONFIG: _ClassVar[MonitorServiceRequest]
    STREAM_SOURCES: _ClassVar[MonitorServiceRequest]
DEBUG: LogLevel
INFO: LogLevel
WARNING: LogLevel
ERROR: LogLevel
CRITICAL: LogLevel
OFFLINE: ServiceStatus
ONLINE: ServiceStatus
LOGS_HISTORY: MonitorServiceRequest
SERVICES_STATUS: MonitorServiceRequest
FILTER_CONFIG: MonitorServiceRequest
SETTINGS_CONFIG: MonitorServiceRequest
STREAM_SOURCES: MonitorServiceRequest

class LogMsg(_message.Message):
    __slots__ = ("timestamp", "log_level", "src", "msg")
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    LOG_LEVEL_FIELD_NUMBER: _ClassVar[int]
    SRC_FIELD_NUMBER: _ClassVar[int]
    MSG_FIELD_NUMBER: _ClassVar[int]
    timestamp: int
    log_level: LogLevel
    src: str
    msg: str
    def __init__(self, timestamp: _Optional[int] = ..., log_level: _Optional[_Union[LogLevel, str]] = ..., src: _Optional[str] = ..., msg: _Optional[str] = ...) -> None: ...

class LogMsgList(_message.Message):
    __slots__ = ("logs",)
    LOGS_FIELD_NUMBER: _ClassVar[int]
    logs: _containers.RepeatedCompositeFieldContainer[LogMsg]
    def __init__(self, logs: _Optional[_Iterable[_Union[LogMsg, _Mapping]]] = ...) -> None: ...

class ServicesStatusMap(_message.Message):
    __slots__ = ("map",)
    class MapEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: ServiceStatus
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[ServiceStatus, str]] = ...) -> None: ...
    MAP_FIELD_NUMBER: _ClassVar[int]
    map: _containers.ScalarMap[str, ServiceStatus]
    def __init__(self, map: _Optional[_Mapping[str, ServiceStatus]] = ...) -> None: ...

class Filter(_message.Message):
    __slots__ = ("filter", "input_src", "output_channel", "enable_recording", "filter_params")
    class FilterParamsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    FILTER_FIELD_NUMBER: _ClassVar[int]
    INPUT_SRC_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_CHANNEL_FIELD_NUMBER: _ClassVar[int]
    ENABLE_RECORDING_FIELD_NUMBER: _ClassVar[int]
    FILTER_PARAMS_FIELD_NUMBER: _ClassVar[int]
    filter: str
    input_src: str
    output_channel: str
    enable_recording: bool
    filter_params: _containers.ScalarMap[str, float]
    def __init__(self, filter: _Optional[str] = ..., input_src: _Optional[str] = ..., output_channel: _Optional[str] = ..., enable_recording: bool = ..., filter_params: _Optional[_Mapping[str, float]] = ...) -> None: ...

class Filters(_message.Message):
    __slots__ = ("filters",)
    class FiltersEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Filter
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Filter, _Mapping]] = ...) -> None: ...
    FILTERS_FIELD_NUMBER: _ClassVar[int]
    filters: _containers.MessageMap[str, Filter]
    def __init__(self, filters: _Optional[_Mapping[str, Filter]] = ...) -> None: ...

class ConnectionParams(_message.Message):
    __slots__ = ("address", "username", "password", "channel")
    ADDRESS_FIELD_NUMBER: _ClassVar[int]
    USERNAME_FIELD_NUMBER: _ClassVar[int]
    PASSWORD_FIELD_NUMBER: _ClassVar[int]
    CHANNEL_FIELD_NUMBER: _ClassVar[int]
    address: str
    username: str
    password: str
    channel: str
    def __init__(self, address: _Optional[str] = ..., username: _Optional[str] = ..., password: _Optional[str] = ..., channel: _Optional[str] = ...) -> None: ...

class StreamSource(_message.Message):
    __slots__ = ("source_id", "source_type", "source_name", "enable_recording", "connection_params")
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TYPE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    ENABLE_RECORDING_FIELD_NUMBER: _ClassVar[int]
    CONNECTION_PARAMS_FIELD_NUMBER: _ClassVar[int]
    source_id: str
    source_type: str
    source_name: str
    enable_recording: bool
    connection_params: ConnectionParams
    def __init__(self, source_id: _Optional[str] = ..., source_type: _Optional[str] = ..., source_name: _Optional[str] = ..., enable_recording: bool = ..., connection_params: _Optional[_Union[ConnectionParams, _Mapping]] = ...) -> None: ...

class StreamSources(_message.Message):
    __slots__ = ("stream_sources",)
    class StreamSourcesEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: StreamSource
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[StreamSource, _Mapping]] = ...) -> None: ...
    STREAM_SOURCES_FIELD_NUMBER: _ClassVar[int]
    stream_sources: _containers.MessageMap[str, StreamSource]
    def __init__(self, stream_sources: _Optional[_Mapping[str, StreamSource]] = ...) -> None: ...
