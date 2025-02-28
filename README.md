# PDF parser
A _Python_ project to extract data from PDF files. This project demonstrate two ways to parse PDF to extract data.
The first way we used is using Templates, in these templates user can define how to pick what from PDFs. The second way we use is
LLM based solution where we send PDFs data into ChatGPT and ask to extract required data.

### Template based solution
Template based solution is fast and more deterministic. However, user will have to define templates for each PDF file layout by brand 
in `templates.json` file present in the `data` folder.

**Assuming** our data (pdf_files) is separated by `brand` folders. Template should look like this

```
<brand_name>: {
        <property_name>: {"<Header | Paragraph>": <index>},
        # for images
        <property_name>: {"Image_index": [<page_num>, <image_index>]}
} 
```
For example
```json
{
    "uzin": {
        "product_name": {"Header": 2},
        "properties": {"Paragraph": 9},
        "product_image": {"Image_index": [1, 2]}
    }
}
```
We first convert PDFs to markdown, these templates heavily relying on our markdown converter (`pymupdf4llm`) and parser (`markdown-analysis`). We noticed that
our markdown parser uses Regex to extract various sections from markdown and it struggles with some files. For example, it could not figure out `properties` 
section for pdf files of `sto` brand.

### LLM based solution
LLM based solution is expensive, little bit slow and not 100% reliable (due to Hallucination). However, here we dont have to write any templates hence it can scale infinitely theoretically!
It works flawlessly and was able to extract data with high accuracy. We tested it with Chatgpt's `gpt-4o-mini`.

### What could be done more?
Alot, I did not write tests for LLM based solution. This solution can easily be **scaled and parallelized** using tools like Apache Airflow.
I could also use OCR technologies to read brand name from PDF files. 

# Running the solution

## Prerequisites
* Python >= 3.13, you can use for example [pyenv](https://github.com/pyenv/pyenv#installation) to manage that
* [Poetry](https://python-poetry.org/docs/#installation)

## Installing dependencies
```bash
make install
```

## Running the project

This project uses ChatGPT `gpt-4o-mini` hence requires API key. Please rename `.env.copy` to `.env` and put OpenAI API key.

```bash
make run-template-solution
```

```bash
make run-llm-solution
```

Both task will create a `json` file in `data/output` folder.

## Tests and checks
To run all tests and checks:
```bash
make check
```

To run all tests (unit and integration):
```bash
make test
```

### unit-tests
To just run unit-tests:
```bash
make unit-test
```

### Auto-formatting
```bash
make auto-format
```

### Linting
```bash
make lint
```

### Check types
```bash
make type-check
```
