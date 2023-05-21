import pandas as pd


def error_check_decorator(method):
    def wrapper(self, *args, **kwargs):
        try:
            return method(self, *args, **kwargs)
        except Exception as e:
            line_number = kwargs.get('index') + 1 if 'index' in kwargs else -1
            print(f"Error occurred in line {line_number}: {str(e)}")
    return wrapper


def bad_line_handler(line):
    print(line)
    return "warn"


class M3UTransformer:

    def __init__(self, input_file, settings):
        self.input_file = input_file
        self.settings = settings
        self.df = None
        self.output_file = input_file[:-4]+self.settings["replace_file_value"] +".m3u"

        if self.settings["replace_file"]:
            self.output_file = self.input_file

    def transform(self):
        self.read_m3u_file()
        self.switch_slash_placement()
        self.delete_lines_containing(self.settings["kill_line"])
        self.replace_lines_starting_with(self.settings["initiator"], self.settings["replacement"])
        self.write_m3u_file()

        print("Transformation complete. Output file:", self.output_file)

    @error_check_decorator
    def read_m3u_file(self):
        self.df = pd.read_csv(self.input_file, header=None, on_bad_lines=bad_line_handler, engine='python',sep='\t')

    @error_check_decorator
    def replace_lines_starting_with(self, search_str, replace_str):
        for index, row in self.df.iterrows():
            if row[0].startswith(search_str):
                self.df.at[index, 0] = replace_str + row[0][len(search_str):]

    @error_check_decorator
    def delete_lines_containing(self, search_str):
        for index, row in self.df.iterrows():
            if search_str in row[0]:
                self.df.drop(index, inplace=True)

    @error_check_decorator
    def switch_slash_placement(self):
        for index, row in self.df.iterrows():
            self.df.at[index, 0] = row[0].replace("\\", "/")

    def write_m3u_file(self):
        self.df.columns = [self.settings["header"]]
        self.df.to_csv(self.output_file, sep="\t", header=True, index=False)
