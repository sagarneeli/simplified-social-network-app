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

We utilize Github and [pull requests](https://help.github.com/articles/creating-a-pull-request/) for collaborating on code. Create a new [branch](https://git-scm.com/book/en/v2/Git-Branching-Basic-Branching-and-Merging) for your submission. While working on the exercise feel free to commit as much as you like.

You have 7 days from the time that you receive the take-home to submit. Please do not spend more than three or four hours on the project and feel free to submit your solution early if finished ahead of the 7-day deadline.
Please make sure to document how to run your exercise as well as any other information or consideration you think is relevant.

When you are ready to submit, open a pull request against the master branch. In your pull request, make sure to specify how to run your exercise as well as any other information you think is relevant.

If your submission passes review, your next session will be a review of the code you submit for this exercise.
