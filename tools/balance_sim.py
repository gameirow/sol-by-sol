"""Sol by Sol balance simulator: plays many missions with different player types and prints how often each survives.
OLD = the rules before 15 Nov 2026 (too easy). PHASE1 = the rules now in the game (design/game-balance-plan.md).
Keep PHASE1 in sync with the constants in src/index.src.html.

    python tools/balance_sim.py"""
import json, math, random, sys, copy
D = sys.argv[1] if len(sys.argv) > 1 else str(__import__('pathlib').Path(__file__).resolve().parent.parent)
POOL = json.load(open(f'{D}/data/pool.json')); WEATHER = json.load(open(f'{D}/data/weather.json'))
SOLS, BG, QF = 10, 115, 3.05
BUDGET = round(600/860*SOLS*1.0275, 2)
radIndex = lambda u: max(0, min(10, round(10*math.log(max(u, 80)/80)/math.log(1700/80))))
cl = lambda v: max(0, min(10, v))
OLD = dict(solar={'V':11,'H':10,'M':9,'L':7}, farm_need=3, inside=.5, eva_full=60, dust=.06, dust_storm=.2, dust_max=.6,
           start=dict(rad=10, fit=7, air=9, well=7, mood=6), food0=7, meal_food=2, meal_mood=1.5,
           fit_up=1.5, fit_down=1.5, rest_up=1.5, rest_down=.8, mood_down=1.5, call=2.5, eva_mood=1.5, air_bad=2,
           fail_h=3, acts=2, low_mood_one_act=False, low_fit_slow=False, sick_no_ex=False, crystal_far=False, rad_stars=False,
           events=False, cold_farm=False, storm_inside=0, shelter=False, shelter_keep=.25)

PHASE1 = dict(OLD, solar={'V':10,'H':9,'M':8,'L':6}, dust=.1, dust_storm=.25, dust_max=1.0, fit_down=1.0, mood_down=1.5, rest_down=1.0,
              storm_inside=.5, shelter=True, shelter_keep=.25,
              crystal_far=True, low_mood_one_act=True, low_fit_slow=True, sick_no_ex=True, cold_farm=True)

def need_air(w): return 3 + (w[1] < -75) + (w[1] < -85)

