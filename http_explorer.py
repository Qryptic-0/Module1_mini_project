import httpx
import argparse
from typing import Optional, Dict, Any
import json
import sys

BASE_URL = "https://jsonplaceholder.typicode.com"

class HTTPExplorer:
    """Main class for HTTP Explorer tool"""
    
    def __init__(self):
        self.base_url = BASE_URL
        self.request_count = 0
        self.success_count = 0
        self.method_counts = {}
    
    def _track_request(self, method: str, status_code: int):
        """Track statistics for each request"""
        self.request_count += 1
        if 200 <= status_code < 300:
            self.success_count += 1
        self.method_counts[method] = self.method_counts.get(method, 0) + 1

    def _display_response(self, response: httpx.Response):
        """Helper to print response and track stats"""
        self._track_request(response.request.method, response.status_code)
        print(f"\n[HTTP {response.status_code}]")
        try:
            print(json.dumps(response.json(), indent=2))
        except:
            print(response.text)
        print("-" * 30)

    def list_resources(self, resource_type: str):
        try:
            with httpx.Client() as client:
                response = client.get(f"{self.base_url}/{resource_type}")
                self._display_response(response)
        except Exception as e:
            print(f"Error: {e}")
    
    def get_resource(self, resource_type: str, resource_id: int):
        try:
            with httpx.Client() as client:
                response = client.get(f"{self.base_url}/{resource_type}/{resource_id}")
                self._display_response(response)
        except Exception as e:
            print(f"Error: {e}")
    
    def create_post(self, title: str, body: str, user_id: int):
        data = {"title": title, "body": body, "userId": user_id}
        try:
            with httpx.Client() as client:
                response = client.post(f"{self.base_url}/posts", json=data)
                self._display_response(response)
        except Exception as e:
            print(f"Error: {e}")
    
    def update_post(self, post_id: int, title: Optional[str] = None, 
                    body: Optional[str] = None, partial: bool = True):
        data = {}
        if title: data["title"] = title
        if body: data["body"] = body
        
        method = "PATCH" if partial else "PUT"
        try:
            with httpx.Client() as client:
                if partial:
                    response = client.patch(f"{self.base_url}/posts/{post_id}", json=data)
                else:
                    response = client.put(f"{self.base_url}/posts/{post_id}", json=data)
                self._display_response(response)
        except Exception as e:
            print(f"Error: {e}")
    
    def delete_post(self, post_id: int):
        try:
            with httpx.Client() as client:
                response = client.delete(f"{self.base_url}/posts/{post_id}")
                self._display_response(response)
        except Exception as e:
            print(f"Error: {e}")
    
    def show_stats(self):
        """Display request statistics"""
        print("\n=== Request Statistics ===")
        print(f"Total Requests: {self.request_count}")
        print(f"Successful Requests: {self.success_count}")
        if self.request_count > 0:
            success_rate = (self.success_count / self.request_count) * 100
            print(f"Success Rate: {success_rate:.1f}%")
        print("\nMethods Used:")
        for method, count in self.method_counts.items():
            print(f"  {method}: {count}")

def main():
    parser = argparse.ArgumentParser(
        description="HTTP Methods Explorer - Test HTTP methods with JSONPlaceholder API"
    )
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # List command
    list_p = subparsers.add_parser('list', help='List resources')
    list_p.add_argument('resource_type', choices=['posts', 'users', 'comments'])
    
    # Get command
    get_p = subparsers.add_parser('get', help='Get specific resource')
    get_p.add_argument('resource_type', choices=['posts', 'users', 'comments'])
    get_p.add_argument('resource_id', type=int)
    
    # Create command
    create_p = subparsers.add_parser('create', help='Create a new post')
    create_p.add_argument('--title', required=True)
    create_p.add_argument('--body', required=True)
    create_p.add_argument('--user-id', type=int, required=True)
    
    # Update command
    update_p = subparsers.add_parser('update', help='Update a post')
    update_p.add_argument('post_id', type=int)
    update_p.add_argument('--title')
    update_p.add_argument('--body')
    update_p.add_argument('--full', action='store_false', dest='partial', help='Do a full PUT update')
    update_p.set_defaults(partial=True)
    
    # Delete command
    delete_p = subparsers.add_parser('delete', help='Delete a post')
    delete_p.add_argument('post_id', type=int)
    
    # Stats command
    subparsers.add_parser('stats', help='Show session statistics')

    args = parser.parse_args()
    explorer = HTTPExplorer()
    
    # In a real CLI session, we'd loop or use a file to keep explorer alive.
    # For this assignment, we execute the one command requested.
    if args.command == 'list':
        explorer.list_resources(args.resource_type)
    elif args.command == 'get':
        explorer.get_resource(args.resource_type, args.resource_id)
    elif args.command == 'create':
        explorer.create_post(args.title, args.body, args.user_id)
    elif args.command == 'update':
        explorer.update_post(args.post_id, args.title, args.body, args.partial)
    elif args.command == 'delete':
        explorer.delete_post(args.post_id)
    elif args.command == 'stats':
        # Note: Since the script exits after one command, 
        # stats only show for that single run.
        explorer.show_stats()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
  
