"""
cae_open_loop.py
============================================================================
Open-loop three-chamber simulation. Produces FIGURE 3 of

    M. Munoz-Arias, L. M. Esquivel-Sancho and D. del Puerto-Flores,
    "Energy-Based Speed Regulation of Compressed-Air Engines,"
    IEEE Transactions on Control Systems Technology (submitted).

and prints every number quoted in Section V-A.

----------------------------------------------------------------------------
WHAT THIS SCRIPT SHOWS
----------------------------------------------------------------------------
The engine self-starts from rest with a tank charged to six bar and a FIXED
valve opening. There is no controller anywhere in this script. Two throttle
settings are compared, D = 1.0 (fully open) and D = 0.5 (half open), and each
run continues until the tank reaches atmospheric pressure and the engine
stops.

Three features of Figure 3 are discussed in Section V-A:

  1. The tank discharges monotonically and the engine stops when it does.
     This is the depleting-tank behaviour of Remark 7, and it is why
     Assumption 1 (regulated supply) is needed for the regulation problem of
     Section IV to be well posed at all.

  2. Chamber pressure and pipe flow both carry a ripple at the port-timing
     frequency, and the flow shows a backflow transient at start-up when the
     intake routing switches between chambers.

  3. The two throttle settings trade start-up against endurance. Fully open
     reaches the higher peak but empties the tank sooner. This is the
     one-sided authority of Remark 8 seen from the plant side: throttling
     removes energy and cannot add it, so a fixed opening can only trade
     peak against run time.

----------------------------------------------------------------------------
USAGE (Windows PowerShell)
----------------------------------------------------------------------------
    python cae_open_loop.py
    python cae_open_loop.py --show                 open an interactive window
    python cae_open_loop.py --outdir figures       write into .\\figures\\
    python cae_open_loop.py --tmax 30 --n 12000    run length, sample count

Outputs
    openloop_response.pdf    vector figure, exactly as used in the paper
    openloop_response.png    raster preview
    a printed summary of the Section V-A numbers

Runtime is roughly half a minute: two thirty-second runs of a stiff
seven-state system.
============================================================================
"""

import argparse
import os

import numpy as np
from scipy.integrate import solve_ivp
import matplotlib

import cae_model as M

# ---------------------------------------------------------------------------
# Operating conditions, stated in Section V-A
# ---------------------------------------------------------------------------
T_MAX_DEFAULT = 30.0       # simulated duration                       [s]
N_OUT_DEFAULT = 12000      # output samples
STOP_RPM = 5.0             # speed below which the engine counts as stopped

# The two fixed throttle settings, D of eq. (12), with their plot colours.
CASES = [
    (1.0, "tab:green", "D = 1.0 (fully open)"),
    (0.5, "tab:blue",  "D = 0.5 (half open)"),
]


def simulate(D, t_max, n_out):
    """Integrate the open-loop model of eqs. (31) to (35) at fixed opening D.

    LSODA is used because the system is stiff: the pneumatic states move on a
    millisecond scale while the tank drains over ten seconds. `max_step` is
    capped so the port-timing gates of cae_model section 5 are never stepped
    over.
    """
    t_eval = np.linspace(0.0, t_max, n_out)
    sol = solve_ivp(
        M.three_chamber_rhs,
        t_span=(0.0, t_max),
        y0=M.initial_state(),
        args=(D,),                 # tau_load defaults to zero: no load applied
        t_eval=t_eval,
        method="LSODA",
        rtol=1e-7,
        atol=1e-9,
        max_step=2.0e-3,
    )
    if not sol.success:
        raise RuntimeError(f"integration failed at D = {D}: {sol.message}")
    return sol


def unpack(sol):
    """Convert a solution to the plotting units used in Figure 3."""
    return dict(
        t=sol.t,
        P1_bar=sol.y[0] / M.BAR,                          # tank pressure
        flow_lph=M.mass_to_litre_per_hour(sol.y[1]),      # pipe flow
        p_gauge_bar=(sol.y[2] - M.P_ATM) / M.BAR,         # chamber 1, gauge
        omega_rpm=sol.y[5] / M.J_SH / M.RPM,              # shaft speed
    )


