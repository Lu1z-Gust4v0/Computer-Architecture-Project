class Clock:
    def __init__(self):
        self.ticks = 0
        self.debug = False

    def execution_message(self):
        print(f"Execution finished in {self.ticks} steps")

    def set_debug_mode(self):
        print("The debug mode is active")
        self.debug = True

    def start(self, cpu):
        success = True

        while success:
            if self.debug:
                input()
            success = cpu.step()

            if success:
                self.ticks += 1

        self.execution_message()


clock = Clock()
