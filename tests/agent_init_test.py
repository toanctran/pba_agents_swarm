import inspect
import json
import os
import sys
import unittest

sys.path.insert(0, '../agency-swarm')

from test_agent import TestAgent

from organization_swarm import set_openai_key, Agent


class AgentInitTest(unittest.TestCase):
    agent = None

    def setUp(self):
        self.agent = TestAgent().init_oai()
        with open(self.get_class_folder_path() + '/test_agent/instructions.md', 'r') as f:
            self.test_instructions = f.read()



    def test_init_agent(self):
        """it should create assistant and save it to settings"""
        self.assertTrue(self.agent.id)

        self.assertTrue(len(self.agent.tools) == 2)

        self.settings_path = self.agent.get_settings_path()
        self.assertTrue(os.path.exists(self.settings_path))

        # find assistant in settings by id
        with open(self.settings_path, 'r') as f:
            settings = json.load(f)
            for assistant_settings in settings:
                if assistant_settings['id'] == self.agent.id:
                    self.assertTrue(self.agent._check_parameters(assistant_settings))

        self.assertEqual(self.agent.instructions, self.test_instructions)

    def test_init_agent_local(self):
        agent = Agent(name="test_agent_local",
                      files_folder="./test_agent/files",
                      instructions="./test_agent/instructions.md",
                      tools=[])

        agent.init_oai()

        self.assertTrue(agent.id)

        self.assertTrue(len(agent.file_ids) == 1)

    def test_load_agent(self):
        """it should load assistant from settings"""
        agent2 = TestAgent().init_oai()
        self.assertEqual(self.agent.id, agent2.id)
        self.assertEqual(self.agent.instructions, self.test_instructions)
        print(self.agent.files_folder)

    def get_class_folder_path(self):
        return os.path.abspath(os.path.dirname(inspect.getfile(self.__class__)))

    # def tearDown(self):
    #     self.agent.delete_assistant()
    #     pass


if __name__ == '__main__':
    unittest.main()
