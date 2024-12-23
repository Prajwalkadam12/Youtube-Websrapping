import csv
from googleapiclient.discovery import build
import time

# Set up your YouTube API key here
API_KEY = 'AIzaSyA_MaHgS06E4Zsu83s6miB2pvne3kubeLs'


# Function to fetch top 500 videos based on genre
def fetch_videos_by_genre(genre, max_results=500):
    youtube = build('youtube', 'v3', developerKey=API_KEY)

    video_data = []
    next_page_token = None
    batch_size = 50  # Maximum videos per API call

    print(f"Fetching videos for genre: {genre}...")

    while len(video_data) < max_results:
        # Fetch video IDs using the search endpoint
        search_request = youtube.search().list(
            q=genre,
            part="id,snippet",
            type="video",
            maxResults=batch_size,
            pageToken=next_page_token
        )
        search_response = search_request.execute()

        video_ids = [item["id"]["videoId"] for item in search_response["items"]]

        # Fetch video details in a batch
        video_request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=",".join(video_ids)
        )
        video_response = video_request.execute()

        for video in video_response["items"]:
            # Extracting required data
            video_data.append({
                "Video URL": f"https://www.youtube.com/watch?v={video['id']}",
                "Title": video["snippet"]["title"],
                "Description": video["snippet"]["description"],
                "Channel Title": video["snippet"]["channelTitle"],
                "Keyword Tags": video["snippet"].get("tags", "No tags available"),
                "Video Category": genre,
                "Published At": video["snippet"]["publishedAt"],
                "Video Duration": video["contentDetails"]["duration"],
                "View Count": video["statistics"].get("viewCount", 0),
                "Comment Count": video["statistics"].get("commentCount", 0),
                "Captions Available": video["contentDetails"].get("caption", "false") == "true",
                "Location of Recording": video["snippet"].get("location", "Not available")
            })

        next_page_token = search_response.get("nextPageToken")
        if not next_page_token:
            break

        print(f"Fetched {len(video_data)} videos so far...")
        time.sleep(1)  # Add delay to avoid hitting rate limits

    return video_data[:max_results]  # Return only the top 500 videos


# Function to save data to a CSV file
def save_to_csv(videos, filename="top_videos.csv"):
    if videos:
        keys = videos[0].keys()
        with open(filename, mode="w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=keys)
            writer.writeheader()
            writer.writerows(videos)
        print(f"Data saved to {filename}")
    else:
        print("No data to save.")


# Main function
def main():
    genre = input("Enter the genre to fetch videos for: ")
    max_results = 500

    # Fetch videos and save to CSV
    videos = fetch_videos_by_genre(genre, max_results)
    save_to_csv(videos)


if __name__ == "__main__":
    main()
