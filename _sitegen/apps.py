# Prater Apps catalogue: one entry per App Store app, plus PluggedIn (coming soon).
# accent = brand color, deep = dark hero color, tint = light card color, ink = text on accent.
APPS = [
    dict(id=6759991282, slug="yappp", name="YAPPP", full="YAPPP - AAC", tagline="Accessible speech tiles for everyday communication.",
         cat="Communication", accent="#8B5CF6", deep="#1A1238", tint="#EDE4FF", featured=1),
    dict(id=6758161277, slug="passee", name="PASSEE", tagline="Greeting cards that move. Turn your photos into beautiful postcards.",
         cat="Social", accent="#E8734A", deep="#13202B", tint="#FFE9DD", featured=2),
    dict(id=6801964305, slug="hawt-potato", name="Hawt Potato", full="HAWT POTATO", tagline="A fast, fun hot-potato party game.",
         cat="Games", accent="#F26B1D", deep="#3A1406", tint="#FFE4CC", featured=3),
    dict(id=6762436895, slug="aucommadate", name="Au'commadate", tagline="A touch-only communication board and family support app.",
         cat="Communication", accent="#1074F2", deep="#062A5C", tint="#DDEBFF"),
    dict(id=6800102822, slug="storeemail", name="StoreeMail", tagline="Your email, told as stories you can watch and hear.",
         cat="Productivity", accent="#7C4DFF", deep="#170F33", tint="#ECE4FF"),
    dict(id=6808848853, slug="ahem", name="Ahem.", tagline="Video messages in your own voice, for when a text isn't enough.",
         cat="Communication", accent="#E07B2E", deep="#140D08", tint="#FBE6D3"),
    dict(id=6757371181, slug="wis", name="W.I.S.", tagline="Who Is Speaking: say what you mean, and be heard.",
         cat="Communication", accent="#4A6CF7", deep="#141933", tint="#E2E8FF"),
    dict(id=6761792393, slug="who-is-talking", name="WHO IS TALKING2?", tagline="See the shape of a conversation, not just the words.",
         cat="Communication", accent="#A43CC4", deep="#24103A", tint="#F3E3FA"),
    dict(id=6762071288, slug="checkfineprint", name="CHECKFINEPRINT", tagline="Read contracts and long forms before you sign.",
         cat="Productivity", accent="#2F5BD8", deep="#0F1C45", tint="#E1E9FF"),
    dict(id=6829661621, slug="checktheshelf", name="CHECKTHESHELF", tagline="Before you buy it, check it. Recalls and date codes in a scan.",
         cat="Productivity", accent="#E3263A", deep="#14224F", tint="#FFE3E6"),
    dict(id=6826647627, slug="truss", name="TRUSS", full="TRUSS: Crew Push to Talk", tagline="Crew push-to-talk that runs the whole production day.",
         cat="Productivity", accent="#D4A62A", deep="#1A1814", tint="#F8EFD6"),
    dict(id=6807252430, slug="pewhipee", name="PeWhipee", tagline="Memory games made from your own photos.",
         cat="Games", accent="#D9608E", deep="#3A1426", tint="#FBE1EB"),
    dict(id=6762622197, slug="double-jumpx", name="Double Jumpx", tagline="A stylish jump-rope rhythm game.",
         cat="Games", accent="#E23CC8", deep="#1C1240", tint="#FCE0F6"),
    dict(id=6804324442, slug="wink-one", name="Wink One", tagline="Note-passing for real life.",
         cat="Social", accent="#E9A93A", deep="#1C2A60", tint="#FCEFD8"),
    dict(id=6758415886, slug="roozer-signals", name="ROOZER!", tagline="Send energy, mood and reaction without typing a paragraph.",
         cat="Social", accent="#F0A030", deep="#24160A", tint="#FDEBD0"),
    dict(id=6758159950, slug="roozer", name="ROOZER", tagline="Face, eye and voice challenge games. Don't flinch.",
         cat="Games", accent="#C9A45C", deep="#111111", tint="#F3EBDA"),
    dict(id=6757205397, slug="gee-14", name="GEE-14", tagline="Don't Flinch: fast reflex and focus games.",
         cat="Games", accent="#F2600C", deep="#2A0B02", tint="#FFE2D2"),
    dict(id=6825290820, slug="honey-badger", name="Honey Badger", full="HoneyBadger Game", tagline="Honey Badger: The Last Hive. A cartoon action adventure.",
         cat="Games", accent="#E0A82E", deep="#1A1A1A", tint="#F8EDD3"),
    # No local image files yet: icon and screenshots load from the App Store until copies are added to assets/apps/gormee/.
    dict(id=6758402171, slug="gormee", name="GORMEE", tagline="Scan, save and check receipts, labels and warranty terms.",
         cat="Productivity", accent="#1FA8E0", deep="#06283D", tint="#DCF2FB",
         icon_url="https://is1-ssl.mzstatic.com/image/thumb/Purple221/v4/7c/cc/d1/7cccd14c-9f1e-c337-d316-310c2390a028/AppIcon-0-0-1x_U007epad-0-1-85-220.png/512x512bb.jpg",
         shot_urls=["https://is1-ssl.mzstatic.com/image/thumb/PurpleSource221/v4/24/15/c2/2415c24e-0265-0c76-7622-0c69ffc571c7/GORMEE-iPhone-01-Scan-1206x2622.png/600x1304bb.jpg",
                    "https://is1-ssl.mzstatic.com/image/thumb/PurpleSource211/v4/7d/06/ac/7d06acef-f737-9e6c-6d7a-6708c60a2ac3/GORMEE-iPhone-02-Tools-1206x2622.png/600x1304bb.jpg",
                    "https://is1-ssl.mzstatic.com/image/thumb/PurpleSource211/v4/74/aa/7b/74aa7b19-211a-a1a2-e99b-a5121e93c10d/GORMEE-iPhone-03-Receipt-Import-1206x2622.png/600x1304bb.jpg"]),
]

