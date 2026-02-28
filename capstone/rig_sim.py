# Rig Interlock Simulator – Energizing sequence only (focused version)
# START + safe energization logic – fixed checkbox handling

import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle
import matplotlib.patheffects as path_effects
from matplotlib.widgets import Button, CheckButtons

class RigEnergizeSim:
    def __init__(self):
        # ── State ──────────────────────────────────────────────────
        self.beacon       = "Red"
        self.maglock      = 0           # 0 = unlocked, 1 = locked
        self.grid_sim     = False
        self.acd2         = False
        self.acd3         = False
        self.acd_t1       = False
        self.acd_t2       = False
        self.ats1         = False
        self.ats2         = False

        self.occupancy    = 1           # 1 = detected (unsafe), 0 = clear
        self.door_contact = 1           # 1 = open (unsafe), 0 = closed
        self.taps_configured = False

        self.sequence_started = False
        self.step_count   = 0

        # ── Figure setup ───────────────────────────────────────────
        self.fig = plt.figure(figsize=(13, 8))
        self.fig.suptitle("Rig Energizing Simulator – START Sequence Only", fontsize=15)

        gs = self.fig.add_gridspec(2, 3,
                                   height_ratios=[3.2, 1.1],
                                   width_ratios=[1, 3.2, 1.4],
                                   wspace=0.35, hspace=0.22)

        self.ax_beacon   = self.fig.add_subplot(gs[0, 0])
        self.ax_switches = self.fig.add_subplot(gs[0, 1])
        self.ax_status   = self.fig.add_subplot(gs[0, 2])
        self.ax_controls = self.fig.add_subplot(gs[1, :])

        for ax in [self.ax_beacon, self.ax_switches, self.ax_status, self.ax_controls]:
            ax.axis('off')

        self._init_visuals()
        self._add_controls()

        # Use subplots_adjust instead of tight_layout to avoid warning
        self.fig.subplots_adjust(left=0.02, right=0.98, top=0.94, bottom=0.08,
                                 wspace=0.35, hspace=0.25)

        plt.show()

    def _init_visuals(self):
        # Beacon
        self.beacon_patch = Circle((0.5, 0.5), 0.38, color='darkred', ec='black', lw=2.5)
        self.ax_beacon.add_patch(self.beacon_patch)
        self.beacon_label = self.ax_beacon.text(
            0.5, 0.5, "RED", ha='center', va='center',
            fontsize=36, fontweight='bold', color='white')
        self.beacon_label.set_path_effects([path_effects.withStroke(linewidth=5, foreground='black')])
        self.ax_beacon.set_title("Beacon", fontsize=13)

        # Switches
        self.sw_patches = {}
        self.sw_texts = {}
        names = ['Grid Sim', 'ACD2', 'ACD3', 'ACD T1', 'ACD T2', 'ATS1', 'ATS2', 'Maglock']
        y = 0.95
        for name in names:
            rect = Rectangle((0.06, y-0.078), 0.36, 0.068, fc='lightgray', ec='black', lw=1)
            self.ax_switches.add_patch(rect)
            txt = self.ax_switches.text(0.49, y-0.039, f"{name}: Open", fontsize=10.5, va='center')
            self.sw_patches[name] = rect
            self.sw_texts[name] = txt
            y -= 0.09
        self.ax_switches.set_title("Actuators", fontsize=13)

        # Status
        self.status_text = self.ax_status.text(0.06, 0.97, "", va='top', fontsize=10.8, family='monospace')
        self.ax_status.set_title("Status", fontsize=13)

        self._update()

    def _add_controls(self):
        # START button
        ax_start = self.fig.add_axes([0.08, 0.28, 0.14, 0.65])
        self.btn_start = Button(ax_start, 'START', color='limegreen', hovercolor='lightgreen')
        self.btn_start.on_clicked(self._on_start)

        # Reset button
        ax_reset = self.fig.add_axes([0.26, 0.28, 0.14, 0.65])
        self.btn_reset = Button(ax_reset, 'Reset', color='orange', hovercolor='gold')
        self.btn_reset.on_clicked(self._on_reset)

        # Checkboxes – using descriptive labels
        ax_chk = self.fig.add_axes([0.45, 0.08, 0.52, 0.80])
        self.labels = [
            "Occupancy Detected (someone inside)",
            "Door Open (fault)",
            "Taps Configured"
        ]
        self.check = CheckButtons(ax_chk, self.labels, [True, True, False])
        for lbl in self.check.labels:
            lbl.set_fontsize(10.5)
        self.check.on_clicked(self._on_checkbox)

    def _on_start(self, event):
        if self.sequence_started:
            return
        self.sequence_started = True
        self.grid_sim = True
        self.beacon = "Green"
        print("START → Grid Simulator closed, Beacon → Green")
        self._run_energize_logic()
        self._update()

    def _on_reset(self, event):
        self.__init__()
        print("Reset complete")
        self._update()

    def _on_checkbox(self, label):
        # Get current states in order of labels
        states = self.check.get_status()

        # Option 1: exact label matching
        if label == "Occupancy Detected (someone inside)":
            self.occupancy = 1 if states[0] else 0
            print(f"Occupancy → {self.occupancy} (from checkbox)")

        elif label == "Door Open (fault)":
            self.door_contact = 1 if states[1] else 0
            print(f"Door → {self.door_contact} (from checkbox)")

        elif label == "Taps Configured":
            self.taps_configured = states[2]
            print(f"Taps configured → {self.taps_configured}")

        # Trigger logic update if sequence is active
        if self.sequence_started:
            self._run_energize_logic()
        self._update()

    def _run_energize_logic(self):
        self.step_count += 1

        if self.beacon == "Green":

            # Step: close ACD2 & ACD3
            if not self.acd2 or not self.acd3:
                self.acd2 = self.acd3 = True
                print("→ ACD2 & ACD3 Closed")

            # Step: safe → lock doors + close ATS
            if self.occupancy == 0 and self.door_contact == 0:
                if self.maglock == 0:
                    self.maglock = 1
                    print("→ SAFE CONDITIONS → Maglock locked, doors secured")
                self.ats1 = self.ats2 = True

                # Step: taps configured → close ACD T1 & T2
                if self.taps_configured and not (self.acd_t1 and self.acd_t2):
                    self.acd_t1 = self.acd_t2 = True
                    print("→ Taps configured → ACD T1 & T2 Closed")

        # Fault monitoring
        if self.sequence_started and self.beacon in ["Green", "Yellow"]:
            if self.occupancy == 1 or self.door_contact == 1:
                if self.beacon != "Yellow":
                    print("→ UNSAFE CONDITION DETECTED → Beacon Yellow")
                self.beacon = "Yellow"

    def _update(self):
        # Beacon
        colors = {"Red": "darkred", "Yellow": "gold", "Green": "limegreen"}
        self.beacon_patch.set_color(colors.get(self.beacon, "gray"))
        self.beacon_label.set_text(self.beacon.upper())
        self.beacon_label.set_color("white" if self.beacon in ["Red", "Green"] else "black")

        # Switches
        states = {
            'Grid Sim': self.grid_sim,
            'ACD2': self.acd2,
            'ACD3': self.acd3,
            'ACD T1': self.acd_t1,
            'ACD T2': self.acd_t2,
            'ATS1': self.ats1,
            'ATS2': self.ats2,
            'Maglock': self.maglock == 1
        }
        for name, closed in states.items():
            self.sw_patches[name].set_facecolor("limegreen" if closed else "tomato")
            self.sw_texts[name].set_text(f"{name}: {'Closed' if closed else 'Open'}")

        # Status
        lines = [
            f"Step:          {self.step_count}",
            f"Beacon:        {self.beacon}",
            f"Maglock:       {'Locked' if self.maglock else 'Unlocked'}",
            f"Occupancy:     {'CLEAR' if self.occupancy == 0 else 'DETECTED'}",
            f"Door:          {'CLOSED' if self.door_contact == 0 else 'OPEN'}",
            f"Taps:          {'Configured' if self.taps_configured else 'Not configured'}",
            f"Sequence:      {'Running' if self.sequence_started else 'Idle'}"
        ]
        self.status_text.set_text("\n".join(lines))

        self.fig.canvas.draw_idle()


if __name__ == "__main__":
    sim = RigEnergizeSim()