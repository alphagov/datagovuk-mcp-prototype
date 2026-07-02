import os
from mcp.server.fastmcp import FastMCP
import pathlib
import json
from starlette.responses import PlainTextResponse

mcp = FastMCP("datagovuk-mcp", host="0.0.0.0", port=5050)


@mcp.tool()
async def get_content_for_collection_topic(collection_name: str, topic_name: str) -> str:
    result = []
    base_dir = pathlib.Path().resolve().joinpath("content").joinpath("collections")
    for collection in [f for f in os.listdir(base_dir) if os.path.isdir(base_dir.joinpath(f)) and f != "data"]:
        if collection != collection_name:
            continue
        for filename in os.listdir(base_dir.joinpath(collection)):
            if filename != f"{topic_name}.md":
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
    base_dir = pathlib.Path().resolve().joinpath("content").joinpath("collections")
    for collection in [f for f in os.listdir(base_dir) if os.path.isdir(base_dir.joinpath(f)) and f != "data"]:
        if collection_name and collection != collection_name:
            continue
        collection = collection.replace(".md", "")
        result.append(collection)
    return json.dumps(result)

@mcp.tool()
async def list_topics_in_a_collection(collection_name: str) -> str:
    result = []
    base_dir = pathlib.Path().resolve().joinpath("content").joinpath("collections")
    for collection in [f for f in os.listdir(base_dir) if os.path.isdir(base_dir.joinpath(f)) and f != "data"]:
        if collection != collection_name:
            continue
        for filename in os.listdir(base_dir.joinpath(collection)):
            filename = filename.replace(".md", "")
            result.append(filename)
    return json.dumps(result)

@mcp.tool()
async def list_data_manual() -> str:
    result = []
    base_dir = pathlib.Path().resolve().joinpath("content", "data-manual")
    for filename in os.listdir(base_dir):
        filename = filename.replace(".md", "")
        result.append(filename)
    return json.dumps(result)

@mcp.tool()
async def get_data_manual(filename: str) -> str:
    base_dir = pathlib.Path().resolve().joinpath("content", "data-manual")
    with open(base_dir.joinpath(f"{filename}.md"), "r") as file:
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

@mcp.tool()
async def get_topic_visualisation_data(topic_name: str | None = None) -> str:
    result = []
    base_dir = pathlib.Path().resolve().joinpath("content").joinpath("data")
    for folder in os.listdir(base_dir):
        if not topic_name:
            result.append({
                "topic": folder
            })
            continue
        if folder != f"{topic_name}":
            continue
        for filename in os.listdir(base_dir.joinpath(folder)):
            with open(base_dir.joinpath(folder).joinpath(filename), "r") as file:
                result.append({
                    "topic": folder,
                    "filename": filename,
                    "content": file.read()
                })
    
    if not topic_name:
        return json.dumps({
            "message": "No topic name provided, returning list of topics with data",
            "topics": result
        })

    return json.dumps(result)


@mcp.tool()
async def get_collection_topic_with_data(collection_name: str, topic_name: str) -> str:
    base_dir = pathlib.Path().resolve().joinpath("content")
    collections_dir = base_dir.joinpath("collections")
    data_dir = base_dir.joinpath("data")

    topic_file = collections_dir.joinpath(collection_name).joinpath(f"{topic_name}.md")
    if not topic_file.exists():
        return json.dumps({"error": f"Topic '{topic_name}' not found in collection '{collection_name}'"})

    with open(topic_file, "r") as f:
        topic_content = f.read()

    data_files = []
    if data_dir.joinpath(topic_name).exists():
        data_folder = data_dir.joinpath(topic_name)
        for filename in os.listdir(data_folder):
            with open(data_folder.joinpath(filename), "r") as f:
                data_files.append({"filename": filename, "content": f.read()})

    return json.dumps({
        "collection": collection_name,
        "topic": topic_name,
        "content": topic_content,
        "data": data_files,
    })


@mcp.custom_route("/", methods=["GET"])
async def health_check(request) -> PlainTextResponse:
    return PlainTextResponse("OK")
 

def main():
    # Initialize and run the server
    mcp.run(transport="streamable-http")


if __name__ == "__main__":
    mcp.run(transport="streamable-http")