def mission(R, player, rng):
    hits = [s for s in POOL if s['hit']]; misses = [s for s in POOL if not s['hit']]
    may = next(s for s in hits if s['id'] == '2024-05-03')
    picked = [may if rng.random() < .5 else rng.choice(hits)]
    while len(picked) < 3:
        c = rng.choice(hits if rng.random() < .2 else misses)
        if c not in picked: picked.append(c)
    sols = rng.sample([2,3,4,5,6,7,8], 3); storms = [dict(s=s, sol=sols[i]) for i, s in enumerate(picked)]
    wx = WEATHER[0 if rng.random() < .6 else 1] if rng.random() < .2 else rng.choice(WEATHER[2:])
    S = dict(sol=1, food=R['food0'], dose=0., samples=0, dust=0., f=dict(R['start']), H=[], shelter=False)
    def first(st): return next((i for i, v in enumerate(st['s']['marsDose']) if v - st['s']['base'] >= 25), -1)
    for sol in range(1, SOLS+1):
        S['sol'] = sol; w = wx[sol-1]; f = S['f']
        old = fresh = 0
        for st in storms:
            i = sol - st['sol']; d = st['s']['marsDose']; b = st['s']['base']
            if 0 <= i < len(d):
                e = max(0, d[i]-b)
                if e > 0:
                    if i == first(st): fresh += e
                    else: old += e
        watch = any(sol >= st['sol'] and sol <= st['sol'] + (first(st) if first(st) >= 0 else 1) for st in storms)
        alert = any(st['sol'] == sol for st in storms)
        fc = any(st['sol'] == sol and st['s']['forecastHitsMars'] for st in storms)
        if S['shelter'] and not (watch or old + fresh > 0): S['shelter'] = False   # storm over: bags go back
        idx = radIndex(BG + old)
        solar = round(R['solar'][w[4]] * (1 - S['dust'])); need = need_air(w)
        nacts = 1 if (R['low_mood_one_act'] and f['mood'] < 4) else R['acts']
        ctx = dict(fc=fc, shelter=S['shelter'], f=f, idx=idx, watch=watch or alert, solar=solar, need=need, food=S['food'], dust=S['dust'], samples=S['samples'], sol=sol, nacts=nacts, R=R)
        acts, air, farm, meal, eva_s, run_home = player(ctx, rng)
        acts = acts[:nacts]
        if 'shelter' in acts and R['shelter']: S['shelter'] = True
        if R['sick_no_ex'] and f['well'] < 4 and 'exercise' in acts: acts = [a for a in acts if a != 'exercise']
        # power: activities first, then air, farm gets what is left
        cost = sum(1 for a in acts if a in ('exercise', 'call'))
        while cost + air + farm > solar and farm > 0: farm -= 1
        while cost + air + farm > solar and air > 0: air -= 1
        while cost + air + farm > solar and cost > 0: acts = [a for a in acts if a not in ('call',)] if 'call' in acts else [a for a in acts if a != 'exercise']; cost = sum(1 for a in acts if a in ('exercise','call'))
        if meal and S['food'] >= R['meal_food']: S['food'] -= R['meal_food']; ate = True
        else: ate = False
        eva = 'eva' in acts; eva_t = 0; storm_t = 0
        if eva:
            eva_t = eva_s * (1.35 if (R['low_fit_slow'] and f['fit'] < 4) else 1)
            if fresh > 0:
                onset = 8 + rng.random()*14
                if eva_t > onset: storm_t = (6 if run_home else eva_t - onset); eva_t = min(eva_t, onset + storm_t)
            need_t = 30 if (R['crystal_far'] and S['samples'] >= 1) else 18
            if eva_t >= need_t: S['samples'] += 1
            if eva_t >= 20: S['dust'] = 0
        frac = min(1, eva_t / R['eva_full'])
        uGy = BG*R['inside'] + frac*(BG*(1-R['inside']) + old) + min(1, storm_t/(R['eva_full']/2))*fresh + (1-frac)*(old + fresh)*R['storm_inside']*(R['shelter_keep'] if S['shelter'] else 1)
        S['dose'] += uGy*QF/1000
        S['food'] = max(0, min(10, S['food'] + farm - R['farm_need']))
        if R['cold_farm'] and air < need: S['food'] = max(0, S['food'] - 1)
        f['rad'] = cl(10*(1 - S['dose']/BUDGET))
        f['fit'] = cl(f['fit'] + (R['fit_up'] if 'exercise' in acts else -R['fit_down']))
        f['air'] = cl(f['air'] + (1 if air >= need else -R['air_bad']*(need-air)))
        dusty = w[4] == 'L'
        f['well'] = cl(f['well'] + (R['rest_up'] if 'rest' in acts else -R['rest_down']) + (-2 if S['food'] <= 0 else -1 if S['food'] <= 2 else 0) + (-1 if dusty and eva else 0))
        f['mood'] = cl(f['mood'] - R['mood_down'] + (R['call'] if 'call' in acts else 0) + (R['eva_mood'] if eva else 0) + (R['meal_mood'] if ate else 0) + (-.5 if dusty else 0))
        S['dust'] = min(R['dust_max'], S['dust'] + (R['dust_storm'] if dusty else R['dust']))
        H = sum(f.values())/5; S['H'].append(H)
        if H < R['fail_h'] or min(f.values()) <= 0:
            return dict(ok=False, minH=min(S['H']), sol=sol, stars=0, H=H, dose=S['dose'], samples=S['samples'], why=('health' if H < R['fail_h'] else min(f, key=f.get)))
    H = S['H'][-1]
    stars = 1 + (S['samples'] >= 3) + (H >= 7) + ((S['dose'] <= BUDGET*.5) if R['rad_stars'] else 0)
    return dict(ok=True, minH=min(S['H']), sol=10, stars=min(3, stars) if not R['rad_stars'] else stars, H=H, dose=S['dose'], samples=S['samples'], why='')

