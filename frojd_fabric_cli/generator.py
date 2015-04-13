import os
import re
import jinja2


class Generator(object):
    stages = None
    path = None
    loader = None
    environment = None

    def __init__(self, stages=None, path=None, *args, **kwargs):
        self.validate_stages(stages)

        self.stages = stages
        self.path = path

        current_dir = os.path.dirname(os.path.abspath(__file__))
        templates_dir = os.path.join(current_dir,  "templates")
        self.loader = jinja2.FileSystemLoader(templates_dir)
        self.environment = jinja2.Environment(loader=self.loader)

    def create_index(self):
        template = self.environment.get_template("index.py.txt")
        output = template.render(stages=self.stages)

        stage_dir = self.get_stages_path()
        os.makedirs(stage_dir)

        index_path = os.path.join(stage_dir, "__init__.py")
        self.write_file(output, index_path)

    def create_stage(self, name=None):
        template = self.environment.get_template("stage.py.txt")
        stage = self.get_stage(name)
        output = template.render(stage=stage)

        stage_dir = self.get_stages_path()
        if not os.path.exists(stage_dir):
            os.makedirs(stage_dir)

        file_path = os.path.join(stage_dir, "%s.py" % name)
        self.write_file(output, file_path)

    def create_stages(self):
        for stage in self.stages:
            self.create_stage(stage["NAME"])

    def get_stages_path(self):
        return os.path.join(self.path, "stages")

    def get_stage(self, name):
        for stage in self.stages:
            if stage["NAME"] == name:
                return stage

    def write_file(self, content, path):
        with open(path, "w") as fout:
            fout.write(content)

    def validate_stages(self, stages):
        for stage in stages:
            if not re.search("^\w{1,}$", stage["NAME"]):
                raise Exception("Bad Configuration")

