# Avtor: Matej Petković
import math
from hyperopt import hp, tpe, rand, fmin, Trials
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from hyperopt import pyll, base
from tqdm import trange


# x = (0, ..., 0)
def f1_n(kwargs):
    n = len(kwargs)
    a = 10.0
    args = [kwargs[x] for x in sorted(kwargs)]
    return a * n + sum(x ** 2 - a * math.cos(2 * math.pi * x) for x in args)


space1 = {"x1": hp.uniform("x1", -5.12, 5.12), "x2": hp.uniform("x2", -5.12, 5.12)}
space2 = {"x1": hp.uniform("x1", -5.12, 5.12),
          "x2": hp.uniform("x2", -5.12, 5.12),
          "x3": hp.uniform("x3", -5.12, 5.12),
          "x4": hp.uniform("x4", -5.12, 5.12),
          "x5": hp.uniform("x5", -5.12, 5.12),
          "x6": hp.uniform("x6", -5.12, 5.12)}


def f3(kwargs):
    x1, x2, x3, x4, x5, x6, x7 = [kwargs[x] for x in sorted(kwargs)]
    return sum(x ** 2 for x in (x1, x2, x3, x4, x5, x6, x7))


space3 = {"x1": hp.uniform("x1", -10.0, 10.0),
          "x2": hp.uniform("x2", -10.0, 10.0),
          "x3": hp.uniform("x3", -10.0, 10.0),
          "x4": hp.uniform("x4", -10.0, 10.0),
          "x5": hp.uniform("x5", -10.0, 10.0),
          "x6": hp.uniform("x6", -10.0, 10.0),
          "x7": hp.uniform("x7", -10.0, 10.0)}


def f4(kwargs):
    x, y = [kwargs[x] for x in sorted(kwargs)]
    # (3, 0.5), [-4.5, 4.5]
    return (1.5 - x + x * y) ** 2 + (2.25 - x + x * y ** 2) ** 2 + (2.625 - x + x * y ** 3) ** 2


space4 = {"x1": hp.uniform("x1", -4.5, 4.5), "x2": hp.uniform("x2", -4.5, 4.5)}


def f5(kwargs):
    x1, x2, x3, x4, x5 = [kwargs[x] for x in sorted(kwargs)]
    # (-2.903534, ..., -2.903534)   [-5, 5]
    return sum(x ** 4 - 16 * x ** 2 + 5 * x for x in (x1, x2, x3, x4, x5)) / 2.0


space5 = {"x1": hp.uniform("x1", -5.0, 5.0),
          "x2": hp.uniform("x2", -5.0, 5.0),
          "x3": hp.uniform("x3", -5.0, 5.0),
          "x4": hp.uniform("x4", -5.0, 5.0),
          "x5": hp.uniform("x5", -5.0, 5.0)
          }


def f6(kwargs):
    x, y = [kwargs[x] for x in sorted(kwargs)]
    return - math.cos(x) * math.cos(y) * math.exp(-((x - math.pi) ** 2 + (y - math.pi) ** 2))


space6 = {"x1": hp.uniform("x1", -100.0, 100.0),
          "x2": hp.uniform("x2", -100.0, 100.0)
          }


def f7(args):
    return (args["x"] - 4) ** 2


space7 = {"x": hp.uniform("x", -1000, 1000)}


def f8(args):
    x, y = sorted(args.values())
    return (x - 4) ** 2 + y ** 2


space8 = space6

problems = {1: (f1_n, space1, 0, 2),
            2: (f1_n, space2, 0, 6),
            3: (f3, space3, 0, 7),
            4: (f4, space4, 0, 2),
            5: (f5, space5, -39.166617 * 5, 5),
            6: (f6, space6, -1, 2),
            7: (f7, space7, 0, 1),
            8: (f8, space8, 0, 2)}


def optimize(problem, method):
    loss, space, _, _ = problems[problem]
    trials = Trials()
    best = fmin(fn=loss,
                space=space,
                algo=method,
                max_evals=1000,
                trials=trials)
    best_value = loss(best)
    xs = [trial["misc"]["vals"] for trial in trials.trials]
    ys = [trial["result"]["loss"] for trial in trials.trials]
    return xs, ys, best, best_value


def plot_results(title, domain, values, out_file=None):
    bound = 10 ** 6
    for label, (_, ys, best, best_value) in zip(domain, values):
        ys = [max(-bound, min(y, bound)) for y in ys]
        best = [best[x] for x in sorted(best)]
        best = tuple([f"{x:.2f}" for x in best])
        sns.distplot(ys, rug=True, label=f"{label}: ({best_value:.4f}, {best})")  # , rug_kws={"alpha": 0.3})
    plt.legend()
    plt.title(title)
    if out_file is not None:
        plt.savefig(out_file)
    else:
        plt.show()
    plt.cla()
    plt.clf()


