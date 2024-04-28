import os
import sys
import dotenv
from dotenv import load_dotenv, dotenv_values
from typing import Tuple
from langchain.prompts.prompt import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain.chains import LLMChain
from third_parties.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import summary_parser, Summary

def ice_break_with(name) -> Tuple[Summary, str]:
  linkedin_url = linkedin_lookup_agent(name=name)
  linkedin_data = scrape_linkedin_profile(linkedin_profile_url=linkedin_url)
  summary_template = """ given a linkedin profile information {information} for a person I want you to create:
  1. Ashort summary
  2. two interesting facts about them
  \n{format_instructions}
  """
  summary_prompt_template = PromptTemplate(input_variables=["information"], template=summary_template, partial_variables={"format_instructions":summary_parser.get_format_instructions()})
  
  llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo")
  #chain = LLMChain(llm=llm, prompt=summary_prompt_template)
  chain = summary_prompt_template | llm | summary_parser
  res: Summary= chain.invoke(input={"information": linkedin_data})
  return res, linkedin_data.get("profile_pic_url")

if __name__== '__main__':
  load_dotenv()
  print("Ice Breaker Enter")
  ice_break_with(name="Rehmana Younis")
  
  
  
  