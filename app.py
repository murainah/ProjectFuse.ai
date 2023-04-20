from flask import Flask, render_template, request, redirect, url_for
from langchain.llms import OpenAI
import os
from langchain.prompts import PromptTemplate
import re

os.environ["OPENAI_API_KEY"] = "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"
llm = OpenAI(temperature=0.9)


app = Flask(__name__)
d=["descipline", "area_of_focus", "country"]
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        return redirect(url_for('result.html'))
    else:
        return render_template('search.html')


@app.route('/result.html')
def result():
    discipline = request.args.get('discipline')
    project_type = request.args.get('project_type')
    country = request.args.get('country')
    area_of_focus = request.args.get('area_of_focus')
    sop = request.args.get('sop')
    if country == "No":
        country = ""
    if project_type is not None:
        if sop == "No":
            prompt = PromptTemplate(
            input_variables=["discipline", "area_of_focus", "project_type", "country"],
            template="give me a project topic for final year {discipline} student on {project_type} student in {area_of_focus}  sector in {country} ",
        )
            result = llm(prompt.format(discipline=discipline, area_of_focus=area_of_focus, country=country, project_type = project_type))

            return render_template('result.html', result = result)
        else:
            prompt = PromptTemplate(
                input_variables=["discipline", "area_of_focus", "project_type", "country"],
                template="give me a project topic for final year {discipline} student on {project_type} in {area_of_focus}  sector in {country} with statement of problem",
            )
            result = llm(prompt.format(discipline=discipline, area_of_focus=area_of_focus, country=country,project_type=project_type))

            return render_template('result.html', result=result)

    else:
        if sop == "No":
            prompt = PromptTemplate(
                input_variables=["discipline", "area_of_focus", "country"],
                template="give me a project topic for final year  {discipline}  student in {area_of_focus}  sector in {country} ",
            )
            result = llm(prompt.format(discipline=discipline, area_of_focus=area_of_focus, country=country,))
            return render_template('result.html', result=result)
        else:
            prompt = PromptTemplate(
                input_variables=["discipline", "area_of_focus", "country"],
                template="give me a project topic for final year  {discipline} student in {area_of_focus}  sector in {country} with statement of problem",
            )
            result = llm(prompt.format(discipline=discipline, area_of_focus=area_of_focus, country=country,))
            return render_template('result.html', result=result)

if __name__ == '__main__':
    app.run(port=8000, debug=True)
