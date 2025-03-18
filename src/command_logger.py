class CommandLogger:
    def __init__(self):
        self.command_history = []

    def log_command(self, command_sequence):
        """
        Logs a command or sequence of commands.
        """
        self.command_history.append(command_sequence)
        print(f"Logged command: {command_sequence}")

    def get_last_command(self):
        """
        Returns the last executed command sequence.
        """
        if self.command_history:
            return self.command_history[-1]
        return None

    def get_history(self):
        """
        Returns the full command history.
        """
        return self.command_history

    def clear_last_command(self):
        """
        Removes the last command from history.
        """
        if self.command_history:
            self.command_history.pop()
            print("Last command removed from history.")
