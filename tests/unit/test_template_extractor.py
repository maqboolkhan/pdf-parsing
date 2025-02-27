from unittest.mock import patch, MagicMock

import pytest

from chagos.template_extractor import parse_md_by_template


@patch("chagos.template_extractor.MarkdownAnalyzer", return_value=MagicMock())
def test_parse_md_by_template_for_more_than_one_no_of_selectors(mock):
    md_file_path = "md/sample_pdf.md"
    template = {"product_name": {"Beader": 1, "Paragraph": 1}}
    with pytest.raises(ValueError) as err:
        parse_md_by_template(md_file_path, template)

    assert str(err.value) == "Invalid selector object, it should have only one selector"


@patch("chagos.template_extractor.MarkdownAnalyzer", return_value=MagicMock())
def test_parse_md_by_template_for_invalid_selector(mock):
    md_file_path = "md/sample_pdf.md"
    template = {"product_name": {"Beader": 1}, "properties": {"Paragraph": 1}}
    with pytest.raises(ValueError) as err:
        parse_md_by_template(md_file_path, template)

    assert (
        str(err.value)
        == "Invalid selector, it should be one of these: Header, Paragraph, Image_index"
    )


def test_parse_md_by_template_for_uzin_pdf():
    md_file_path = "data/md/uzin_UZIN_PE_355.md"
    template = {
        "product_name": {"Header": 2},
        "properties": {"Paragraph": 9},
        "product_image": {"Image_index": [1, 2]},
    }
    extracted_data = parse_md_by_template(md_file_path, template)
    assert extracted_data["product_name"] == "UZIN PE 355"
    assert (
        extracted_data["properties"]
        == "UZIN PE 355 ist eine schnell trocknende, gebrauchsfertig\neingestellte Grundierung, die vor Spachtelarbeiten auf\nsaugfähigen, mineralischen Untergründen eingesetzt wird.\nDie Grundierung bindet Oberflächenstaub, reduziert die\nSaugfähigkeit des Untergrundes und bietet eine\nhervorragende Haftbasis für nachfolgende Spachtelmassen.\nFür den Innenbereich."
    )
    assert extracted_data["product_image"] == "uzin_UZIN_PE_355.pdf-0-1.png"


def test_parse_md_by_template_for_conti_pdf():
    md_file_path = "data/md/conti_TM_EPFinish.md"
    template = {
        "product_name": {"Header": 1},
        "properties": {"Paragraph": 1},
        "product_image": {"Image_index": [1, 1]},
    }
    extracted_data = parse_md_by_template(md_file_path, template)
    assert extracted_data["product_name"] == "EP FINISH"
    assert (
        extracted_data["properties"]
        == "Wasserverdünnbare, seidenglänzende Zweikomponenten-Be\xad\nschichtung auf Epoxidharzbasis, für hoch beanspruchte Flächen,\nideal einsetzbar als Bodensiegel in Garagen, Fahrzeug- und La\xad\ngerhallen, abriebfest, öl- und benzinbeständig."
    )
    assert extracted_data["product_image"] == "conti_TM_EPFinish.pdf-0-0.png"
