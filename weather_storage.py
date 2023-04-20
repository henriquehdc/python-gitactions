from bs4 import BeautifulSoup
from google.cloud import storage
from google.oauth2 import service_account
import requests

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36(KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}

credentials_dict = {
  "type": "service_account",
  "project_id": "my-project-dataops",
  "private_key_id": "04a5b0ab4e5dc5fdd1977fb2278422123e6aed12",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQDNzWz3hoZzA6dv\ngGPjrItkwQiWVw11KbW+sNpbCRlBFNCc1uXuYAGIXMBjJR/ytsKK2edn/RvLsK5D\nnpVppzADeMFT3BFQ7UNrdQq6QmlZ+IAMYDL9OLQ1EycexWTRpVU8DdY5Ka5ICrQz\nAE3lImm5Nif+oWpe6/zXO8LxVJmIkL4UB7xQLyy4DgqAAYyCTJ+iCTIltE4IQ2wf\ncYLC56FjBPS/wQIkSADCFBkYb1YUsmrqWJ+ZsH6kFYe2DTQGCxqi4gjGm2HXCr94\n94sd2H/T4U6DHadG8OrXv+loe8YQzVLJVHg7p1OzGjau2JZ7fcViSSGcSeoG9D0y\nk6ixxgrdAgMBAAECgf8FF37e+PsOd+sxz/IO/H0oCZWlV5Jz9rbszz5alIjYS7fb\nW4qqobA6fdVFdaVPHC7+pffNL737FguI04HXYeBzjNyCi1ptJWcwKeqF4PowOVNm\nJAlZIqCtFP6bgj0LoXXp+uOVgf8txuHGWcs//MfhCgue72/cdyoBJAVRyiyscpVM\nW65V2ZkfFtIDO30SfSlTMecaMcXbwjh2mFktzmmZaFexCNWiQHmsb+8rX1j7vkLj\nmXoS0XXzt9CsjhMjCXnrMhjZR4xsU9Kabjgpi2P7b7JC3Dl/lPFryNPQYPEvaF/5\nFdVq38jf1gjFcHEtpcSWuOqA3rCso0Ojt3kM+MMCgYEA8yAulxennxvyj7KRT8EE\n7FV7QXUsIyi8+zCrA/jC1L9DGFvOH8iKNE2SulDdXZQvcDIwMHJCRp9tFhyoFIua\nMq8574BAyxZcr5iMcZmHnad8v1PMogHxElEVlzFfnc8g1fGvsffnn2s5XphFHhdq\n17cdhKmk+469Nf6LZNXPUv8CgYEA2LNJ3nnayHIDFT0E5iXSQnN45LvsXUq33Mwo\nbloTYEbeMksL34/ttYtswAsgOAKlKWXv0Bes4NsVMOjDlpNS4bo23giHsGGmbJZ+\nSbsb16sr2mU8zB44LskPorl5cXGxTme3qnYXN6PcK8ZICKUIMsYyBLY+uORVjjtY\nCQjcTiMCgYEA7nddW1OXVMebxfhW8QwYoRpDF/Quw5mcqyCUTQP9TaD/1W+OoLwZ\nWq3PwjG4vqWvVfPUMmCPwydyXuLitawsJZSbVd/NLaWUaaNN9cqqKydxg1RVfX48\nD0Q60h5ac7YKte4l74CBzmrkTXU7LgW4BTeVm16t9ROPYNt3rALPJM8CgYEAsVe5\nAmtzE0vLHhx73+Xf9yYNMBRjUc4OPpKOHBF3fflBaqNkKifeAA8Ehv4T9gKkLAcS\nhZh6kOJ6qzYyqw4SbE07DeapNT4VNxTKcYjBNnUNRIRJhzrL++3r794edyr2UhYr\nh0NxqMVfMCvrU7fLx9HPqW+EUUf8hJQobexkb0UCgYBZvKabBf5KXQI60NmWPtjx\nHCspUoiEDSP0k1UD6FlRCAQcJGWPK8/zCqxS1X3VYrnuV/9a2sLgx8de7U60HpEg\nvf1JMsZO8sj8dfibATget7fqUNKRajxQ3JrILJGQtX8fwzdg1pxoNnHqdn65s5xK\nQI7px2LHBSV8xu+N2dpUUQ==\n-----END PRIVATE KEY-----\n",
  "client_email": "968503817904-compute@developer.gserviceaccount.com",
  "client_id": "100789134554038510887",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/968503817904-compute%40developer.gserviceaccount.com"
}

try:
    res = requests.get(f'https://www.google.com/search?q=SaoPauloCidade&oq=SaoPauloCidade&aqs=chrome.0.35i39l2j0l4j46j69i60.6128j1j7&sourceid=chrome&ie=UTF-8', headers=headers)
    print("Loading...")
    
    soup = BeautifulSoup(res.text, 'html.parser')
    info = soup.find_all("span", class_="LrzXr kno-fv wHYlTd z8gr9e")[0].getText()
    print(info)

    credentials = service_account.Credentials.from_service_account_info(credentials_dict)
    storage_client = storage.Client(credentials=credentials)
    bucket = storage_client.get_bucket('dalla_dataops')
    blob = bucket.blob('weather_info_actions.txt')

    blob.upload_from_string(info + '\n')
    print('File uploaded.')

    print("Finished.")
   
except Exception as ex:
    print(ex)
