pip install "betterproto[compiler]"  --trusted-host pypi.org
protoc --python_betterproto_out=. nakama.proto

