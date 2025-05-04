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
        #pygame.mixer.music.play(-1)
        pyxel.mouse(True)
        pyxel.sounds[0].set(
            notes="d2", 
            tones="t",
            volumes="7",
            effects="n",
            speed=10   
        )
        pyxel.run(self.update, self.draw)
        

    def update(self):
        if pyxel.btnp(pyxel.KEY_Q):
            pyxel.quit()
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            pyxel.play(0, 0)
            print("advance scene")
            self.clickCount+=1
            mx=pyxel.mouse_x
            my=pyxel.mouse_y
            if self.openChoice:
                print("choice detected")
                #box1 coordinate bounds: (10, 7) to (149, 36)
                #box2 coordinate bounds: (10, 45) to (149, 74)
                #box3 coordinate bounds: (10, 83) to (149, 112)
                if 10<=mx<=149 and 7<=my<=36:
                    self.openChoice=False
                    self.choices.append(1)
                    print("choice 1 closed")
                elif 10<=mx<=149 and 45<=my<=74:
                    self.openChoice=False
                    self.choices.append(2)
                    print("choice 2 closed")
                elif 10<=mx<=149 and 83<=my<=112:
                    self.openChoice=False
                    self.choices.append(3)
                    print("choice 3 closed")

        if pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT) and self.clickCount!=0 and self.noGoingBack==False:
            pyxel.play(0, 0)
            print("retreat scene")
            self.clickCount-=1

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

    def scene1(self):
        scene_1_lines = [
            "You stand in a stark, minimalist office.",
            "A single wooden desk, a chair. A window facing a brick wall."
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
            "You hear a sharp, distinct rap on the frosted glass of the office door.",
            "The sound is an intrusion. Unexpected. Loud.",
            "You don't move immediately. You listen.",
            "Another rap, firmer this time.",
            "(Sound: Second knock, more insistent)",
            "It's not the landlord. Not a delivery. It has the sound of purpose.",
            "Slowly, you rise. The chair scrapes faintly on the floorboards.",
            "You walk to the door. Your reflection is a vague silhouette in the frosted glass.",
            "You turn the knob. It feels cold.",
            "The door latch clicks open."
            "Rain sounds become slightly louder, mixing with faint city noise",
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
            "You feel a flicker. Not excitement. Not dread. The stasis is broken.",
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
        scene1_start_click = len(self.opener)
        scene1_end_click = scene1_start_click + len(scene_1_lines)
        
        if scene1_start_click <= self.clickCount <= scene1_end_click:
            pyxel.cls(13)
            if pyxel.frame_count % 2 == 0:
                for _ in range(20):
                    pyxel.pset(pyxel.rndi(0, pyxel.width-1), pyxel.rndi(0, 79), 1)
                    #rain sound effect would be really cool
            pyxel.rect(10,75,140,8,7)
            curLine=scene_1_lines[self.clickCount-(len(self.opener)+1)]
            if self.clickCount-len(self.opener)<scene_1_lines.index("Standing there is a man.")+2:
                self.displayText(curLine,0)
            else:
                pyxel.rectb(50,10,60,60,7)
                if "\"" in  curLine:
                    self.displayText(curLine,7)
                else:
                    self.displayText(curLine,0)
        else:
            pyxel.cls(13) # Pink/Purple background for choice screen
            choice_options = [
                "\"Black. Tell me what I need to know about him. Habits? Appearance? Why watch?\"", # E1
                "\"Just watch? For how long? What if I need to stop?\"", # E2
                "\"The apartment is ready now? I'll need funds. When do I start?\"", # E3
            ]
            # --- Calculate Box Positions (Horizontal Boxes Stacked Vertically) ---
            num_boxes = len(choice_options)
            horizontal_margin = 10 # Margin from screen edge
            box_w = pyxel.width - (horizontal_margin * 2) # Make boxes wide
            box_h = 30 # Adjust height for 2-3 lines of text
            vertical_gap = 8 # Gap between boxes
            # Calculate total height needed to center the block of boxes
            total_boxes_height = (num_boxes * box_h) + ((num_boxes - 1) * vertical_gap)
            start_y = (pyxel.height - total_boxes_height) // 2
            # Fixed horizontal position for all boxes
            box_x = horizontal_margin

            # You might want to store these boxes in self.choice_boxes in __init__
            # and calculate only once, or recalculate here each frame.
            # For click detection in self.update, you'll need these calculated boxes.
            # Let's assume self.choice_boxes = [] is done elsewhere or calculated here:
            # self.choice_boxes = [] # Recalculate boxes for click detection
            current_y = start_y

            # --- Draw Boxes and Text ---
            for i, option_text in enumerate(choice_options):
                # Current box Y position
                current_box_y = current_y
                # Store calculated box for click detection in update (if not done elsewhere)
                # self.choice_boxes.append([box_x, current_box_y, box_w, box_h])
                # Highlight box on hover
                mx, my = pyxel.mouse_x, pyxel.mouse_y
                border_col = 7 # Default white border
                fill_col = 1 # Dark Blue fill
                text_col = 7 # White text
                # Check hover using the current box's Y position
                if box_x <= mx < box_x + box_w and current_box_y <= my < current_box_y + box_h:
                    border_col = 10 # Highlight with Yellow border
                    fill_col = 5 # Dark Purple fill
                    text_col = 10 # Yellow text
                pyxel.rect(box_x, current_box_y, box_w, box_h, fill_col)
                pyxel.rectb(box_x, current_box_y, box_w, box_h, border_col)
                # Display text inside the box using modified displayText
                text_margin_x = 4 # Slightly more horizontal margin inside the box
                text_margin_y = 4 # Vertical margin inside the box
                # Calculate max chars based on the NEW wider box width
                max_chars = (box_w - text_margin_x * 2) // 4 # Approx chars per line (default font: 4px wide)
                line_h = 8 # Smaller line height for options text

                self.displayText(option_text, # Line text
                                text_col,      # Color
                                box_x + text_margin_x, # start_x
                                current_box_y + text_margin_y, # start_y
                                max_chars,             # max_width_chars
                                line_h                 # line_height
                                )
                # Update Y position for the next box
                current_y += box_h + vertical_gap
            if self.choices==[]:
                self.openChoice=True
    
    def draw(self):
        if(self.clickCount<len(self.opener)):
            pyxel.cls(13)
            pyxel.rect(10,75,140,8,7)
            if len(self.opener[self.clickCount])<35:
                pyxel.text(80-2*len(self.opener[self.clickCount]), 90,(self.opener[self.clickCount]), 0)
            else:
                strAsList=self.opener[self.clickCount].split(' ')
                curCharCount=0
                stringPt1=''
                stringPt2=''
                stringPt3=''
                for word in strAsList:
                    if curCharCount+len(word)+1<30:
                        stringPt1+=word+' '
                        curCharCount+=len(word)

                    elif curCharCount+len(word)+1>30 and curCharCount+len(word)+1<56:
                        stringPt2+=word+' '
                        curCharCount+=len(word)
                        
                    elif curCharCount+len(word)+1<81:
                        stringPt3+=word+' '
                        curCharCount+=len(word)
                    else:
                        pass
                pyxel.text(10,90,stringPt1,0)
                pyxel.text(10,100,stringPt2,0)
                pyxel.text(10,110,stringPt3,0)
        elif self.clickCount<len(self.opener)+1 and self.clickCount>len(self.opener)-1:
            pyxel.cls(7)
            pyxel.text(70,30,"Ghosts",5)
            pyxel.text(2.5,50,"A visual novel game by Nadir Elyaddasse",5)
            pyxel.text(15,60,"Based on the novel by Paul Austere",5)
            self.noGoingBack=True
        else:
            self.scene1()

    #slide function takes: 
    #   speaker(object with shape and color)
    #   line of text

App()
