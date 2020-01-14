import pyautogui
import keyboard
import math
import copy
import _pickle as cPickle


KEY_X = 66
KEY_Y = 73
R = (KEY_X + KEY_Y) / 4
START_X = 926
START_Y = 776
ST_VALUE = 0.04
EN_VALUE = 0.04
SIGMA_S = R * 5
SIGMA_L = R * 5
DIST_THRESHOLD = R * 3
METRIC_NUMBER = 50
L = R
STOP = False
LETTER_POS = dict()
LEXICON = list()
ALPHA = list()


class Word(object):
    def __init__(self, trace, word="NULL", freq=0):
        self.word = word
        self.freq = freq
        self.trace = copy.deepcopy(trace)
        self.normalized_trace = copy.deepcopy(trace)
        self.center = [0, 0]
        self.width = self.get_width()
        self.height = self.get_height()
        self.s = L / max(self.width, self.height)
        self.normalize_trace()
        self.ps = 0.0
        self.marginalized_ps = 0.0
        self.pl = 0.0
        self.marginalized_pl = 0.0
        self.c = 0.0
        self.p = 0

    def get_width(self):
        min_x, max_x = self.trace[0][0], self.trace[0][0]
        for pos in self.trace:
            min_x = min(min_x, pos[0])
            max_x = max(max_x, pos[0])
        self.center[0] = (min_x + max_x) / 2
        return (max_x - min_x) + KEY_X

    def get_height(self):
        min_y, max_y = self.trace[0][1], self.trace[0][1]
        for pos in self.trace:
            min_y = min(min_y, pos[1])
            max_y = max(max_y, pos[1])
        self.center[1] = (min_y + max_y) / 2
        return (max_y - min_y) + KEY_Y

    def normalize_trace(self):
        for i in range(len(self.trace)):
            self.normalized_trace[i][0] -= self.center[0]
            self.normalized_trace[i][1] -= self.center[1]
            self.normalized_trace[i][0] *= self.s
            self.normalized_trace[i][1] *= self.s


def cal_p_gauss(x, sigma):
    return math.exp(-0.5 * (x / sigma) ** 2)


def init_letter_pos():
    global LETTER_POS
    LETTER_POS = {'q': (), 'w': (), 'e': (), 'r': (), 't': (), 'y': (), 'u': (), 'i': (), 'o': (), 'p': (),
                  'a': (), 's': (), 'd': (), 'f': (), 'g': (), 'h': (), 'j': (), 'k': (), 'l': (),
                  'z': (), 'x': (), 'c': (), 'v': (), 'b': (), 'n': (), 'm': ()}
    cnt = 0.0
    for letter in LETTER_POS:
        if 0 <= cnt <= 9:
            LETTER_POS[letter] = [KEY_X * (cnt + 0.5), KEY_Y * 0.5]
        elif 10 <= cnt <= 18:
            LETTER_POS[letter] = [KEY_X * (cnt - 9.0), KEY_Y * 1.5]
        else:
            LETTER_POS[letter] = [KEY_X * (cnt - 17.0), KEY_Y * 2.5]
        cnt += 1


def init_alpha():
    n = METRIC_NUMBER // 2
    diff1 = (1.0 - 2 * n * ST_VALUE) / (n * (n - 1))
    diff2 = (1.0 - 2 * n * EN_VALUE) / (n * (n - 1))
    alpha1 = [ST_VALUE - diff1 * i for i in range(n)]
    alpha2 = [EN_VALUE - diff2 * (n - i - 1) for i in range(n)]
    global ALPHA
    ALPHA = alpha1 + alpha2


def get_word_trace(word):
    trace = list()
    for letter in word:
        trace.append(LETTER_POS[letter])
    return trace


def input_lexicon(file):
    global LEXICON
    load = 1
    if load:
        with open('lex.pkl', 'rb') as read_file:
            LEXICON = cPickle.load(read_file)
    else:
        with open(file, "r") as f:
            words = f.read().split("\n")[:-1]
            for word in words:
                wor, fre = word.split(" ")[0], int(word.split(" ")[1])
                w = Word(sample_pos(get_word_trace(wor)), wor, fre)
                LEXICON.append(w)
        with open("lex.pkl", "wb+") as write_file:
            cPickle.dump(LEXICON, write_file)


def distance(point1, point2):
    return math.sqrt((point1[0]-point2[0])**2 + (point1[1]-point2[1])**2)


def sample_pos(trace):
    sample_list = list()
    length = 0.0
    for i in range(len(trace) - 1):
        length += distance(trace[i], trace[i + 1])
    length /= (METRIC_NUMBER - 1)
    u = 0
    left = 0.0
    for k in range(METRIC_NUMBER):
        while u + 1 < len(trace) and distance(trace[u], trace[u + 1]) <= left:
            left -= distance(trace[u], trace[u + 1])
            u += 1
        pos = copy.deepcopy(trace[u])
        if u + 1 < len(trace):
            pos[0] += (trace[u + 1][0] - trace[u][0]) * (left / distance(trace[u], trace[u + 1]))
            pos[1] += (trace[u + 1][1] - trace[u][1]) * (left / distance(trace[u], trace[u + 1]))
        sample_list.append([pos[0], pos[1]])
        left += length
    return sample_list


