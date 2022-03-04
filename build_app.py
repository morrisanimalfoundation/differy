import json
import sys
import urllib.request
import urllib.parse
import os
import markdown
from jinja2 import Environment, FileSystemLoader

api_token = sys.argv[1]
project_id = sys.argv[2]
release_wiki_slug = urllib.parse.quote_plus(sys.argv[3])
visualization_directory = sys.argv[4]

# Tokenize the wiki detail endpoint.
gitlab_endpoint = 'https://gitlab.com/api/v4/projects/{project_id}/wikis/{release_wiki_slug}?with_content=1' \
    .format(project_id=project_id, release_wiki_slug=release_wiki_slug)

# Build out the API request.
request = urllib.request.Request(gitlab_endpoint)
request.add_header("PRIVATE-TOKEN", api_token)
handle = urllib.request.urlopen(request)
response = json.loads(handle.read().decode(handle.info().get_param('charset') or 'utf-8'))

# Begin building context up for our "app" template html file.
# Find all of our charts.
visualizations = []
for file in os.listdir(visualization_directory):
    full_path = os.path.join(visualization_directory, file)
    if os.path.isfile(full_path):
        visualizations.append('./images/' + file)

# Get ready to render our template.
current_directory = os.path.dirname(os.path.abspath(__file__))
env = Environment(loader=FileSystemLoader(current_directory + '/templates'))

# Render it and print it into stdout.
# The host can figure out where to put it.
final_content = env.get_template('index.html')\
    .render(title=response['title'], content=markdown.markdown(response['content']), visualizations=visualizations)
print(final_content)
