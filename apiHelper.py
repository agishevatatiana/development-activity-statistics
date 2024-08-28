import requests
import datetime

import os
from dotenv import load_dotenv

load_dotenv()

class APIHelper:
  __tk = os.getenv('tk')

  __headers = {}
  
  if __tk is not None:
    __headers = {'Authorization': f'Bearer {__tk}'}


  def __parse_issues_total_count_data(self, repo: str, type: str, status: str):
    end = datetime.datetime.today()
    end_str = str(datetime.datetime.today()).split()[0]

    start = end - datetime.timedelta(days=30)
    start_str = str(start).split()[0]

    try:
      issues = requests.get(f'https://api.github.com/search/issues?q=repo:{repo} type:{type} is:{status} created:{start_str}..{end_str}', headers=self.__headers)
      if issues.status_code != 200:
        raise Exception('Error')
      else: 
        return issues.json()['total_count']
    except:
      return 'Error: API error with issues request'

  
  def __get_pulse_string(self, repo: str):
    try:
      pulse = requests.get(f'https://github.com/{repo}/pulse_diffstat_summary?period=monthly', headers=self.__headers)
      if pulse.status_code != 200:
        raise Exception('Error')
      else:
        return pulse.text.replace('\n','')
    except:
      return 'Error: API error with pulse request'

  def __parse_data_from_pulse(self, repo: str, find_str: str, range_start: int, range_end: int):
    pulse_str = self.__get_pulse_string(repo)
    if 'Error' in pulse_str:
      return pulse_str
    else:     
      index = pulse_str.find(find_str)
      if index != -1:
        for i in range(range_start,range_end,-1):
          data = pulse_str[index - i:index-range_end].replace(',','')
          if data.isnumeric():
            return int(data)


  def get_github_api_repo_activity_data(self, repo: str):
    if repo == '':
      return 0
    
    return {
      'unique_authors': self.__parse_data_from_pulse(repo,'authors',5,1),
      'commits_to_main': self.__parse_data_from_pulse(repo,'</span> commits</strong> to main',8,0),
      'commits_to_all': self.__parse_data_from_pulse(repo,'</span> commits</strong>  to all branches',8,0),
      'files_changed': self.__parse_data_from_pulse(repo,'files</strong>  have changed',10,1),
      'closed_issues': self.__parse_issues_total_count_data(repo, 'issue', 'closed'),
      'open_issues': self.__parse_issues_total_count_data(repo, 'issue', 'open'),
      'merged_pr': self.__parse_issues_total_count_data(repo, 'pr', 'merged'),
      'open_pr': self.__parse_issues_total_count_data(repo, 'pr', 'open')
    }
    