def get_d(p, q):
    tmp = list()
    global R
    for i in range(METRIC_NUMBER):
        ret = min([distance(p[i], q[j]) for j in range(METRIC_NUMBER)])
        if ret > R:
            return 1
        tmp.append(ret)
    return 0


def get_delta(u, t):
    if get_d(u, t) == 0 and get_d(t, u) == 0:
        return [0 for index in range(50)]
    delta = list()
    for i in range(METRIC_NUMBER):
            delta.append(distance(u[i], t[i]))
    return delta


def input_word():
    keyboard.wait('a')
    input_word_trace = list()
    old_mouse_x, old_mouse_y = -1, -1
    global STOP
    # print(STOP)
    while not STOP:
        # print(1)
        current_mouse_x, current_mouse_y = pyautogui.position()
        if current_mouse_x == old_mouse_x and current_mouse_y == old_mouse_y:
            continue
        input_word_trace.append([current_mouse_x - START_X, current_mouse_y - START_Y])
        old_mouse_x, old_mouse_y = current_mouse_x, current_mouse_y
        print("(X,Y):", current_mouse_x - START_X, current_mouse_y - START_Y)
    STOP = False
    return Word(sample_pos(input_word_trace))


def cal_xs(input_wor, template_wor):
    xs = 0.0
    for i in range(METRIC_NUMBER):
        xs += distance(input_wor.normalized_trace[i], template_wor.normalized_trace[i])
    return xs


def cal_xl(input_wor, template_wor):
    if distance(input_wor.trace[0], template_wor.trace[0]) > DIST_THRESHOLD or \
            distance(input_wor.trace[METRIC_NUMBER-1], template_wor.trace[METRIC_NUMBER-1]) > DIST_THRESHOLD:
        return -1
    xl = 0.0
    delta = get_delta(input_wor.trace, template_wor.trace)
    for i in range(METRIC_NUMBER):
        xl += ALPHA[i] * delta[i]
    return xl


def get_match_list_xs(input_wor):
    match_list = dict()
    for word in LEXICON:
        xs = cal_xs(input_wor, word)
        match_list[word] = xs
    s = sorted(match_list, key=match_list.__getitem__)[:100]
    # for word in s:
    #     print(word.word, match_list[word])
    return s


def get_match_list_xl(input_wor):
    match_list = dict()
    for word in LEXICON:
        xl = cal_xl(input_wor, word)
        if xl < 0:
            continue
        match_list[word] = xl
    s = sorted(match_list, key=match_list.__getitem__)[:100]
    # for word in s:
    #     print(word.word, match_list[word])
    return s


def get_match_list_integrate(input_wor):
    ws, wl = list(), list()
    sum_ps, sum_pl = 0.0, 0.0
    i, j = 0, 0
    for word in LEXICON:
        xs, xl = cal_xs(input_wor, word), cal_xl(input_wor, word)
        if xl < 0:
            continue
        if xl < SIGMA_L * 2:
            # print("Location: ", j)
            j += 1
            word.pl = cal_p_gauss(xl, SIGMA_L)
            sum_pl += word.pl
            wl.append(word)
        if xs < SIGMA_S * 2:
            # print("Shape: ", i)
            i += 1
            word.ps = cal_p_gauss(xs, SIGMA_S)
            sum_ps += word.ps
            ws.append(word)
    for word in ws:
        word.marginalized_ps = word.ps / sum_ps
    for word in wl:
        word.marginalized_pl = word.pl / sum_pl
    wsl = list(set(ws).intersection(set(wl)))
    print("Shape:", len(ws), " Location:", len(wl), " Intersection:", len(wsl), "\n")
    # for word in wsl:
    #     print(word.word, word.marginalized_ps, word.marginalized_pl)
    sum_psl = 0.0
    match_list = dict()
    for word in wsl:
        sum_psl += word.marginalized_ps * word.marginalized_pl
    for word in wsl:
        word.c = (word.marginalized_ps * word.marginalized_pl) / sum_psl
        match_list[word] = word.c
    return sorted(match_list, key=match_list.__getitem__, reverse=True)[:100]


def get_match_list_freq(input_wor):
    tmp = get_match_list_integrate(input_wor)
    sum_freq = 0
    match_list = dict()
    for wor in tmp:
        sum_freq += math.log2(wor.freq)
    for wor in tmp:
        wor.p = (wor.c**2) * (math.log2(wor.freq) / sum_freq)
        match_list[wor] = wor.p
    s = sorted(match_list, key=match_list.__getitem__, reverse=True)[: 100]
    for wor in s:
        print(wor.word, wor.c, wor.freq, wor.p)
    return s


def set_stop():
    global STOP
    STOP = True


def main():
    keyboard.add_hotkey('b', set_stop)
    init_letter_pos()
    init_alpha()
    input_lexicon("Lexicon.txt")
    print("OK")
    mode = 1
    if mode == 1:
        match_list = get_match_list_freq(input_word())
    elif mode == 2:
        match_list = get_match_list_integrate(input_word())
    elif mode == 3:
        match_list = get_match_list_xl(input_word())
    elif mode == 4:
        match_list = get_match_list_xs(input_word())
    for key in match_list:
        print("word:", key.word)


if __name__ == "__main__":
    main()

#abaabatbababababab