def make_figure(results, outdir):
    """Draw Figure 3: four panels, two throttle settings each."""
    import matplotlib.pyplot as plt

    plt.rcParams.update({"font.family": "DejaVu Sans",
                         "mathtext.fontset": "dejavusans"})

    # 7.16 x 4.70 in is the size the manuscript includes at width=6in.
    fig, ax = plt.subplots(2, 2, figsize=(7.16, 4.70))

    for colour, label, d in results:
        ax[0, 0].plot(d["t"], d["P1_bar"],      color=colour, lw=1.2, label=label)
        ax[0, 1].plot(d["t"], d["p_gauge_bar"], color=colour, lw=0.8, label=label)
        ax[1, 0].plot(d["t"], d["flow_lph"],    color=colour, lw=0.8, label=label)
        ax[1, 1].plot(d["t"], d["omega_rpm"],   color=colour, lw=0.8, label=label)

    ax[0, 0].set(title=r"Tank pressure $P_1$",
                 xlabel="time (s)", ylabel="bar")
    ax[0, 1].set(title="Chamber pressure (gauge)",
                 xlabel="time (s)", ylabel="bar")
    ax[1, 0].set(title=r"Pipe mass-flow $Q_1$",
                 xlabel="time (s)", ylabel="L/hour")
    ax[1, 1].set(title=r"Shaft speed $\omega_e$",
                 xlabel="time (s)", ylabel="rpm")

    for a in ax.flat:
        a.grid(True, alpha=0.3)
        a.legend(fontsize=7)

    fig.tight_layout()

    os.makedirs(outdir, exist_ok=True)
    pdf = os.path.join(outdir, "openloop_response.pdf")
    png = os.path.join(outdir, "openloop_response.png")
    fig.savefig(pdf)                 # vector, for the manuscript
    fig.savefig(png, dpi=150)        # raster, for quick viewing
    print(f"\nwrote {pdf}\nwrote {png}")
    return fig


def report(results):
    """Print the four numbers per case that Section V-A quotes."""
    print("\n--- numbers quoted in Section V-A "
          "-------------------------------")
    for _, label, d in results:
        alive = d["omega_rpm"] > STOP_RPM
        t_stop = d["t"][alive][-1] if alive.any() else float("nan")
        # the plateau window, chosen after the start-up transient has decayed
        mid = (d["t"] > 2.0) & (d["t"] < 5.0)
        print(f"{label}")
        print(f"    peak shaft speed      {d['omega_rpm'].max():8.1f} rpm")
        print(f"    plateau speed (2-5 s) {d['omega_rpm'][mid].mean():8.1f} rpm")
        print(f"    mean flow (2-5 s)     {d['flow_lph'][mid].mean():8.1f} L/h")
        print(f"    engine stops at       {t_stop:8.2f} s")
    print("    (bench reference: about 1400 L/h and a 2700 rpm plateau;")
    print("     the plateau gap is the port-timing calibration gap of Sec. VII)")
    print("-----------------------------------------------------------------")


def main():
    ap = argparse.ArgumentParser(
        description="Open-loop three-chamber simulation, Figure 3 of the paper")
    ap.add_argument("--tmax", type=float, default=T_MAX_DEFAULT,
                    help="simulated duration in seconds")
    ap.add_argument("--n", type=int, default=N_OUT_DEFAULT,
                    help="number of output samples")
    ap.add_argument("--outdir", default=".",
                    help="directory for the figure files")
    ap.add_argument("--show", action="store_true",
                    help="open an interactive window instead of exiting")
    args = ap.parse_args()

    if not args.show:
        matplotlib.use("Agg")        # headless: must precede pyplot import

    results = []
    for D, colour, label in CASES:
        print(f"integrating D = {D} ...")
        results.append((colour, label, unpack(simulate(D, args.tmax, args.n))))

    make_figure(results, args.outdir)
    report(results)

    if args.show:
        import matplotlib.pyplot as plt
        plt.show()


if __name__ == "__main__":
    main()
