# Software Engineering Exercise

Design and implement a simplified version of a social network application where users can create new posts, follow/unfollow another user and is able to see the 10 most recent posts in the user's feed.

Each user has a userId, each post has a postId and belongs to a user.

Your design should support the following methods:

- `compose(post)`: Compose a new post.
- `getFeed(userId)`: Retrieve the 10 most recent posts in the user's news feed. Each item in the news feed must be posted by users who the user followed or by the user herself. Posts must be ordered from most recent to least recent.
- `follow(followerId, followeeId)`: Follower starts following a followee.
- `unfollow(followerId, followeeId)`: Follower stops following a followee.

## Task:

- Write the application that implements the described behaviour;
- Write a small (REST) web service that exposes these operations.

You can use any language or framework/library of your choice.

## Submission:

Create a new [branch](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging) and add your [pull requests](https://help.github.com/articles/creating-a-pull-request/) for your submission. While working on the exercise feel free to commit as much as you like.

Please make sure to document how to run your exercise as well as any other information or consideration you think is relevant.

When you are ready to submit, open a pull request against the main branch. In your pull request, make sure to specify how to run your exercise as well as any other information you think is relevant.
