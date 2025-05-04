import pyxel,pygame

class App:

    clickCount=0
    opener = [
    "First of all there is Blue.",
    "Later there is White, and then there is Black, and before the beginning there was Brown.",
    "Brown broke you in, Brown taught you the ropes, and when Brown grew old, you took over.",
    "That is how it began.",
    "The place is New York, the time is the present, and neither one will ever change.",
    "You go to your office every day and sit at your desk, waiting for something to happen.",
    "For a long time nothing does, and then a man named White walks through the door...", 
    "and that is how it begins.",
    ]
    noGoingBack=False
    openChoice=False
    choices=[]

    def __init__(self):
        pyxel.init(160, 120, title="Ghosts") #full title: Ghosts \nA visual novel game by Nadir Elyaddasse, based on the works of Paul Austere 
        pygame.mixer.init()
        pygame.mixer.music.load("assets\combinedSoundtrack.mp3")
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
        pyxel.mouse(True)
        pyxel.sounds[0].set( # Example sound
            notes="d2", tones="t", volumes="7", effects="n", speed=10
        )

        # --- Game State ---
        self.game_state = "OPENER" # Start with the opener

        # --- Content Loading ---
        self.clickCount = 0
        self.noGoingBack = False # Initialize here

        self.opener = [
            "First of all there is Blue.",
            "Later there is White, and then there is Black, and before the beginning there was Brown.",
            "Brown broke you in, Brown taught you the ropes, and when Brown grew old, you took over.",
            "That is how it began.",
            "The place is New York, the time is the present, and neither one will ever change.",
            "You go to your office every day and sit at your desk, waiting for something to happen.",
            "For a long time nothing does, and then a man named White walks through the door...",
            "and that is how it begins.",
        ]

        # Store scene 1 lines directly (will be used by draw_scene1)
        self.scene_1_lines = [
                "You stand in a stark, minimalist office.",
                "A single wooden desk, a chair. A window showing a perpetual grey cityscape.", # Modified/Combined
                "You sit at the desk, posture still.",
                "The office feels… adequate. Like a coat that fits, if not comfortably.",
                "Brown. The name echoes sometimes, in the quiet moments.",
                "A fading photograph in your mind. Thick hands. The smell of pipe tobacco. Grit.",
                "He'd pointed to the chair you now occupy.",
                "\"It's yours, Blue,\" he'd rasped, his voice thin as old paper. \"Keep it warm.\"",
                "Then he'd walked out, dissolving into New York City's grey breath.",
                "You haven't seen him since. You don't expect to.",
                "Cars like steel insects crawl below. People are fleeting shadows under umbrellas.",
                "The details blur. The city is a constant hum, a backdrop.",
                "Like the rain. Always the rain.",
                "Your routine is your structure. It's the bones of the day.",
                "Arrive at eight. Unlock the door (the tumblers click, a familiar sound).",
                "Sit. Stare at the grain of the desk wood.",
                "Stare at the rain on the window.",
                "Stare at the phone that never rings.",
                "The silence isn't empty. It's full of… waiting.",
                "A potentiality that hangs thick and heavy, like the humid air before a storm.",
                "Some days you trace the water rivulets on the glass with your eyes.",
                "Following their paths down, down, until they merge and disappear.",
                "Other days you read. Old case files Brown left behind.",
                "Tales of missing persons who stayed missing. Secrets that unravelled into more secrets.",
                "None of it feels entirely real. More like stories told about someone else.",
                "For a long time nothing does happen.",
                "The clock on the wall (a plain, round face, also Brown's) ticks.",
                "Each tick chips away at the silence, only to have it flood back in.",
                "Tick. Tock. Rain. Hum.",
                "You are an observer. Waiting for something to observe.",
                "It’s what you were trained for. To watch. To record. To disappear into the background.",
                "Brown called it 'the art of absence'.",
                "You wonder if you've mastered it too well. If you're fading even to yourself.",
                "The wood grain under your fingers seems more solid than your own thoughts.",
                "Days bleed into weeks. Weeks into months.",
                "The dust motes dance in the occasional sliver of weak sunlight that breaks the grey.",
                "You watch them rise and fall. Tiny universes, going nowhere.",
                "Like you.",
                "And then, one Tuesday (or Thursday?), the waiting ends.",
                "(Sound: A sharp, distinct rap on the frosted glass of the office door. It cuts through the rain sounds.)", # Combined lines
                "The sound is an intrusion. Unexpected. Loud.",
                "You don't move immediately. You listen.",
                "Another rap, firmer this time.",
                "(Sound: Second knock, more insistent)",
                "It's not the landlord. Not a delivery. It has the sound of purpose.",
                "Slowly, you rise. The chair scrapes faintly on the floorboards.",
                "You walk to the door. Your reflection is a vague silhouette in the frosted glass.",
                "You turn the knob. It feels cold.",
                "(Sound: Door latch clicks open. Rain sounds become slightly louder, mixing with faint city noise)", # Combined lines
                #white enters
                "Standing there is a man.",
                "He is dressed immaculately in a pale suit. White. Blindingly white against the grey day.",
                "His face is nondescript, easily forgettable, yet his eyes are sharp. Focused.",
                "He looks directly at you. No hesitation.",
                "\"Blue?\" he asks. His voice is calm, level. It carries easily over the rain.",
                "You nod. Words feel thick in your throat.",
                "The man steps inside without waiting for an invitation, bringing a chill gust of air with him.",
                "He glances around the spare office, his gaze lingering for a fraction of a second on the chair, the desk.",
                "As if assessing, cataloguing.",
                "He turns back to you.",
                "\"My name is White,\" he says simply. As if stating a fundamental truth.",
                "You remain silent. Waiting. Observing. This is the job, after all.",
                "White doesn't offer a handshake. He gets straight to the point.",
                "\"I have a case for you, Blue.\"",
                "He pauses, letting the words hang in the air.",
                "\"A surveillance case. Long-term.\"",
                "He watches you, gauging your reaction. Or perhaps your lack of it.",
                "You feel a flicker. Not excitement. Not dread. Just… a change. The stasis is broken.", # Combined lines
                "Something is finally happening.",
                "White continues, his voice still maddeningly neutral.",
                "\"There is a man. His name is Black.\"",
                "The name drops into the room like a stone into water. Black. The opposite. The shadow.",
                "\"He lives in an apartment across the street. Room 4B.\" White gestures vaguely towards the window.",
                "\"I want you to watch him.\"",
                "Just that. Watch him.",
                "\"Rent the apartment opposite his. Room 4A. It's already arranged.\"",
                "He produces a key from his white suit pocket. Plain brass.",
                "He lays it on the desk. It glints under the weak light.",
                "\"Observe him. Write reports. Daily.\"",
                "He names a figure for payment. Generous. More than generous.",
                "\"You will report only to me. Mail the reports to this post office box.\"",
                "He places a small, white card next to the key.",
                "No questions about your qualifications. No discussion of methods.",
                "It's assumed you know. Assumed you will comply.",
                "Like Brown trained you. Like the colour implies. Blue. Steady. Reliable.",
                "White looks at you expectantly. The silence stretches again.",
                "It demands a response. An acceptance. A commitment.",
                "This is it. The start. The case. The reason for the waiting.",
                "And that is how it begins.",
                "White waits, patient as stone.",
                "The key gleams on the desk. The rain falls outside. The city hums.",
                "Your first decision. Your first word to this new figure.",]

        # --- Example: Preload Scene 2 text (adjust based on branching) ---
        self.scene_2_E1_lines = [ # Path if choice 1 was made
            "White nods curtly. \"Black is... a writer. Keeps to himself.\"",
            "\"He rarely leaves the apartment. Reads. Writes. Stares out the window.\"",
            "\"Your job is simply to document this. Every detail matters.\"",
            "He turns to leave. \"The key. The address. Start immediately.\"",
            # ... more lines ...
        ]
        self.scene_2_E2_lines = [ # Path if choice 2 was made
            "White's eyes narrow almost imperceptibly.",
            "\"The duration is indefinite. You stop when I say you stop.\"",
            "\"Or when the subject... is no longer relevant.\"",
            "\"Consider the implications before you accept, Blue.\"",
            # ... more lines ... leading perhaps to another choice or Blue moving in
        ]
        self.scene_2_E3_lines = [ # Path if choice 3 was made
            "\"Excellent,\" White says, a flicker of something unreadable in his eyes.",
            "\"The funds will be deposited weekly to account number...\" He recites a number.",
            "\"Get settled in Apartment 4A. Your first report is due tomorrow.\"",
            "He gives a final, assessing look and departs.",
            # ... more lines ...
        ]

        # Store scene text in a dictionary for easier access by state? (Optional but good practice)
        self.scene_texts = {
            "SCENE_1": self.scene_1_lines,
            "SCENE_2_E1": self.scene_2_E1_lines,
            "SCENE_2_E2": self.scene_2_E2_lines,
            "SCENE_2_E3": self.scene_2_E3_lines,
            # Add entries for SCENE_3, ENDING_1 etc.
        }

        # --- Choice handling ---
        # Calculate choice box bounds (do this once if they don't change position)
        self.choice_boxes = self._calculate_choice_boxes()
        self.openChoice = False # Flag to indicate if choices are active

        pyxel.run(self.update, self.draw)

    def displayText(self, line, color, start_x=None, start_y=None, max_width_chars=None, line_height=None):
        """
        Draws text, wrapping within a given character width.
        If start_x/y/max_width are None, uses default narrative box settings.
        Otherwise, uses provided coordinates and constraints (for choice boxes).
        """
        DEFAULT_MAX_CHARS = 35
        DEFAULT_MARGIN_X = 10
        DEFAULT_START_Y = 90
        DEFAULT_LINE_HEIGHT = 10

        if not line:
            return

        use_defaults = (start_x is None or start_y is None or max_width_chars is None or line_height is None)

        _max_chars = max_width_chars if not use_defaults else DEFAULT_MAX_CHARS
        _start_y = start_y if not use_defaults else DEFAULT_START_Y
        _line_height = line_height if not use_defaults else DEFAULT_LINE_HEIGHT
        _start_x = start_x if not use_defaults else DEFAULT_MARGIN_X

        # Handle centering for short lines ONLY when using defaults
        if use_defaults and len(line) < _max_chars:
            text_width = len(line) * 4 # Approximate width
            _start_x = (pyxel.width - text_width) // 2
            pyxel.text(_start_x, _start_y, line, color)
            return # Displayed as a single centered line

        # Word wrapping logic for default area OR specified boxes
        words = line.split(' ')
        lines_to_display = []
        current_line = ""

        for word in words:
            # Simplified check: if word is too long, let it overflow or truncate
            # if len(word) > _max_chars: word = word[:_max_chars]

            potential_len = len(current_line) + len(word)
            if current_line:
                potential_len += 1 # Account for space

            if potential_len <= _max_chars:
                if current_line:
                    current_line += " " + word
                else:
                    current_line = word
            else:
                lines_to_display.append(current_line)
                current_line = word

        if current_line:
            lines_to_display.append(current_line)

        # Display the wrapped lines
        for i, text_line in enumerate(lines_to_display):
            # Optional: Add check here if you need to limit lines based on box height
            pyxel.text(_start_x, _start_y + i * _line_height, text_line, color)
    
    # Helper function to calculate choice boxes (called from init)
    def _calculate_choice_boxes(self):
        boxes = []
        num_boxes = 3 # Assuming always 3 choices for now
        horizontal_margin = 10
        box_w = pyxel.width - (horizontal_margin * 2)
        box_h = 30
        vertical_gap = 8
        total_boxes_height = (num_boxes * box_h) + ((num_boxes - 1) * vertical_gap)
        start_y = (pyxel.height - total_boxes_height) // 2
        box_x = horizontal_margin
        current_y = start_y
        for i in range(num_boxes):
            boxes.append([box_x, current_y, box_w, box_h])
            current_y += box_h + vertical_gap
        return boxes
    
    # In your update method:
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()

        # --- State: OPENER ---
        if self.game_state == "OPENER":
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                pyxel.play(0, 0)
                if self.clickCount < len(self.opener) - 1:
                    self.clickCount += 1
                else:
                    # Finished opener, move to title
                    self.game_state = "TITLE"
                    self.clickCount = 0 # Reset click count for the next phase (title doesn't use it)
                    self.noGoingBack = True # Prevent going back from title screen
                    print("State -> TITLE")
            # Handle right click for opener if needed (similar logic)

        # --- State: TITLE ---
        elif self.game_state == "TITLE":
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                pyxel.play(0, 0)
                # Move from title to scene 1 narrative
                self.game_state = "SCENE_1" # Use a single state for Scene 1
                self.clickCount = 0 # Reset click count for Scene 1 narrative
                self.noGoingBack = False # Allow going back within scene 1 narrative initially
                print("State -> SCENE_1")

        # --- State: SCENE_1 (Handles both narrative and choice drawing via draw_scene1) ---
        elif self.game_state == "SCENE_1":
            scene1_end_click_index = len(self.scene_1_lines) - 1 # Index of last line

            if not self.openChoice: # If we are showing narrative
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    pyxel.play(0, 0)
                    if self.clickCount < scene1_end_click_index:
                        self.clickCount += 1
                    else:
                        # Reached end of narrative, enable choices
                        self.openChoice = True
                        self.noGoingBack = True # Can't go back once choices appear
                        print("Scene 1 Choices Activated")

                elif pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT) and self.clickCount > 0 and not self.noGoingBack:
                    pyxel.play(0, 0)
                    self.clickCount -= 1

            else: # Choices are active (self.openChoice is True)
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                    mx, my = pyxel.mouse_x, pyxel.mouse_y
                    for i, box in enumerate(self.choice_boxes):
                        x, y, w, h = box
                        if x <= mx < x + w and y <= my < y + h:
                            pyxel.play(0, 0)
                            print(f"Scene 1 Choice {i+1} selected!")
                            # --- BRANCHING LOGIC ---
                            if i == 0: # Choice 1 (E1 Path)
                                self.game_state = "SCENE_2_E1"
                            elif i == 1: # Choice 2 (E2 Path)
                                self.game_state = "SCENE_2_E2"
                            elif i == 2: # Choice 3 (E3 Path)
                                self.game_state = "SCENE_2_E3"

                            print(f"State -> {self.game_state}")
                            self.clickCount = 0 # Reset click count for the new scene
                            self.openChoice = False # Deactivate choices
                            self.noGoingBack = False # Allow back clicks in next narrative (optional)
                            break # Exit choice checking loop

        # --- State: SCENE_2_E1 (Example Next Scene) ---
        elif self.game_state == "SCENE_2_E1":
            scene_lines = self.scene_texts[self.game_state] # Get text for this state
            scene_end_click_index = len(scene_lines) - 1

            # Similar logic to SCENE_1 narrative part
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                pyxel.play(0, 0)
                if self.clickCount < scene_end_click_index:
                    self.clickCount += 1
                else:
                    # End of Scene 2 E1 - maybe move to Scene 3 or another choice
                    print("End of SCENE_2_E1 reached")
                    # self.game_state = "NEXT_STATE"
                    # self.clickCount = 0
                    pass # Add transition logic here

            elif pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT) and self.clickCount > 0: # Allow going back?
                pyxel.play(0, 0)
                self.clickCount -= 1

        # --- Add elif blocks for SCENE_2_E2, SCENE_2_E3, etc. ---
        # Each will have similar logic for handling clicks and advancing text/state

    # Replace your existing draw function with this:
    def draw(self):
        # --- State-Based Dispatcher ---
        if self.game_state == "OPENER":
            self.draw_opener()
        elif self.game_state == "TITLE":
            self.draw_title()
        elif self.game_state == "SCENE_1":
            # draw_scene1 handles both narrative and choices internally
            self.draw_scene1()
        elif self.game_state == "SCENE_2_E1":
            self.draw_scene_generic("SCENE_2_E1") # Use a generic drawing function
        elif self.game_state == "SCENE_2_E2":
            self.draw_scene_generic("SCENE_2_E2")
        elif self.game_state == "SCENE_2_E3":
            self.draw_scene_generic("SCENE_2_E3")
        # --- Add elif branches for more scenes/states ---
        # elif self.game_state == "SCENE_3":
        #     self.draw_scene3()
        # elif self.game_state == "ENDING_1":
        #     self.draw_ending1()
        else:
            # Fallback for unknown state
            pyxel.cls(8) # Red background for error
            pyxel.text(10, 10, f"ERROR: Unknown Game State!", 7)
            pyxel.text(10, 20, f"State: {self.game_state}", 7)
    
    # --- NEW Drawing Functions ---
    def draw_opener(self):
        pyxel.cls(13) # Background color
        # Draw text box border/fill (optional, adapt from scene1)
        pyxel.rect(10, 85, 140, 30, 1) # Example box
        pyxel.rectb(10, 85, 140, 30, 7)

        if 0 <= self.clickCount < len(self.opener):
            current_line = self.opener[self.clickCount]
            # Use the better displayText for consistency
            self.displayText(current_line, 0, start_x=15, start_y=90, max_width_chars=35, line_height=10)
            # Or keep your original opener text logic if preferred:
            # if len(current_line) < 35: ... else: ... etc ...

    def draw_title(self):
        pyxel.cls(7) # White background
        pyxel.text(70, 30, "Ghosts", 5) # Dark Blue text
        pyxel.text(2.5, 50, "A visual novel game by Nadir Elyaddasse", 5)
        pyxel.text(15, 60, "Based on the novel by Paul Austere", 5)

    # RENAME your existing scene1 function to draw_scene1
    # It will be called ONLY when self.game_state is "SCENE_1"
    def draw_scene1(self):
        # This function now implicitly knows it's drawing scene 1
        # It uses self.clickCount relative to the start of scene 1 lines
        # and self.openChoice to decide whether to show narrative or choices

        scene_lines = self.scene_1_lines # Use the preloaded lines
        scene_end_click_index = len(scene_lines) - 1

        # --- Draw Narrative Part ---
        if not self.openChoice:
            # Draw background visuals for narrative scene
            pyxel.cls(0) # Black background for narrative part
            pyxel.rect(0, 0, pyxel.width, 80, 6) # Greyish upper area
            if pyxel.frame_count % 2 == 0: # Rain
                for _ in range(20):
                    pyxel.pset(pyxel.rndi(0, pyxel.width-1), pyxel.rndi(0, 79), 7)

            # Draw Text Box Area
            text_box_y = 85
            text_box_h = pyxel.height - text_box_y - 5
            pyxel.rect(5, text_box_y, pyxel.width - 10, text_box_h, 1) # Dark blue box
            pyxel.rectb(5, text_box_y, pyxel.width - 10, text_box_h, 7) # White border

            if 0 <= self.clickCount <= scene_end_click_index:
                curLine = scene_lines[self.clickCount]
                # Determine color
                line_color = 0
                if "\"" in curLine: line_color = 7
                elif curLine.startswith("("): line_color = 13
                else: line_color = 6
                # Use the better displayText
                self.displayText(curLine, line_color, start_x=10, start_y=90, max_width_chars=35, line_height=10)

                # Draw White indicator
                try:
                    white_appears_index = scene_lines.index("Standing there is a man.")
                    if self.clickCount >= white_appears_index:
                        pyxel.rect(pyxel.width // 2 - 5 , 50, 10, 20, 7)
                except ValueError: pass

        # --- Draw Choices Part ---
        else: # self.openChoice is True
            pyxel.cls(13) # Pink/Purple background for choice screen
            choice_options = [ # Define choices locally or load from self if needed
                "\"Black. Tell me what I need to know about him. Habits? Appearance? Why watch?\"", # E1
                "\"Just watch? For how long? What if I need to stop?\"", # E2
                "\"The apartment is ready now? I'll need funds. When do I start?\"", # E3
            ]

            # Draw the choice boxes using pre-calculated bounds
            for i, option_text in enumerate(choice_options):
                box_x, current_box_y, box_w, box_h = self.choice_boxes[i]

                # Highlight box on hover
                mx, my = pyxel.mouse_x, pyxel.mouse_y
                border_col, fill_col, text_col = 7, 1, 7 # Defaults
                if box_x <= mx < box_x + box_w and current_box_y <= my < current_box_y + box_h:
                    border_col, fill_col, text_col = 10, 5, 10 # Hover colors

                pyxel.rect(box_x, current_box_y, box_w, box_h, fill_col)
                pyxel.rectb(box_x, current_box_y, box_w, box_h, border_col)

                # Display text inside the box
                text_margin_x, text_margin_y, line_h = 4, 4, 8
                max_chars = (box_w - text_margin_x * 2) // 4
                self.displayText(option_text, text_col, box_x + text_margin_x, current_box_y + text_margin_y, max_chars, line_h)


    # --- Generic Scene Drawing Function (Example) ---
    # You can create more specific functions if scenes need unique visuals
    def draw_scene_generic(self, scene_state_key):
        # Get the lines for the current scene state
        if scene_state_key not in self.scene_texts:
            self.draw_error(f"Text not found for {scene_state_key}")
            return

        scene_lines = self.scene_texts[scene_state_key]
        scene_end_click_index = len(scene_lines) - 1

        # --- Draw Background (Make this adaptable per scene) ---
        pyxel.cls(1) # Default dark blue background
        # Example: Maybe draw apartment interior?
        pyxel.rect(10, 10, 140, 70, 14) # Beige wall?
        pyxel.rect(50, 20, 60, 50, 0) # Window?

        # --- Draw Text Box ---
        text_box_y = 85
        text_box_h = pyxel.height - text_box_y - 5
        pyxel.rect(5, text_box_y, pyxel.width - 10, text_box_h, 6) # Grey box
        pyxel.rectb(5, text_box_y, pyxel.width - 10, text_box_h, 7) # White border

        # --- Draw Current Line ---
        if 0 <= self.clickCount <= scene_end_click_index:
            curLine = scene_lines[self.clickCount]
            # Determine color (can enhance this logic)
            line_color = 7 if "\"" in curLine else 6 # Simple example
            self.displayText(curLine, line_color, start_x=10, start_y=90, max_width_chars=35, line_height=10)

        # --- Draw Characters/Elements (Adapt per scene) ---
        # If Blue is watching Black, maybe draw silhouettes?
        pyxel.rect(60, 40, 10, 20, 0) # Black's silhouette?
        pyxel.rect(90, 40, 10, 20, 7) # White's silhouette (if present)?


    def draw_error(self, message):
        """Helper to draw error messages."""
        pyxel.cls(8) # Red background
        self.displayText(message, 7, 10, 10, 38, 10) # Use displayText

    # --- Make sure you have the modified displayText function in your class ---
    # (The one that accepts start_x, start_y, max_width_chars, line_height)

App()