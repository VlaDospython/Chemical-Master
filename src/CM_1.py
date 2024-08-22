from tkinter import *
from tkinter import filedialog
import random
import time
from PIL import ImageTk, Image
import pygame
import pyperclip
# from tkinter import ttk


def digital_print_onlabel(text: str, label: Label, window: Toplevel | None):
    for i, c in enumerate(text, 1):
        label.config(text=text[:i])
        window.update()
        time.sleep(0.042)
    label.config(text=text)


def play_sound(sound_: str):
    """
    Відтворення звуку на окремому звуковому каналі
    :param sound_: шлях до звуку
    :return: програє звук
    """
    pygame.mixer.Sound(sound_).play()


def play_background_music(music: str):
    pygame.mixer.music.load(music)  # ваша фонова музика
    pygame.mixer.music.set_volume(0.5)  # призначення гучності фонової музики
    pygame.mixer.music.play(loops=-1)  # loops=-1 означає нескінченне відтворення


def fade_out_music(duration):
    current_volume = pygame.mixer.music.get_volume()

    # Обчислюємо кількість кроків затухання
    steps = int(duration * 1000 / 10)  # Переводимо секунди в мілісекунди та ділимо на 10 мілісекунд кожен крок

    # Зменшуємо гучність протягом вказаного часу
    def decrease_volume(step):
        nonlocal current_volume
        current_volume -= 1 / steps
        pygame.mixer.music.set_volume(max(current_volume, 0))  # Обмежуємо гучність від 0 до 1
        if step < steps:
            root.after(10, decrease_volume, step + 1)

    decrease_volume(0)


def fade_in_music(duration):
    current_volume = pygame.mixer.music.get_volume()
    max_volume = 0.5

    steps = int(duration * 1000 / 10)  # Переводимо секунди в мілісекунди та ділимо на 10 мілісекунд кожен крок

    def increase_volume(step):
        nonlocal current_volume
        current_volume += 1 / steps
        pygame.mixer.music.set_volume(min(current_volume, max_volume))
        if step < steps:
            root.after(10, increase_volume, step + 1)

    increase_volume(0)


def set_all_channels_volume_to_zero():
    for i in range(pygame.mixer.get_num_channels()):
        channel = pygame.mixer.Channel(i)
        channel.set_volume(0)

    pygame.mixer.music.set_volume(0)


class AnimateGifLabel(Label):
    def __init__(self, *argv, image = None,  **kwargs):
        self.master = argv[0]
        self.filename = image
        self.check_cadrs()
        self.i = 0
        self.img = Image.open(image)
        self.img.seek(0)
        self.image = ImageTk.PhotoImage(self.img)
        super().__init__(*argv, image = self.image, **kwargs)
        if 'delay' in kwargs:
            self.delay = kwargs['delay']
        else:
            try:
                self.delay = self.img.info['duration']
            except:
                self.delay = 1
        self.after(self.delay, self.show_new_cadr)

    def check_cadrs(self):
        self.cadrs = Image.open(self.filename).n_frames

    def show_new_cadr(self):
        if self.i == self.cadrs:
            self.i = 0
        self.img.seek(self.i)
        self.image = ImageTk.PhotoImage(self.img)
        self.config(image=self.image)
        self.i += 1
        self.master.after(self.delay, self.show_new_cadr)


def set_user_music():
    play_background_music(filedialog.askopenfilename(filetypes=(('Music (mp3, wav)', '*.mp3'), ('All files', '*.*'))))



