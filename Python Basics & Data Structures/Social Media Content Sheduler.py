posts = []
historical_engagement = {
    "Twitter": {"08:00-10:00": 85, "17:00-19:00": 92},
    "LinkedIn": {"14:00-16:00": 78},
    "Instagram":{"20:00-00:00": 95, "00:00-3:00":70}
}

def add_post(content, platform, time, tags):
    posts.append({"content": content, "platform": platform, "time": time, "tags": tags})

def check_similarity():
    for i in range(len(posts)):
        for j in range(i + 1, len(posts)):
            if posts[i]["content"] == posts[j]["content"]:
                print("WARNING: Similar content detected:")
                print("-",posts[i]['content'],"-",posts[i]['time'])
                print("-",posts[j]['content'],"-",posts[j]['time'])
                print("Recommendation: Reschedule at least 48 hours apart")

def display_schedule():
    print("\nScheduled Posts:")
    for post in posts:
        print("-", post['content'], "-" , post['platform'], "-", post['time'])

def user_input():
    while True:
        print("\nSocial Media Content Scheduler: \n 1) Add Post  2) Check Similarity  3) Display Schedule  4) Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            content = input("Enter post content: ")
            platform = input("Enter platform (Twitter/LinkedIn/Instagram): ")
            time = input("Enter preferred posting time (YYYY-MM-DD HH:MM): ")
            tags = input("Enter tags (comma-separated): ").split(",")
            add_post(content, platform, time, tags)
        elif choice == "2":
            check_similarity()
        elif choice == "3":
            display_schedule()
        elif choice == "4":
            break
        else:
            print("Invalid choice! Please try again.")
user_input()