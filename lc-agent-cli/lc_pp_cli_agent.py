import argparse
from langchain.agents import initialize_agent
from langchain.llms import OpenAI
# from langchain import LLMChain
# from langchain.prompts import PromptTemplate
import json
from langchain.agents import Tool
# from langchain.chains.question_answering import load_qa_chain

from flask import Flask
from flask_cors import CORS

from flask import *
import json, time

# import custom tools

llm = OpenAI(temperature=1)

request_format_sr = '{{"user":"<user name>","role":"<role>"}}'
description_sr = f'helps to assign security role to the user. For example, if you get a query "assign security role system administrator to the user Dhina", the role is System Administrator and Dhina is the user name. Another example would be "assign the role Supervisor to John", then Supervisor is the role and John is the user name. Input should be JSON in the following format: {request_format_sr}'

request_format_backup = '{{"environment":"<environment name>"}}'
description_backup = f'helps to backup a particular environment. You would typically receive a query for example "take a backup of the dev environment", then dev is the envrionment name. Input should be JSON in the following format: {request_format_backup}'

request_format_team = '{{"user":"<user name>","team":"<team>"}}'
description_team = f'helps to add the user to a particular team. For example, if you get a query "add Dhina to Contact Center Agents team", then Dhina is the user name and Contact Center Agents is the team. Another example would be "Add the user John to the Contact Center Agents", then John is the user name and Contact Center Agents is the team. Input should be JSON in the following format: {request_format_team}'

request_format_audit = '{{"table":"<table name>"}}'
description_audit = f'helps to enable audit for a table. You would typically receive a query like "Enable audit for Case", then case is the table name. Another example "Enable audit for Account entity", then Account is the table name. Input should be JSON in the following format: {request_format_audit}'

def assign_security_role_DVAPI(user: str = None, role: str = None) -> str:
        print("\nCalling Dataverse API to assign '" + role + "' security role to user '" + user + "'")

def assign_security_role(json_request: str) -> str:
    arguments_dictionary = json.loads(json_request)

    user = arguments_dictionary["user"]
    role = arguments_dictionary["role"]
    return assign_security_role_DVAPI(user=user, role=role)

def backup_environment_DVAPI(environment: str = None) -> str:
        print("\nCalling Dataverse API to backup the environment '" + environment + "'")
        

def backup_environment(json_request: str) -> str:
    arguments_dictionary = json.loads(json_request)

    environment = arguments_dictionary["environment"]
    return backup_environment_DVAPI(environment=environment)

def add_user_to_team_DVAPI(user: str = None, team: str = None) -> str:
        print("\nCalling Dataverse API to add the user '" + user + "' to the team '" + team + "'")

def add_user_to_team(json_request: str) -> str:
    arguments_dictionary = json.loads(json_request)

    user = arguments_dictionary["user"]
    team = arguments_dictionary["team"]
    return add_user_to_team_DVAPI(user=user, team=team)

def enable_audit_for_table_DVAPI(table: str = None) -> str:
        print("\nCalling Dataverse API to enable audit for table '" + table + "'")

def enable_audit_for_table(json_request: str) -> str:
    arguments_dictionary = json.loads(json_request)

    table = arguments_dictionary["table"]
    return enable_audit_for_table_DVAPI(table=table)

tools = [
    Tool( #assign security role
    name="Assign Security Role", func=assign_security_role, description=description_sr
    ),
    Tool( #backup environment
        name="Backup Environment", func=backup_environment, description=description_backup
    ),
    Tool( #add user to the team
        name="Add User to Team", func=add_user_to_team, description=description_team
    ),
        Tool( #enable audit for a table
        name="Enable Audit for Table", func=enable_audit_for_table, description=description_audit
    )
]


# Construct the react agent type.
agent = initialize_agent(
    tools,
    llm,
    agent="zero-shot-react-description",
    verbose=True
)


#
# get the question asa a command line argument.
# $ python3 weather_agent.py --question "What about the weather today in Genova, Italy"
#
# parser = argparse.ArgumentParser(description='agent calling power platform api to perform actions')
# parser.add_argument('-q', '--question', dest='question', type=str, help='question to submit to the agent. Enclose the question sentence in quotes.', required=True)
# args = parser.parse_args()

# # run the agent
# agent.run(args.question)

app = Flask(__name__)
CORS(app)

@app.route('/request/admin/', methods=['GET'])
def home_page():
    query = str(request.args.get('question')) #/request/admin/?question=Dhina
    agent_response = agent.run(query)

    data_set = {'Message': agent_response}
    json_dump = json.dumps(data_set)
    return json_dump

if __name__ == "__main__":
    app.run(port=7778)


