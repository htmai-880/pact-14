# Contributing

When contributing to this repository, please first discuss the change you wish
to make via issue with the owners of this repository before making a change. 

Please note we have a code of conduct, please follow it in all your interactions with the project.

## Commit messages
Commit messages must match the following format according [conventionalcommits.org](https://www.conventionalcommits.org/en/v1.0.0-beta.4/):
```
[type]([scope]): [short desc]

[long desc]

BREAKING CHANGE: [changes]

Closes [closed issue]
```
Where :

- `[type]` is the type of commit. One of :
  * `feature` &rarr; A new feature
  * `fix` &rarr; A bug fix
  * `docs` &rarr; Documentation only changes
  * `style` &rarr; Changes that do not affect the meaning of the code (white-space, formatting, missing semi-colons, etc)
  * `refactor` &rarr; A code change that neither fixes a bug nor adds a feature
  * `perf` &rarr; A code change that improves performance
  * `test` &rarr; Adding missing tests or correcting existing tests
  * `build` &rarr; Changes that affect the build system or external dependencies (example scopes: gulp, broccoli, npm)
  * `ci` &rarr; Changes to our CI configuration files and scripts (example scopes: Travis, Circle, BrowserStack, SauceLabs)
  * `chore` &rarr; Other changes that don't modify src or test files
  * `revert` &rarr; Reverts a previous commit
- `[scope]` is the scope of the change. Can be one of :
  * Folder
  * File
  * Class
  * Function
- `[short desc]` is the commit message.
- `[long desc]` (optional) To explain more precisely the modifications.
- `[changes]` (optional) Changes in interfaces.
- `[closed issue]` (optional) Which issues this commit close (ex: `#23`).

You can also install [git commit message helper](https://plugins.jetbrains.com/plugin/13477-git-commit-message-helper) to automate the boring stuff.

## Pull Request process
The branch `master` is protected so no one can push into master.
You must create a PR for each change you make.

### External dev

1. Create an issue with the problem clearly explained in this repo.
2. Fork this repo.
3. Create a new branch.
4. Do some changes.
5. Add a PR for this branch into master of this repo.

### Internal dev

1. Clone this repo.
2. Create a new branch.
3. Do some changes.
4. Add a PR for this branch into master.
