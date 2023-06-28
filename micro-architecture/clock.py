class Clock:
    def __init__(self):
        self.ticks = 0

    def execution_message(self):
        print(f"Execution finished in {self.ticks} steps")

    def start(self, cpu, auto=True):
        success = True

        while success:
            if not auto:
                input()
            success = cpu.step()

            if success:
                self.ticks += 1

        self.execution_message()


clock = Clock()
