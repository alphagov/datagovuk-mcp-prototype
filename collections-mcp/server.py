import os
from mcp.server.fastmcp import FastMCP
import pathlib
import json

mcp = FastMCP("collections")


@mcp.tool()
async def get_all_collections_topics() -> str:
    result = []
    base_dir = pathlib.Path().resolve().joinpath("content")
    for collection in os.listdir(base_dir):
        for filename in os.listdir(base_dir.joinpath(collection)):
            with open(base_dir.joinpath(collection).joinpath(filename), "r") as file:
                result.append({
                    "collection": collection,
                    "filename": filename,
                    "content": file.read()
                })

    return json.dumps(result)


@mcp.tool()
async def get_data()-> str:
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


def main():
    # Initialize and run the server
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()