# ---------------- player types ----------------
def sensible(c, rng):
    f, R = c['f'], c['R']
    cand = []
    want_out = c['idx'] < 6 and (c['samples'] < 3 or c['dust'] >= .18)
    if want_out: cand.append(('eva', 3 + (2 if c['dust'] >= .18 else 0)))
    if R['shelter'] and c['watch'] and not c['shelter']: cand.append(('shelter', 9 if c['fc'] else 4))
    cand += [('exercise', 10 - f['fit']), ('call', 10 - f['mood']), ('rest', 10 - f['well'])]
    cand.sort(key=lambda x: -x[1]); acts = [a for a, _ in cand[:c['nacts']]]
    air = c['need']; farm = max(0, c['solar'] - air - sum(1 for a in acts if a in ('exercise','call')))
    farm = min(farm, 5)
    meal = c['food'] >= 5 and f['mood'] < 7
    return acts, air, farm, meal, (28 if c['watch'] else 35), True

def careless(c, rng):   # likes going outside, ignores alarms, stays long
    s = sensible(c, rng); acts = s[0]
    if 'eva' not in acts and c['idx'] < 10: acts = ['eva'] + acts[:1]
    return acts, s[1], s[2], s[3], 55, False

def indoor(c, rng):      # never goes outside
    f = c['f']; cand = sorted([('exercise', 10-f['fit']), ('call', 10-f['mood']), ('rest', 10-f['well'])], key=lambda x: -x[1])
    acts = [a for a, _ in cand[:c['nacts']]]; air = c['need']; farm = max(0, c['solar'] - air - sum(1 for a in acts if a != 'rest'))
    return acts, air, min(farm, 5), c['food'] >= 5, 0, True

def random_p(c, rng):
    acts = rng.sample(['eva', 'exercise', 'call', 'rest'] + (['shelter'] if c['R']['shelter'] else []), c['nacts'])
    air = rng.choice([c['need']-1, c['need'], c['need']+1]); farm = rng.randint(1, 5)
    return acts, max(0, air), farm, rng.random() < .5, rng.uniform(15, 60), rng.random() < .5

def onetrack(c, rng):    # same two things every sol (exercise + call), default power
    return ['exercise', 'call'][:c['nacts']], c['need'], 3, False, 0, True

PLAYERS = dict(sensible=sensible, careless=careless, indoor=indoor, random=random_p, onetrack=onetrack)

def run(R, n=2000, seed=1):
    out = {}
    for name, p in PLAYERS.items():
        rng = random.Random(seed); res = [mission(R, p, rng) for _ in range(n)]
        ok = [r for r in res if r['ok']]
        why = {}
        for r in res:
            if not r['ok']: why[r['why']] = why.get(r['why'], 0) + 1
        out[name] = dict(survive=round(100*len(ok)/n), three=round(100*sum(r['stars'] >= 3 for r in res)/n),
                         stars=round(sum(r['stars'] for r in res)/n, 2), tense=round(100*sum(r['minH']<5.5 for r in res)/n), H=round(sum(r['H'] for r in res)/n, 1),
                         lost_sol=round(sum(r['sol'] for r in res if not r['ok'])/max(1, n-len(ok)), 1),
                         why=dict(sorted(why.items(), key=lambda x: -x[1])[:3]))
    return out

if __name__ == '__main__':
    for name, R in (('OLD', OLD), ('PHASE1', PHASE1)):
        print(name)
        for k, v in run(R).items(): print(f'  {k:9}', v)
