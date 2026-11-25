from dotenv import load_dotenv
load_dotenv()
import uvicorn
uvicorn.run("api.app:app",host="0.0.0.0",port=8000)
