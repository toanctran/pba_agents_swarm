import inspect
import time
from typing import Literal
import json
import os
from organization_swarm.agents import Agent
from organization_swarm.messages import MessageOutput
from organization_swarm.user import User
from organization_swarm.util.oai import get_openai_client
import sys

class Thread:
    id: str = None
    thread = None
    run = None

    def __init__(self, agent: Literal[Agent, User], recipient_agent: Agent):
        self.agent = agent
        self.recipient_agent = recipient_agent
        self.client = get_openai_client()
        self.chat_history = []

    def save_thread_history(self, thread_id):
        """
        Saves the current thread history to a file.
        """
        main_script_path = sys.argv[0]
        root_directory = os.path.dirname(main_script_path)
        file_path = os.path.join(root_directory,f'{thread_id}.json')  # File name based on thread ID
        with open(file_path, 'w') as file:
            json.dump(self.chat_history, file, indent=4)


    def get_completion(self, message: str, message_files=None, yield_messages=True):
        if not self.thread:
            if self.id:
                self.thread = self.client.beta.threads.retrieve(self.id)
            else:
                self.thread = self.client.beta.threads.create()
                self.id = self.thread.id

            # Determine the sender's name based on the agent type
            sender_name = "user" if isinstance(self.agent, User) else self.agent.name
            playground_url = f'https://platform.openai.com/playground?assistant={self.recipient_agent._assistant.id}&mode=assistant&thread={self.thread.id}'
            print(f'THREAD:[ {sender_name} -> {self.recipient_agent.name} ]: URL {playground_url}')

        # send message
        self.client.beta.threads.messages.create(
            thread_id=self.thread.id,
            role="user",
            content=message,
            file_ids=message_files if message_files else [],
        )

        # self.chat_history.append({'sender': sender_name, 'message': message})

        if yield_messages:
            yield MessageOutput("text", self.agent.name, self.recipient_agent.name, message)

        # create run
        self.run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.recipient_agent.id,
        )

        while True:
            # wait until run completes
            while self.run.status in ['queued', 'in_progress']:
                time.sleep(0.5)
                self.run = self.client.beta.threads.runs.retrieve(
                    thread_id=self.thread.id,
                    run_id=self.run.id
                )

            # function execution
            if self.run.status == "requires_action":
                tool_calls = self.run.required_action.submit_tool_outputs.tool_calls
                tool_outputs = []
                for tool_call in tool_calls:
                    if yield_messages:
                        yield MessageOutput("function", self.recipient_agent.name, self.agent.name, str(tool_call.function))

                    output = self._execute_tool(tool_call)
                    if inspect.isgenerator(output):
                        try:
                            while True:
                                item = next(output)
                                if isinstance(item, MessageOutput) and yield_messages:
                                    yield item
                        except StopIteration as e:
                            output = e.value
                    else:
                        if yield_messages:
                            yield MessageOutput("function_output", tool_call.function.name, self.recipient_agent.name, output)

                    tool_outputs.append({"tool_call_id": tool_call.id, "output": str(output)})
                    self.chat_history.append({'sender': self.recipient_agent.name, 'tool_outputs': tool_outputs})

                # submit tool outputs
                self.run = self.client.beta.threads.runs.submit_tool_outputs(
                    thread_id=self.thread.id,
                    run_id=self.run.id,
                    tool_outputs=tool_outputs
                )
            # error
            elif self.run.status == "failed":
                self.chat_history.append({'sender': self.recipient_agent.name, 'last_run_error': self.run.last_error})
                raise Exception("Run Failed. Error: ", self.run.last_error)
            # return assistant message
            else:
                messages = self.client.beta.threads.messages.list(
                    thread_id=self.id
                )
                message = messages.data[0].content[0].text.value
                self.chat_history.append({'sender': self.recipient_agent.name, 'message':message})
                if yield_messages:
                    yield MessageOutput("text", self.recipient_agent.name, self.agent.name, message)
                self.save_thread_history(thread_id=self.id)
                return message

    def _execute_tool(self, tool_call):
        funcs = self.recipient_agent.functions
        # func = next(iter([func for func in funcs if func.__name__ == tool_call.function.name]))
        func = next((func for func in funcs if func.__name__ == tool_call.function.name), None)

        if not func:
            return f"Error: Function {tool_call.function.name} not found. Available functions: {[func.__name__ for func in funcs]}"

        try:
            # init tool
            func = func(**eval(tool_call.function.arguments))
            # get outputs from the tool
            output = func.run()

            return output
        except Exception as e:
            return "Error: " + str(e)
