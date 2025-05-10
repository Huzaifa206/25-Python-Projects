import requests
from bs4 import BeautifulSoup

def scrape_github_avatar(username):
    # Construct the GitHub profile URL
    url = f"https://github.com/{username}"
    
    try:
        # Send HTTP request with a user-agent
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        response = requests.get(url, headers=headers)
        
        # Check for successful response
        if response.status_code != 200:
            print(f"Failed to fetch profile for '{username}'. Status code: {response.status_code}")
            return None
        
        # Parse HTML
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the avatar image (img tag with class="avatar-user")
        avatar_img = soup.find('img', {'class': 'avatar-user'})
        
        # Fallback: try img with alt containing username
        if not avatar_img:
            avatar_img = soup.find('img', {'alt': f'@{username}'})
        
        if not avatar_img:
            print(f"No avatar found for user '{username}'. Check HTML structure or username validity.")
            return None
        
        # Extract the src attribute (avatar URL)
        avatar_url = avatar_img['src']
        # Ensure full URL
        if avatar_url.startswith('/'):
            avatar_url = f"https://github.com{avatar_url}"
        return avatar_url
    
    except requests.RequestException as e:
        print(f"Error fetching profile for '{username}': {e}")
        return None

def save_avatar_url(username, avatar_url, filename='avatar.txt'):
    if avatar_url:
        with open(filename, 'w') as f:
            f.write(f"Username: {username}\nAvatar URL: {avatar_url}\n")
        print(f"Saved avatar URL to {filename}")
    else:
        print("No avatar URL to save.")

def main():
    # Prompt for GitHub username
    username = input("Enter GitHub username: ").strip()
    
    print(f"Scraping avatar for '{username}'...")
    avatar_url = scrape_github_avatar(username)
    
    if avatar_url:
        print(f"Avatar URL: {avatar_url}")
        save_avatar_url(username, avatar_url)
    else:
        print("Failed to retrieve avatar URL.")

if __name__ == "__main__":
    main()