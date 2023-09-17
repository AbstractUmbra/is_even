import uvicorn

if __name__ == "__main__":
    uvicorn.run("is_even:app", host="0.0.0.0", port=8080, workers=2)  # type: ignore # bad upstream types
