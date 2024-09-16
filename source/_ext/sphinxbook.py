import os
import re
import json
from datetime import datetime
import frontmatter
from docutils.parsers.rst import directives
from sphinx_design.grids import GridDirective
from operator import attrgetter

class PostGridDirective(GridDirective):
    option_spec = dict(GridDirective.option_spec, **{
        "tags": directives.unchanged,
        "sort": str
    })

    class PostMetadata:
        def __init__(self):
            self.tags = []
            self.icon = None
            self.title = "Untitled Post"
            self.date = datetime.min
            self.desc = ""
            self.link = ""

    def get_post_metadata(self, file_path):
        post = frontmatter.load(file_path)
        post_metadata = PostGridDirective.PostMetadata()

        if "tags" in post.metadata:
            post_metadata.tags = post.metadata["tags"]

        if "title" in post.metadata:
            post_metadata.title = post.metadata["title"]
        else:
            match = re.search(r"^# (.+)", post.content, re.MULTILINE)
            if match:
                post_metadata.title = match.group(1)

        if "date" in post.metadata:
            post_metadata.date = datetime.strptime(post.metadata["date"], "%Y-%m-%d")

        if "desc" in post.metadata:
            post_metadata.desc = post.metadata["desc"]
        else:
            for line in post.content.split("\n\n"):
                if line and line[0].isalnum():
                    post_metadata.desc = line
                    break

        if "icon" in post.metadata:
            post_metadata.icon = post.metadata["icon"]
        
        source_dir = self.state.document.settings.env.srcdir
        post_metadata.link = os.path.relpath(file_path, source_dir)
        post_metadata.link = post_metadata.link.removesuffix(".md")

        return post_metadata
    
    def is_post(file_path):
        return file_path.endswith(".md")
    
    def is_section_folder(file_path):
        if not os.path.isdir(file_path):
            return False
        
        folder_contains_toc_file = os.path.isfile(os.path.join(file_path, "_toc.md"))
        
        return folder_contains_toc_file
    
    def add_post_metadata_to_grid(self, post_metadata):
        display_title = post_metadata.title
        if len(display_title) > 53:
            display_title = display_title[:50].strip() + "..."

        display_desc = post_metadata.desc
        if len(display_desc) > 103:
            display_desc = display_desc[:100].strip() + "..."

        if post_metadata.icon != None:
            display_title = f"{post_metadata.icon} {display_title}"

        self.content += [
            f":::{{grid-item-card}} {display_title}",
            f":link: {post_metadata.link}",
            "",
            f"{display_desc}",
            ":::"
        ]

    def get_section_metadata(self, folder_path):
        toc_file_path = os.path.join(folder_path, "_toc.md")
        section_opening_filename = None

        with open(toc_file_path, "r") as f:
            previous_line = None
            for line in f:
                if previous_line == "```{toctree}":
                    section_opening_filename = line.strip() + ".md"
                    break

                previous_line = line.strip()

        if section_opening_filename == None:
            return
        
        section_opening_file_path = os.path.join(folder_path, section_opening_filename)
        section_metadata = self.get_post_metadata(section_opening_file_path)
        
        return section_metadata
    
    def run(self):
        # get directive options
        if "tags" not in self.options:
            self.tags_filter = []
        else:
            self.tags_filter = json.loads(self.options["tags"])
            
        if "sort" not in self.options:
            self.sort_by = None
        else:
            sort_options = self.options["sort"]
            
            # shortcuts
            if sort_options == "newest":
                sort_options = "date desc"
            elif sort_options == "oldest":
                sort_options = "date asc"
            
            sort_options = sort_options.split(" ")
            self.sort_by = sort_options[0]

            if len(sort_options) == 1:
                if self.sort_by == "title":
                    self.sort_order = "asc"
                elif self.sort_by == "date":
                    self.sort_order = "desc"
            else:
                self.sort_order = sort_options[1]

        # get all post metadata
        source_dir = self.state.document.settings.env.srcdir
        posts_dir = os.path.join(source_dir, "posts/")
        post_metadata_list = []
        
        for file in os.listdir(posts_dir):
            file_path = os.path.join(posts_dir, file)

            if PostGridDirective.is_post(file_path):
                post_metadata = self.get_post_metadata(file_path)
            elif PostGridDirective.is_section_folder(file_path):
                post_metadata = self.get_section_metadata(file_path)

            post_metadata_list.append(post_metadata)

        # sort post metadata
        if self.sort_by != None:
            post_metadata_list = sorted(post_metadata_list, key=attrgetter(self.sort_by), reverse=(self.sort_order == "desc"))

        # add post metadata to content
        self.content = []

        for post_metadata in post_metadata_list:
            if self.tags_filter != []:
                post_contains_at_least_one_tag = bool(set(self.tags_filter) & set(post_metadata.tags))
                
                if not post_contains_at_least_one_tag:
                    continue

            self.add_post_metadata_to_grid(post_metadata)

        # set default settings for grid directive
        self.arguments = ["1 2 2 3"]
        self.options["gutter"] = ["sd-g-4", "sd-g-xs-4", "sd-g-sm-4", "sd-g-md-4", "sd-g-lg-4"]

        return super().run_with_defaults()
    
def setup(app):
    app.add_directive("post-grid", PostGridDirective)
