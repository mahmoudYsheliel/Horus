#!/bin/bash

protoc --proto_path=proto --python_out=protoc --pyi_out=protoc $1