def plot_one(loss, x_min, x_max, xs, ys, best, best_value):
    if len(xs[0]) > 1:
        raise ValueError("Only 1D problems supported")
    xs = [x["x"][0] for x in xs]
    plt.plot(xs, ys, "r.")
    xs = [{"x": x} for x in np.linspace(x_min, x_max, 1000)]
    ys = [loss(x) for x in xs]
    xs = [x["x"] for x in xs]
    plt.plot(xs, ys, "b--")
    plt.plot([best["x"]], [best_value], "go")
    plt.show()
    plt.cla()
    plt.clf()


def solve_problem(n):
    results = []
    methods = [tpe.suggest, rand.suggest]
    names = ["tpe", "random"]
    for m in methods:
        results.append(optimize(n, m))
    plot_results(f"Problem {n}: opt = {problems[n][2]}", names, results)


# for i in range(7, 9):
#     solve_problem(i)

# plot_one(f7, -1000, 1000, *optimize(7, tpe.suggest))


class MySearch:
    # First, random seeds: this is for faking purposes
    # Later, use parsen with n_candidates modified maybe (and different random seeds)
    DUMMY_LOSS = 123.456789

    def __init__(self, space, hp_suggest, previous_results, n_to_generate):
        self.count = 0
        # [({var_name1: var_value1, ...}, loss1), ...] where every pair (xs, y) corresponds to a trial
        self.previous_results = previous_results if previous_results is not None else []
        self.index_last_suggested = -1
        self.n_to_generate = n_to_generate
        self.space = space
        self.hp_suggest = hp_suggest

    def __call__(self, *args, **kwargs):
        # semi-ugly hack ;)
        if self.count < len(self.previous_results):
            y = self.previous_results[self.count][1]
            self.count += 1
        else:
            y = MySearch.DUMMY_LOSS
            # raise ValueError("Too many tries!")
        return y

    def suggest(self, new_ids, domain, trials, seed):
        assert self.index_last_suggested + 1 == self.count
        if self.count < len(self.previous_results):
            xs = self.previous_results[self.count][0]
            self.index_last_suggested = self.count
            return MySearch._suggest_helper(new_ids, domain, trials, seed, xs)
        else:
            return self.hp_suggest(new_ids, domain, trials, seed)

    @staticmethod
    def _suggest_helper(new_ids, domain, trials, seed, xs):
        rng = np.random.RandomState(seed)
        rval = []
        for ii, new_id in enumerate(new_ids):
            # -- sample new specs, idxs, vals
            idxs, _ = pyll.rec_eval(
                domain.s_idxs_vals, memo={domain.s_new_ids: [new_id], domain.s_rng: rng}
            )
            new_result = domain.new_result()
            new_misc = dict(tid=new_id, cmd=domain.cmd, workdir=domain.workdir)
            base.miscs_update_idxs_vals([new_misc], idxs, xs)
            rval.extend(trials.new_trial_docs([new_id], [None], [new_result], [new_misc]))
        return rval

    def run(self):
        trials = Trials()
        fmin(fn=self,
             space=self.space,
             algo=self.suggest,
             max_evals=len(self.previous_results) + self.n_to_generate,
             trials=trials,
             show_progressbar=False)
        xs = [trial["misc"]["vals"] for trial in trials.trials[-self.n_to_generate:]]
        ys = [trial["result"]["loss"] for trial in trials.trials]
        assert len(ys) == len(self.previous_results) + self.n_to_generate
        # check first len(...)
        for i in range(len(self.previous_results)):
            if ys[i] != self.previous_results[i][1]:
                raise ValueError(f"Weird: {ys[i]} != {self.previous_results[i][1]}")
        # and check the last n_generate
        for i in range(self.n_to_generate):
            if ys[-(i + 1)] != MySearch.DUMMY_LOSS:
                raise ValueError(f"Weird: {ys[-(i + 1)]} != {MySearch.DUMMY_LOSS}")
        return xs


def optimize_with_cluster(problem, iterations, trials_per_iteration, hp_method):
    loss, space, _, n_args = problems[problem]
    # fake first grid search
    trials = Trials()
    fmin(fn=loss,
         space=space,
         algo=rand.suggest,
         max_evals=trials_per_iteration,
         trials=trials)
    xs = [trial["misc"]["vals"] for trial in trials.trials]
    ys = [trial["result"]["loss"] for trial in trials.trials]
    for _ in trange(iterations):
        my_search = MySearch(space, hp_method, list(zip(xs, ys)), trials_per_iteration)
        xs_new = my_search.run()
        # fake subsequent grid evaluation
        ys += [loss({name: values[0] for name, values in x.items()}) for x in xs_new]
        xs += xs_new
    i = int(np.argmin(ys))
    return xs, ys, {name: values[0] for name, values in xs[i].items()}, ys[i]


def solve_problem_with_cluster(n):
    results = []
    methods = [tpe.suggest, rand.suggest]
    names = ["tpe", "random"]
    iterations = 1000
    rounds = 10
    per_round = iterations // rounds
    for m in methods:
        results.append(optimize_with_cluster(n, rounds, per_round, m))
    plot_results(f"Problem {n}: opt = {problems[n][2]}", names, results,
                 out_file=f"../results/hyperopt/f{n}-{per_round}hyper.png")


for i in range(7, 9):
    solve_problem_with_cluster(i)