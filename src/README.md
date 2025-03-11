## To do:
# Speed Control: 
    1. PID without encoder?
# Trajectory Planning: 
    1. Cable Driven Parallel Robots (CDPR)
# Workflow
    0. clone the repo
    1. Create a new branch <dev-name> from the dev branch
        ```
        git checkout dev
        git pull origin dev  # Ensure you have the latest changes
        git checkout -b <dev-name>  # Create and switch to a new branch
        ```
    2. Make changes and commit
        ```
        git add .
        git commit -m "Description of changes"
        ```
    3. Push the new branch to remote
        ```sh
        git push -u origin <dev-name>
        ```
    4. Open a Pull Request (PR) to merge into the `dev` branch
    5. After review and merge:
        - Switch back to `dev` and pull the latest updates:
            ```
            git checkout dev
            git pull origin dev
            ```
        - Delete the feature branch:
            ```
            git branch -d <dev-name>
            git push origin --delete <dev-name>  # Remove remote branch
            ```

