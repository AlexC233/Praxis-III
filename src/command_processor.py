import constant
from controller import Controller
from command_logger import CommandLogger

class CommandProcessor:
    def __init__(self):
        self.controller = Controller()
        self.logger = CommandLogger()
        self.command_map = {
            'w': self.controller.forward,
            's': self.controller.backward,
            'a': self.controller.left,
            'd': self.controller.right,
            'u': self.controller.up,
            'n': self.controller.down
        }

    def execute_command(self, command_sequence):
        """
        Executes a sequence of commands if valid.
        """
        if not self.is_valid_sequence(command_sequence):
            print("Invalid command sequence.")
            return

        print(f"Executing sequence: {command_sequence}")
        for command in command_sequence:
            if command in self.command_map:
                self.command_map[command]()
        
        self.logger.log_command(command_sequence)
    
    def is_valid_sequence(self, command_sequence):
        """
        Checks if all commands in the sequence are valid.
        """
        return all(cmd in self.command_map for cmd in command_sequence)
    
    def reverse_last_command(self):
        """
        Reverses the last executed command sequence and removes it from history.
        """
        last_command = self.logger.get_last_command()
        if last_command:
            reverse_sequence = ''.join(self.get_reverse_command(cmd) for cmd in reversed(last_command))
            print(f"Reversing sequence: {reverse_sequence}")
            for command in reverse_sequence:
                if command in self.command_map:
                    self.command_map[command]()
            self.logger.clear_last_command()  # Remove last command from history
        else:
            print("No command to reverse.")
    
    def get_reverse_command(self, command):
        """
        Returns the reverse of a given command.
        """
        reverse_map = {
            'w': 's', 's': 'w', 'a': 'd', 'd': 'a', 'u': 'n', 'n': 'u'
        }
        return reverse_map.get(command, command)
