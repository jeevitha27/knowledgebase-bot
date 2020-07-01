from flask import Blueprint, request, render_template
import os,sys
from controllers.readLogic import getFilesInAllSubFolder,response,convert,pdf_dict
main=Blueprint('main',__name__)

resultDict, res_sen_list = pdf_dict()

@main.route("/KBSearchEngine")
def get_bot_response():
    flag=True
    while(flag==True):
        user_response = request.args.get('msg')
        user_response=user_response.lower()
        result = response(user_response, resultDict, res_sen_list)
        return result

@main.route("/HelloWorld")
def hello():
    return "Hello World"

@main.route("/")
def home():
    return render_template("index.html")