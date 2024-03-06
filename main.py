import os
import requests
from fastapi import FastAPI
import uvicorn
from docxtpl import DocxTemplate, InlineImage
from docx.shared import Mm
from starlette.responses import FileResponse
import subprocess
import base64

app = FastAPI()

LIBRE_OFFICE_WINDOWS = r"C:\Program Files\LibreOffice\program\soffice.exe"
URL_GLOBAL = '116.213.55.46'
URL_LOCAL = '10.10.10.10'

def cors_headers(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
        )
    return app

@app.get('/qrcode')
async def getDocument(id:int):
	response = requests.get(
		f"http://{URL_LOCAL}/work-management/api/v2/work/gen-qrcode?mp_recom_id={id}",
		headers={
			'Authorization': 'Bearer ey8ihslkdyd993ijenw69araeqiep093qjjqns6780o2h9759834kiuy35y7sjhs8s90ppwlmxvcftw89w0'
			})
	# print(response.status_code)
	status = response.status_code
	if status != 200:
		raise Exception(response.content)

	data = response.json()

	image_filename = "file.png"
	with open(image_filename, "wb") as f:
		image_data = base64.b64decode(data['img_b64'])
		print(image_data)
		f.write(image_data)

	doc = DocxTemplate("template.docx")
	# image = InlineImage(doc, 'file.jpg', width=Mm(40))
	image = InlineImage(doc, image_filename , width=Mm(40))

	context = { 
		'company_name' : "World company",
		'qrcode': image
	}

	doc.render(context)
	file_name = "result.docx"
	doc.save(file_name)
	
	file_path = os.getcwd() + "/" + file_name
	return FileResponse(path=file_path, media_type='application/octet-stream',filename=file_name)

	# args = [LIBRE_OFFICE, '--headless', '--convert-to', 'pdf', file_name]
	# result = subprocess.run(args)

	# file_pdf = "result.pdf"
	# return FileResponse(path=file_pdf,filename=file_pdf, media_type='application/pdf')

if __name__ == "__main__":
    uvicorn.run("main:app", port=4444, host="0.0.0.0", reload=False, access_log=False)