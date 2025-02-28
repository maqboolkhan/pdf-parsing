import json
import os
import sys
import click
import pymupdf4llm
import dotenv
from openai import OpenAI

from chagos.template_extractor import parse_md_by_template

dotenv.load_dotenv()

def get_pdf_files_by_folder(pdfs_data_dir: str) -> dict[str, list[str]]:
    pdfs_object: dict[str, list[str]] = {}
    for root, dirs, files in os.walk(pdfs_data_dir):
        for file in files:
            if file.endswith(".pdf"):
                folder = root.split("/")[-1]
                if folder not in pdfs_object:
                    pdfs_object[folder] = []
                pdf_path = os.path.join(root, file)
                pdfs_object[folder].append(pdf_path)
    return pdfs_object


def convert_pdf_to_markdown(pdf_path: str, md_path: str, md_image_path: str):
    md = pymupdf4llm.to_markdown(pdf_path, write_images=True, image_path=md_image_path)
    with open(md_path, "w") as f:
        f.write(md)


@click.command()
@click.option(
    "--input_folder",
    default="data/pdf_files/",
    help="Folder containing sub folders of pdfs to parse.",
)
@click.option(
    "--output_folder",
    default="data/output/",
    help="Path where output json file should be generated.",
)
@click.option(
    "--solution_type",
    default="template",
    type=click.Choice(['template', 'llm'])
)
@click.option(
    "--templates_path",
    default="data/templates.json",
    help="Path to JSON file defining templates",
)
def main(input_folder, output_folder, solution_type, templates_path) -> int:
    extracted_data = []

    if solution_type == "template":
        with open(templates_path) as templates_fp:
            templates = json.load(templates_fp)

    client = OpenAI(
        api_key=os.environ.get("OPENAI_API_KEY"),  # This is the default and can be omitted
    )
    with open("data/prompt") as prompt_fp:
        prompt = prompt_fp.read()

    pdf_files_path = get_pdf_files_by_folder(input_folder)
    for pdf_file_folder in pdf_files_path:
        for pdf_file_path in pdf_files_path[pdf_file_folder]:
            parsed_data = {}
            path_components = pdf_file_path.split("/")
            brand = path_components[2]
            file_name = path_components[-1][:-4]
            md_file_path = f"data/md/{brand}_{file_name}.md"
            convert_pdf_to_markdown(pdf_file_path, md_file_path, "data/md/images")

            if solution_type == "template":
                parsed_data = parse_md_by_template(md_file_path, templates[brand])
            if solution_type == "llm":
                with open(md_file_path) as f:
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=
                        [
                            {
                                "role": "user",
                                "content": prompt.replace("{product_markdown}", f.read())
                            }
                        ],
                        response_format={"type": "json_object"}
                    )
                    parsed_data = json.loads(response.choices[0].message.content)
                    parsed_data["product_image"] = "" # Let it be

            parsed_data["brand"] = brand
            parsed_data[
                "product_image"
            ] = f"data/md/images/{parsed_data["product_image"]}"
            extracted_data.append(parsed_data)

    output_filename = "tamplate_based_output" if solution_type == "template" else "llm_based_output"
    with open(f"{output_folder}/{output_filename}.json", "w") as output_folder_fp:
        json.dump(extracted_data, output_folder_fp, indent=2)
    print("Done")
    return 0


if __name__ == "__main__":
    sys.exit(main())
