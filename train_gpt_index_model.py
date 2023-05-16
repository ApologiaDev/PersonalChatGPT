
import os
from argparse import ArgumentParser

from dotenv import load_dotenv
from gpt_index import SimpleDirectoryReader, GPTSimpleVectorIndex, LLMPredictor, PromptHelper
from langchain.chat_models import ChatOpenAI


load_dotenv()

os.environ['OPENAI_API_KEY'] = os.getenv('OPENAIKEY')


def construct_index(directory_path, output_index_path):
    max_input_size = 4096
    num_outputs = 512
    max_chunk_overlap = 20
    chunk_size_limit = 600

    prompt_helper = PromptHelper(max_input_size, num_outputs, max_chunk_overlap, chunk_size_limit=chunk_size_limit)

    llm_predictor = LLMPredictor(llm=ChatOpenAI(temperature=0.7, model_name="gpt-3.5-turbo", max_tokens=num_outputs))

    documents = SimpleDirectoryReader(directory_path).load_data()

    index = GPTSimpleVectorIndex(documents, llm_predictor=llm_predictor, prompt_helper=prompt_helper)

    index.save_to_disk(output_index_path)

    return index


def get_argparser():
    argparser = ArgumentParser(description='Train GPT index from documents')
    argparser.add_argument('corpusdir', help='directory of the training data')
    argparser.add_argument('outputpath', help='path of output index (.json)')
    return argparser


if __name__ == '__main__':
    args = get_argparser().parse_args()
    _ = construct_index(args.corpusdir, args.outputpath)
