import os
import re
import shutil

# Paths
posts_dir = r"E:\Documents\scratch\themes\nostyleplease\content"
attachments_dir = r"E:\Documents\Obsidian\Merged\Attachments"
static_images_dir = r"E:\Documents\scratch\static\images"

# Regex pattern to find image references in the format ![[some/path/image.png]]
image_pattern = re.compile(r'!\[\[([^]]*\.png)\]\]')

# Step 1: Process each markdown file in the posts directory and subdirectories
for root, _, files in os.walk(posts_dir):
    for filename in files:
        if filename.endswith(".md"):
            filepath = os.path.join(root, filename)
            
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()
            
            # Step 2: Find all image links
            images = image_pattern.findall(content)
            
            # Step 3: Process each found image
            for image_rel_path in images:
                image_source = os.path.join(attachments_dir, image_rel_path)  # Full path in attachments
                image_name = os.path.basename(image_source)  # Extract only filename
                image_dest = os.path.join(static_images_dir, image_name)

                # Step 4: Copy the image if it exists
                if os.path.exists(image_source):
                    shutil.copy(image_source, image_dest)
                    print(f"Copied: {image_source} -> {image_dest}")

                    # Step 5: Replace the old link in Markdown with the new format
                    markdown_image = f"![Image Description](/images/{image_name.replace(' ', '%20')})"
                    content = content.replace(f"[[{image_rel_path}]]", markdown_image)
                else:
                    print(f"Warning: {image_source} not found")

            # Step 6: Write the updated content back to the markdown file
            with open(filepath, "w", encoding="utf-8") as file:
                file.write(content)

print("Markdown files processed and images copied successfully.")
