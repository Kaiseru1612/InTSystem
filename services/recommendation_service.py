import markdown
from services.ai_model import AIModel  # Import AIModel
import os
from http.client import responses

from icecream import ic
from flask import Flask, render_template, request, session, redirect, url_for
from flask import render_template_string
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import google.generativeai as genai
import markdown
from markdown.extensions.fenced_code import FencedCodeExtension
import re
import os
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import openai  # don't go for upgraded version
import json
import requests
from flask_weasyprint import HTML, render_pdf
from weasyprint import CSS


API_KEY = os.getenv("GOOGLE_API_KEY")
genai.configure(api_key=API_KEY)
# model = genai.GenerativeModel(model_name="gemini-1.5-pro-002")
model = genai.GenerativeModel(model_name="gemini-2.0-flash")

# Create a Markdown instance with the FencedCodeExtension
md = markdown.Markdown(extensions=[FencedCodeExtension()])

def generate_text(course):
    prompts = {
    'approach': f"You are a pedagogy expert and you are designing a learning material for {course} for an undergrad university student. You have to decide the approach to take for learning from this learning material. Please provide a brief description of the approach you would take to study this learning material (provide in points). After that, please provide a brief description of the learning outcomes that you expect from this learning material.",
    'modules': f"Based on the course {course}, please provide a list of modules that you would include in the course. Each module should be a subtopic of the course and should be listed in bullet points. Additionally, please provide a brief description of each module to give an overview of the content covered in the module.",
    }
    completions = {}

    for key, prompt in prompts.items():
        response = model.generate_content(prompt)
        print("Answer: ", response)

        if key == 'modules':
            if response.parts[0].text:
                print(markdown_to_list(response.parts[0].text))
                completions[key] = markdown_to_list(response.parts[0].text)
        else:
            completions[key] = markdown.markdown(response.parts[0].text) if response.parts[0].text else ""

    # for key, prompt in prompts.items():
    #     completion = model.generate_content(
    #         model=model,
    #         prompt=prompt,
    #         temperature=0.1,
    #         max_output_tokens=5000,
    #     )
    #     # Convert the markdown string to a list
    #     if key == 'modules':
    #         # Replace bullet points with asterisks
    #         markdown_string = completion.result.replace('•', '*') if completion.result else ""
    #         completions[key] = markdown_to_list(markdown_string) if markdown_string else []
    #     else:
    #         completions[key] = markdown.markdown(completion.result) if completion.result else ""
    ic(completions)
    return completions




def generate_module_content(course_name,module_name):
    # First prompt for module content
    module_prompt = f"Course Name: {course_name} Topic: {module_name}. Please provide a comprehensive explanation of {module_name}. Feel free to use examples or analogies to clarify complex ideas. Additionally, if there are specific aspects or questions you'd like to address within the topic, please mention them for a more focused response."

    module_completion = model.generate_content(module_prompt)
    if module_completion.parts:
        module_content = module_completion.parts[0].text if module_completion.parts[0].text else ""
    else:
        module_content = ""
    # Second prompt for code snippets
    code_prompt = f"Course Name: {course_name} Topic: {module_name}. If the explanation of {module_name} requires code snippets for better understanding, please provide the relevant code snippets."
    code_completion = model.generate_content(code_prompt)
    if code_completion.parts:
        code_content = code_completion.parts[0].text if code_completion.parts[0].text else ""
    else:
        code_content = ""
    # Second prompt for ASCII art
    ascii_prompt = f"Course Name: {course_name} Topic: {module_name}. If the explanation of {module_name} requires diagram snippets for better understanding, please provide the relevant diagram snippets in the form of ASCII art."
    ascii_completion  = model.generate_content(ascii_prompt)
    if ascii_completion.parts:
        ascii_content = ascii_completion.parts[0].text if ascii_completion.parts[0].text else ""
    else:
        ascii_content = ""
    # Convert the markdown string to HTML, wrapping code snippets with <pre><code> tags
    module_content_html = md.convert(module_content)
    code_content_html = md.convert(code_content)
    ascii_content_html = md.convert(ascii_content)

    # Combine the module content and code snippets
    combined_content = f"{module_content_html}\n{code_content_html}\n{ascii_content_html}"

    return  combined_content

def generate_recommendations(saved_courses):
    recommended_courses = []
    for course in saved_courses:
        prompt = f"Based on the course {course.course_name}, please provide just a single course name at the top and a description for new recommended course that would be beneficial for the student to take next. The description should be concise and informative (less than 70 characters)."
        response= model.generate_content(prompt)
        print("New Course Name: ", response)

        if response.parts[0].text:
            course_description = markdown.markdown(response.parts[0].text)
            recommended_courses.append({'name': course.course_name, 'description': course_description})

    return recommended_courses
