import os
from mcp.server.fastmcp import FastMCP
import pathlib
import json
from starlette.responses import PlainTextResponse

mcp = FastMCP("collections", host="0.0.0.0", port=5050)


@mcp.tool()
async def get_content_for_collection_topic(collection_name: str, topic_name: str) -> str:
    result = []
    base_dir = pathlib.Path().resolve().joinpath("content")
    for collection in [f for f in os.listdir(base_dir) if os.path.isdir(base_dir.joinpath(f)) and f != "data"]:
        if collection != collection_name:
            continue
        for filename in os.listdir(base_dir.joinpath(collection)):
            if filename != topic_name:
                continue
            with open(base_dir.joinpath(collection).joinpath(filename), "r") as file:
                result.append({
                    "collection": collection,
                    "filename": filename,
                    "content": file.read()
                })

    return json.dumps(result)

@mcp.tool()
async def list_collections(collection_name: str | None = None) -> str:
    result = []
    base_dir = pathlib.Path().resolve().joinpath("content")
    for collection in [f for f in os.listdir(base_dir) if os.path.isdir(base_dir.joinpath(f)) and f != "data"]:
        if collection_name and collection != collection_name:
            continue
        result.append(collection)
    return json.dumps(result)

@mcp.tool()
async def list_topics_in_a_collection(collection_name: str) -> str:
    result = []
    base_dir = pathlib.Path().resolve().joinpath("content")
    for collection in [f for f in os.listdir(base_dir) if os.path.isdir(base_dir.joinpath(f)) and f != "data"]:
        if collection != collection_name:
            continue
        for filename in os.listdir(base_dir.joinpath(collection)):
            result.append(filename)
    return json.dumps(result)

@mcp.tool()
async def list_data_manual() -> str:
    result = []
    base_dir = pathlib.Path().resolve().joinpath("content", "data-manual")
    for filename in os.listdir(base_dir):
        result.append(filename)
    return json.dumps(result)

@mcp.tool()
async def get_data_manual(filename: str) -> str:
    base_dir = pathlib.Path().resolve().joinpath("content", "data-manual")
    with open(base_dir.joinpath(filename), "r") as file:
        return file.read()

@mcp.tool()
async def get_data() -> str:
    result = []
    base_dir = pathlib.Path().resolve().joinpath("content", "data")
    for data_type in os.listdir(base_dir):
        for filename in os.listdir(base_dir.joinpath(data_type)):
            with open(base_dir.joinpath(data_type).joinpath(filename), "r") as file:
                result.append({
                    "data_type": data_type,
                    "filename": filename,
                    "content": file.read()
                })
    return json.dumps(result)


@mcp.custom_route("/", methods=["GET"])
async def health_check(request) -> PlainTextResponse:
    return PlainTextResponse("OK")
 

def main():
    # Initialize and run the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    mcp.run(transport="stdio")