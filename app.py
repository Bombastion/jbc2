from flask import Flask, jsonify, request
from app_service import AppService
import json

app = Flask(__name__)
appService = AppService()


@app.route("/")
def home():
    return "App Works!!!"

@app.route("/inventory/create", methods=["POST"])
def create_inventory():
    data = request.form
    return jsonify(appService.create_inventory(name=data["name"]))