class Chemical_Master:
    def __init__(self, root):
        self.root = root
        pygame.init()
        pygame.mixer.init()
        self.version = "CM 3.1.1"
        self.root.title("Chemical Master")
        self.root.resizable(False, False)
        self.root.attributes("-topmost", True)
        self.root.iconbitmap("../res/pictures/icons/icon.ico")
        self.window_width = 900
        self.window_height = 600
        self.root_x = (self.root.winfo_screenwidth() - self.window_width) // 2
        self.root_y = (self.root.winfo_screenheight() - self.window_height) // 2
        self.root.geometry(f"{self.window_width}x{self.window_height}+{self.root_x}+{self.root_y - 25}")
        self.gif = AnimateGifLabel(root, image="../res/GIF/ODM.gif")
        self.gif.pack()
        self.board_size = 3
        self.popup_width = 700
        self.popup_height = 200
        self.index = 0
        self.photo_label_width = 300
        self.photo_label_height = 172
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.delay = 700
        self.time_of_GIF = 6500
        self.correct_answer_sound = "../res/sounds/correct_answer_sound.wav"
        self.incorrect_answer_sound = "../res/sounds/incorrect_answer_sound.mp3"
        self.end_of_game_sound = "../res/sounds/end_of_game_sound.mp3"
        self.start_game_sound = "../res/sounds/start_game_sound.mp3"
        self.background_music_1 = "../res/sounds/background_music/background_music.mp3"
        self.close_game_sound = "../res/sounds/close_game_sound.mp3"
        self.gmail = 'odmcmquestion@gmail.com'
        self.time_to_answers = 45
        self.study_variant_flag = False
        self.index_of_window = 0
        self.moved = False  # Змінна для відстеження руху вікна
        self.var = IntVar()
        self.var.set(0)
        # self.style = ttk.Style()
        # self.style.theme_use('classic')
        # self.style.configure("red.Horizontal.TProgressbar", foreground='PaleGreen3', background='PaleGreen3')
        self.autors_text = ("Учні 8-В класу СШ №304, м.Київ:\nМоскаленко Влад - розробник коду Python, генератор ідей\n"
                            "Орлов Георгій - інформація про хімічні сполуки\nДанилейко Данило - фото хімічних сполук\n\nДата випуску - 18.03.2024"
                            "\n \nРозробник: ODM Game World; Видавець: ODM Game World;\n ©ODM Game World\n"
                            f"\nЗ приводу питань і пропозицій звертайтеся за поштою:\n{self.gmail}")

        self.describe_salt_str = ("Со́лі — хімічні речовини йонної будови, до складу яких\n"
                                  "входять кислотні залишки, поєднані з катіонами різного походження.\n"
                                  "Утворюються солі внаслідок реакції нейтралізації кислот та основ.\n"
                                  "Як правило, солі є кристалічними речовинами. Найпростіший приклад\n"
                                  "солі — кухонна сіль, хімічна формула якої — NaCl.")
        self.describe_acid_str = ("Кислотами називають складні речовини, що складаються\n"
                                  "з атомів Гідрогену, які можуть заміщуватися\n"
                                  "металами, і кислотних залишків. Кислотним залишком\n"
                                  "називають частину молекули кислоти, сполучену з атомами Гідрогену.")
        self.describe_oxide_str = ("Оксидами називають бінарні сполуки, які складаються з двох\n"
                                   "хімічних елементів, одним з яких є Оксиген. В оксидах\n"
                                   "хімічний елемент Оксиген має ступінь окиснення -2.\n"
                                   "Оксиди — досить поширений в природі клас сполук.\n"
                                   "Вони знаходяться в повітрі, поширені в гідросфері і літосфері.")
        self.about_all_in_one_mode_str = ("\nВипробуйте самого себе, спробувавши відгадати одразу\n"
                                          "9 випадкових солей, кислот і оксидів разом!")

        self.salts_dict = {
            "CaSO₄": {
                "correct_name": "Сульфат кальцію",
                "image": "../res/pictures/salts_pictures/CaSO4.jpg",
                "description": "Речовина є білими, гігроскопічними кристалами, малорозчинними у воді, неорганічна сполука. Сульфат кальцію переважно застосовується у виготовленні будівельних матеріалів, зокрема як компонент цементів. Також він використовується як осушувач, кальцієвмісна харчова добавка, добриво. Також сульфат кальцію перебуває у морській воді."
            },
            "MgSO₄": {
                "correct_name": "Сульфат магнію",
                "image": "../res/pictures/salts_pictures/MgSO4.jpg",
                "description": "Високоефективне добриво, як цінне джерело магнію та сірки для широкого спектру сільськогосподарських культур. Сульфат магнію швидко і повністю розчиняється у воді."
                               "Сульфат магнію ідеально підходить для застосування в овочівництві відкритого та захищеного ґрунту."
            },
            "KI": {
                "correct_name": "Йодид калію",
                "image": "../res/pictures/salts_pictures/KI.jpg",
                "description": "Речовина є безбарвними кристалами, які добре розчиняються у воді. Незначною мірою йодид калію поширений у морських водоростях. Йодид калію використовується як лікарський засіб при йододефіцитних захворюваннях, для захисту щитоподібної залози від впливу радіоактивного йоду-131. Також KI застосовується як харчова добавка (наприклад, до кухонної солі) та у фотографічній справі."
            },
            "CaCl₂": {
                "correct_name": "Кальцій хлористий",
                "image": "../res/pictures/salts_pictures/CaCl2.jpg",
                "description": "Біла неорганічна речовина, кальцієва сіль. Ця речовина має широкий спектр застосування: як харчова добавка Е509: для пом'якшення м'яса, для консервації фруктів та овочів, в полочному виробництві тощо;в лабораторії - для наповнення осушуючих трубок для осушки газів від водяних парів;в будівництві - як прискорювач процесу твердіння бетонів; при виготовленні силікатної цегли, тротуарної плитки;як засіб проти ожеледиці взимку;як засіб для знепилення грунтових доріг."
            },
            "K₂CO₃": {
                "correct_name": "Карбонат калію",
                "image": "../res/pictures/salts_pictures/K2CO3.jpg",
                "description": "Застосовується в сільськ.госп. - для дезінфекції приміщень, призначених для утримання худоби і птиці та як калійне добриво, в будівництві - використовують як антифриз, тому додається в цементні і бетонні суміші, тому процес зведення будівлі може здійснюватися навіть при -50°С. У виробництві скла - в якості сировини для виробництва скляної оболонки кінескопа та спеціальних скляних матеріалів, оптичного скла, скла для відеоекранів телевізорів і комп'ютерів, а також лабораторного посуду."
            },
            "Na₂SiO₃": {
                "correct_name": "Силікат натрію",
                "image": "../res/pictures/salts_pictures/Na2SiO3.jpg",
                "description": "За звичайних умов є білою, аморфною речовиною, що плавиться без розкладання. Силікат натрію є переважно компонентом, аніж реактантом. Маючи сильнолужну реакцію, основна його частина застосовується у виготовленні мила й детергентів. У харчовій промисловості силікат натрію використовується як антиспікаючий агент і зареєстрований у системі харчових добавок за номером E550."
            },
            "KNO₃": {
                "correct_name": "Нітрат калію",
                "image": "../res/pictures/salts_pictures/KNO3.jpg",
                "description": "Використовується, як натрієва селітра, для отримання азотної кислоти та інших нітро-з'єднань, азотних добрив і у виробництві вибухових речовин."
            },
            "NiCl₂": {
                "correct_name": "Хлорид нікелю",
                "image": "../res/pictures/salts_pictures/NiCl2.jpg",
                "description": "Неорганічна сіль. При тривалому контакті може викликати інтоксикацію і, ймовірно, рак. Безводний хлорид нікелю жовтий, але комерційний продукт, який випускається у формі гексагідрату (+ 6H₂O), має зелений колір. Хлориди нікелю - це тверді кристалічні речовини, гігроскопічні, абсорбують вологу з повітря. Розчини нікелю (II) хлористого мають досить кислу реакцію, з рН близько 4. Найчастіше хлорид нікелю виробляють із залишків, отриманих при випаленні нікелевих руд."
            },
            "NaCl": {
                "correct_name": "Кухонна сіль",
                "image": "../res/pictures/salts_pictures/NaCl.jpg",
                "description": "Життєво необхідна для життєдіяльності людини, так само як усіх інших живих істот. Вона бере участь у підтриманні та регулюванні водно-сольового балансу в організмі, натрій-калієвого іонного обміну."
            },
            "KCl": {
                "correct_name": "Хлорид калію",
                "image": "../res/pictures/salts_pictures/KCl.jpg",
                "description": "Широко застосовується в сільськ.госп. як калійне добриво. Крім того, служить сировиною для одержання гідроксиду калію та інших сполук калію. Іноді застосовується як добавка до кухонної солі (так звана «сіль з пониженим вмістом натрію»)."
            },
            "Na₂S": {
                "correct_name": "Сульфід натрію",
                "image": "../res/pictures/salts_pictures/Na2S.jpg",
                "description": "Середня натрієва сіль сульфідної кислоти. Сульфід натрію отримують при сплавленні сульфату натрію з кам'яним вугіллям або коксом при температурі 900°C. Має широке застосування як компонент складу для вичинки шкір при підготовці до дублення, також у фарбуванні, при виготовленню паперу, очищення стічних вод, застосовується в процесі виробництва целюлози, а також барвників і пігментів."
            },
            "NaBr": {
                "correct_name": "Бромід натрію",
                "image": "../res/pictures/salts_pictures/NaBr.jpg",
                "description": "Неорганічна бінарна сполука, середня сіль лужного металу натрію та бромистоводневої кислоти. Білий кристалічний порошок без запаху, солоного смаку. Бромід натрію нетоксичний. Однак передозування бромідів в організмі небезпечне. Застосовують препарати брому при неврастенії, неврозах, істерії, підвищеній дратівливості, безсонні, початкових формах гіпертонічної хвороби, а також при епілепсії та хореї. Може посилювати процеси гальмування в корі великого мозку."
            },
            "NaF": {
                "correct_name": "Фторид натрію",
                "image": "../res/pictures/salts_pictures/NaF.jpg",
                "description": "Неорганічна кристалічна речовина. Білий порошок, який не має запаху. Додається до води (фторування води) та зубної пасти для укріплення зубної емалі, як миючий засіб, антисептик; в хімічній промисловості для синтезу (зокрема фреонів), а також в металургії та біохімії; як компонент речовин для очищення та алитірування металів, флюсів для пайки та переплавки металів, скла, кераміки, вогнетривів, кислототривкого цементу, термостійких мастил, речовин для травлення скла, твердих електролітів."
            },
            "PbS": {
                "correct_name": "Плюмбум сульфід",
                "image": "../res/pictures/salts_pictures/PbS.jpg",
                "description": "Розчин солі на водній основі, який широко використовується в культурі клітин, наприклад, для підтримання рН, розведення речовин або промивання клітинних контейнерів, нетоксичний і забезпечує клітини водою та неорганічними іонами, необхідними для клітинного метаболізму."
            },
            "AlCl₃": {
                "correct_name": "Хлорид алюмінію",
                "image": "../res/pictures/salts_pictures/AlCl3.JPG",
                "description": "Містить лише слідові кількості чистого алюмінію. Він найчастіше використовується в антиперспірантах і дезодорантах (і деяких ліках) з великими показниками безпеки."
            },
            "KMnO₄": {
                "correct_name": "Перманганат калію",
                "image": "../res/pictures/salts_pictures/KMnO4.jpg",
                "description": "Калію перманганат – сильний окиснювач. У присутності органічних речовин, що легко окиснюються (компоненти тканин, гнійні виділення), легко відщеплює кисень і перетворюється у діоксид марганцю, який залежно від концентрації розчину проявляє в'яжучу, подразнювальну, припікальну дію."
            },
            "CaF₂": {
                "correct_name": "Фторид кальцію",
                "image": "../res/pictures/salts_pictures/CaF2.jpg",
                "description": "Кристали кальцію прозорі у діапазоні широкого спектра. Продукт знаходить застосування у вікнах, лінзах, що працюють у смузі УФ і ІЧ спектрів. Лазерне використання: фторид кальцію також використовується як решітка приймача для лазерних кристалів. Завдяки своєму складу, має значно довший термін служби, ніж більшість матеріалів при використанні в середовищі фтору. Фторид кальцію використовується для оптичних вікон, свердлених дисків, лінз і призм."
            },
            "Na₂SO₄": {
                "correct_name": "Сульфат натрію",
                "image": "../res/pictures/salts_pictures/Na2SO4.jpg",
                "description": "Використовується для виробництва паперу за сульфатним методом, у виробництві соди, а також у скляній промисловості, застосовується у виробництві мила, сульфатної целюлози, шкіряної продукції, кольорових металів та для фарбування бавовняного текстилю."
            },
            "MgCO₃": {
                "correct_name": "Карбонат магнію",
                "image": "../res/pictures/salts_pictures/MgCO3.jpg",
                "description": "Неорганічна сполука. За звичайних умов є білими кристалами, що мають діамагнітні властивості. У холодній воді він не розчиняється, а в гарячій переходить у гідроксокарбонат. Застосовується у виготовленні вогнетривких матеріалів, пігментів."
            },
            "CuSO₄": {
                "correct_name": "Купрум сульфат",
                "image": "../res/pictures/salts_pictures/CuSO4.jpg",
                "description": "Сульфат міді, мідний купорос — сіль міді сірчаної кислоти, в безводному стані, біла дрібнокристалічна речовина, при поглинанні води стає синьою або блакитною. Добре розчиняється у воді. З водного розчину кристалізується у вигляді кристалогідрату синього кольору, відомого під назвою мідний купорос."
            },
            "Na₃PO₄": {
                "correct_name": "Ортофосфат натрію",
                "image": "../res/pictures/salts_pictures/Na3PO4.jpg",
                "description": "Це неорганічна сполука, біла гранульована або кристалічна тверда речовина, добре розчинна у воді, утворюючи лужний розчин. Використовується як миючий засіб, наповнювач, мастило, харчова добавка, засіб для виведення плям і знежирювач."
            },
            "BaCO₃": {
                "correct_name": "Карбонат барію",
                "image": "../res/pictures/salts_pictures/BaCO3.jpg",
                "description": "За звичайних умов є білими, малорозчинними у воді кристалами. У природі сполука поширена у вигляді мінералів вітериту й альстоніту. Застосовується у виробництві скла, цегли і бетону, магнітних матеріалів, у фотографії."
            },
            "MgCl₂": {
                "correct_name": "Хлорид магнію",
                "image": "../res/pictures/salts_pictures/MgCl2.jpg",
                "description": "Ці солі є типовими іонними галогенідами, добре розчинними у воді. Хлорид магнію можна добути з розсолу або морської води. Застосовують головним чином у виробництві металевого магнію. Також використовується для обробки крижаного і сніжного покрову. У результаті реакції зі снігом викликає його танення. В медицині хлорид магнію застосовується як послаблюючий засіб. Хлорид магнію зареєстрований як харчова добавка за номером E511."
            },
            "K₃PO₄": {
                "correct_name": "Ортофосфат калію",
                "image": "../res/pictures/salts_pictures/K3PO4.jpg",
                "description": "Використовується як добриво в сільському господарстві для підживлення рослин калієм та фосфором. Сприяє збільшенню врожайності та покращенню якості плодів. Ортофосфат калію також використовується в синтезі органічних реактивів та в харчовій промисловості як добавка для регулювання pH."
            },
            "BaZrO₃": {
                "correct_name": "Цирконат барію",
                "image": "../res/pictures/salts_pictures/BaZrO3.jpg",
                "description": "Неорганічна речовина, відома своєю високою діелектричною проникливістю та стійкістю до високих температур. Властивості цієї сполуки роблять її ідеальним матеріалом для виробництва конденсаторів високої ємності, електролітів для паливних елементів та інших електронних пристроїв, де важлива стабільність у високих температурах та висока діелектрична проникливість."
            },
        }
        self.acid_dict = {
            "HF": {
                "correct_name": "Флуоридна кислота",
                "image": "../res/pictures/acid_pictures/HF.JPG",
                "description": "Флуори́дна кислота (пла́викова кислота́) — розчин фтороводню у воді. Назва «плавикова кислота» походить від плавикового шпату(CaF₂), з якого добувають фтороводень дією сульфатної кислоти(H₂SO₄). "
                               "При контакті зі шкірою спочатку утворюються безболісні опіки, пізніше омертвіння тканин. Може викликати зупинку серця та смерть. "
                               "Використовується як електроліт у літій-іонних акумуляторах. Такі акумулятори застосовуються у різних пристроях, від портативних електронних пристроїв до електромобілів."
            },
            "HCl": {
                "correct_name": "Хлоридна кислота",
                "image": "../res/pictures/acid_pictures/HCl.jpg",
                "description": "Хлоридна кислота має широке застосування у різних галузях. Вона використовується як каталізатор і реактив у хімічних процесах, чистці металів, регулюванні pH, виробництві лікарських засобів, а також у дезінфекції і очищенні. Цей хімічний реагент має важливе значення в промисловості, лабораторіях та комерційних додатках."
            },
            "HBr": {
                "correct_name": "Бромідна кислота",
                "image": "../res/pictures/acid_pictures/HBr.jpg",
                "description": "Має широке застосування у хімічній промисловості та наукових дослідженнях. Вона використовується як каталізатор та реактив у різноманітних хімічних синтезах, таких як синтез органічних сполук, фармацевтичних засобів та пестицидів. Крім того, використовується в електроніці для виробництва напівпровідників та в аналітичних лабораторіях для визначення хімічних складових речовин. Ця кислота грає важливу роль у багатьох галузях."
            },
            "HI": {
                "correct_name": "Йодидна кислота",
                "image": "../res/pictures/acid_pictures/HI.jpg",
                "description": "Сильна одноосновна, безоксигенова кислота. Утворює солі - йодиди. Чиста кислота - безбарвна, але під дією світла, внаслідок окиснення та виділення йоду, набуває жовтого чи бурого кольору. Відіграє ключову роль у хімічних реакціях та синтезі. Одним із застосувань є використання її у виробництві йодованих сполук, які широко використовуються у медицині та фармації. Крім того, може використовуватися як джерело йоду в хімічних аналізах та дослідженнях."
            },
            "H₂S": {
                "correct_name": "Сульфідна кислота",
                "image": "../res/pictures/acid_pictures/H2S.jpg",
                "description": "Ця кислота дуже слабка. Відіграє важливу роль у багатьох сферах. Одне із застосувань полягає у використанні її у виробництві сульфідів, які знаходять широке застосування у виробництві різних матеріалів, включаючи метали і пластмаси. Також може використовуватися в якості джерела сірки в хімічних процесах. Вона також застосовується в якості каталізатора у деяких хімічних реакціях."
            },
            "H₂SO₄": {
                "correct_name": "Сульфатна кислота",
                "image": "../res/pictures/acid_pictures/H2SO4.jpg",
                "description": "Сульфа́тна кислота́ (сірчана кислота) — безбарвна масляниста, дуже в'язка і гігроскопічна рідина. Одна з найсильніших неорганічних кислот і є дуже їдкою та небезпечною. Сірчана кислота є однією з найважливіших технічних речовин у світі і лідирує за кількістю виробництва. Вона використовується в основному у формі водних розчинів для виробництва добрив, як каталізатор в органічних синтезах, а також у виробництві інших неорганічних кислот."
            },
            "HNO₃": {
                "correct_name": "Нітратна кислота",
                "image": "../res/pictures/acid_pictures/HNO3.jpg",
                "description": "Сильна одноосновна кислота. Висококорозійна кислота, реагує з більшістю металів, сильний окисник. Має тенденцію набувати жовтого відтінку через накопичення оксидів азоту, при довгому зберіганні. Зазвичай азотна кислота має концентрацію 68 %, оскільки саме таким є склад її азеотропної суміші з водою. Якщо ж концентрація перевищує 86 %, то вона називається димною кислотою. В залежності від кольору «диму» концентрована кислота поділяється на білу та червону в концентрації, більшій за 95 %."
            },
            "HNO₂": {
                "correct_name": "Нітритна кислота",
                "image": "../res/pictures/acid_pictures/HNO2.jpg",
                "description": "Одноосновна слабка кислота, відома лише в розбавлених водних розчинах та в газовій формі. Солі азотистої кислоти називаються нітритами. Нітрити набагато стійкіші, ніж сама кислота, всі вони токсичні. Використовується у промисловості та харчовій галузі як консервант у харчових продуктах, а також у виробництві кольорових фарб, де вона виступає як окислювач і реагент у хімічних процесах. В медицині вона може використовуватися у лікуванні інфекцій та вірусів."
            },
            "H₂CrO₄": {
                "correct_name": "Хромова кислота",
                "image": "../res/pictures/acid_pictures/H2CrO4.jpg",
                "description": "Хромова кислота – кристалічна речовина червоного кольору. Зазвичай не існує у вільній формі, оскільки вона є нестійкою та легко розкладається. Замість цього, її солі та похідні широко використовуються в хімічній промисловості та лабораторіях. Хромова кислота є сильною кислотою, може виступати як окислювач у реакціях."
            },
            "Н₃PO₄": {
                "correct_name": "Ортофосфатна кислота",
                "image": "../res/pictures/acid_pictures/H3PO4.jpg",
                "description": "За кімнатної температури є білою кристалічною речовиною, а при нагріванні до 42,35 °C перетворюється на безбарвну в'язку рідину. Широко застосовується для отримання мінеральних добрив, для створення захисних покриттів, у виробництві косметики та скла. На відміну від багатьох сполук фосфору, ортофосфатна кислота не отруйна."
            },
        }
        self.oxide_dict = {
            "CO": {
                "correct_name": "Карбон (II) оксид",
                "image": "../res/pictures/oxide_pictures/CO.jpg",
                "description": "Карбон II оксид(монооксид карбону, чадни́й газ) — безбарвний, дуже отруйний газ без запаху. Утворюється внаслідок неповного згоряння пального в автомобільних двигунах та опалюваних приладах, які працюють на вугіллі або на інших видах природного палива. Важливий у фотосинтезі"
            },
            "CO₂": {
                "correct_name": "Карбон (IV) оксид",
                "image": "../res/pictures/oxide_pictures/CO2.jpg",
                "description": "Безбарвний газ без запаху. Він приблизно у 1,5 рази важчий за повітря. Є малорозчинним у воді. Газовий складник атмосфери Землі, головний газовий викид у результаті спалювання вуглеводнів."
            },
            "NO": {
                "correct_name": "Нітроген (II) оксид",
                "image": "../res/pictures/oxide_pictures/NO.png",
                "description": "Нітроген (II) оксид (оксид азоту II) — неорганічна сполука. За звичайних умов є безбарвним, токсичним і незаймистим газом, що утворюється під час горіння в атмосфері. Використовується у виробництві аміаку(NH₃) та інших хімічних сполук."
            },
            "NO₂": {
                "correct_name": "Нітроген (IV) оксид",
                "image": "../res/pictures/oxide_pictures/NO2.jpg",
                "description": "За звичайних умов є газом червоно-бурого кольору, з характерним гострим запахом або жовтуватою рідиною. Газовий продукт згорання палива, головний забруднювач атмосфери, спричиняє смог та кислотний дощ."
            },
            "SO₂": {
                "correct_name": "Сульфур (IV) оксид",
                "image": "../res/pictures/oxide_pictures/SO2.jpg",
                "description": "За звичайних умов це безбарвний газ з різким задушливим запахом. Проявляє доволі сильні відновні властивості. Використовується у синтезі сульфатної кислоти, а також як відбілювач і для обробки приміщень від шкідників. Важчий від повітря більш ніж удвічі. Утворюється під час згоряння сірки у вугіллі та нафтопродуктах. Спричиняє кислотний дощ та інші екологічні проблеми."
            },
            "SiO₂": {
                "correct_name": "Силіцій (IV) оксид",
                "image": "../res/pictures/oxide_pictures/SiO2.jpg",
                "description": "Кремнезем — один з найважливіших і найпоширеніших мінералів силіцію(кремнію). У природі буває у вигляді кварцу, гірського кришталю тощо. Використовується у виробництві скла, кераміки, бетону та інших матеріалів."
            },
            "Al₂O₃": {
                "correct_name": "Оксид алюмінію",
                "image": "../res/pictures/oxide_pictures/Al2O3.jpg",
                "description": "Являє собою білі кристали, хімічно дуже стійкі, температура плавлення 2050 °C. У воді оксид алюмінію не розчиняється і не взаємодіє з нею. Проявляє амфотерні властивості. Алюміній має високу хімічну активність і тому в природі зустрічається тільки у зв'язаному стані, у формі різних мінералів (корунд, рубін, сапфір) і гірських порід. Близько 250 різних мінералів містять алюміній. Сполуку застосовують для одержання алюмінію, виготовлення вогнетривів, каталізаторів, сорбентів тощо."
            },
            "CaO": {
                "correct_name": "Кальцій оксид",
                "image": "../res/pictures/oxide_pictures/CaO.jpg",
                "description": "Кальцій оксид (негашене вапно) — неорганічна бінарна сполука кальцію та кисню. В'язка мінеральна кристалічна тугоплавка речовина білого кольору. Температура плавлення 2585 °С. Проявляє сильні осно́вні властивості. У техніці оксид кальцію називають зазвичай негашеним, або паленим вапном. Використовується у виробництві цементу, вапняку та інших будівельних матеріалів."
            },
            "P₂O₅": {
                "correct_name": "Фосфор (V) оксид",
                "image": "../res/pictures/oxide_pictures/P2O5.jpg",
                "description": "Найпоширеніший та найважливіший з оксидів фосфору. Утворюється при згорянні фосфору у вигляді білого густого диму, який осідає як пухка снігоподібна маса. Сполука є кислотним оксидом — ангідридом ортофосфатної кислоти. Надзвичайно енергійно сполучається з водою, поглинає вологу з повітря, а також дегідратує деякі інші сполуки. Завдяки цій властивості оксид часто використовується в лабораторіях для осушування різних речовин. Основним застосуванням оксиду є синтез ортофосфатної кислоти."
            },
            "TiO₂": {
                "correct_name": "Титан (IV) оксид",
                "image": "../res/pictures/oxide_pictures/TiO2.jpg",
                "description": "Оксид титану (IV) (харчовий барвник E171) — амфотерний оксид чотиривалентного титану — найважливіший з усіх оксидів цього елементу. Чистий діоксид титану — безбарвні кристали (при нагріванні жовтіють, при охолодженні знебарвлюються). Широко використовується у целюлозній промисловості, у лакофарбовій промисловості, у виробництві гумових виробів, пластмас, термостійкого та оптичного скла, білої емалі, керамічних діелектриків тощо. Може накопичуватися в організмі людини."
            },
            "HgO": {
                "correct_name": "Меркурій (II) оксид",
                "image": "../res/pictures/oxide_pictures/HgO.jpg",
                "description": "Оксид є кристалами жовтого або червоного кольору. Зустрічається у природі у вигляді доволі рідкісного мінералу монтроїдиту. Як і всі сполуки ртуті, оксид має токсичну дію. Потрапляючи до організму людини через шкіру або дихальні шляхи, він може викликати нудоту, діарею, ураження нервової системи."
            },
            "Fe₂O₃": {
                "correct_name": "Ферум (III) оксид",
                "image": "../res/pictures/oxide_pictures/F2O3.jpg",
                "description": "Проявляє слабкі амфотерні властивості. Широко застосовується як пігмент у виготовленні фарб, також використовується у виробництві футеровочної кераміки, цементу й магнітних стрічок. Є найбільш стійкою кисневмісною сполукою заліза з тих, що зустрічаються у природі. Даний оксид поширений не лише у вільному стані, а й у складі залізних руд. До їхнього числа належать, зокрема, мінерали магнетит, гематит, лимоніт тощо."
            },
            "Cr₂O₃": {
                "correct_name": "Хром (III) оксид",
                "image": "../res/pictures/oxide_pictures/Cr2O3.jpg",
                "description": "Являє собою речовину зеленого кольору, з гексагональною будовою кристалів. Проявляє амфотерні властивості. Поширений головним чином у складі мінералу хроміту. Не токсичний, на відміну від інших хромових сполук. Не відіграє ніякої ролі в організмі, при попаданні в очі може тільки подразнювати їх. Є каталізатором процесів окиснення амоніаку на повітрі, отримання альдегідів окисненням вуглеводнів та спиртів, утворення SO3 з SO2 та кисню."
            },
            "Cu₂O": {
                "correct_name": "Купрум (I) оксид",
                "image": "../res/pictures/oxide_pictures/Cu2O.jpg",
                "description": "За звичайних умов є ортогональними кристалами темно-червоного кольору. Проявляє слабкі амфотерні властивості. Застосовується у виробництві пігментів. У природі оксид міді зустрічається у вигляді мінералу куприту, який містить до 88,82% цього оксиду."
            },
            "V₂O₅": {
                "correct_name": "Ванадій (V) оксид",
                "image": "../res/pictures/oxide_pictures/V2O5.jpg",
                "description": "Отруйний порошок без запаху і смаку, малорозчинний у воді. Його колір коливається від помаранчево-жовтого до цегляно-коричневого. Його вдихання серйозно подразнює дихальні шляхи, що може супроводжуватися задишкою і астмою, негативним впливом на легені. Проковтування речовини є потенційно смертельним, потрапивши до організму, вона впливає на ЦНС. При контакті за шкірою може спостерігатися алергічна реакція. Є потенційним канцерогеном."
            },
        }

        self.salts_acids_oxides_dict = {**self.salts_dict, **self.acid_dict, **self.oxide_dict}

        self.main_keys = list(self.salts_acids_oxides_dict.keys())
        random.shuffle(self.main_keys)

        self.salts_acids_oxides_dict_shuffled = {key: self.salts_acids_oxides_dict[key] for key in self.main_keys}

        self.all_dicts = [self.salts_dict, self.acid_dict, self.oxide_dict, self.salts_acids_oxides_dict_shuffled]

        self.canvas = Canvas(root, width=self.window_width, height=self.window_height)
        self.canvas.pack()

        root.after(self.time_of_GIF, self.commands_after_gif)


    # def on_minimize(self, event):
    #     root.iconify()
    #     self.popup.iconify()
    #
    # def on_deiconify(self, event):
    #     root.deiconify()
    #     self.popup.deiconify()

    def commands_after_gif(self):
        self.gif.destroy()
        self.set_picture_on_background("../res/pictures/background_pictures/chemistry_png.jpg")
        self.create_menu()
        self.show_message("Завантаження завершено!\nОберіть режим гри і почніть грати (або вийти)", 3, 700, 170)

        # root.bind("<Unmap>", self.on_minimize)
        # self.popup.bind("<Unmap>", self.on_minimize)
        #
        # root.bind("<Map>", self.on_deiconify)
        # self.popup.bind("<Map>", self.on_deiconify)

    def create_menu(self):
        self.menubar = Menu(self.root)
        self.root.config(menu=self.menubar)

        self.menubar.add_command(label="Про авторів", command=lambda: self.show_message(self.autors_text, 1, 700, 450))

        self.menu_music = Menu(self.menubar, tearoff=0)
        self.menu_music.add_command(label="Вимкнути музику", command=set_all_channels_volume_to_zero)
        self.menu_music.add_command(label="Ввімкнути музику", command=lambda: fade_in_music(1))
        self.menu_music.add_separator()
        self.menu_music.add_command(label="Використати власну музику", command=set_user_music)

        self.menubar.add_cascade(label="Параметри музики", menu=self.menu_music)

    def create_widgets(self):
        self.button_frame = Frame(self.root)
        self.button_frame.place(relx=0.5, rely=0.7, anchor=CENTER)

        self.buttons = [[None] * self.board_size for _ in range(self.board_size)]

        for x in range(self.board_size):
            for y in range(self.board_size):
                self.buttons[x][y] = Button(self.button_frame, font=("Consolas", 22), bg='light yellow', relief=RAISED,
                                            overrelief=GROOVE, bd=3.5, width=10, activebackground='bisque2',
                                            cursor="hand2", command=lambda x=x, y=y: self.check_salt(x, y))
                self.buttons[x][y].grid(row=x, column=y, padx=7, pady=7)

        self.salt_label = Label(root, font=("Consolas", 30), fg='black', bg='khaki2', relief=RIDGE, width=20, bd=4)
        self.salt_label.place(relx=0.5, rely=0.1, anchor=CENTER)

        self.describe_salt_label = Label(root, font=("Consolas", 12), fg='black', bg='grey90', relief=RIDGE, bd=4, wraplength=535, anchor='nw', justify='left', height=9)
        self.describe_salt_label.place(relx=0.685, rely=0.33, anchor=CENTER)

        self.picture_label = Label(root, bd=4, relief=RIDGE)
        self.picture_label.place(relx=0.20, rely=0.33, anchor=CENTER)

        self.score_label = Label(root, text=f" √: {self.correct_answers} ", font=("Consolas", 18), bg='green2',relief=RIDGE)
        self.score_label.place(relx=0.82, rely=0.1, anchor=CENTER)

        self.unscore_label = Label(root, text=f" X: {self.incorrect_answers} ", font=("Consolas", 18), bg='red2',relief=RIDGE)
        self.unscore_label.place(relx=0.92, rely=0.1, anchor=CENTER)

        self.number_of_question_label = Label(root, text=f" № питання {self.index}/9 ", height=1, font=("Consolas", 14), bg='light yellow', relief=RIDGE)
        self.number_of_question_label.place(relx=0.12, rely=0.1, anchor=CENTER)

        self.version_label = Label(root, text=f"Version: {self.version}", font=("Consolas", 10))
        self.version_label.place(relx=0, rely=1, anchor=SW)

        self.countdown_label = Label(root, text="Timer", font=("Consolas", 15), width=14, bd=2, bg='khaki2', highlightbackground="green2", highlightthickness=5, relief=RIDGE)

        self.create_menu()

    def check_salt(self, x: int, y: int):
        def correct():
            self.correct_answers += 1
            self.score_label.config(text=f" √: {self.correct_answers} ")
            self.buttons[x][y].configure(bg='green1')
            play_sound(self.correct_answer_sound)
            self.set_disabled_state_on_button()

        def incorrect():
            self.incorrect_answers += 1
            self.unscore_label.config(text=f" X: {self.incorrect_answers} ")
            self.buttons[x][y].configure(bg='red')
            play_sound(self.incorrect_answer_sound)
            if not self.study_variant_flag:
                self.set_disabled_state_on_button()

        def check():
            if self.all_dicts[self.var.get()][self.buttons[x][y]["text"]]["correct_name"] == self.salt_9_name[self.index]:
                correct()
            else:
                incorrect()

        def set_button_color():
            for x in range(self.board_size):
                for y in range(self.board_size):
                    self.buttons[x][y].config(bg='light yellow')

        if not self.study_variant_flag:
            check()
            self.index += 1
            self.set_original_button_color(x, y)
            root.after(self.delay, self.shuffle_buttons)
            root.after(self.delay, self.set_normal_state_on_button)
        else:
            if self.all_dicts[self.var.get()][self.buttons[x][y]["text"]]["correct_name"] == self.salt_9_name[self.index]:
                correct()
                self.index += 1
                play_sound(self.correct_answer_sound)
                root.after(self.delay, set_button_color)
                root.after(self.delay, self.shuffle_buttons)
                root.after(self.delay, self.set_normal_state_on_button)
            else:
                incorrect()
                self.buttons[x][y].config(state=DISABLED)

        root.after(self.delay, self.update_salt)
        root.after(self.delay, lambda: self.number_of_question_label.config(text=f" № питання {self.index}/9 "))

        if self.index == 9:
            fade_out_music(1.7)
            root.after(self.delay + 1000, self.end_of_game)

    def show_message(self, message: str, number_of_buttons: int, popup_width: int, popup_height):
        self.popup_x = (root.winfo_screenwidth() - popup_width) // 2
        self.popup_y = (root.winfo_screenheight() - popup_height) // 2

        self.popup = Toplevel(root)
        self.popup.title("Chemical_Master: message")
        self.popup.attributes("-topmost", True)
        self.popup.geometry(f"{popup_width}x{popup_height}+{self.popup_x}+{self.popup_y - 50}")
        self.popup.iconbitmap("../res/pictures/icons/icon.ico")
        self.popup.resizable(False, False)

        self.popup.update()
        self.popup.transient(root)

        # Визначення початкового зміщення
        self.delta_x = self.popup.winfo_x() - root.winfo_x()
        self.delta_y = self.popup.winfo_y() - root.winfo_y()

        # Ініціалізація останніх координат
        self.last_x, self.last_y = root.winfo_x(), root.winfo_y()

        # Прив'язка подій до обох вікон
        root.bind("<Configure>", self.sync_windows)
        self.popup.bind("<Configure>", self.sync_windows)

        label = Label(self.popup, text=message, font=("Consolas", 14))
        label.pack(padx=10, pady=10)

        close_button = Button(self.popup, text="Закрити", font=("Consolas", 13), width=20, relief=RAISED,
                              overrelief=GROOVE, bd=3, command=lambda: self.popup.destroy(), cursor="hand2")

        new_game_button = Button(self.popup, text="Нова гра", font=("Consolas", 13), width=20, relief=RAISED,
                                 overrelief=GROOVE, bd=3, command=self.new_game, cursor="hand2")

        button3 = Button(self.popup, text="Навчання", font=("Consolas", 13), width=20, relief=RAISED, overrelief=GROOVE,
                         bd=3, command=self.user_select_section_study, cursor="hand2")

        self.radio_b_1 = Radiobutton(self.popup, text="Солі", variable=self.var, value=0, font=("Consolas", 20),
                                     relief=RAISED, width=17, bd=4, justify=CENTER,
                                     command=self.first_radio_button_change_section, cursor="hand2")
        self.radio_b_2 = Radiobutton(self.popup, text="Кислоти", variable=self.var, value=1, font=("Consolas", 20),
                                     relief=RAISED, width=17, bd=4, justify=CENTER,
                                     command=self.second_radio_button_change_section, cursor="hand2")
        self.radio_b_3 = Radiobutton(self.popup, text="Оксиди", variable=self.var, value=2, font=("Consolas", 20),
                                     relief=RAISED, width=17, bd=4, justify=CENTER,
                                     command=self.third_radio_button_change_section, cursor="hand2")
        self.radio_b_4 = Radiobutton(self.popup, text="Все разом", variable=self.var, value=3, font=("Consolas", 20),
                                     relief=RAISED, width=17, bd=4, justify=CENTER,
                                     command=self.fourth_radio_button_change_section, cursor="hand2")

        if self.var.get() == 0:
            self.first_radio_button_change_section()
        elif self.var.get() == 1:
            self.second_radio_button_change_section()
        elif self.var.get() == 2:
            self.third_radio_button_change_section()
        elif self.var.get() == 3:
            self.fourth_radio_button_change_section()

        self.radio_b_1.bind("<Enter>", self.solt_is)
        self.radio_b_2.bind("<Enter>", self.acid_is)
        self.radio_b_3.bind("<Enter>", self.oxide_is)
        self.radio_b_4.bind("<Enter>", self.all_in_one_mode_is)

        self.radio_b_1.bind("<Leave>", self.mouse_leave_radiobutton)
        self.radio_b_2.bind("<Leave>", self.mouse_leave_radiobutton)
        self.radio_b_3.bind("<Leave>", self.mouse_leave_radiobutton)
        self.radio_b_4.bind("<Leave>", self.mouse_leave_radiobutton)

        if number_of_buttons == 1:
            new_game_button.config(text="Скопіювати", command=lambda: pyperclip.copy(self.gmail))
            new_game_button.pack(side=TOP)
            close_button.pack(side=BOTTOM, pady=12)
        elif number_of_buttons == 2:
            self.popup.title("Chemical_Master: game results")
            new_game_button.pack(pady=10, side=LEFT, padx=50)
            close_button.config(text="Вийти з гри", foreground="OrangeRed4", command=self.close_game)
            close_button.pack(pady=10, side=RIGHT, padx=50)
        elif number_of_buttons == 3:
            self.popup.title("Chemical_Master: new game")
            close_button.config(text="Вийти з гри", foreground="OrangeRed4", command=self.close_game)
            button3.pack(pady=10, side=LEFT, padx=20)
            new_game_button.pack(pady=10, side=LEFT, padx=20)
            new_game_button.config(text="Тест", command=self.user_select_section)
            close_button.pack(pady=10, side=LEFT, padx=20)
        elif number_of_buttons == 4:
            self.radio_b_1.pack(side=TOP, pady=5)
            self.radio_b_2.pack(side=TOP, pady=5)
            self.radio_b_3.pack(side=TOP, pady=5)
            close_button.config(text="Підтвердити", command=self.change_section_2)
            close_button.pack(side=BOTTOM, pady=10)
        elif number_of_buttons == 5:
            self.radio_b_1.pack(side=TOP, pady=5)
            self.radio_b_2.pack(side=TOP, pady=5)
            self.radio_b_3.pack(side=TOP, pady=5)
            self.radio_b_4.pack(side=TOP, pady=5)
            close_button.config(text="Підтвердити", command=self.change_section_1)
            close_button.pack(side=BOTTOM, pady=10)
        elif number_of_buttons == 6:
            self.radio_b_1.pack(side=TOP, pady=5)
            self.radio_b_2.pack(side=TOP, pady=5)
            self.radio_b_3.pack(side=TOP, pady=5)
            close_button.config(text="Підтвердити", command=self.change_section_1)
            close_button.pack(side=BOTTOM, pady=10)

    def sync_windows(self, event):
        """Синхронізація позицій вікон з затримкою."""
        if event.widget == root:
            # Рухаємо Toplevel разом з root
            new_x = root.winfo_x() + self.delta_x
            new_y = root.winfo_y() + self.delta_y
            if (new_x, new_y) != (self.last_x, self.last_y):
                self.popup.geometry(f"+{new_x}+{new_y}")
                self.last_x, self.last_y = new_x, new_y
        elif event.widget == self.popup:
            # Рухаємо root разом з Toplevel
            new_x = self.popup.winfo_x() - self.delta_x
            new_y = self.popup.winfo_y() - self.delta_y
            if (new_x, new_y) != (self.last_x, self.last_y):
                root.geometry(f"+{new_x}+{new_y}")
                self.last_x, self.last_y = new_x, new_y

    def update_salt(self):
        if self.index < 9:
            self.salt_label.config(text=self.salt_9_name[self.index])
            self.describe_salt_label.config(text=self.salt_9_description[self.index])
            self.set_picture_on_label(self.salt_9_images[self.index], self.picture_label)

    def set_picture_on_label(self, image_path: str, label: Label):
        self.original_image = Image.open(image_path)
        self.resized_image = self.original_image.resize((self.photo_label_width, self.photo_label_height), Image.LANCZOS)
        self.image = ImageTk.PhotoImage(self.resized_image)
        label.config(image=self.image)

    def set_picture_on_background(self, image_path: str):
        self.image = Image.open(image_path)

        # Масштабуйте зображення до розміру Canvas
        self.image = self.image.resize((self.window_width, self.window_height), Image.LANCZOS)

        # Створіть об'єкт ImageTk зображення для використання на Canvas
        self.photo = ImageTk.PhotoImage(self.image)

        # Створіть зображення на Canvas
        self.canvas.create_image(0, 0, anchor="nw", image=self.photo)
        self.canvas.image = self.photo  # Збережіть посилання на зображення, щоб уникнути видалення з пам'яті

    def set_original_button_color(self, x: int, y: int):
        root.after(self.delay, lambda: self.buttons[x][y].configure(bg="light yellow"))

    def shuffle_buttons(self):
        self.button_coords = [(x, y) for x in range(self.board_size) for y in range(self.board_size)]

        random.shuffle(self.button_coords)

        for x in range(self.board_size):
            for y in range(self.board_size):
                new_x, new_y = self.button_coords.pop()
                self.buttons[x][y].grid(row=new_x, column=new_y)

    def end_of_game(self):
        play_sound(self.end_of_game_sound)

        for widget in root.winfo_children():
            widget.destroy()

        self.canvas = Canvas(root, width=self.window_width, height=self.window_height)
        self.canvas.pack()

        self.set_picture_on_background("../res/pictures/background_pictures/chemistry_png.jpg")

        if not self.study_variant_flag:
            self.show_message(
                f"Вітаємо Вас із закінченням гри!\nСподіваємося, ви дізналися щось нове або повторили вже відоме.\nВаш результат: {self.correct_answers}/9 балів.\n"
                f"\nТут могла б бути Ваша реклама :)",
                2, 700, 200)
        else:
            self.show_message(
                f"Вітаємо Вас із закінченням гри!\nСподіваємося, ви дізналися щось нове.\nКількіть Ваших неправильних спроб: {self.incorrect_answers}.\n"
                f"\nТут могла б бути Ваша реклама :)",
                2, 700, 200)

        self.study_variant_flag = False

    def new_game(self):
        self.popup.destroy()
        self.index = 0
        self.correct_answers = 0
        self.incorrect_answers = 0
        self.time_to_answers = 45

        self.show_message("Оберіть режим гри і продовжіть грати (або вийти)", 3, 700, 170)

    def close_game(self):
        set_all_channels_volume_to_zero()

        play_sound(self.close_game_sound)
        root.after(800, lambda: self.root.destroy())

    def timer(self, seconds):
        if seconds >= 0:
            self.countdown_label.config(text=f"00:{str(seconds).rjust(2, '0')}")
            self.time_to_answers -= 1
            root.after(1000, lambda: self.timer(self.time_to_answers))

        if 20 > seconds >= 10:
            self.countdown_label.config(highlightbackground="orange2")

        if 10 > seconds:
            self.countdown_label.config(highlightbackground="red2")

        if seconds <= 2:
            fade_out_music(4)

        if seconds == 0:
            self.set_disabled_state_on_button()

            play_sound(self.incorrect_answer_sound)

            def function_():
                for widget in root.winfo_children():
                    widget.destroy()

                self.canvas = Canvas(root, width=self.window_width, height=self.window_height)
                self.canvas.pack()

                self.set_picture_on_background("../res/pictures/background_pictures/chemistry_png.jpg")

                self.show_message(
                    f"Час вийшов!\nСподіваємося, ви дізналися щось нове або повторили вже відоме.\nВаш результат: {self.correct_answers}/9 балів.\n"
                    f"\nТут могла б бути Ваша реклама :)",
                    2, 700, 200)

            root.after(700, function_)

    def set_disabled_state_on_button(self):
        for x in range(self.board_size):
            for y in range(self.board_size):
                self.buttons[x][y].config(state=DISABLED)

    def set_normal_state_on_button(self):
        for x in range(self.board_size):
            for y in range(self.board_size):
                self.buttons[x][y].config(state=NORMAL)

    def change_section_2(self):
        """
        Звичайна функція зміни
        """
        for widget in root.winfo_children():
            widget.destroy()

        self.create_widgets()
        self.very_important_func()

        self.menubar.add_command(label="Змінити розділ", command=lambda: self.show_message("Виберіть розділ: ", 4, 500, 300))

        self.menu_exit = Menu(self.menubar, tearoff=0)
        self.menu_exit.add_command(label="Так, я дійсно хочу вийти з гри", command=self.close_game)
        self.menu_exit.add_command(label="Ні, я передумав - краще продовжу грати :)")
        self.menubar.add_cascade(label="Вихід з гри", menu=self.menu_exit)

        self.update_salt()


    def change_section_1(self):
        """
        Початковий вибір секції на самому початку гри
        """
        if self.study_variant_flag:
            self.popup.destroy()
            self.canvas.delete("all")

            self.create_widgets()

            self.menubar.add_command(label="Змінити розділ", command=lambda: self.show_message("Виберіть розділ: ", 4, 500, 300))
            self.menu_exit = Menu(self.menubar, tearoff=0)
            self.menu_exit.add_command(label="Так, я дійсно хочу вийти з гри", command=self.close_game)
            self.menu_exit.add_command(label="Ні, я передумав - краще продовжу грати :)")
            self.menubar.add_cascade(label="Вихід з гри", menu=self.menu_exit)

            self.study_variant_flag = True

            self.very_important_func()
            self.update_salt()

            play_sound(self.start_game_sound)

            root.after(2500, lambda: play_background_music(self.background_music_1))

        else:
            self.popup.destroy()
            self.canvas.delete("all")

            self.create_widgets()
            self.menu_exit = Menu(self.menubar, tearoff=0)
            self.menu_exit.add_command(label="Так, я дійсно хочу вийти з гри", command=self.close_game)
            self.menu_exit.add_command(label="Ні, я передумав - краще продовжу грати :)")
            self.menubar.add_cascade(label="Вихід з гри", menu=self.menu_exit)

            self.countdown_label.place(relx=0.5, rely=0.98, anchor=S)

            self.very_important_func()
            self.update_salt()
            self.timer(self.time_to_answers)

            play_sound(self.start_game_sound)

            root.after(2500, lambda: play_background_music(self.background_music_1))

    def first_radio_button_change_section(self):
        self.radio_b_1.config(bg="PaleGreen2")
        self.radio_b_2.config(bg="SystemButtonFace")
        self.radio_b_3.config(bg="SystemButtonFace")
        self.radio_b_4.config(bg="SystemButtonFace")
    def second_radio_button_change_section(self):
        self.radio_b_1.config(bg="SystemButtonFace")
        self.radio_b_2.config(bg="PaleGreen2")
        self.radio_b_3.config(bg="SystemButtonFace")
        self.radio_b_4.config(bg="SystemButtonFace")
    def third_radio_button_change_section(self):
        self.radio_b_1.config(bg="SystemButtonFace")
        self.radio_b_2.config(bg="SystemButtonFace")
        self.radio_b_3.config(bg="PaleGreen2")
        self.radio_b_4.config(bg="SystemButtonFace")

    def fourth_radio_button_change_section(self):
        self.radio_b_1.config(bg="SystemButtonFace")
        self.radio_b_2.config(bg="SystemButtonFace")
        self.radio_b_3.config(bg="SystemButtonFace")
        self.radio_b_4.config(bg="PaleGreen2")

    def show_information_about(self, message: str):
        self.popup_2_x = (root.winfo_screenwidth() - 720) // 2
        self.popup_2_y = (root.winfo_screenheight() - 150 - 400) // 2

        self.popup_2 = Toplevel(root)
        self.popup_2.title("Chemical Master: message")
        self.popup_2.attributes("-topmost", True)
        self.popup_2.geometry(f"{720}x{150}+{self.popup_2_x}+{self.popup_2_y - 50}")
        self.popup_2.iconbitmap("../res/pictures/icons/icon.ico")

        self.popup_2.update()
        self.popup_2.lift()

        label = Label(self.popup_2, text=message, font=("Consolas", 14))
        label.pack(padx=10, pady=10)

    def solt_is(self, event):
        self.show_information_about(self.describe_salt_str)
        self.first_radio_button_change_section()

    def acid_is(self, event):
        self.show_information_about(self.describe_acid_str)
        self.second_radio_button_change_section()

    def oxide_is(self, event):
        self.show_information_about(self.describe_oxide_str)
        self.third_radio_button_change_section()

    def all_in_one_mode_is(self, event):
        self.show_information_about(self.about_all_in_one_mode_str)
        self.fourth_radio_button_change_section()

    def mouse_leave_radiobutton(self, event):
        self.popup_2.destroy()

    def user_select_section(self):
        self.popup.destroy()
        self.show_message("Виберіть розділ: ", 5, 500, 350)

    def user_select_section_study(self):
        self.study_variant_flag = True
        self.popup.destroy()
        self.show_message("Виберіть розділ: ", 6, 500, 300)

    def very_important_func(self):
        self.random_salt_formulas = random.sample(sorted(self.all_dicts[self.var.get()].keys()), 9)
        self.salt_9_name = [self.all_dicts[self.var.get()][salt]["correct_name"] for salt in self.random_salt_formulas]
        self.salt_9_description = [self.all_dicts[self.var.get()][description]["description"] for description in self.random_salt_formulas]
        self.salt_9_images = [self.all_dicts[self.var.get()][image]["image"] for image in self.random_salt_formulas]

        for x in range(self.board_size):
            for y in range(self.board_size):
                self.buttons[x][y].config(text=self.random_salt_formulas[x * self.board_size + y])


if __name__ == "__main__":
    try:
        root = Tk()
        game = Chemical_Master(root)
        root.mainloop()
    except SystemExit:
        print("Something went wrong :(")
