from fastapi import Request, APIRouter, HTTPException, BackgroundTasks, UploadFile
from starlette.requests import Request as ARequest
from starlette.responses import FileResponse
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from config import settings
from tasks import handle_csv_userdata
from redis_api import REDIS_API

ALLOWED_FILES_ENDPOINT_FILE_EXTENSION = ("application/vnd.ms-excel",)

router = APIRouter()

templates = Jinja2Templates(directory="static/templates")

def files_template_response(request):
    return templates.TemplateResponse("files.html", {"request": request, "task_status": REDIS_API.get_dict('tasks:status')})

@router.get("/files", response_class=HTMLResponse)
async def files_get(request: Request):
    
    return files_template_response(request)

@router.post("/files", response_class=HTMLResponse)
async def files_post(
    file: UploadFile, request: ARequest, background_tasks: BackgroundTasks
):
    if file.content_type not in ALLOWED_FILES_ENDPOINT_FILE_EXTENSION:
        raise HTTPException(
            400,
            f"File content type not allowed. Use one of the following: {ALLOWED_FILES_ENDPOINT_FILE_EXTENSION}",
        )
    hashedfilename = file.filename.split(".")[0] + "_" + str(file.size)
    path = settings.tempfiles_dir + "/" + hashedfilename
    with open(path, "wb") as f:
        f.write(file.file.read())
    task = handle_csv_userdata.apply_async(
        (path,),
        task_id=hashedfilename,
    )
    #task = handle_csv_userdata(path) #DEBUG
    REDIS_API.set_key('tasks:status',task.id if task else 'eager', 'pending')
    
    return files_template_response(request)

@router.get("/file/{filename}")
async def file_download(filename: str):
    return FileResponse(settings.result_dir + "/" + filename + ".csv")