PLUGGEDIN = dict(slug="pluggedin", name="PluggedIn", tagline="Hire local help or earn on your schedule. Every job verified.",
                 cat="Productivity", accent="#FFD60A", deep="#111111", tint="#FFF4BF", url="/pluggedin/", soon=True)

# Coming-soon apps (not on the App Store yet). Each gets a page at /apps/<slug>/.
# about = list of (heading, paragraph or list of bullets). platforms = where it will run.
SOON = [
    dict(slug="owwl", name="OWWL", tagline="Private messaging you can answer with your face.",
         cat="Social", accent="#F2B84B", deep="#0E1330", tint="#E9EAF8", soon=True, platforms=["iPhone", "iPad"],
         about=[
             ("", "OWWL is a private messenger built around hands-free replies. Raise your eyebrows, smile or blink, and OWWL sends your answer. It is for the moments when your hands are full, and for people who find typing hard."),
             ("What we're building", [
                 "Reply with a simple face gesture, picked from a library of gestures",
                 "Gestures simple enough for a kid to understand without a lesson",
                 "Pseudonymous channels, with no phone number or email needed",
                 "Built on iCloud, with no Prater Apps server in the middle",
                 "Nearby device-to-device chat when you're in the same room",
                 "Every channel gets its own name, typeface and mood colors",
             ]),
             ("Status", "OWWL is in development for iPhone and iPad."),
         ]),
    dict(slug="doozer", name="Doozer", tagline="Say it with your face. Messages without typing.",
         cat="Communication", accent="#19B5A5", deep="#062B2E", tint="#D9F5F1", soon=True, platforms=["iPhone"],
         about=[
             ("", "Doozer reads simple face gestures and turns them into words as you make them, so you can write and send a message without typing or speaking out loud."),
             ("Made for", [
                 "People who can't easily type or speak",
                 "Quiet moments when you need to say something without anyone noticing",
                 "Getting a message to someone you trust, fast",
             ]),
             ("What we're building", [
                 "A full-screen composer that opens blank and stays out of your way",
                 "Preset phrases, quick-send and predictive text",
                 "A settings page where you choose what each gesture means",
                 "Support for eye tracking, head tracking and Switch Control",
                 "One trusted contact you pick as your caregiver",
                 "Real two-way conversations, with a text message fallback for people who don't have Doozer",
             ]),
             ("Status", "Doozer is in development for iPhone."),
         ]),
    dict(slug="prater", name="Prater", tagline="One game across your iPhone, Apple Watch and headphones.",
         cat="Games", accent="#FF4F6D", deep="#1A0B1F", tint="#FFE1E7", soon=True,
         platforms=["iPhone", "iPad", "Apple Watch", "Apple TV"],
         about=[
             ("", "Prater turns the devices you already carry into one playground. A sound lands in one ear, a tap lands on your wrist, and you answer by tapping or tilting your phone. Every round gets faster."),
             ("What we're building", [
                 "Crosswire, the first game: answer on the same side, or the opposite side, before time runs out",
                 "Sound cues that work with any Bluetooth headphones, not just AirPods",
                 "Apple Watch taps and wrist controls",
                 "iPhone and iPad motion: lift the side you heard",
                 "Play against a bot or challenge a friend",
                 "Sound packs you choose: music bites, instrumentals and animal sounds",
                 "A short daily reaction check, so you can see your own reflexes over time",
                 "An Apple TV version for the living room",
             ]),
             ("Status", "Prater is in development for iPhone, iPad, Apple Watch and Apple TV."),
         ]),
    dict(slug="heroles", name="HEROLES", tagline="Race the clock through the maze. Heroes against villains.",
         cat="Games", accent="#E5383B", deep="#0B1B3A", tint="#FFE2E2", soon=True, platforms=["iPhone"],
         about=[
             ("", "HEROLES is a timed maze game. Heroes have to reach the safe area before the clock runs out, while the villains hunt them down."),
             ("How it plays", [
                 "Themed mazes with a countdown on every run",
                 "Tag and hide-and-seek inside the maze",
                 "Capture the flag: lose all your flags and you're out",
                 "One player or many",
                 "Kids play the heroes. Parents and loved ones play the villains.",
             ]),
             ("Status", "HEROLES is in development, starting on iPhone."),
         ]),
]

# Apps beyond the iPhone. live=True means the App Store lists that platform today.
WATCH = [
    dict(slug="hawt-potato", live=True, note="The hot-potato party game comes with an Apple Watch app."),
    dict(slug="yappp", live=True, note="Speech tiles for everyday communication, on Apple Watch as well as iPhone, iPad, Mac and CarPlay."),
    dict(slug="truss", live=True, note="Push-to-talk, the time clock and fall detection, right from the wrist."),
    dict(slug="passee", live=True, note="Moving greeting cards on iPhone, iPad and Apple Watch, kept in sync with iCloud."),
    dict(slug="prater", live=False, note="Built around the Watch: taps on your wrist are part of the game."),
]
TV = [
    dict(slug="hawt-potato", live=True, note="The party game has an Apple TV app, so the whole room can play along."),
    dict(slug="honey-badger", live=True, note="Honey Badger: The Last Hive, a cartoon action adventure you can play on the big screen."),
    dict(slug="prater", live=False, note="An Apple TV version is planned for the first release."),
]
