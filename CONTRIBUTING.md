# How to contribute
* This is a generic document for all my repositories. Please adapt the URLs and repository names for this repository as needed.

## Getting Started

* (Optional) We adopt [Git Flow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow). Most feature branches are pushed to the repository and deleted when merged to *develop* branch.
* (**Important**): Submit pull requests to the *develop* branch or *feature/* branches
* Use *GitHub Issues* for feature requests and bug reports. Include as much information as possible while reporting bugs.  


## Contributing (Step-by-step)

1. [Fork the repo](http://help.github.com/fork-a-repo) and clone it to your local computer, and set up the upstream remote:

        git clone git://github.com/YourGitHubUserName/this-repository-name.git
        git remote add upstream
        https://github.com/MyGitHubName/this-repository-name.git

* MyGitHubName may be *dermatologist* or *E-Health* 

2. Checkout out a new local branch based on your master and update it to the latest (TRUNK-123 is the branch name, You can name it whatever you want. Try to give it a meaningful name. If you are fixing an issue, please include the issue #).

        git checkout -b TRUNK-123 develop
        git clean -df
        git pull --rebase upstream develop

 > Please keep your code clean. If you find another bug, you want to fix while being in a new branch, please fix it in a separated branch instead.

3. Push the branch to your fork. Treat it as a backup.

        git push origin TRUNK-123

4. Code

  * Adhere to common conventions you see in the existing code.
  * Include tests as much as possible, and ensure they pass.

5. Commit to your branch

         git commit -m "TRUNK-123: Put change summary here (can be a ticket title)"

  **NEVER leave the commit message blank!** Provide a detailed, clear, and complete description of your commit!

7. Update your branch to the latest code.
  
        git pull --rebase upstream develop

8. **Important** If you have made many commits, please squash them into atomic units of work. (Most Git GUIs such as sourcetree and smartgit offer a squash option)

        git checkout develop
        git pull --rebase upstream develop
        git checkout TRUNK-123
        git rebase -i develop

  (**Optionally**) you can create a new branch for PR and do the squash commit on the new branch:
  
        git checkout develop
        git pull --rebase upstream develop
        git checkout -b TRUNK-123-PR TRUNK-123
        git rebase -i develop
  

  Push changes to your fork (For the second option above *force* (-f) is not required):

        git push -f

8. Issue a Pull Request

  In order to make a pull request,
  * Navigate to the repository you just pushed to (e.g. https://github.com/your-user-name/repository-name)
  * Click "Pull Request".
  * Write your branch name (TRUNK-123-PR if you adopted option 2) in the branch field (this is filled with "master" by default)
  * **Choose the *develop* branch of the main repository (default is master)**
  * Click "Update Commit Range".
  * Ensure the changesets you introduced are included in the "Commits" tab.
  * Ensure that the "Files Changed" incorporate all of your changes.
  * Fill in some details about your potential patch including a meaningful title.
  * Click "Send pull request".

  Thanks for that -- we'll get to your pull request ASAP. We love pull requests!

## Feedback

   If you need to contact me, see my contact details on my profile page.
