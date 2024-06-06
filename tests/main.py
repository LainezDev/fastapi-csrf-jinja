from typing import Annotated, Union
from fastapi.templating import Jinja2Templates
from fastapi import FastAPI, Request, Form, Header, HTTPException
from pydantic import BaseModel
from fastapi_csrf_jinja.middleware import FastAPICSRFJinjaMiddleware
from fastapi_csrf_jinja.jinja_processor import csrf_token_processor

fake_secret_token = "coneofsilence"

fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}

app = FastAPI()

cookie_name = "cookie_name"
header_name = "header_name"

app.add_middleware(
    FastAPICSRFJinjaMiddleware, 
    secret = "your_secret",
    cookie_name = cookie_name,
    header_name = header_name,
    )

templates = Jinja2Templates(
    directory="templates", 
    context_processors=[csrf_token_processor(cookie_name, header_name)]
    )

class Item(BaseModel):
    id: str
    title: str
    description: Union[str, None] = None


@app.get("/get")
async def get():
    return {"hello": "world"}

@app.post("/post1")
async def post1(request: Request):
    json_data = await request.json()
    return json_data

@app.post("/post2")
async def post1(request: Request, form_data: dict = Form(...)):    
    return form_data
    
@app.get("/form")
async def get_form(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})