import subprocess, json, os
import sublime, sublime_plugin

class NpmCommand(object):
	def parse_json(self, json_string):
		json.loads(str(json_string))

	#TODO def find_npm(self)
		#find npm's bin path so we don't need to use `shell=True` with subprocess (lookin' at you, Windows)
		#self.npm_path = ...

	def run_npm(self, commands):
		dir_name = os.path.dirname(self.view.file_name())
		proc = subprocess.Popen(['npm']+commands, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=dir_name)
		out, err = proc.communicate()
		return_code = proc.poll()
		#sublime.status_message("proc exited with code "+str(return_code))
		#show results
		window = sublime.active_window()
		output_view = window.get_output_panel("textarea")
		window.run_command("show_panel", {"panel": "output.textarea"})
		output_view.set_read_only(False)
		# sections commented out are the sublime v2 way, AFAIK they're the only bits preventing v2 compatability
		# edit = output_view.begin_edit()
		# output_view.insert(edit, output_view.size(), "Hello, World!")
		# TODO: pretty-fy the feedback to the user...err OR out show? npm warnings enough to show err? even use output panel?
		output_view.run_command("append", {"characters": "Out: "+out.decode("utf-8")})
		output_view.run_command("append", {"characters": "Err: "+err.decode("utf-8")})
		# output_view.end_edit(edit)
		output_view.set_read_only(True)
		# return the process result
		return_code