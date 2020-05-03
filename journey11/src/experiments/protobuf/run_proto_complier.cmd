REM conda activate notebook_gpu_netx
REM make sure conda\bin conda\scripts are on the system file path
REM
protoc --proto_path=. --python_out=. ./helloworld.proto
protoc --proto_path=. --python_out=. ./state.proto
protoc --proto_path=. --python_out=. ./task.proto
protoc --proto_path=. --python_out=. ./complex.proto