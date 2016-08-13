import random


class MobberManager(object):
    def __init__(self, randomize=False, drive_after_navigating=True):
        self.current_driver_index = 0
        self.next_driver_index = 1
        self.navigator_index = self.next_driver_index
        self.mobber_list = []
        self.mobber_list_change_callbacks = []
        self.randomize = randomize
        self.drive_after_navigating = drive_after_navigating

    def mobber_count(self):
        return self.mobber_list.__len__()

    def add_mobber(self, mobber_name):
        clean_mobber_name = str(mobber_name).strip()
        if clean_mobber_name != "" and not self.mobber_list.__contains__(clean_mobber_name):
            self.mobber_list.append(mobber_name)
            self.fire_mobber_list_change_callbacks()

    def get_mobbers(self):
        return self.mobber_list

    def remove_mobber(self, remove_mobber_index):
        if self.mobber_count() == 0:
            return
        del self.mobber_list[remove_mobber_index]
        self.fire_mobber_list_change_callbacks()

    def move_mobber_up(self, swap_index):
        if self.mobber_count() == 0: return
        destination_index = swap_index - 1
        self.mobber_list[swap_index], self.mobber_list[destination_index] = self.mobber_list[destination_index], \
                                                                            self.mobber_list[swap_index]
        self.fire_mobber_list_change_callbacks()

    def move_mobber_down(self, swap_index):
        if self.mobber_count() == 0: return
        destination_index = (swap_index + 1) % self.mobber_list.__len__()
        self.mobber_list[swap_index], self.mobber_list[destination_index] = self.mobber_list[destination_index], \
                                                                            self.mobber_list[swap_index]
        self.fire_mobber_list_change_callbacks()

    def subscribe_to_mobber_list_change(self, mobber_list_change_callback):
        self.mobber_list_change_callbacks.append(mobber_list_change_callback)
        self.fire_mobber_list_change_callbacks()

    def fire_mobber_list_change_callbacks(self):
        self.update_next_driver_index()
        for mobber_list_change_callback in self.mobber_list_change_callbacks:
            if mobber_list_change_callback:
                mobber_list_change_callback(self.mobber_list, self.current_driver_index, self.next_driver_index, self.navigator_index)

    def clear(self):
        self.mobber_list = []
        self.fire_mobber_list_change_callbacks()

    def switch_next_driver(self):
        mobber_count = self.mobber_list.__len__()
        if mobber_count > 0:
            if self.randomize and mobber_count > 2:
                self.current_driver_index = self.next_driver_index
            else:
                self.current_driver_index = (self.current_driver_index + 1) % mobber_count
        self.fire_mobber_list_change_callbacks()

    def update_next_driver_index(self):
        mobber_count = self.mobber_list.__len__()
        if mobber_count > 0:
            if self.randomize and mobber_count > 2:
                self.next_driver_index = int(random.uniform(0, mobber_count))
                while self.current_driver_index == self.next_driver_index:
                    self.next_driver_index = int(random.uniform(0, mobber_count))
            else:
                self.current_driver_index = self.current_driver_index % mobber_count
                self.next_driver_index = (self.current_driver_index + 1) % mobber_count

            if self.drive_after_navigating:
                self.navigator_index = self.next_driver_index
            else:
                self.navigator_index = (self.current_driver_index + mobber_count - 1) % mobber_count
        else:
            self.current_driver_index = 0
            self.next_driver_index = 1
            self.navigator_index = self.next_driver_index

    def rewind_driver(self):
        mobber_count = self.mobber_list.__len__()
        if mobber_count > 0:
            self.current_driver_index = (self.current_driver_index - 1)
            if self.current_driver_index < 0:
                self.current_driver_index = mobber_count - 1
        self.update_next_driver_index()
        self.fire_mobber_list_change_callbacks()

    def set_mobber_list(self, mobber_list):
        if self.mobber_list != mobber_list:
            self.mobber_list = []
            for mobber_name in mobber_list:
                clean_mobber_name = str(mobber_name).strip()
                if clean_mobber_name != "" and not self.mobber_list.__contains__(clean_mobber_name):
                    self.mobber_list.append(mobber_name)
            self.fire_mobber_list_change_callbacks()

