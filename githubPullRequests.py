import requests
import datetime

print("List PRs for how many days?: ")
days_input=input()
print("Please enter your github API token: ")
github_api_token=input()
print(days_input)

pageNum=1
stopFetchingPR=False
headers = {'Authorization': 'token ' + github_api_token}

print("\n\n\nFrom: devops-team@sailpoint.com")
print("To: scrum-master@sailpoint.com")
print("Subject: List of PRs in last " + days_input + " days\n\n\n")
while True:

    url="https://api.github.com/repos/kubernetes/kubernetes/pulls?state=all&per_page=100&sort=created&direction=desc&page=%d" % (pageNum)
    
    response = requests.get(url, headers=headers)

    pullRequests = response.json()

    for idx in range(len(pullRequests)):
        pr_created_at = datetime.datetime.strptime(pullRequests[idx]["created_at"], "%Y-%m-%dT%H:%M:%SZ").date()

        current_date = datetime.datetime.now().date()
        num_days_ago_date = current_date - datetime.timedelta(days=int(days_input))

        if pr_created_at >= num_days_ago_date:
            print("\nPR # " + str(idx))
            print("==============================")
            print("URL: " + pullRequests[idx]["url"])
            print("Title: " + pullRequests[idx]["title"])
            print("Created On: " + pullRequests[idx]["created_at"])
            print("State: " + pullRequests[idx]["state"])
        else:
            stopFetchingPR=True
            break
    if stopFetchingPR:
        print("=======================================")
        print("\n\nFINISHED GENERATING PR REPORT\n")
        print("=======================================")
        break
    pageNum=pageNum+1