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
    AGENTS_CONFIG: _ClassVar[MonitorServiceRequest]
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
AGENTS_CONFIG: MonitorServiceRequest

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

class SingleFilterChain(_message.Message):
    __slots__ = ("name", "params")
    class ParamsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: float
        def __init__(self, key: _Optional[str] = ..., value: _Optional[float] = ...) -> None: ...
    NAME_FIELD_NUMBER: _ClassVar[int]
    PARAMS_FIELD_NUMBER: _ClassVar[int]
    name: str
    params: _containers.ScalarMap[str, float]
    def __init__(self, name: _Optional[str] = ..., params: _Optional[_Mapping[str, float]] = ...) -> None: ...

class Filter(_message.Message):
    __slots__ = ("camera_name", "input_src", "output_src", "enable_recording", "filters_chain")
    CAMERA_NAME_FIELD_NUMBER: _ClassVar[int]
    INPUT_SRC_FIELD_NUMBER: _ClassVar[int]
    OUTPUT_SRC_FIELD_NUMBER: _ClassVar[int]
    ENABLE_RECORDING_FIELD_NUMBER: _ClassVar[int]
    FILTERS_CHAIN_FIELD_NUMBER: _ClassVar[int]
    camera_name: str
    input_src: str
    output_src: str
    enable_recording: bool
    filters_chain: _containers.RepeatedCompositeFieldContainer[SingleFilterChain]
    def __init__(self, camera_name: _Optional[str] = ..., input_src: _Optional[str] = ..., output_src: _Optional[str] = ..., enable_recording: bool = ..., filters_chain: _Optional[_Iterable[_Union[SingleFilterChain, _Mapping]]] = ...) -> None: ...

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

class BoundingBox(_message.Message):
    __slots__ = ("x", "y", "w", "h")
    X_FIELD_NUMBER: _ClassVar[int]
    Y_FIELD_NUMBER: _ClassVar[int]
    W_FIELD_NUMBER: _ClassVar[int]
    H_FIELD_NUMBER: _ClassVar[int]
    x: int
    y: int
    w: int
    h: int
    def __init__(self, x: _Optional[int] = ..., y: _Optional[int] = ..., w: _Optional[int] = ..., h: _Optional[int] = ...) -> None: ...

class DetectionData(_message.Message):
    __slots__ = ("class_name", "bounding_box", "confidence")
    CLASS_NAME_FIELD_NUMBER: _ClassVar[int]
    BOUNDING_BOX_FIELD_NUMBER: _ClassVar[int]
    CONFIDENCE_FIELD_NUMBER: _ClassVar[int]
    class_name: str
    bounding_box: BoundingBox
    confidence: float
    def __init__(self, class_name: _Optional[str] = ..., bounding_box: _Optional[_Union[BoundingBox, _Mapping]] = ..., confidence: _Optional[float] = ...) -> None: ...

class AIDetectionAgent(_message.Message):
    __slots__ = ("model_name", "timestamp", "source_name", "details")
    MODEL_NAME_FIELD_NUMBER: _ClassVar[int]
    TIMESTAMP_FIELD_NUMBER: _ClassVar[int]
    SOURCE_NAME_FIELD_NUMBER: _ClassVar[int]
    DETAILS_FIELD_NUMBER: _ClassVar[int]
    model_name: str
    timestamp: int
    source_name: str
    details: _containers.RepeatedCompositeFieldContainer[DetectionData]
    def __init__(self, model_name: _Optional[str] = ..., timestamp: _Optional[int] = ..., source_name: _Optional[str] = ..., details: _Optional[_Iterable[_Union[DetectionData, _Mapping]]] = ...) -> None: ...

class Agent(_message.Message):
    __slots__ = ("path", "agent", "input_src", "agent_params")
    class AgentParamsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: str
        def __init__(self, key: _Optional[str] = ..., value: _Optional[str] = ...) -> None: ...
    PATH_FIELD_NUMBER: _ClassVar[int]
    AGENT_FIELD_NUMBER: _ClassVar[int]
    INPUT_SRC_FIELD_NUMBER: _ClassVar[int]
    AGENT_PARAMS_FIELD_NUMBER: _ClassVar[int]
    path: str
    agent: str
    input_src: str
    agent_params: _containers.ScalarMap[str, str]
    def __init__(self, path: _Optional[str] = ..., agent: _Optional[str] = ..., input_src: _Optional[str] = ..., agent_params: _Optional[_Mapping[str, str]] = ...) -> None: ...

class Agents(_message.Message):
    __slots__ = ("agents",)
    class AgentsEntry(_message.Message):
        __slots__ = ("key", "value")
        KEY_FIELD_NUMBER: _ClassVar[int]
        VALUE_FIELD_NUMBER: _ClassVar[int]
        key: str
        value: Agent
        def __init__(self, key: _Optional[str] = ..., value: _Optional[_Union[Agent, _Mapping]] = ...) -> None: ...
    AGENTS_FIELD_NUMBER: _ClassVar[int]
    agents: _containers.MessageMap[str, Agent]
    def __init__(self, agents: _Optional[_Mapping[str, Agent]] = ...) -> None: ...

class TrackObject(_message.Message):
    __slots__ = ("image_width", "image_height", "image_data", "object_x", "object_y", "object_w", "object_h", "track_name", "stream_src")
    IMAGE_WIDTH_FIELD_NUMBER: _ClassVar[int]
    IMAGE_HEIGHT_FIELD_NUMBER: _ClassVar[int]
    IMAGE_DATA_FIELD_NUMBER: _ClassVar[int]
    OBJECT_X_FIELD_NUMBER: _ClassVar[int]
    OBJECT_Y_FIELD_NUMBER: _ClassVar[int]
    OBJECT_W_FIELD_NUMBER: _ClassVar[int]
    OBJECT_H_FIELD_NUMBER: _ClassVar[int]
    TRACK_NAME_FIELD_NUMBER: _ClassVar[int]
    STREAM_SRC_FIELD_NUMBER: _ClassVar[int]
    image_width: int
    image_height: int
    image_data: _containers.RepeatedScalarFieldContainer[int]
    object_x: int
    object_y: int
    object_w: int
    object_h: int
    track_name: str
    stream_src: str
    def __init__(self, image_width: _Optional[int] = ..., image_height: _Optional[int] = ..., image_data: _Optional[_Iterable[int]] = ..., object_x: _Optional[int] = ..., object_y: _Optional[int] = ..., object_w: _Optional[int] = ..., object_h: _Optional[int] = ..., track_name: _Optional[str] = ..., stream_src: _Optional[str] = ...) -> None: ...
