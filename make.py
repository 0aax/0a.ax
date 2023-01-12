import os
from datetime import datetime
from pathlib import Path
from shutil import copytree, rmtree
from markdown2 import markdown
from jinja2 import Environment, FileSystemLoader

content_dir = Path('./content').resolve()
output_dir = Path('./output').resolve()
template_dir = Path('./templates').resolve()

def make_site():
    rmtree(output_dir)
    copytree(template_dir.joinpath('static'), output_dir.joinpath('static'))
    
    if not os.path.exists(output_dir.joinpath('posts')):
        os.makedirs(output_dir.joinpath('posts'))
    
    if not os.path.exists(output_dir.joinpath('static')):
        os.makedirs(output_dir.joinpath('static'))

    all_posts = []
    for post_path in content_dir.glob('posts/*.md'):
        all_posts.append(post_path.relative_to(content_dir))
    
    posts_list = []
    for post in all_posts:
        posts_list.append(make_post(post))

    posts_list.sort(key=lambda x: x['date'], reverse=True)
    for i, post in enumerate(posts_list):
        format_date = posts_list[i]['date'].strftime('%Y-%m-%d')
        posts_list[i]['date'] = format_date

    make_index(posts_list)

def make_index(posts_list):
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('index_template.html')

    input_page = content_dir.joinpath(Path('index.md'))
    output_page = output_dir.joinpath(Path('index.html'))

    with open(input_page, 'r') as file:
        parsed_md = markdown(file.read(), extras=['metadata', 'footnotes'])
    
    try: post_title = parsed_md.metadata['title']
    except: post_title = ''

    page = {
        'title': post_title,
        'content': parsed_md
    }

    html = template.render(post=page, list_posts=posts_list)

    with open(output_page, 'w', encoding='utf-8') as file: 
        file.write(html)

def make_post(post_path):
    post_relative_path = str(post_path).split('.')[0]
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('post_template.html')

    input_page = content_dir.joinpath(Path(post_relative_path + '.md'))
    output_page = output_dir.joinpath(Path(post_relative_path + '.html'))

    with open(input_page, 'r') as file:
        parsed_md = markdown(file.read(), extras=['metadata', 'footnotes'])

    try: post_date = datetime.strptime(parsed_md.metadata['date'], '%Y-%m-%d')
    except: post_date = datetime(1999, 1, 1)
    try: post_title = parsed_md.metadata['title']
    except: post_title = ''
    try: post_slug = parsed_md.metadata['slug']
    except: post_slug = ''

    post = {
        'title': post_title,
        'date': post_date.strftime('%Y-%m-%d'),
        'content': parsed_md
    }

    html = template.render(post=post)

    with open(output_page, 'w', encoding='utf-8') as file: 
        file.write(html)

    return {'title': post_title, 'date': post_date, 'slug': post_slug}

if __name__ == '__main__':
    make_site()