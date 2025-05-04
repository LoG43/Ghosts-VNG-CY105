import pyxel
import pygame
import random # For rain and maybe other effects

class App:
    # Initial class variables (some might be better moved to __init__)
    clickCount = 0
    noGoingBack = False
    openChoice = False
    # choices = [] # This seems unused, removing

    def __init__(self):
        pyxel.init(160, 120, title="Ghosts", display_scale=5) # Increased scale for visibility
        pygame.mixer.init()
        try:
            # Ensure the path uses forward slashes or is a raw string for cross-platform compatibility
            pygame.mixer.music.load("assets/combinedSoundtrack.mp3")
            pygame.mixer.music.set_volume(0.3)
            pygame.mixer.music.play(-1) # Loop music
        except pygame.error as e:
            print(f"Warning: Could not load or play music. Error: {e}")

        pyxel.mouse(True)
        pyxel.sounds[0].set( # Click sound
            notes="c2", tones="n", volumes="3", effects="f", speed=15
        )
        pyxel.sounds[1].set( # Door knock sound
            notes="f2 f2", tones="p", volumes="6", effects="n", speed=8
        )
        pyxel.sounds[2].set( # Door open sound
            notes="c3", tones="n", volumes="4", effects="f", speed=20
        )
        # Add more sounds if needed

        # --- Game State & Variables ---
        self.game_state = "OPENER"
        self.clickCount = 0
        self.noGoingBack = False
        self.openChoice = False
        self.guilt = 0 # Initialize guilt score

        # --- Content Loading ---
        self.load_content() # Load text into self.scene_texts and self.choice_texts

        # --- Choice handling ---
        self.choice_boxes = self._calculate_choice_boxes()

        # --- Character Positions (Example - adapt per scene) ---
        self.char_positions = {
            "blue": (20, 50), # Player representation (rarely drawn?)
            "white": (110, 45),
            "black": (70, 40),
            "orange": (40, 60),
            "green": (90, 60)
        }
        # Track which characters are visible in the current state
        self.visible_chars = []

        pyxel.run(self.update, self.draw)

    def load_content(self):
        """Loads all narrative and choice text."""
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

        scene_1_lines = [
                "You stand in a stark, minimalist office.",
                "A single wooden desk, a chair. A window showing a perpetual grey cityscape.",
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
                "(Sound: A sharp, distinct rap on the frosted glass of the office door.)", # Sound cue
                "The sound is an intrusion. Unexpected. Loud.",
                "You don't move immediately. You listen.",
                "Another rap, firmer this time.",
                "(Sound: Second knock, more insistent)",
                "It's not the landlord. Not a delivery. It has the sound of purpose.",
                "Slowly, you rise. The chair scrapes faintly on the floorboards.",
                "You walk to the door. Your reflection is a vague silhouette in the frosted glass.",
                "You turn the knob. It feels cold.",
                "(Sound: Door latch clicks open.)", # Sound cue
                "Rain sounds become slightly louder, mixing with faint city noise.",
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
                "You feel a flicker. Not excitement. Not dread. Just… a change. The stasis is broken.",
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

        # --- Scene 2 Text (Paths diverge based on C1) ---
        scene_2_e1_lines = [ # Path C1_1: Focus on Black
            "White nods curtly. \"Black is... a writer. Keeps to himself.\"",
            "\"He rarely leaves the apartment. Reads. Writes. Stares out the window.\"",
            "\"He seems unremarkable. That is often where the secrets lie.\"",
            "\"Your job is simply to document this. Every detail matters. No matter how small.\"",
            "He turns to leave. \"The key. The address. Start immediately. Your first report is expected.\"",
            "White departs as silently as he arrived, leaving you with the key and the P.O. box card.",
            "The room feels heavy with the new task.",
            "You pick up the key. Cool metal.",
            "Apartment 4A. Directly opposite 4B.",
            "You lock your office and step out into the unending rain.",
            "The building across the street looms, another grey block.",
            "You find 4A. The lock turns smoothly.",
            "The apartment is furnished, sparsely. A table, a chair, a bed. A window facing Black's.",
            "You sit at the window. You wait. You begin to watch.",
        ]
        scene_2_e2_lines = [ # Path C1_2: Focus on Purpose/Self
            "White's eyes narrow almost imperceptibly.",
            "\"The duration is indefinite, Blue. The job continues until I say it stops.\"",
            "\"Or until the subject... is no longer relevant.\"",
            "He pauses, letting the implication hang.",
            "\"As for stopping... This is not a job one simply quits.\"",
            "\"There are commitments. Responsibilities.\"",
            "\"Consider the implications carefully before you accept the key.\"",
            "He gestures towards the brass key on the desk.",
            "Is this a warning? Or just a statement of fact?",
            "The rain seems louder now.",
            "You look at the key, then back at White's impassive face.",
            "He offers no further clarification.",
            "The choice, it seems, was already made when he walked in.",
            "You take the key. \"I understand.\"",
            "White gives a slight nod. \"Good. Apartment 4A. First report tomorrow.\"",
            "He leaves. You are alone with the key, the rain, and the unasked questions.",
            "You head across the street, unlock 4A, and take your position by the window.",
        ]
        scene_2_e3_lines = [ # Path C1_3: Focus on Mechanics
            "\"Excellent,\" White says, a flicker of something unreadable in his eyes.",
            "\"Pragmatism is a valuable asset in this line of work.\"",
            "\"The apartment is indeed ready. Basic furnishings.\"",
            "\"Funds will be deposited weekly to account number...\" He recites a string of digits.",
            "\"Keep receipts for necessary surveillance expenses. Submit them with your reports.\"",
            "\"Get settled in Apartment 4A. Your first report is due tomorrow via the P.O. Box.\"",
            "He gives a final, assessing look. \"No direct contact unless absolutely necessary. Understood?\"",
            "You nod.",
            "\"Good day, Blue.\"",
            "White departs, leaving the scent of rain and ozone.",
            "You pocket the key and the card.",
            "Business as usual, in a way. Just a new target.",
            "You cross the street, find 4A, enter.",
            "The place is anonymous. Perfect.",
            "You set up by the window overlooking 4B. The job has begun.",
        ]

        # --- Scene 3 Text (Paths mostly converge, tone differs) ---
        scene_3_lines = [
            "Days turn into weeks. The routine sets in.",
            "Watch Black. Write report. Mail report. Repeat.",
            "Black's life is one of quiet repetition.",
            "He reads thick books. He writes at a small desk.",
            "Sometimes he just sits, staring at the wall, or perhaps out his own window.",
            "Does he know you're watching? Impossible to say.",
            "His movements are minimal. Predictable.",
            "He orders food in. Occasionally, a woman visits. Orange hair. You note her down.",
            "You start to anticipate his schedule. His small habits.",
            "The way he taps his pen. The brand of cigarettes he smokes.",
            "You buy the same brand. You read the authors you see on his desk.",
            "The lines blur. Whose life are you documenting?",
            "Your reports become mechanical, yet filled with detail.",
            "You are becoming an expert on Black.",
            "Or perhaps, an expert on watching.",
            "One afternoon, you see the woman with Orange hair again, arguing with Black near the entrance.",
            "You can't hear the words, but the gestures are sharp.",
            "She leaves quickly, glancing up towards the windows.",
            "Does she suspect?",
        ]

        # --- Scene 4 Text ---
        scene_4_lines = [
             "The monotony deepens. It becomes a strange comfort.",
             "The city outside is noise. The rain is static.",
             "Inside 4A, there is only the observation. The ritual.",
             "You begin to feel like a reflection.",
             "You start mirroring Black's actions unintentionally.",
             "You sit when he sits. You pace when he paces.",
             "One night, he stands at his window, looking directly across.",
             "You freeze. Caught in the beam of his unseen gaze.",
             "Or are you imagining it? Is he just looking at the city?",
             "He turns away. You exhale.",
             "The paranoia is a new texture in the silence.",
             "You see the Orange-haired woman again, sitting alone in a cafe down the street.",
             "She looks tired. Sad.",
             "A part of you wants to... what? Warn her? Talk to her?",
             "Brown's voice echoes: 'Never engage. Observe only.'",
             "But Brown isn't here.",
             "Another man appears sometimes. Green coat. Stands across the street, looking up.",
             "Is he watching Black? Or you? Or someone else?",
             "The layers of observation fold in on themselves.",
        ]

        # --- Scene 5 Text ---
        scene_5_lines = [
            "Something has shifted. Or perhaps it's you who has shifted.",
            "Black's routine becomes erratic. He stays up late. Paces more.",
            "He seems agitated. Looks out the window frequently.",
            "Is he aware? Has White tipped him off?",
            "Or is this the natural progression of his own story?",
            "The man in the Green coat appears more often now.",
            "You feel a growing unease. A sense of being watched watching.",
            "The reports feel futile. What are you even recording?",
            "The slow decay of a man in a room? Or your own?",
            "One evening, Black packs a small bag. He seems ready to leave.",
            "He pauses at his door, looks back at the room, then steps out.",
            "He doesn't look towards your window.",
            "Down on the street, he walks away quickly, melting into the city night.",
            "Is the case over? Do you report this?",
            "Or do you follow?",
            "The Orange-haired woman is back at the cafe. She waves, tentatively. At you?",
            "The Green coat man is gone.",
            "The silence in room 4A is absolute now. Only the rain remains.",
        ]

        # --- Ending Text ---
        ending_1_lines = [ # Obsession / Ghost
            "Black is gone. But the watching isn't.",
            "You remain in Apartment 4A. Or perhaps you leave it.",
            "It doesn't matter. The city has become the room.",
            "You wander the streets, searching.",
            "Looking for Black? For White? For Brown?",
            "Or for the Blue that existed before the case?",
            "Faces blur. Buildings merge. Time itself is a mystery.",
            "There is nothing to do but let it carry you along.",
            "You become another shadow in the perpetual rain.",
            "A ghost haunted by the identity of another.",
            "Lost in the labyrinth.",
            "(The End?)"
        ]
        ending_2_lines = [ # Escape / Orange
            "Black is gone. White doesn't contact you.",
            "The case dissolves. Or you dissolve it.",
            "You look across at the cafe. At Orange.",
            "You leave the apartment, locking the door behind you.",
            "You don't look back at 4B.",
            "You cross the street. The rain feels different now.",
            "You enter the cafe. Sit opposite Orange.",
            "\"Hi,\" she says. A small, hesitant smile.",
            "\"Hello,\" you reply. The word feels real.",
            "There is no answer to the questions White and Black posed.",
            "Perhaps there never was an answer.",
            "Maybe friendship is enough.",
            "Maybe escape is possible.",
            "(The End)"
        ]
        ending_3_lines = [ # Confrontation / Kill
            "He's leaving. But it can't end like this.",
            "The paradox. The reflection. It demands resolution.",
            "You race down the stairs, out into the rain.",
            "You see Black ahead, walking quickly.",
            "\"Black!\" you shout. Your voice is rough.",
            "He stops. Turns slowly.",
            "His face... is it your own? No. Similar. Worn.",
            "\"Blue?\" he asks, confused.",
            "This has to end. The doubling. The erasure.",
            "You close the distance. There is a struggle. Or perhaps not.",
            "Perhaps it is an acceptance.",
            "Later, you stand alone in the rain.",
            "Black is gone. Truly gone.",
            "You have rejected the mirror. Asserted... something.",
            "But the silence that follows is heavy. Absolute.",
            "What have you become?",
            "(The End)"
        ]

        # --- Store text in dictionary ---
        self.scene_texts = {
            "SCENE_1": scene_1_lines,
            "SCENE_2_E1": scene_2_e1_lines,
            "SCENE_2_E2": scene_2_e2_lines,
            "SCENE_2_E3": scene_2_e3_lines,
            "SCENE_3": scene_3_lines,
            "SCENE_4": scene_4_lines,
            "SCENE_5": scene_5_lines,
            "ENDING_1": ending_1_lines,
            "ENDING_2": ending_2_lines,
            "ENDING_3": ending_3_lines,
        }

        # --- Choice Text ---
        self.choice_texts = {
            "CHOICE_1": [
                "\"Black. Tell me what I need to know about him. Habits? Appearance? Why watch?\"", # E1 hint / Guilt 0
                "\"Just watch? For how long? What if I need to stop?\"",                         # E2 hint / Guilt -1
                "\"The apartment is ready now? I'll need funds. When do I start?\"",             # E3 hint / Guilt +1
            ],
            "CHOICE_2": [
                "Purchase the same brand of cigarettes Black smokes.",                              # Obsession / Guilt -2
                "Focus solely on observation, avoid mimicking Black.",                             # Neutral / Guilt +0
                "Leave the apartment for a short walk, clear your head.",                         # Detachment / Guilt +2
            ],
            "CHOICE_3": [
                "Ignore the Orange-haired woman in the cafe. Stick to the mission.",             # Isolation / Guilt -1
                "Observe Orange from a distance. Note her behavior.",                           # Cautious Engagement / Guilt +1
                "Briefly consider approaching Orange, but decide against it.",                  # Hesitation / Guilt +0
            ],
            "CHOICE_4": [
                "Focus intently on the Green coat man. Is he a threat?",                          # Paranoia / Guilt -2
                "Document Green coat's presence dispassionately in the report.",                 # Neutral Observation / Guilt +0
                "Dismiss Green coat as irrelevant city noise. Focus on Black.",                  # Denial / Guilt +1
            ],
             "CHOICE_5": [
                "Follow Black. He can't just disappear. [E1 Path]",                              # Obsession / Guilt -3
                "Go talk to Orange at the cafe. Leave the case behind. [E2 Path]",               # Escape / Guilt +3
                "Confront Black on the street. Demand answers. [E3 Path]",                       # Confrontation / Guilt +0 (Decision point)
            ]
            # Note: Choice 5 directly leads to ending states now based on guilt/explicit path choice.
        }

    # --- displayText and _calculate_choice_boxes remain the same ---
    def displayText(self, line, color, start_x=None, start_y=None, max_width_chars=None, line_height=None):
        DEFAULT_MAX_CHARS = 35
        DEFAULT_MARGIN_X = 10
        DEFAULT_START_Y = 90
        DEFAULT_LINE_HEIGHT = 10
        if not line: return
        use_defaults = (start_x is None or start_y is None or max_width_chars is None or line_height is None)
        _max_chars = max_width_chars if not use_defaults else DEFAULT_MAX_CHARS
        _start_y = start_y if not use_defaults else DEFAULT_START_Y
        _line_height = line_height if not use_defaults else DEFAULT_LINE_HEIGHT
        _start_x = start_x if not use_defaults else DEFAULT_MARGIN_X
        if use_defaults and len(line) < _max_chars:
            text_width = len(line) * 4
            _start_x = (pyxel.width - text_width) // 2
            pyxel.text(_start_x, _start_y, line, color)
            return
        words = line.split(' '); lines_to_display = []; current_line = ""
        for word in words:
            potential_len = len(current_line) + len(word) + (1 if current_line else 0)
            if potential_len <= _max_chars:
                current_line += (" " if current_line else "") + word
            else:
                lines_to_display.append(current_line); current_line = word
        if current_line: lines_to_display.append(current_line)
        for i, text_line in enumerate(lines_to_display):
             # Prevent drawing outside a theoretical box height if needed
             # if not use_defaults and (i + 1) * _line_height > box_h - text_margin_y * 2: break
             pyxel.text(_start_x, _start_y + i * _line_height, text_line, color)

    def _calculate_choice_boxes(self):
        boxes = []; num_boxes = 3; horizontal_margin = 10
        box_w = pyxel.width - (horizontal_margin * 2); box_h = 30; vertical_gap = 8
        total_boxes_height = (num_boxes * box_h) + ((num_boxes - 1) * vertical_gap)
        start_y = (pyxel.height - total_boxes_height) // 2; box_x = horizontal_margin
        current_y = start_y
        for i in range(num_boxes):
            boxes.append([box_x, current_y, box_w, box_h]); current_y += box_h + vertical_gap
        return boxes

    # --- Update Function: Handles State Transitions and Logic ---
    def update(self):
        if pyxel.btnp(pyxel.KEY_Q): pyxel.quit()

        current_state = self.game_state # Cache state for clarity

        # Generic Text Advancement Logic (used by many states)
        def advance_text_or_choose(scene_state_key, next_choice_state):
            scene_lines = self.scene_texts.get(scene_state_key)
            if not scene_lines: return # Should not happen if content loaded correctly

            scene_end_click_index = len(scene_lines) - 1
            proceed = False

            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                pyxel.play(0, 0) # Click sound
                if self.clickCount < scene_end_click_index:
                    self.clickCount += 1
                else:
                    proceed = True # Reached end, proceed to choice/next state

            elif pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT) and self.clickCount > 0 and not self.noGoingBack:
                pyxel.play(0, 0)
                self.clickCount -= 1

            if proceed:
                self.game_state = next_choice_state
                self.openChoice = True
                self.noGoingBack = True # Can't go back from choices
                print(f"End of {scene_state_key}. State -> {self.game_state}. Guilt: {self.guilt}")

        # Choice Handling Logic (used by choice states)
        def handle_choice(choice_state_key, choice_guilt_map, next_state_map):
            if self.openChoice and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                mx, my = pyxel.mouse_x, pyxel.mouse_y
                for i, box in enumerate(self.choice_boxes):
                    x, y, w, h = box
                    if x <= mx < x + w and y <= my < y + h:
                        pyxel.play(0, 0)
                        print(f"{choice_state_key} Choice {i+1} selected!")

                        # Update Guilt
                        guilt_change = choice_guilt_map.get(i, 0)
                        self.guilt += guilt_change
                        print(f"Guilt change: {guilt_change:+}. New Guilt: {self.guilt}")

                        # Determine Next State
                        next_state = next_state_map.get(i)
                        if next_state:
                            self.game_state = next_state
                            self.clickCount = 0
                            self.openChoice = False
                            self.noGoingBack = False # Allow back clicks in next narrative (optional)
                            print(f"State -> {self.game_state}. Guilt: {self.guilt}")
                        else:
                             print(f"Error: No next state defined for choice {i} in {choice_state_key}")
                        break # Choice made

        # --- State Machine Logic ---
        if current_state == "OPENER":
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                pyxel.play(0, 0)
                if self.clickCount < len(self.opener) - 1: self.clickCount += 1
                else:
                    self.game_state = "TITLE"; self.clickCount = 0; self.noGoingBack = True
                    print("State -> TITLE")
            # Add right click handling if desired

        elif current_state == "TITLE":
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                pyxel.play(0, 0)
                self.game_state = "SCENE_1"; self.clickCount = 0; self.noGoingBack = False
                print("State -> SCENE_1")

        elif current_state == "SCENE_1":
             # SCENE_1 text leads to CHOICE_1
             advance_text_or_choose("SCENE_1", "CHOICE_1")

        elif current_state == "CHOICE_1":
            choice_guilt = {0: 0, 1: -1, 2: 1} # Map choice index to guilt change
            # Map choice index to the *next* scene state based on the C1 branch
            next_state = {0: "SCENE_2_E1", 1: "SCENE_2_E2", 2: "SCENE_2_E3"}
            handle_choice("CHOICE_1", choice_guilt, next_state)

        # Scene 2 branches - they all lead to CHOICE_2
        elif current_state == "SCENE_2_E1": advance_text_or_choose("SCENE_2_E1", "CHOICE_2")
        elif current_state == "SCENE_2_E2": advance_text_or_choose("SCENE_2_E2", "CHOICE_2")
        elif current_state == "SCENE_2_E3": advance_text_or_choose("SCENE_2_E3", "CHOICE_2")

        elif current_state == "CHOICE_2":
            choice_guilt = {0: -2, 1: 0, 2: 2}
            # All C2 options lead to the same SCENE_3 narrative
            next_state = {0: "SCENE_3", 1: "SCENE_3", 2: "SCENE_3"}
            handle_choice("CHOICE_2", choice_guilt, next_state)

        elif current_state == "SCENE_3":
            advance_text_or_choose("SCENE_3", "CHOICE_3")

        elif current_state == "CHOICE_3":
            choice_guilt = {0: -1, 1: 1, 2: 0}
            next_state = {0: "SCENE_4", 1: "SCENE_4", 2: "SCENE_4"}
            handle_choice("CHOICE_3", choice_guilt, next_state)

        elif current_state == "SCENE_4":
            advance_text_or_choose("SCENE_4", "CHOICE_4")

        elif current_state == "CHOICE_4":
            choice_guilt = {0: -2, 1: 0, 2: 1}
            next_state = {0: "SCENE_5", 1: "SCENE_5", 2: "SCENE_5"}
            handle_choice("CHOICE_4", choice_guilt, next_state)

        elif current_state == "SCENE_5":
            advance_text_or_choose("SCENE_5", "CHOICE_5")

        elif current_state == "CHOICE_5":
            # Final choice logic determines ending based on Guilt Thresholds
            if self.openChoice and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                mx, my = pyxel.mouse_x, pyxel.mouse_y
                for i, box in enumerate(self.choice_boxes):
                    x, y, w, h = box
                    if x <= mx < x + w and y <= my < y + h:
                        pyxel.play(0, 0)
                        print(f"CHOICE_5 Choice {i+1} selected!")
                        # Update guilt based on this final choice
                        guilt_map = {0: -3, 1: 3, 2: 0}
                        self.guilt += guilt_map.get(i, 0)
                        print(f"Final Guilt: {self.guilt}")

                        # --- Determine Ending based on Guilt ---
                        # Define thresholds (adjust these based on testing)
                        threshold_high_guilt = 2 # Guilt >= 2 leads to E3 (Confrontation lean)
                        threshold_low_guilt = -3 # Guilt <= -3 leads to E1 (Obsession lean)
                        # Otherwise, default to E2 (Escape)

                        # Explicit choice overrides can also be implemented here if desired
                        # e.g., if i == 1 (Talk to Orange), force E2 regardless of guilt?
                        # For now, we use guilt score after the final choice:

                        if self.guilt >= threshold_high_guilt:
                             self.game_state = "ENDING_3"
                        elif self.guilt <= threshold_low_guilt:
                             self.game_state = "ENDING_1"
                        else:
                             self.game_state = "ENDING_2"


                        print(f"State -> {self.game_state}")
                        self.clickCount = 0
                        self.openChoice = False
                        self.noGoingBack = True # Endings are final
                        break

        # Ending States - Allow quitting or maybe restart?
        elif current_state in ["ENDING_1", "ENDING_2", "ENDING_3"]:
             if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                 print("Game ended. Click to quit.")
                 pyxel.quit() # Or implement a restart feature

    # --- Draw Function: Calls specific draw methods ---
    def draw(self):
        # Dispatch drawing based on the current game state
        state_draw_func = {
            "OPENER": self.draw_opener,
            "TITLE": self.draw_title,
            "SCENE_1": self.draw_scene1, # Handles narrative and C1 choices
            "CHOICE_1": lambda: self.draw_choices("CHOICE_1"), # Use lambda for generic choice draw
            "SCENE_2_E1": lambda: self.draw_scene_narrative("SCENE_2_E1", "apartment"),
            "SCENE_2_E2": lambda: self.draw_scene_narrative("SCENE_2_E2", "apartment"),
            "SCENE_2_E3": lambda: self.draw_scene_narrative("SCENE_2_E3", "apartment"),
            "CHOICE_2": lambda: self.draw_choices("CHOICE_2"),
            "SCENE_3": lambda: self.draw_scene_narrative("SCENE_3", "apartment_orange"),
            "CHOICE_3": lambda: self.draw_choices("CHOICE_3"),
            "SCENE_4": lambda: self.draw_scene_narrative("SCENE_4", "apartment_green"),
            "CHOICE_4": lambda: self.draw_choices("CHOICE_4"),
            "SCENE_5": lambda: self.draw_scene_narrative("SCENE_5", "apartment_leaving"),
            "CHOICE_5": lambda: self.draw_choices("CHOICE_5"),
            "ENDING_1": lambda: self.draw_ending("ENDING_1", "city_wander"),
            "ENDING_2": lambda: self.draw_ending("ENDING_2", "cafe"),
            "ENDING_3": lambda: self.draw_ending("ENDING_3", "street_confront"),
        }

        draw_function = state_draw_func.get(self.game_state)

        if draw_function:
            draw_function()
        else:
            self.draw_error(f"No draw function for state: {self.game_state}")

    # --- Drawing Helper Functions ---
    def draw_character(self, char_type, x, y):
        """Draws a simple representation of a character."""
        w, h, r = 10, 20, 6 # Basic dimensions
        if char_type == 'white': # White rect outline
            pyxel.rectb(x, y, w, h, 7)
        elif char_type == 'black': # Black circle
             # Draw outline then fill slightly smaller to see outline?
             # pyxel.circb(x + w//2, y + h//2, r, 7)
             pyxel.circ(x + w//2, y + h//2, r, 12) # Dark grey circle (color 12)
        elif char_type == 'orange': # Orange triangle
             pyxel.tri(x, y + h, x + w / 2, y, x + w, y + h, 9)
        elif char_type == 'green': # Green rectangle
             pyxel.rect(x, y, w, h, 3)
        # Add 'blue' if needed?

    def draw_background(self, bg_type="office"):
        """Draws different simple backgrounds."""
        pyxel.cls(0) # Default black background
        if bg_type == "office":
            pyxel.rect(0, 0, pyxel.width, 80, 6) # Greyish upper area
            # Rain effect
            if pyxel.frame_count % 3 != 0: # Slower rain
                 for _ in range(15):
                      y_rain = pyxel.rndi(0, 79)
                      start_x = pyxel.rndi(0, pyxel.width-1)
                      pyxel.line(start_x, y_rain, start_x+random.choice([-1,0,1]), y_rain+pyxel.rndi(1,3), 7)
        elif bg_type == "apartment":
            pyxel.rect(0, 0, pyxel.width, 80, 14) # Beige wall?
            pyxel.rect(40, 15, 80, 50, 0) # Black window frame
            pyxel.rect(42, 17, 76, 46, 6) # Grey window view (maybe add rain?)
            # Add rain streaks on window?
            if pyxel.frame_count % 3 == 0:
                 for _ in range(5):
                      start_x = pyxel.rndi(42, 118)
                      pyxel.line(start_x, 17, start_x, 17+pyxel.rndi(5,15), 7)

        elif bg_type == "city_wander" or bg_type == "street_confront":
             # Abstract city - grey shapes, rain
             pyxel.cls(6) # Grey background
             for _ in range(10): # Darker shapes
                 pyxel.rect(pyxel.rndi(-10, 150), pyxel.rndi(-10, 110), pyxel.rndi(10,50), pyxel.rndi(20,80), random.choice([0,1,5]))
             # Rain
             if pyxel.frame_count % 2 == 0:
                 for _ in range(40):
                      y_rain = pyxel.rndi(0, pyxel.height-1)
                      start_x = pyxel.rndi(0, pyxel.width-1)
                      pyxel.line(start_x, y_rain, start_x+random.choice([-1,0,1]), y_rain+pyxel.rndi(1,3), 7)
        elif bg_type == "cafe":
             pyxel.rect(0, 0, pyxel.width, pyxel.height, 14) # Beige interior
             pyxel.rect(10, 10, pyxel.width-20, pyxel.height-60, 6) # Window view
             pyxel.rectb(10, 10, pyxel.width-20, pyxel.height-60, 0) # Window frame


    def draw_text_box_area(self, box_color=1, border_color=7):
         """Draws the standard narrative text box."""
         text_box_y = 85
         text_box_h = pyxel.height - text_box_y - 5
         pyxel.rect(5, text_box_y, pyxel.width - 10, text_box_h, box_color)
         pyxel.rectb(5, text_box_y, pyxel.width - 10, text_box_h, border_color)

    # --- Specific State Drawing Functions ---
    def draw_opener(self):
        self.draw_background("office") # Use office bg
        self.draw_text_box_area()
        if 0 <= self.clickCount < len(self.opener):
            current_line = self.opener[self.clickCount]
            self.displayText(current_line, 0) # Black text for opener

    def draw_title(self):
        pyxel.cls(7); pyxel.text(70, 30, "Ghosts", 5)
        pyxel.text(10, 50, "A visual novel game by Nadir Elyaddasse", 5) # Centered better
        pyxel.text(15, 65, "Based on the novel by Paul Austere", 5) # Centered better

    def draw_scene1(self):
        # This combines narrative and choice drawing for Scene 1
        scene_lines = self.scene_texts["SCENE_1"]
        scene_end_click_index = len(scene_lines) - 1

        if not self.openChoice: # Draw Narrative
            self.draw_background("office")
            self.draw_text_box_area()

            # Draw White character after he appears
            try: white_appears_index = scene_lines.index("Standing there is a man.")
            except ValueError: white_appears_index = -1 # Should not happen
            if self.clickCount >= white_appears_index:
                 self.draw_character('white', self.char_positions['white'][0], self.char_positions['white'][1])

            if 0 <= self.clickCount <= scene_end_click_index:
                curLine = scene_lines[self.clickCount]
                # Sound Cues
                if "(Sound: A sharp, distinct rap" in curLine and pyxel.frame_count % 60 == 1: pyxel.play(1,1) # Play knock sound once
                if "(Sound: Second knock" in curLine and pyxel.frame_count % 60 == 1: pyxel.play(1,1) # Play knock sound once
                if "(Sound: Door latch clicks open.)" in curLine and pyxel.frame_count % 60 == 1: pyxel.play(1,2) # Play door sound once

                line_color = 0
                if "\"" in curLine: line_color = 7 # White's speech
                elif curLine.startswith("("): line_color = 13 # Sound cue color
                else: line_color = 6 # Narration color
                self.displayText(curLine, line_color)
        else: # Draw Choices for C1
            self.draw_choices("CHOICE_1")

    def draw_scene_narrative(self, scene_state_key, bg_type):
        """Generic function to draw narrative scenes."""
        scene_lines = self.scene_texts.get(scene_state_key)
        if not scene_lines: self.draw_error(f"Text missing: {scene_state_key}"); return
        scene_end_click_index = len(scene_lines) - 1

        self.draw_background(bg_type) # Draw appropriate background
        self.draw_text_box_area(box_color=6, border_color=7) # Use grey box maybe

        # --- Draw relevant characters based on scene ---
        if bg_type == "apartment":
             # Assume watching Black
             self.draw_character('black', self.char_positions['black'][0], self.char_positions['black'][1])
        if bg_type == "apartment_orange" and self.clickCount > 5: # Show orange later in scene 3
             self.draw_character('orange', self.char_positions['orange'][0], self.char_positions['orange'][1])
        if bg_type == "apartment_green" and self.clickCount > 10: # Show green later in scene 4
             self.draw_character('green', self.char_positions['green'][0], self.char_positions['green'][1])
        if bg_type == "apartment_leaving": # Maybe show Black near edge?
             self.draw_character('black', self.char_positions['black'][0] + 60, self.char_positions['black'][1])

        # Draw Text
        if 0 <= self.clickCount <= scene_end_click_index:
            curLine = scene_lines[self.clickCount]
            line_color = 7 if "\"" in curLine else 6 # White for speech, Grey for narration
            self.displayText(curLine, line_color)

    def draw_choices(self, choice_state_key):
         """Generic function to draw choice screens."""
         pyxel.cls(13) # Pink/Purple background
         choice_options = self.choice_texts.get(choice_state_key)
         if not choice_options: self.draw_error(f"Choices missing: {choice_state_key}"); return

         for i, option_text in enumerate(choice_options):
             box_x, current_box_y, box_w, box_h = self.choice_boxes[i]
             mx, my = pyxel.mouse_x, pyxel.mouse_y
             border_col, fill_col, text_col = 7, 1, 7 # Defaults
             if box_x <= mx < box_x + box_w and current_box_y <= my < current_box_y + box_h:
                 border_col, fill_col, text_col = 10, 5, 10 # Hover colors

             pyxel.rect(box_x, current_box_y, box_w, box_h, fill_col)
             pyxel.rectb(box_x, current_box_y, box_w, box_h, border_col)
             text_margin_x, text_margin_y, line_h = 4, 4, 8
             max_chars = (box_w - text_margin_x * 2) // 4
             self.displayText(option_text, text_col, box_x + text_margin_x, current_box_y + text_margin_y, max_chars, line_h)

    def draw_ending(self, ending_state_key, bg_type):
        """Draws the final ending screens."""
        ending_lines = self.scene_texts.get(ending_state_key)
        if not ending_lines: self.draw_error(f"Ending text missing: {ending_state_key}"); return
        ending_end_click_index = len(ending_lines) - 1

        self.draw_background(bg_type) # Draw final background

        # --- Draw final characters based on ending ---
        if ending_state_key == "ENDING_1": pass # Just wandering city
        elif ending_state_key == "ENDING_2":
            self.draw_character('orange', self.char_positions['orange'][0]+40, self.char_positions['orange'][1]-10) # Draw Orange in cafe
        elif ending_state_key == "ENDING_3": pass # Just confrontation aftermath

        # Draw final text box
        self.draw_text_box_area(box_color=0, border_color=7) # Black box

        # Display ending text - maybe slightly different color?
        if 0 <= self.clickCount <= ending_end_click_index:
            curLine = ending_lines[self.clickCount]
            self.displayText(curLine, 7) # White text for endings
        elif self.clickCount > ending_end_click_index:
             # Keep showing last line or display "Click to Exit"
             self.displayText(ending_lines[-1], 7)
             pyxel.text(pyxel.width // 2 - 25, pyxel.height - 8, "Click to Exit", pyxel.frame_count % 16 // 8 * 7) # Flashing text


    def draw_error(self, message):
        pyxel.cls(8); pyxel.text(5, 5, "GAME ERROR:", 7)
        self.displayText(message, 7, 5, 15, 38, 10) # Use displayText to wrap error

# --- Run the App ---
App()