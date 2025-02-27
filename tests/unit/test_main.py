from chagos.main import get_pdf_files_by_folder


def test_if_get_pdf_files_returning_all_pdfs():
    pdf_files_by_folder = get_pdf_files_by_folder("data/pdf_files/")
    no_of_pdf_files = sum(
        [len(pdf_files_by_folder[folder]) for folder in pdf_files_by_folder]
    )
    assert no_of_pdf_files == 15
