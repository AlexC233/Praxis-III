# How to Github 

[github desktop](https://desktop.github.com/download/)
## Clone repo
```
git clone https://github.com/AlexC233/Praxis-III.git
```

## Editing code
Pull latest changes from `dev`
```
git checkout dev
git pull origin dev
```

Commit and push
```
git add .
git commit -m "Description of changes"
git push -u origin <dev-name>
```

Open pull request
- go to your branch 
- click "Pull Request" 
- "New Pull Request"

## Branch manipulation 
Create a new branch `<dev-name>` from the dev branch
```
git checkout dev
git pull origin dev  # Ensure you have the latest changes
git checkout -b <dev-name>  # Create and switch to a new branch
```

Delete branches
```
git branch -d <dev-name>
git push origin --delete <dev-name> 
```
