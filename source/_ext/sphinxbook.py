import os
import re
import frontmatter
from sphinx_design.grids import GridDirective

class PostGridDirective(GridDirective):
    class PostMetadata:
        def __init__(self):
            self.icon = None
            self.title = "Untitled Post"
            self.desc = ""

    def get_post_metadata(file_path):
        post = frontmatter.load(file_path)
        post_metadata = PostGridDirective.PostMetadata()

        if "title" in post.metadata:
            post_metadata.title = post.metadata["title"]
        else:
            match = re.search(r"^# (.+)", post.content, re.MULTILINE)
            if match:
                post_metadata.title = match.group(1)

        if "desc" in post.metadata:
            post_metadata.desc = post.metadata["desc"]
        else:
            for line in post.content.split("\n\n"):
                if line and line[0].isalnum():
                    post_metadata.desc = line
                    break

        if "icon" in post.metadata:
            post_metadata.icon = post.metadata["icon"]

        return post_metadata
    
    def add_post_to_grid(self, file_path, section_folder=None):
        post_metadata = PostGridDirective.get_post_metadata(file_path)

        display_title = post_metadata.title
        display_desc = post_metadata.desc

        if section_folder == None:
            display_link = os.path.join(self.posts_folder, os.path.basename(file_path))
        else:
            display_link = os.path.join(section_folder, os.path.basename(file_path))

        display_link = display_link.removesuffix(".md")

        if len(display_title) > 53:
            display_title = display_title[:50].strip() + "..."

        if len(display_desc) > 103:
            display_desc = display_desc[:100].strip() + "..."

        if post_metadata.icon != None:
            display_title = post_metadata.icon + " " + display_title

        self.content += [
            f":::{{grid-item-card}} {display_title}",
            f":link: {display_link}",
            "",
            f"{display_desc}",
            ":::"
        ]

    def add_section_to_grid(self, folder_path, section_folder):
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
        self.add_post_to_grid(section_opening_file_path, os.path.join(self.posts_folder, section_folder))
    
    def run(self):
        # add pages and sections from posts folder
        self.posts_folder = "posts/"
        self.content = []

        source_dir = self.state.document.settings.env.srcdir
        posts_dir = os.path.join(source_dir, self.posts_folder)
        
        for file in os.listdir(posts_dir):
            file_path = os.path.join(posts_dir, file)

            if file_path.endswith(".md"):
                self.add_post_to_grid(file_path)
            elif os.path.isdir(file_path):
                is_section_folder = os.path.isfile(os.path.join(file_path, "_toc.md"))
                if is_section_folder:
                    self.add_section_to_grid(file_path, os.path.basename(file_path))

        # set default settings for grid directive
        self.arguments = ["1 2 2 3"]
        self.options["gutter"] = ["sd-g-4", "sd-g-xs-4", "sd-g-sm-4", "sd-g-md-4", "sd-g-lg-4"]

        return super().run_with_defaults()
    
def setup(app):
    app.add_directive("post-grid", PostGridDirective)
