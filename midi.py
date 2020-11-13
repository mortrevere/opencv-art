import time
import rtmidi.midiutil
import rtmidi
import mido

global_filter_addr_to_parameter_index = {
    16: 0,
    17: 1,
    18: 2,
    19: 3,
    20: 4,
    21: 5,
    22: 6,
    23: 7,
}
midi_addr_to_parameter_index = {}

controls = {58: "previous", 59: "next", 60: "set"}
modifiers = {"global_filter": 46}
toggle_buttons_list = list(range(32, 72))
trigger_buttons_list = [58, 59]

# trigger and toggle lists are exclusive
for bt in trigger_buttons_list:
    toggle_buttons_list.remove(bt)


class MidiController:
    def __init__(self, orchestrator):
        self.o = orchestrator
        midiin = rtmidi.MidiIn(
            rtmidi.midiutil.get_api_from_environment(rtmidi.API_UNSPECIFIED)
        )
        ports = midiin.get_ports()
        for i in range(len(ports)):
            if "nanoKONTROL" in ports[i]:
                self.port_id = i
                print("Found MIDI Mix at port", self.port_id)

        try:
            self.midiin, self.port_name = rtmidi.midiutil.open_midiinput(self.port_id)
            self.midiout, _ = rtmidi.midiutil.open_midioutput(self.port_id)
        except:
            print("No midi.")
            return

        self.buttons = [ToggleButton(self.midiout, i) for i in toggle_buttons_list]
        self.buttons += [TriggerButton(self.midiout, i) for i in trigger_buttons_list]

        # flash all buttons
        # pretty and also checks on assignations
        for button in self.buttons:
            button.on()
            time.sleep(0.02)
        for button in self.buttons:
            button.off()
            time.sleep(0.02)

        # buttons will be accessed by MIDI id when handling MIDI input
        self.buttons_by_id = {}
        for button in self.buttons:
            self.buttons_by_id[button.id] = button

        print("Attaching MIDI input callback handler to", self.port_name)
        print(self.o.current_filter)
        self.midiin.set_callback(MidiInputHandler(self.port_name, self))


class MidiInputHandler:
    def __init__(self, port, controller):

        self.port = port
        self._wallclock = time.time()
        self.buttons_by_id = controller.buttons_by_id
        self.o = controller.o
        self.filter = self.o.current_filter

    def normalize(self, value):
        return value / 127

    def __call__(self, event, data=None):
        message, deltatime = event
        self._wallclock += deltatime
        print("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        # self.o.send_ui_info("[%s] @%0.6f %r" % (self.port, self._wallclock, message))
        addr = message[1]
        value = self.normalize(message[2])  # 0-127 -> 0-1

        if self.buttons_by_id.get(addr):
            if value:  # note ON
                if isinstance(self.buttons_by_id.get(addr), ToggleButton):
                    self.buttons_by_id[addr].toggle()
                if isinstance(self.buttons_by_id.get(addr), TriggerButton):
                    self.buttons_by_id[addr].on()

                action = controls.get(addr)
                print(addr, action)
                if action == "next":
                    self.o.next_filter()
                if action == "previous":
                    self.o.prev_filter()
            else:  # note OFF
                if isinstance(self.buttons_by_id.get(addr), TriggerButton):
                    self.buttons_by_id[addr].released = True
                if isinstance(self.buttons_by_id.get(addr), TriggerButton):
                    self.buttons_by_id[addr].off()

        # if global filter modifier is on ...
        if self.buttons_by_id[modifiers["global_filter"]].state:
            # ... and the knob is linked to a parameter
            if global_filter_addr_to_parameter_index.get(addr, None) is not None:
                parameter_index = global_filter_addr_to_parameter_index[addr]
                self.o.global_filter.set_parameter(parameter_index, value)
                return
        else:  # global filter is turned off ...
            # but not yet released ! (and "set" pressed)
            if (
                not self.buttons_by_id[modifiers["global_filter"]].released
                and controls.get(addr) == "set"
            ):
                self.o.global_filter.reset_all_parameters()

        if midi_addr_to_parameter_index.get(addr, None) is None:
            return
        parameter_index = midi_addr_to_parameter_index[addr]
        self.o.current_filter.set_parameter(parameter_index, value)


class ToggleButton:
    def __init__(self, midiout, id):
        self.id = id
        self.midiout = midiout
        self.state = False  # on or off
        self.released = False  # button is being pressed or not

    def toggle(self):
        self.released = False
        if self.state:
            self.off()
        else:
            self.on()

    def on(self):
        self.state = True
        m = [176, self.id, 127]
        self.midiout.send_message(m)

    def off(self):
        self.state = False
        m = [176, self.id, 0]
        self.midiout.send_message(m)


class TriggerButton:
    def __init__(self, midiout, id):
        self.id = id
        self.midiout = midiout

    def on(self):
        m = [0x90, self.id, 127]
        self.midiout.send_message(m)

    def off(self):
        m = [0x90, self.id, 0]
        self.midiout.send_message(m)
