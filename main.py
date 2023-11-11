import uvicorn

from settings import get_settings

if __name__ == "__main__":
    settings = get_settings()
    server = settings.uvicorn
    uvicorn.run(
        app="src.app:app",
        host=server.host,
        port=server.port,
        log_level=server.log_level,
        reload=server.reload
    )
