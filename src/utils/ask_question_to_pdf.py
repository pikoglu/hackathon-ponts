from io import StringIO
import os
import fitz
import openai
from dotenv import load_dotenv
from nltk.tokenize import sent_tokenize

load_dotenv()


def open_file(filepath):
    with open(filepath, "r", encoding="utf-8") as infile:
        return infile.read()


openai.api_key = os.getenv("OPENAI_API_KEY")
openai.organization = os.getenv("OPENAI_ORGANIZATION")


def read_pdf(filename):
    context = ""

    # Open the PDF file
    with fitz.open(filename) as pdf_file:
        # Get the number of pages in the PDF file
        num_pages = pdf_file.page_count

        # Loop through each page in the PDF file
        for page_num in range(num_pages):
            # Get the current page
            page = pdf_file[page_num]

            # Get the text from the current page
            page_text = page.get_text().replace("\n", "")

            # Append the text to context
            context += page_text
    return context


def split_text(text, chunk_size=5000):
    """
    Splits the given text into chunks of approximately the specified chunk size.

    Args:
    text (str): The text to split.

    chunk_size (int): The desired size of each chunk (in characters).

    Returns:
    List[str]: A list of chunks, each of approximately the specified chunk size.
    """

    chunks = []
    current_chunk = StringIO()
    current_size = 0
    sentences = sent_tokenize(text)
    for sentence in sentences:
        sentence_size = len(sentence)
        if sentence_size > chunk_size:
            while sentence_size > chunk_size:
                chunk = sentence[:chunk_size]
                chunks.append(chunk)
                sentence = sentence[chunk_size:]
                sentence_size -= chunk_size
                current_chunk = StringIO()
                current_size = 0
        if current_size + sentence_size < chunk_size:
            current_chunk.write(sentence)
            current_size += sentence_size
        else:
            chunks.append(current_chunk.getvalue())
            current_chunk = StringIO()
            current_chunk.write(sentence)
            current_size = sentence_size
    if current_chunk:
        chunks.append(current_chunk.getvalue())
    return chunks


filename = os.path.join(os.path.dirname(__file__), "filename.pdf")
document = read_pdf(filename)
chunks = split_text(document)


# fonction gpt3_completion modifiée pour prendre en compte le contexte
def gpt3_completion(prompt, historique, max_tokens=500, temperature=0.2):
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt="En t'aidant de cet historique : ".join(historique)
        + " réagis en français et de manière concise à : "
        + prompt,
        max_tokens=max_tokens,
        temperature=temperature,
    )

    completion_text = response.choices[0].text

    return completion_text


text = "Ancien élève de la promotion 1979 de l'École polytechnique1, Luc Dormieux intègre le Corps des ponts et chaussées et obtient un doctorat ès sciences physiques en mécanique à l'École nationale des ponts et chaussées en 1989, puis une habilitation à diriger des recherches lui permettant d'être directeur de thèse2. Il est professeur chargé de cours à l'École polytechnique, maître de conférences à l'École nationale des ponts et chaussées et directeur de recherche en mécanique des milieux continus au Laboratoire Navier3,4, au LMSGC5 et au Laboratoire central des ponts et chaussées, qui font partie intégrante de l'École nationale des ponts et chaussées."


def ask_question_to_pdf(question, historique):
    prompt = text + " " + question

    response = gpt3_completion(prompt, historique)

    return response
