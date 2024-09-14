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

    def get_post_metadata(self, file_path):
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
    
    def run(self):
        posts_folder = "posts/"

        # set default values for grid directive
        self.arguments = ["1 2 2 3"]
        self.options["gutter"] = ["sd-g-4", "sd-g-xs-4", "sd-g-sm-4", "sd-g-md-4", "sd-g-lg-4"]

        self.content = []
        source_dir = self.state.document.settings.env.srcdir
        posts_dir = os.path.join(source_dir, posts_folder)

        for file in os.listdir(posts_dir):
            if not file.endswith(".md"):
                continue

            file_path = os.path.join(posts_dir, file)
            post_metadata = PostGridDirective.get_post_metadata(file_path)

            display_title = post_metadata.title
            display_desc = post_metadata.desc
            display_link = os.path.join(posts_folder, file)
            display_link = display_link.removesuffix(".md")

            if len(display_title) > 53:
                display_title = display_title[:50].strip() + "..."

            if len(display_desc) > 103:
                display_desc = display_desc[:100].strip() + "..."

            if post_metadata.icon != None:
                display_title = post_metadata.icon + " " + display_title

            self.content = [
                f":::{{grid-item-card}} {display_title}",
                f":link: {display_link}",
                "",
                f"{display_desc}",
                ":::"
            ]

        return super().run_with_defaults()
    
def setup(app):
    app.add_directive("post-grid", PostGridDirective)
