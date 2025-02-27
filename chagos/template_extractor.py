from mrkdwn_analysis import MarkdownAnalyzer
from typing_extensions import Union


def parse_md_by_template(
    md_file_path: str, template: dict[str, dict[str, Union[int, list[int]]]]
) -> dict[str, str]:
    analyzer = MarkdownAnalyzer(md_file_path)
    headings = analyzer.identify_headers()
    paragraphs = analyzer.identify_paragraphs()
    parsed_markdowns = {}
    parsed_markdowns.update(headings)
    parsed_markdowns.update(paragraphs)
    available_selectors = ["Header", "Paragraph", "Image_index"]
    extracted_data = {}

    for entity_to_extract in template:
        value = ""
        selector_object = template[entity_to_extract]
        if len(selector_object.keys()) > 1:
            raise ValueError(
                "Invalid selector object, it should have only one selector"
            )
        selector = list(selector_object.keys())[0]
        if selector not in available_selectors:
            raise ValueError(
                "Invalid selector, it should be one of these: Header, Paragraph, Image_index"
            )

        if selector == "Header":
            header_obj = parsed_markdowns[selector][selector_object[selector] - 1]
            value = header_obj["text"]
        elif selector == "Paragraph":
            value = parsed_markdowns[selector][selector_object[selector] - 1]
        elif selector == "Image_index":
            file_name = md_file_path.split("/")[-1]
            indexes = template[entity_to_extract][selector]
            value = f"{file_name[:-3]}.pdf-{indexes[0]-1}-{indexes[1]-1}.png"

        extracted_data[entity_to_extract] = value
    return extracted_data
