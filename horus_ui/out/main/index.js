"use strict";
const electron = require("electron");
const path = require("path");
const utils = require("@electron-toolkit/utils");
const pb_1 = require("google-protobuf");
const zmq = require("zeromq");
function _interopNamespaceDefault(e) {
  const n = Object.create(null, { [Symbol.toStringTag]: { value: "Module" } });
  if (e) {
    for (const k in e) {
      if (k !== "default") {
        const d = Object.getOwnPropertyDescriptor(e, k);
        Object.defineProperty(n, k, d.get ? d : {
          enumerable: true,
          get: () => e[k]
        });
      }
    }
  }
  n.default = e;
  return Object.freeze(n);
}
const pb_1__namespace = /* @__PURE__ */ _interopNamespaceDefault(pb_1);
const zmq__namespace = /* @__PURE__ */ _interopNamespaceDefault(zmq);
const icon = path.join(__dirname, "../../resources/icon.png");
var LogLevel = /* @__PURE__ */ ((LogLevel2) => {
  LogLevel2[LogLevel2["DEBUG"] = 0] = "DEBUG";
  LogLevel2[LogLevel2["INFO"] = 1] = "INFO";
  LogLevel2[LogLevel2["WARNING"] = 2] = "WARNING";
  LogLevel2[LogLevel2["ERROR"] = 3] = "ERROR";
  LogLevel2[LogLevel2["CRITICAL"] = 4] = "CRITICAL";
  return LogLevel2;
})(LogLevel || {});
var MonitorServiceRequest = /* @__PURE__ */ ((MonitorServiceRequest2) => {
  MonitorServiceRequest2[MonitorServiceRequest2["LOGS_HISTORY"] = 0] = "LOGS_HISTORY";
  MonitorServiceRequest2[MonitorServiceRequest2["SERVICES_STATUS"] = 1] = "SERVICES_STATUS";
  MonitorServiceRequest2[MonitorServiceRequest2["FILTER_CONFIG"] = 2] = "FILTER_CONFIG";
  MonitorServiceRequest2[MonitorServiceRequest2["SETTINGS_CONFIG"] = 3] = "SETTINGS_CONFIG";
  MonitorServiceRequest2[MonitorServiceRequest2["STREAM_SOURCES"] = 4] = "STREAM_SOURCES";
  MonitorServiceRequest2[MonitorServiceRequest2["AGENTS_CONFIG"] = 5] = "AGENTS_CONFIG";
  return MonitorServiceRequest2;
})(MonitorServiceRequest || {});
class LogMsg extends pb_1__namespace.Message {
  #one_of_decls = [];
  constructor(data) {
    super();
    pb_1__namespace.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [], this.#one_of_decls);
    if (!Array.isArray(data) && typeof data == "object") {
      if ("timestamp" in data && data.timestamp != void 0) {
        this.timestamp = data.timestamp;
      }
      if ("log_level" in data && data.log_level != void 0) {
        this.log_level = data.log_level;
      }
      if ("src" in data && data.src != void 0) {
        this.src = data.src;
      }
      if ("msg" in data && data.msg != void 0) {
        this.msg = data.msg;
      }
    }
  }
  get timestamp() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 1, 0);
  }
  set timestamp(value) {
    pb_1__namespace.Message.setField(this, 1, value);
  }
  get log_level() {
    return pb_1__namespace.Message.getFieldWithDefault(
      this,
      2,
      0
      /* DEBUG */
    );
  }
  set log_level(value) {
    pb_1__namespace.Message.setField(this, 2, value);
  }
  get src() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 3, "");
  }
  set src(value) {
    pb_1__namespace.Message.setField(this, 3, value);
  }
  get msg() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 4, "");
  }
  set msg(value) {
    pb_1__namespace.Message.setField(this, 4, value);
  }
  static fromObject(data) {
    const message = new LogMsg({});
    if (data.timestamp != null) {
      message.timestamp = data.timestamp;
    }
    if (data.log_level != null) {
      message.log_level = data.log_level;
    }
    if (data.src != null) {
      message.src = data.src;
    }
    if (data.msg != null) {
      message.msg = data.msg;
    }
    return message;
  }
  toObject() {
    const data = {};
    if (this.timestamp != null) {
      data.timestamp = this.timestamp;
    }
    if (this.log_level != null) {
      data.log_level = this.log_level;
    }
    if (this.src != null) {
      data.src = this.src;
    }
    if (this.msg != null) {
      data.msg = this.msg;
    }
    return data;
  }
  serialize(w) {
    const writer = w || new pb_1__namespace.BinaryWriter();
    if (this.timestamp != 0)
      writer.writeUint64(1, this.timestamp);
    if (this.log_level != 0)
      writer.writeEnum(2, this.log_level);
    if (this.src.length)
      writer.writeString(3, this.src);
    if (this.msg.length)
      writer.writeString(4, this.msg);
    if (!w)
      return writer.getResultBuffer();
  }
  static deserialize(bytes) {
    const reader = bytes instanceof pb_1__namespace.BinaryReader ? bytes : new pb_1__namespace.BinaryReader(bytes), message = new LogMsg();
    while (reader.nextField()) {
      if (reader.isEndGroup())
        break;
      switch (reader.getFieldNumber()) {
        case 1:
          message.timestamp = reader.readUint64();
          break;
        case 2:
          message.log_level = reader.readEnum();
          break;
        case 3:
          message.src = reader.readString();
          break;
        case 4:
          message.msg = reader.readString();
          break;
        default:
          reader.skipField();
      }
    }
    return message;
  }
  serializeBinary() {
    return this.serialize();
  }
  static deserializeBinary(bytes) {
    return LogMsg.deserialize(bytes);
  }
}
class LogMsgList extends pb_1__namespace.Message {
  #one_of_decls = [];
  constructor(data) {
    super();
    pb_1__namespace.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [1], this.#one_of_decls);
    if (!Array.isArray(data) && typeof data == "object") {
      if ("logs" in data && data.logs != void 0) {
        this.logs = data.logs;
      }
    }
  }
  get logs() {
    return pb_1__namespace.Message.getRepeatedWrapperField(this, LogMsg, 1);
  }
  set logs(value) {
    pb_1__namespace.Message.setRepeatedWrapperField(this, 1, value);
  }
  static fromObject(data) {
    const message = new LogMsgList({});
    if (data.logs != null) {
      message.logs = data.logs.map((item) => LogMsg.fromObject(item));
    }
    return message;
  }
  toObject() {
    const data = {};
    if (this.logs != null) {
      data.logs = this.logs.map((item) => item.toObject());
    }
    return data;
  }
  serialize(w) {
    const writer = w || new pb_1__namespace.BinaryWriter();
    if (this.logs.length)
      writer.writeRepeatedMessage(1, this.logs, (item) => item.serialize(writer));
    if (!w)
      return writer.getResultBuffer();
  }
  static deserialize(bytes) {
    const reader = bytes instanceof pb_1__namespace.BinaryReader ? bytes : new pb_1__namespace.BinaryReader(bytes), message = new LogMsgList();
    while (reader.nextField()) {
      if (reader.isEndGroup())
        break;
      switch (reader.getFieldNumber()) {
        case 1:
          reader.readMessage(message.logs, () => pb_1__namespace.Message.addToRepeatedWrapperField(message, 1, LogMsg.deserialize(reader), LogMsg));
          break;
        default:
          reader.skipField();
      }
    }
    return message;
  }
  serializeBinary() {
    return this.serialize();
  }
  static deserializeBinary(bytes) {
    return LogMsgList.deserialize(bytes);
  }
}
class ServicesStatusMap extends pb_1__namespace.Message {
  #one_of_decls = [];
  constructor(data) {
    super();
    pb_1__namespace.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [], this.#one_of_decls);
    if (!Array.isArray(data) && typeof data == "object") {
      if ("map" in data && data.map != void 0) {
        this.map = data.map;
      }
    }
    if (!this.map)
      this.map = /* @__PURE__ */ new Map();
  }
  get map() {
    return pb_1__namespace.Message.getField(this, 1);
  }
  set map(value) {
    pb_1__namespace.Message.setField(this, 1, value);
  }
  static fromObject(data) {
    const message = new ServicesStatusMap({});
    if (typeof data.map == "object") {
      message.map = new Map(Object.entries(data.map));
    }
    return message;
  }
  toObject() {
    const data = {};
    if (this.map != null) {
      data.map = Object.fromEntries(this.map);
    }
    return data;
  }
  serialize(w) {
    const writer = w || new pb_1__namespace.BinaryWriter();
    for (const [key, value] of this.map) {
      writer.writeMessage(1, this.map, () => {
        writer.writeString(1, key);
        writer.writeEnum(2, value);
      });
    }
    if (!w)
      return writer.getResultBuffer();
  }
  static deserialize(bytes) {
    const reader = bytes instanceof pb_1__namespace.BinaryReader ? bytes : new pb_1__namespace.BinaryReader(bytes), message = new ServicesStatusMap();
    while (reader.nextField()) {
      if (reader.isEndGroup())
        break;
      switch (reader.getFieldNumber()) {
        case 1:
          reader.readMessage(message, () => pb_1__namespace.Map.deserializeBinary(message.map, reader, reader.readString, reader.readEnum));
          break;
        default:
          reader.skipField();
      }
    }
    return message;
  }
  serializeBinary() {
    return this.serialize();
  }
  static deserializeBinary(bytes) {
    return ServicesStatusMap.deserialize(bytes);
  }
}
class SingleFilterChain extends pb_1__namespace.Message {
  #one_of_decls = [];
  constructor(data) {
    super();
    pb_1__namespace.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [], this.#one_of_decls);
    if (!Array.isArray(data) && typeof data == "object") {
      if ("name" in data && data.name != void 0) {
        this.name = data.name;
      }
      if ("params" in data && data.params != void 0) {
        this.params = data.params;
      }
    }
    if (!this.params)
      this.params = /* @__PURE__ */ new Map();
  }
  get name() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 1, "");
  }
  set name(value) {
    pb_1__namespace.Message.setField(this, 1, value);
  }
  get params() {
    return pb_1__namespace.Message.getField(this, 2);
  }
  set params(value) {
    pb_1__namespace.Message.setField(this, 2, value);
  }
  static fromObject(data) {
    const message = new SingleFilterChain({});
    if (data.name != null) {
      message.name = data.name;
    }
    if (typeof data.params == "object") {
      message.params = new Map(Object.entries(data.params));
    }
    return message;
  }
  toObject() {
    const data = {};
    if (this.name != null) {
      data.name = this.name;
    }
    if (this.params != null) {
      data.params = Object.fromEntries(this.params);
    }
    return data;
  }
  serialize(w) {
    const writer = w || new pb_1__namespace.BinaryWriter();
    if (this.name.length)
      writer.writeString(1, this.name);
    for (const [key, value] of this.params) {
      writer.writeMessage(2, this.params, () => {
        writer.writeString(1, key);
        writer.writeFloat(2, value);
      });
    }
    if (!w)
      return writer.getResultBuffer();
  }
  static deserialize(bytes) {
    const reader = bytes instanceof pb_1__namespace.BinaryReader ? bytes : new pb_1__namespace.BinaryReader(bytes), message = new SingleFilterChain();
    while (reader.nextField()) {
      if (reader.isEndGroup())
        break;
      switch (reader.getFieldNumber()) {
        case 1:
          message.name = reader.readString();
          break;
        case 2:
          reader.readMessage(message, () => pb_1__namespace.Map.deserializeBinary(message.params, reader, reader.readString, reader.readFloat));
          break;
        default:
          reader.skipField();
      }
    }
    return message;
  }
  serializeBinary() {
    return this.serialize();
  }
  static deserializeBinary(bytes) {
    return SingleFilterChain.deserialize(bytes);
  }
}
class Filter extends pb_1__namespace.Message {
  #one_of_decls = [];
  constructor(data) {
    super();
    pb_1__namespace.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [5], this.#one_of_decls);
    if (!Array.isArray(data) && typeof data == "object") {
      if ("camera_name" in data && data.camera_name != void 0) {
        this.camera_name = data.camera_name;
      }
      if ("input_src" in data && data.input_src != void 0) {
        this.input_src = data.input_src;
      }
      if ("output_src" in data && data.output_src != void 0) {
        this.output_src = data.output_src;
      }
      if ("enable_recording" in data && data.enable_recording != void 0) {
        this.enable_recording = data.enable_recording;
      }
      if ("filters_chain" in data && data.filters_chain != void 0) {
        this.filters_chain = data.filters_chain;
      }
    }
  }
  get camera_name() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 1, "");
  }
  set camera_name(value) {
    pb_1__namespace.Message.setField(this, 1, value);
  }
  get input_src() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 2, "");
  }
  set input_src(value) {
    pb_1__namespace.Message.setField(this, 2, value);
  }
  get output_src() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 3, "");
  }
  set output_src(value) {
    pb_1__namespace.Message.setField(this, 3, value);
  }
  get enable_recording() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 4, false);
  }
  set enable_recording(value) {
    pb_1__namespace.Message.setField(this, 4, value);
  }
  get filters_chain() {
    return pb_1__namespace.Message.getRepeatedWrapperField(this, SingleFilterChain, 5);
  }
  set filters_chain(value) {
    pb_1__namespace.Message.setRepeatedWrapperField(this, 5, value);
  }
  static fromObject(data) {
    const message = new Filter({});
    if (data.camera_name != null) {
      message.camera_name = data.camera_name;
    }
    if (data.input_src != null) {
      message.input_src = data.input_src;
    }
    if (data.output_src != null) {
      message.output_src = data.output_src;
    }
    if (data.enable_recording != null) {
      message.enable_recording = data.enable_recording;
    }
    if (data.filters_chain != null) {
      message.filters_chain = data.filters_chain.map((item) => SingleFilterChain.fromObject(item));
    }
    return message;
  }
  toObject() {
    const data = {};
    if (this.camera_name != null) {
      data.camera_name = this.camera_name;
    }
    if (this.input_src != null) {
      data.input_src = this.input_src;
    }
    if (this.output_src != null) {
      data.output_src = this.output_src;
    }
    if (this.enable_recording != null) {
      data.enable_recording = this.enable_recording;
    }
    if (this.filters_chain != null) {
      data.filters_chain = this.filters_chain.map((item) => item.toObject());
    }
    return data;
  }
  serialize(w) {
    const writer = w || new pb_1__namespace.BinaryWriter();
    if (this.camera_name.length)
      writer.writeString(1, this.camera_name);
    if (this.input_src.length)
      writer.writeString(2, this.input_src);
    if (this.output_src.length)
      writer.writeString(3, this.output_src);
    if (this.enable_recording != false)
      writer.writeBool(4, this.enable_recording);
    if (this.filters_chain.length)
      writer.writeRepeatedMessage(5, this.filters_chain, (item) => item.serialize(writer));
    if (!w)
      return writer.getResultBuffer();
  }
  static deserialize(bytes) {
    const reader = bytes instanceof pb_1__namespace.BinaryReader ? bytes : new pb_1__namespace.BinaryReader(bytes), message = new Filter();
    while (reader.nextField()) {
      if (reader.isEndGroup())
        break;
      switch (reader.getFieldNumber()) {
        case 1:
          message.camera_name = reader.readString();
          break;
        case 2:
          message.input_src = reader.readString();
          break;
        case 3:
          message.output_src = reader.readString();
          break;
        case 4:
          message.enable_recording = reader.readBool();
          break;
        case 5:
          reader.readMessage(message.filters_chain, () => pb_1__namespace.Message.addToRepeatedWrapperField(message, 5, SingleFilterChain.deserialize(reader), SingleFilterChain));
          break;
        default:
          reader.skipField();
      }
    }
    return message;
  }
  serializeBinary() {
    return this.serialize();
  }
  static deserializeBinary(bytes) {
    return Filter.deserialize(bytes);
  }
}
class Filters extends pb_1__namespace.Message {
  #one_of_decls = [];
  constructor(data) {
    super();
    pb_1__namespace.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [], this.#one_of_decls);
    if (!Array.isArray(data) && typeof data == "object") {
      if ("filters" in data && data.filters != void 0) {
        this.filters = data.filters;
      }
    }
    if (!this.filters)
      this.filters = /* @__PURE__ */ new Map();
  }
  get filters() {
    return pb_1__namespace.Message.getField(this, 1);
  }
  set filters(value) {
    pb_1__namespace.Message.setField(this, 1, value);
  }
  static fromObject(data) {
    const message = new Filters({});
    if (typeof data.filters == "object") {
      message.filters = new Map(Object.entries(data.filters).map(([key, value]) => [key, Filter.fromObject(value)]));
    }
    return message;
  }
  toObject() {
    const data = {};
    if (this.filters != null) {
      data.filters = Object.fromEntries(Array.from(this.filters).map(([key, value]) => [key, value.toObject()]));
    }
    return data;
  }
  serialize(w) {
    const writer = w || new pb_1__namespace.BinaryWriter();
    for (const [key, value] of this.filters) {
      writer.writeMessage(1, this.filters, () => {
        writer.writeString(1, key);
        writer.writeMessage(2, value, () => value.serialize(writer));
      });
    }
    if (!w)
      return writer.getResultBuffer();
  }
  static deserialize(bytes) {
    const reader = bytes instanceof pb_1__namespace.BinaryReader ? bytes : new pb_1__namespace.BinaryReader(bytes), message = new Filters();
    while (reader.nextField()) {
      if (reader.isEndGroup())
        break;
      switch (reader.getFieldNumber()) {
        case 1:
          reader.readMessage(message, () => pb_1__namespace.Map.deserializeBinary(message.filters, reader, reader.readString, () => {
            let value;
            reader.readMessage(message, () => value = Filter.deserialize(reader));
            return value;
          }));
          break;
        default:
          reader.skipField();
      }
    }
    return message;
  }
  serializeBinary() {
    return this.serialize();
  }
  static deserializeBinary(bytes) {
    return Filters.deserialize(bytes);
  }
}
class ConnectionParams extends pb_1__namespace.Message {
  #one_of_decls = [];
  constructor(data) {
    super();
    pb_1__namespace.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [], this.#one_of_decls);
    if (!Array.isArray(data) && typeof data == "object") {
      if ("address" in data && data.address != void 0) {
        this.address = data.address;
      }
      if ("username" in data && data.username != void 0) {
        this.username = data.username;
      }
      if ("password" in data && data.password != void 0) {
        this.password = data.password;
      }
      if ("channel" in data && data.channel != void 0) {
        this.channel = data.channel;
      }
    }
  }
  get address() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 1, "");
  }
  set address(value) {
    pb_1__namespace.Message.setField(this, 1, value);
  }
  get username() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 2, "");
  }
  set username(value) {
    pb_1__namespace.Message.setField(this, 2, value);
  }
  get password() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 3, "");
  }
  set password(value) {
    pb_1__namespace.Message.setField(this, 3, value);
  }
  get channel() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 4, "");
  }
  set channel(value) {
    pb_1__namespace.Message.setField(this, 4, value);
  }
  static fromObject(data) {
    const message = new ConnectionParams({});
    if (data.address != null) {
      message.address = data.address;
    }
    if (data.username != null) {
      message.username = data.username;
    }
    if (data.password != null) {
      message.password = data.password;
    }
    if (data.channel != null) {
      message.channel = data.channel;
    }
    return message;
  }
  toObject() {
    const data = {};
    if (this.address != null) {
      data.address = this.address;
    }
    if (this.username != null) {
      data.username = this.username;
    }
    if (this.password != null) {
      data.password = this.password;
    }
    if (this.channel != null) {
      data.channel = this.channel;
    }
    return data;
  }
  serialize(w) {
    const writer = w || new pb_1__namespace.BinaryWriter();
    if (this.address.length)
      writer.writeString(1, this.address);
    if (this.username.length)
      writer.writeString(2, this.username);
    if (this.password.length)
      writer.writeString(3, this.password);
    if (this.channel.length)
      writer.writeString(4, this.channel);
    if (!w)
      return writer.getResultBuffer();
  }
  static deserialize(bytes) {
    const reader = bytes instanceof pb_1__namespace.BinaryReader ? bytes : new pb_1__namespace.BinaryReader(bytes), message = new ConnectionParams();
    while (reader.nextField()) {
      if (reader.isEndGroup())
        break;
      switch (reader.getFieldNumber()) {
        case 1:
          message.address = reader.readString();
          break;
        case 2:
          message.username = reader.readString();
          break;
        case 3:
          message.password = reader.readString();
          break;
        case 4:
          message.channel = reader.readString();
          break;
        default:
          reader.skipField();
      }
    }
    return message;
  }
  serializeBinary() {
    return this.serialize();
  }
  static deserializeBinary(bytes) {
    return ConnectionParams.deserialize(bytes);
  }
}
class StreamSource extends pb_1__namespace.Message {
  #one_of_decls = [];
  constructor(data) {
    super();
    pb_1__namespace.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [], this.#one_of_decls);
    if (!Array.isArray(data) && typeof data == "object") {
      if ("source_id" in data && data.source_id != void 0) {
        this.source_id = data.source_id;
      }
      if ("source_type" in data && data.source_type != void 0) {
        this.source_type = data.source_type;
      }
      if ("source_name" in data && data.source_name != void 0) {
        this.source_name = data.source_name;
      }
      if ("enable_recording" in data && data.enable_recording != void 0) {
        this.enable_recording = data.enable_recording;
      }
      if ("connection_params" in data && data.connection_params != void 0) {
        this.connection_params = data.connection_params;
      }
    }
  }
  get source_id() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 1, "");
  }
  set source_id(value) {
    pb_1__namespace.Message.setField(this, 1, value);
  }
  get source_type() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 2, "");
  }
  set source_type(value) {
    pb_1__namespace.Message.setField(this, 2, value);
  }
  get source_name() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 3, "");
  }
  set source_name(value) {
    pb_1__namespace.Message.setField(this, 3, value);
  }
  get enable_recording() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 4, false);
  }
  set enable_recording(value) {
    pb_1__namespace.Message.setField(this, 4, value);
  }
  get connection_params() {
    return pb_1__namespace.Message.getWrapperField(this, ConnectionParams, 5);
  }
  set connection_params(value) {
    pb_1__namespace.Message.setWrapperField(this, 5, value);
  }
  get has_connection_params() {
    return pb_1__namespace.Message.getField(this, 5) != null;
  }
  static fromObject(data) {
    const message = new StreamSource({});
    if (data.source_id != null) {
      message.source_id = data.source_id;
    }
    if (data.source_type != null) {
      message.source_type = data.source_type;
    }
    if (data.source_name != null) {
      message.source_name = data.source_name;
    }
    if (data.enable_recording != null) {
      message.enable_recording = data.enable_recording;
    }
    if (data.connection_params != null) {
      message.connection_params = ConnectionParams.fromObject(data.connection_params);
    }
    return message;
  }
  toObject() {
    const data = {};
    if (this.source_id != null) {
      data.source_id = this.source_id;
    }
    if (this.source_type != null) {
      data.source_type = this.source_type;
    }
    if (this.source_name != null) {
      data.source_name = this.source_name;
    }
    if (this.enable_recording != null) {
      data.enable_recording = this.enable_recording;
    }
    if (this.connection_params != null) {
      data.connection_params = this.connection_params.toObject();
    }
    return data;
  }
  serialize(w) {
    const writer = w || new pb_1__namespace.BinaryWriter();
    if (this.source_id.length)
      writer.writeString(1, this.source_id);
    if (this.source_type.length)
      writer.writeString(2, this.source_type);
    if (this.source_name.length)
      writer.writeString(3, this.source_name);
    if (this.enable_recording != false)
      writer.writeBool(4, this.enable_recording);
    if (this.has_connection_params)
      writer.writeMessage(5, this.connection_params, () => this.connection_params.serialize(writer));
    if (!w)
      return writer.getResultBuffer();
  }
  static deserialize(bytes) {
    const reader = bytes instanceof pb_1__namespace.BinaryReader ? bytes : new pb_1__namespace.BinaryReader(bytes), message = new StreamSource();
    while (reader.nextField()) {
      if (reader.isEndGroup())
        break;
      switch (reader.getFieldNumber()) {
        case 1:
          message.source_id = reader.readString();
          break;
        case 2:
          message.source_type = reader.readString();
          break;
        case 3:
          message.source_name = reader.readString();
          break;
        case 4:
          message.enable_recording = reader.readBool();
          break;
        case 5:
          reader.readMessage(message.connection_params, () => message.connection_params = ConnectionParams.deserialize(reader));
          break;
        default:
          reader.skipField();
      }
    }
    return message;
  }
  serializeBinary() {
    return this.serialize();
  }
  static deserializeBinary(bytes) {
    return StreamSource.deserialize(bytes);
  }
}
class StreamSources extends pb_1__namespace.Message {
  #one_of_decls = [];
  constructor(data) {
    super();
    pb_1__namespace.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [], this.#one_of_decls);
    if (!Array.isArray(data) && typeof data == "object") {
      if ("stream_sources" in data && data.stream_sources != void 0) {
        this.stream_sources = data.stream_sources;
      }
    }
    if (!this.stream_sources)
      this.stream_sources = /* @__PURE__ */ new Map();
  }
  get stream_sources() {
    return pb_1__namespace.Message.getField(this, 1);
  }
  set stream_sources(value) {
    pb_1__namespace.Message.setField(this, 1, value);
  }
  static fromObject(data) {
    const message = new StreamSources({});
    if (typeof data.stream_sources == "object") {
      message.stream_sources = new Map(Object.entries(data.stream_sources).map(([key, value]) => [key, StreamSource.fromObject(value)]));
    }
    return message;
  }
  toObject() {
    const data = {};
    if (this.stream_sources != null) {
      data.stream_sources = Object.fromEntries(Array.from(this.stream_sources).map(([key, value]) => [key, value.toObject()]));
    }
    return data;
  }
  serialize(w) {
    const writer = w || new pb_1__namespace.BinaryWriter();
    for (const [key, value] of this.stream_sources) {
      writer.writeMessage(1, this.stream_sources, () => {
        writer.writeString(1, key);
        writer.writeMessage(2, value, () => value.serialize(writer));
      });
    }
    if (!w)
      return writer.getResultBuffer();
  }
  static deserialize(bytes) {
    const reader = bytes instanceof pb_1__namespace.BinaryReader ? bytes : new pb_1__namespace.BinaryReader(bytes), message = new StreamSources();
    while (reader.nextField()) {
      if (reader.isEndGroup())
        break;
      switch (reader.getFieldNumber()) {
        case 1:
          reader.readMessage(message, () => pb_1__namespace.Map.deserializeBinary(message.stream_sources, reader, reader.readString, () => {
            let value;
            reader.readMessage(message, () => value = StreamSource.deserialize(reader));
            return value;
          }));
          break;
        default:
          reader.skipField();
      }
    }
    return message;
  }
  serializeBinary() {
    return this.serialize();
  }
  static deserializeBinary(bytes) {
    return StreamSources.deserialize(bytes);
  }
}
class BoundingBox extends pb_1__namespace.Message {
  #one_of_decls = [];
  constructor(data) {
    super();
    pb_1__namespace.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [], this.#one_of_decls);
    if (!Array.isArray(data) && typeof data == "object") {
      if ("x" in data && data.x != void 0) {
        this.x = data.x;
      }
      if ("y" in data && data.y != void 0) {
        this.y = data.y;
      }
      if ("w" in data && data.w != void 0) {
        this.w = data.w;
      }
      if ("h" in data && data.h != void 0) {
        this.h = data.h;
      }
    }
  }
  get x() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 1, 0);
  }
  set x(value) {
    pb_1__namespace.Message.setField(this, 1, value);
  }
  get y() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 2, 0);
  }
  set y(value) {
    pb_1__namespace.Message.setField(this, 2, value);
  }
  get w() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 3, 0);
  }
  set w(value) {
    pb_1__namespace.Message.setField(this, 3, value);
  }
  get h() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 4, 0);
  }
  set h(value) {
    pb_1__namespace.Message.setField(this, 4, value);
  }
  static fromObject(data) {
    const message = new BoundingBox({});
    if (data.x != null) {
      message.x = data.x;
    }
    if (data.y != null) {
      message.y = data.y;
    }
    if (data.w != null) {
      message.w = data.w;
    }
    if (data.h != null) {
      message.h = data.h;
    }
    return message;
  }
  toObject() {
    const data = {};
    if (this.x != null) {
      data.x = this.x;
    }
    if (this.y != null) {
      data.y = this.y;
    }
    if (this.w != null) {
      data.w = this.w;
    }
    if (this.h != null) {
      data.h = this.h;
    }
    return data;
  }
  serialize(w) {
    const writer = w || new pb_1__namespace.BinaryWriter();
    if (this.x != 0)
      writer.writeInt32(1, this.x);
    if (this.y != 0)
      writer.writeInt32(2, this.y);
    if (this.w != 0)
      writer.writeInt32(3, this.w);
    if (this.h != 0)
      writer.writeInt32(4, this.h);
    if (!w)
      return writer.getResultBuffer();
  }
  static deserialize(bytes) {
    const reader = bytes instanceof pb_1__namespace.BinaryReader ? bytes : new pb_1__namespace.BinaryReader(bytes), message = new BoundingBox();
    while (reader.nextField()) {
      if (reader.isEndGroup())
        break;
      switch (reader.getFieldNumber()) {
        case 1:
          message.x = reader.readInt32();
          break;
        case 2:
          message.y = reader.readInt32();
          break;
        case 3:
          message.w = reader.readInt32();
          break;
        case 4:
          message.h = reader.readInt32();
          break;
        default:
          reader.skipField();
      }
    }
    return message;
  }
  serializeBinary() {
    return this.serialize();
  }
  static deserializeBinary(bytes) {
    return BoundingBox.deserialize(bytes);
  }
}
class DetectionData extends pb_1__namespace.Message {
  #one_of_decls = [];
  constructor(data) {
    super();
    pb_1__namespace.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [], this.#one_of_decls);
    if (!Array.isArray(data) && typeof data == "object") {
      if ("class_name" in data && data.class_name != void 0) {
        this.class_name = data.class_name;
      }
      if ("bounding_box" in data && data.bounding_box != void 0) {
        this.bounding_box = data.bounding_box;
      }
      if ("confidence" in data && data.confidence != void 0) {
        this.confidence = data.confidence;
      }
    }
  }
  get class_name() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 1, "");
  }
  set class_name(value) {
    pb_1__namespace.Message.setField(this, 1, value);
  }
  get bounding_box() {
    return pb_1__namespace.Message.getWrapperField(this, BoundingBox, 2);
  }
  set bounding_box(value) {
    pb_1__namespace.Message.setWrapperField(this, 2, value);
  }
  get has_bounding_box() {
    return pb_1__namespace.Message.getField(this, 2) != null;
  }
  get confidence() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 3, 0);
  }
  set confidence(value) {
    pb_1__namespace.Message.setField(this, 3, value);
  }
  static fromObject(data) {
    const message = new DetectionData({});
    if (data.class_name != null) {
      message.class_name = data.class_name;
    }
    if (data.bounding_box != null) {
      message.bounding_box = BoundingBox.fromObject(data.bounding_box);
    }
    if (data.confidence != null) {
      message.confidence = data.confidence;
    }
    return message;
  }
  toObject() {
    const data = {};
    if (this.class_name != null) {
      data.class_name = this.class_name;
    }
    if (this.bounding_box != null) {
      data.bounding_box = this.bounding_box.toObject();
    }
    if (this.confidence != null) {
      data.confidence = this.confidence;
    }
    return data;
  }
  serialize(w) {
    const writer = w || new pb_1__namespace.BinaryWriter();
    if (this.class_name.length)
      writer.writeString(1, this.class_name);
    if (this.has_bounding_box)
      writer.writeMessage(2, this.bounding_box, () => this.bounding_box.serialize(writer));
    if (this.confidence != 0)
      writer.writeDouble(3, this.confidence);
    if (!w)
      return writer.getResultBuffer();
  }
  static deserialize(bytes) {
    const reader = bytes instanceof pb_1__namespace.BinaryReader ? bytes : new pb_1__namespace.BinaryReader(bytes), message = new DetectionData();
    while (reader.nextField()) {
      if (reader.isEndGroup())
        break;
      switch (reader.getFieldNumber()) {
        case 1:
          message.class_name = reader.readString();
          break;
        case 2:
          reader.readMessage(message.bounding_box, () => message.bounding_box = BoundingBox.deserialize(reader));
          break;
        case 3:
          message.confidence = reader.readDouble();
          break;
        default:
          reader.skipField();
      }
    }
    return message;
  }
  serializeBinary() {
    return this.serialize();
  }
  static deserializeBinary(bytes) {
    return DetectionData.deserialize(bytes);
  }
}
class AIDetectionAgent extends pb_1__namespace.Message {
  #one_of_decls = [];
  constructor(data) {
    super();
    pb_1__namespace.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [4], this.#one_of_decls);
    if (!Array.isArray(data) && typeof data == "object") {
      if ("model_name" in data && data.model_name != void 0) {
        this.model_name = data.model_name;
      }
      if ("timestamp" in data && data.timestamp != void 0) {
        this.timestamp = data.timestamp;
      }
      if ("source_name" in data && data.source_name != void 0) {
        this.source_name = data.source_name;
      }
      if ("details" in data && data.details != void 0) {
        this.details = data.details;
      }
    }
  }
  get model_name() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 1, "");
  }
  set model_name(value) {
    pb_1__namespace.Message.setField(this, 1, value);
  }
  get timestamp() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 2, 0);
  }
  set timestamp(value) {
    pb_1__namespace.Message.setField(this, 2, value);
  }
  get source_name() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 3, "");
  }
  set source_name(value) {
    pb_1__namespace.Message.setField(this, 3, value);
  }
  get details() {
    return pb_1__namespace.Message.getRepeatedWrapperField(this, DetectionData, 4);
  }
  set details(value) {
    pb_1__namespace.Message.setRepeatedWrapperField(this, 4, value);
  }
  static fromObject(data) {
    const message = new AIDetectionAgent({});
    if (data.model_name != null) {
      message.model_name = data.model_name;
    }
    if (data.timestamp != null) {
      message.timestamp = data.timestamp;
    }
    if (data.source_name != null) {
      message.source_name = data.source_name;
    }
    if (data.details != null) {
      message.details = data.details.map((item) => DetectionData.fromObject(item));
    }
    return message;
  }
  toObject() {
    const data = {};
    if (this.model_name != null) {
      data.model_name = this.model_name;
    }
    if (this.timestamp != null) {
      data.timestamp = this.timestamp;
    }
    if (this.source_name != null) {
      data.source_name = this.source_name;
    }
    if (this.details != null) {
      data.details = this.details.map((item) => item.toObject());
    }
    return data;
  }
  serialize(w) {
    const writer = w || new pb_1__namespace.BinaryWriter();
    if (this.model_name.length)
      writer.writeString(1, this.model_name);
    if (this.timestamp != 0)
      writer.writeUint64(2, this.timestamp);
    if (this.source_name.length)
      writer.writeString(3, this.source_name);
    if (this.details.length)
      writer.writeRepeatedMessage(4, this.details, (item) => item.serialize(writer));
    if (!w)
      return writer.getResultBuffer();
  }
  static deserialize(bytes) {
    const reader = bytes instanceof pb_1__namespace.BinaryReader ? bytes : new pb_1__namespace.BinaryReader(bytes), message = new AIDetectionAgent();
    while (reader.nextField()) {
      if (reader.isEndGroup())
        break;
      switch (reader.getFieldNumber()) {
        case 1:
          message.model_name = reader.readString();
          break;
        case 2:
          message.timestamp = reader.readUint64();
          break;
        case 3:
          message.source_name = reader.readString();
          break;
        case 4:
          reader.readMessage(message.details, () => pb_1__namespace.Message.addToRepeatedWrapperField(message, 4, DetectionData.deserialize(reader), DetectionData));
          break;
        default:
          reader.skipField();
      }
    }
    return message;
  }
  serializeBinary() {
    return this.serialize();
  }
  static deserializeBinary(bytes) {
    return AIDetectionAgent.deserialize(bytes);
  }
}
class Agent extends pb_1__namespace.Message {
  #one_of_decls = [];
  constructor(data) {
    super();
    pb_1__namespace.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [], this.#one_of_decls);
    if (!Array.isArray(data) && typeof data == "object") {
      if ("path" in data && data.path != void 0) {
        this.path = data.path;
      }
      if ("agent" in data && data.agent != void 0) {
        this.agent = data.agent;
      }
      if ("input_src" in data && data.input_src != void 0) {
        this.input_src = data.input_src;
      }
      if ("agent_params" in data && data.agent_params != void 0) {
        this.agent_params = data.agent_params;
      }
    }
    if (!this.agent_params)
      this.agent_params = /* @__PURE__ */ new Map();
  }
  get path() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 1, "");
  }
  set path(value) {
    pb_1__namespace.Message.setField(this, 1, value);
  }
  get agent() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 2, "");
  }
  set agent(value) {
    pb_1__namespace.Message.setField(this, 2, value);
  }
  get input_src() {
    return pb_1__namespace.Message.getFieldWithDefault(this, 3, "");
  }
  set input_src(value) {
    pb_1__namespace.Message.setField(this, 3, value);
  }
  get agent_params() {
    return pb_1__namespace.Message.getField(this, 4);
  }
  set agent_params(value) {
    pb_1__namespace.Message.setField(this, 4, value);
  }
  static fromObject(data) {
    const message = new Agent({});
    if (data.path != null) {
      message.path = data.path;
    }
    if (data.agent != null) {
      message.agent = data.agent;
    }
    if (data.input_src != null) {
      message.input_src = data.input_src;
    }
    if (typeof data.agent_params == "object") {
      message.agent_params = new Map(Object.entries(data.agent_params));
    }
    return message;
  }
  toObject() {
    const data = {};
    if (this.path != null) {
      data.path = this.path;
    }
    if (this.agent != null) {
      data.agent = this.agent;
    }
    if (this.input_src != null) {
      data.input_src = this.input_src;
    }
    if (this.agent_params != null) {
      data.agent_params = Object.fromEntries(this.agent_params);
    }
    return data;
  }
  serialize(w) {
    const writer = w || new pb_1__namespace.BinaryWriter();
    if (this.path.length)
      writer.writeString(1, this.path);
    if (this.agent.length)
      writer.writeString(2, this.agent);
    if (this.input_src.length)
      writer.writeString(3, this.input_src);
    for (const [key, value] of this.agent_params) {
      writer.writeMessage(4, this.agent_params, () => {
        writer.writeString(1, key);
        writer.writeString(2, value);
      });
    }
    if (!w)
      return writer.getResultBuffer();
  }
  static deserialize(bytes) {
    const reader = bytes instanceof pb_1__namespace.BinaryReader ? bytes : new pb_1__namespace.BinaryReader(bytes), message = new Agent();
    while (reader.nextField()) {
      if (reader.isEndGroup())
        break;
      switch (reader.getFieldNumber()) {
        case 1:
          message.path = reader.readString();
          break;
        case 2:
          message.agent = reader.readString();
          break;
        case 3:
          message.input_src = reader.readString();
          break;
        case 4:
          reader.readMessage(message, () => pb_1__namespace.Map.deserializeBinary(message.agent_params, reader, reader.readString, reader.readString));
          break;
        default:
          reader.skipField();
      }
    }
    return message;
  }
  serializeBinary() {
    return this.serialize();
  }
  static deserializeBinary(bytes) {
    return Agent.deserialize(bytes);
  }
}
class Agents extends pb_1__namespace.Message {
  #one_of_decls = [];
  constructor(data) {
    super();
    pb_1__namespace.Message.initialize(this, Array.isArray(data) ? data : [], 0, -1, [], this.#one_of_decls);
    if (!Array.isArray(data) && typeof data == "object") {
      if ("agents" in data && data.agents != void 0) {
        this.agents = data.agents;
      }
    }
    if (!this.agents)
      this.agents = /* @__PURE__ */ new Map();
  }
  get agents() {
    return pb_1__namespace.Message.getField(this, 1);
  }
  set agents(value) {
    pb_1__namespace.Message.setField(this, 1, value);
  }
  static fromObject(data) {
    const message = new Agents({});
    if (typeof data.agents == "object") {
      message.agents = new Map(Object.entries(data.agents).map(([key, value]) => [key, Agent.fromObject(value)]));
    }
    return message;
  }
  toObject() {
    const data = {};
    if (this.agents != null) {
      data.agents = Object.fromEntries(Array.from(this.agents).map(([key, value]) => [key, value.toObject()]));
    }
    return data;
  }
  serialize(w) {
    const writer = w || new pb_1__namespace.BinaryWriter();
    for (const [key, value] of this.agents) {
      writer.writeMessage(1, this.agents, () => {
        writer.writeString(1, key);
        writer.writeMessage(2, value, () => value.serialize(writer));
      });
    }
    if (!w)
      return writer.getResultBuffer();
  }
  static deserialize(bytes) {
    const reader = bytes instanceof pb_1__namespace.BinaryReader ? bytes : new pb_1__namespace.BinaryReader(bytes), message = new Agents();
    while (reader.nextField()) {
      if (reader.isEndGroup())
        break;
      switch (reader.getFieldNumber()) {
        case 1:
          reader.readMessage(message, () => pb_1__namespace.Map.deserializeBinary(message.agents, reader, reader.readString, () => {
            let value;
            reader.readMessage(message, () => value = Agent.deserialize(reader));
            return value;
          }));
          break;
        default:
          reader.skipField();
      }
    }
    return message;
  }
  serializeBinary() {
    return this.serialize();
  }
  static deserializeBinary(bytes) {
    return Agents.deserialize(bytes);
  }
}
const monitor_push = new zmq__namespace.Push();
monitor_push.connect("tcp://127.0.0.1:6000");
const monitor_req = new zmq__namespace.Request();
monitor_req.connect("tcp://127.0.0.1:6001");
const monitor_ai_sub = new zmq__namespace.Subscriber();
monitor_ai_sub.connect("tcp://127.0.0.1:7001");
monitor_ai_sub.subscribe("");
const log = new LogMsg();
log.timestamp = 1672215379;
log.log_level = LogLevel.INFO;
log.src = "zmq_cli";
log.msg = "ZMQ CLI Test Log Msg";
async function ai_agent_subscriber(mainWindow) {
  for await (const [channel, msg] of monitor_ai_sub) {
    const SSM = AIDetectionAgent.deserializeBinary(msg);
    const data = { channel: channel.toString(), data: SSM.toObject() };
    mainWindow.webContents.send("ai_agent", data);
  }
}
async function send_log() {
  await monitor_push.send(log.serializeBinary());
  return true;
}
async function get_logs() {
  await monitor_req.send(new Uint8Array([MonitorServiceRequest.LOGS_HISTORY]));
  const packet = await monitor_req.receive();
  const SSM = LogMsgList.deserializeBinary(packet[0]);
  return SSM.toObject();
}
async function get_status() {
  await monitor_req.send(new Uint8Array([MonitorServiceRequest.SERVICES_STATUS]));
  const packet = await monitor_req.receive();
  const SSM = ServicesStatusMap.deserializeBinary(packet[0]);
  return SSM.map;
}
async function get_filters() {
  await monitor_req.send(new Uint8Array([MonitorServiceRequest.FILTER_CONFIG]));
  const packet = await monitor_req.receive();
  const SSM = Filters.deserializeBinary(packet[0]);
  return SSM.toObject();
}
async function get_agents() {
  await monitor_req.send(new Uint8Array([MonitorServiceRequest.AGENTS_CONFIG]));
  const packet = await monitor_req.receive();
  const SSM = Agents.deserializeBinary(packet[0]);
  return SSM.toObject();
}
async function get_stream_sources() {
  await monitor_req.send(new Uint8Array([MonitorServiceRequest.STREAM_SOURCES]));
  const packet = await monitor_req.receive();
  const SSM = StreamSources.deserializeBinary(packet[0]);
  return SSM.toObject();
}
function init_test_zmq(mainWindow) {
  electron.ipcMain.handle("get_monitor_status", async () => {
    const value = await get_status();
    return value;
  });
  electron.ipcMain.handle("get_monitor_logs", async () => {
    const value = await get_logs();
    return value;
  });
  electron.ipcMain.handle("send_log", async () => {
    const value = await send_log();
    return value;
  });
  electron.ipcMain.handle("get_filters", async () => {
    const value = await get_filters();
    return value;
  });
  electron.ipcMain.handle("get_stream_sources", async () => {
    const value = await get_stream_sources();
    return value;
  });
  electron.ipcMain.handle("get_agents", async () => {
    const value = await get_agents();
    return value;
  });
  ai_agent_subscriber(mainWindow);
}
const BASE_HRES = 1280;
const BASE_VRES = 720;
function createWindow() {
  const mainWindow = new electron.BrowserWindow({
    width: process.platform !== "win32" ? BASE_HRES : BASE_HRES + 16,
    height: process.platform !== "win32" ? BASE_VRES : BASE_VRES + 32,
    show: false,
    resizable: true,
    frame: false,
    autoHideMenuBar: true,
    // fullscreen: true,
    ...process.platform === "linux" ? { icon } : {},
    webPreferences: {
      preload: path.join(__dirname, "../preload/index.js"),
      sandbox: false,
      contextIsolation: true,
      nodeIntegration: false,
      webSecurity: false
    }
  });
  mainWindow.on("ready-to-show", () => {
    mainWindow.show();
  });
  mainWindow.webContents.setWindowOpenHandler((details) => {
    electron.shell.openExternal(details.url);
    return { action: "deny" };
  });
  if (utils.is.dev && process.env["ELECTRON_RENDERER_URL"]) {
    mainWindow.loadURL(process.env["ELECTRON_RENDERER_URL"]);
  } else {
    mainWindow.loadFile(path.join(__dirname, "../renderer/index.html"));
  }
  init_test_zmq(mainWindow);
}
electron.app.whenReady().then(() => {
  utils.electronApp.setAppUserModelId("labtronic-control-hub-v2.aAbstract");
  electron.app.on("browser-window-created", (_, window) => {
    utils.optimizer.watchWindowShortcuts(window);
  });
  createWindow();
  electron.app.on("activate", function() {
    if (electron.BrowserWindow.getAllWindows().length === 0) createWindow();
  });
  electron.app.commandLine.appendSwitch("disable-site-isolation-trials");
});
electron.app.on("window-all-closed", () => {
  if (process.platform !== "darwin") {
    electron.app.quit();
  }
});
